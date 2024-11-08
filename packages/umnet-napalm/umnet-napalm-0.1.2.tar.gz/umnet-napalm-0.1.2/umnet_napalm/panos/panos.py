import xml.etree.ElementTree as ET
from typing import List
from datetime import timedelta
from ipaddress import ip_address, ip_network
import re

import xmltodict

from napalm_panos.panos import PANOSDriver

from umnet_napalm.models import IPInterfaceDict, RouteDict, InventoryDict
from ..base import UMnetNapalm, UMnetNapalmError
from ..utils import resolve_nh
from .utils import parse_system_state


PANOS_ROUTING_PROTOCOLS = {
    "H": "local",
    "C": "connected",
    "S": "static",
    "B": "BGP",
    "R": "RIP",
    "O": "OSPF",
    "Oi": "OSPF intra-area",
    "Oo": "OSPF inter-area",
    "O2": "OSPF External Type 2",
    "O1": "OSPF External Type 1",
}


class PANOS(UMnetNapalm, PANOSDriver):
    """
    PANOS Parser
    """

    _effective_running_config = None
    _system_state = None

    def _config_search(self, xpath: str, no_cache: bool = False) -> list:
        """
        Does an xpath search of the effective running config and returns the results.
        """
        cfg = self._get_effective_running_config(no_cache=no_cache)
        return cfg.findall(xpath)

    def _get_effective_running_config(self, no_cache: bool = False) -> ET:
        """
        Gets effective running config and saves it to the local object
        """
        if self._effective_running_config is None or no_cache:
            result = self._send_command(
                "<show><config><effective-running></effective-running></config></show>"
            )
            self._effective_running_config = ET.fromstring(result)

        return self._effective_running_config

    def _get_system_state(self, no_cache: bool = False) -> dict:
        """
        runs 'show system state' and parses the returned pseudo-json into structured output
        """
        if not self._system_state or no_cache:
            raw_result = self._send_command("<show><system><state/></system></show>")
            result = xmltodict.parse(raw_result)["response"]["result"]
            self._system_state = parse_system_state(result)

        return self._system_state

    def _get_mtu_and_comment(self, interface: ET) -> dict:
        """
        Looks up mtu and comment on a particular interface or subinterface
        object. Returns a dict with mtu and comment key/value pairs
        """
        results = {"mtu": 0, "comment": ""}

        # subinterfaces have mtu set at their same level.
        # for non-subinterfaces it is set under "layer3"
        if "." in interface.attrib["name"]:
            mtu = interface.find("./mtu")
        else:
            mtu = interface.find("./layer3/mtu")

        if mtu is not None:
            results["mtu"] = mtu.text

        comment = interface.find("./comment")
        if comment is not None:
            results["comment"] = comment.text

        return results

    def _get_interface_mtus_and_comments(self) -> dict:
        """
        Looks through the effective running config at network/interface for MTU configurations
        and descriptions, aka "comments"
        returns a dict keyed on interface names, with
        dict vaules, eg results[interface_name] = {'mtu':mtu, and 'comment': comment }
        """

        interfaces = self._config_search(".//network/interface/ethernet/entry")

        # for logical interfaces we only care about the subints
        interfaces.extend(
            self._config_search(".//network/interface/tunnel/units/entry")
        )
        interfaces.extend(
            self._config_search(".//network/interface/loopback/units/entry")
        )

        results = {}
        # looping over all the ethernet interfaces
        for interface in interfaces:
            results[interface.attrib["name"]] = self._get_mtu_and_comment(interface)

            # subinterfaces
            for subint in interface.findall("./layer3/units/entry"):
                results[subint.attrib["name"]] = self._get_mtu_and_comment(subint)

        return results

    def _send_command(self, cmd: str) -> str:
        """
        Send XML command to PANOS and get result
        """
        self.device.op(cmd=cmd)
        return self.device.xml_root()

    def get_inventory(self) -> List[InventoryDict]:
        """
        Digs through "show chassis inventory" and "show system state" to pull out linecard and optics information
        """
        # need access to a chassis nexus to implement "show chassis inventory"
        # try:
        #    result = self._send_command("<show><chassis><inventory/></chassis></show>")
        #    inventory = xmltodict.parse(result)["response"]["result"]
        # except PanXapiError:
        #    inventory = []

        # optics data is in system state
        raw_result = self._send_command(
            "<show><system><state><filter>sys.s*.p*.phy</filter></state></system></show>"
        )
        data = parse_system_state(raw_result)

        output = []
        for phy_name, phy_data in data.items():

            # skip copper and unpopulated ports
            if phy_data["media"] in ["CAT5", "SFP-Empty"]:
                continue

            # the 'phy name' is in the format 'sys.sX.pY.phy' which translates to 'EthernetX/Y'
            m = re.match(r"sys.s(\d+).y(\d+)/.phy$", phy_name)
            i_name = f"Ethernet{m.group(1)}/{m.group(2)}"

            output.append(
                {
                    "type": "optic",
                    "name": i_name,
                    "part_number": phy_data.get("vendor-name", ""),
                    "serial_number": phy_data.get("vendor-part-number", ""),
                    "parent": "",
                }
            )

        return output

    def get_ip_interfaces(self) -> List[IPInterfaceDict]:
        """
        napalm_panos doesn't support "get_routing_instances".
        While we could implement that function and combine it with "get_interfaces_ip" and
        "get_interfaces", it's simpler to just run "show interface all" to get most of what we need.

        Note that short of doing "show interface [x]" for every interface, I don't see a way
        to get MTU, so for now it's getting set to 0.
        """

        # "show interface all" gives us most of what we need here
        result = self._send_command("<show><interface>all</interface></show>")
        interfaces = xmltodict.parse(result)["response"]["result"]

        hw_interfaces_by_name = {i["name"]: i for i in interfaces["hw"]["entry"]}
        mtus_and_comments = self._get_interface_mtus_and_comments()

        l3_interfaces = []
        for l3_i in interfaces["ifnet"]["entry"]:
            if l3_i["ip"] == "N/A" and not l3_i["addr6"]:
                continue

            # vrf (aka route-domain) is stored in the 'fwd' attribute
            vrf = None
            if l3_i["fwd"] != "N/A":
                vrf = l3_i["fwd"].replace("vr:", "")

            # look up admin/oper status in 'hw' section of the output
            if "." in l3_i["name"]:
                phy_name = l3_i["name"].split(".")[0]
            else:
                phy_name = l3_i["name"]
            phy = hw_interfaces_by_name.get(phy_name, None)

            # description and mtu came from an xpath query
            mtu_and_desc = mtus_and_comments.get(
                l3_i["name"], {"mtu": 0, "comment": ""}
            )

            # all the non-IP attributes for each IP entry are the same
            l3i_entry = {
                "interface": l3_i["name"],
                "description": mtu_and_desc["comment"],
                "mtu": mtu_and_desc["mtu"] if mtu_and_desc["mtu"] else 1500,
                "admin_up": bool(phy["mode"] != "(power-down)") if phy else None,
                "oper_up": bool(phy["state"] == "up") if phy else None,
                "vrf": vrf,
            }

            # IPv4 interfaces
            if l3_i["ip"] and l3_i["ip"] != "N/A":
                ipv4_entry = l3i_entry.copy()
                ipv4_entry["ip_address"] = l3_i["ip"]
                l3_interfaces.append(ipv4_entry)

            # IPv6 interfaces are stored as a list, or a string if there's only one
            if l3_i["addr6"]:
                if isinstance(l3_i["addr6"]["member"], str):
                    l3_i["addr6"]["member"] = [l3_i["addr6"]["member"]]

                for ipv6_addr in l3_i["addr6"]["member"]:
                    ipv6_entry = l3i_entry.copy()
                    ipv6_entry["ip_address"] = ipv6_addr
                    l3_interfaces.append(ipv6_entry)

        return l3_interfaces

    def get_active_routes(self) -> List[RouteDict]:
        """
        Gets active routes from all vsyses on the PAN
        """
        result = self._send_command("<show><routing><route/></routing></show>")
        routing = xmltodict.parse(result)

        parsed_routes = []
        for route in routing["response"]["result"]["entry"]:

            # if route isn't active (no A in protocol field), skip it
            if not (route["flags"].startswith("A")):
                continue

            # look at the third character in the flags field to determine
            # protocol - don't really care about the different OSPF types
            if route["flags"][2] not in PANOS_ROUTING_PROTOCOLS:
                raise UMnetNapalmError(
                    f"{self.hostname}: Unknown panos routing protocol {route['flags']}"
                )
            protocol = PANOS_ROUTING_PROTOCOLS[route["flags"][2]]

            # next hops of all zeros indicate local routes
            if route["nexthop"] in ["0.0.0.0", "::"]:
                learned_from = "self"
            else:
                learned_from = route["nexthop"]

            # if this is a local route and we don't have a nh interface, the
            # next hop interface is also 'self' (because it's a host route or a locally-owned IP)
            if learned_from == "self" and not route["interface"]:
                route["interface"] = "self"

            parsed_routes.append(
                {
                    "vrf": route["virtual-router"],
                    "prefix": ip_network(route["destination"]),
                    "nh_interface": route["interface"],
                    "learned_from": learned_from,
                    "protocol": protocol,
                    "age": (
                        timedelta(seconds=int(route["age"])) if route["age"] else None
                    ),
                    "nh_ip": (
                        None if learned_from == "self" else ip_address(route["nexthop"])
                    ),
                    "mpls_label": None,
                    "vxlan_vni": None,
                    "vxlan_endpoint": None,
                }
            )

        # second pass to resolve next hop interface
        output = []
        for route in parsed_routes:

            if route["nh_interface"]:
                output.append(route.copy())
                continue

            nh_routes = resolve_nh(route["nh_ip"], route["vrf"], parsed_routes)
            for nh_route in nh_routes:
                resolved_route = route.copy()
                resolved_route["nh_interface"] = nh_route["nh_interface"]
                output.append(resolved_route)

        return output
