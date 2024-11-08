from typing import List
from ipaddress import ip_interface, ip_network, ip_address
from copy import deepcopy
import re

from napalm.nxos_ssh import NXOSSSHDriver
from napalm.base.helpers import textfsm_extractor
from napalm.base.models import FactsDict

from ..base import UMnetNapalmError, UMnetNapalm
from ..models import RouteDict, MPLSDict, IPInterfaceDict, VNIDict, InventoryDict
from ..utils import age_to_datetime, str_to_type, resolve_nh, abbr_interface


class NXOS(UMnetNapalm, NXOSSSHDriver):
    """
    NXOS Parser
    """

    LABEL_VALUE_MAP = {
        "No": [],
        "Pop": ["pop"],
    }

    # for nexus we're going to map the 'description' provided by
    # show inventory to the type
    INVENTORY_TO_TYPE = {
        # note we're using the fact that this dict gets evaluated
        # sequentially
        r"Fabric Module$": "fabric-module",
        r"Supervisor Module$": "re",
        r"Fan Module$": "fan",
        r"Module$": "linecard",
        r"Power Supply$": "psu",
        r"^Transceiver": "optic",
        # don't care about chassis or system controller types
        r"Chassis": None,
        r"System Controller": None,
    }

    def _get_nxos_inventory_type(self, name: str, desc: str) -> str:
        """
        Figures out the inventory type based on the 'name' and 'desc'
        fields from 'show inventory all'
        """

        # the description field is all over the place for 3rd party
        # optics, so we want to rely on the 'name' field, which
        # is always the interface name
        if name.startswith("Ethernet"):
            return "optic"

        # otherwise we want to figure this out based on description
        return self._get_inventory_type(desc)

    def get_active_routes(self) -> List[RouteDict]:
        """
        Parses 'sh ip route detail vrf all'
        """

        parsed_routes = []
        raw_routes = self._send_command("show ip route detail vrf all")
        routes = textfsm_extractor(self, "sh_ip_route_detail_vrf_all", raw_routes)

        for route in routes:
            # skip 'broadcast' and 'local' routes, we don't really care about these
            if route["protocol"] in ["broadcast", "local"]:
                continue

            # "learned from" is one of the keys in our route table that determines
            # uniqueness, as such we need to make sure it's set. Usually it's
            # the IP of the advertising router, but for local/direct/static it should
            # get set to 'self'
            if route["nh_ip"]:
                learned_from = route["nh_ip"]
            elif route["protocol"] in ["direct", "local", "vrrp", "static"]:
                learned_from = "self"
            else:
                raise UMnetNapalmError(f"Could not determine learned from for {route}")

            parsed_routes.append(
                {
                    "vrf": route["vrf"],
                    "prefix": ip_network(route["prefix"]),
                    "nh_interface": route["nh_interface"],
                    "learned_from": learned_from,
                    "protocol": route["protocol"],
                    "age": age_to_datetime(route["age"]),
                    "nh_ip": str_to_type(route["nh_ip"]),
                    "mpls_label": [route["label"]] if route["label"] else [],
                    "vxlan_vni": str_to_type(route["vni"]),
                    "vxlan_endpoint": str_to_type(route["nh_ip"]),
                    "nh_table": "default" if route["mpls_label"] or route["vxlan_vni"] else route["vrf"]
                }
            )

        # second pass to deal with recursive routes
        output = []
        for route in parsed_routes:
            if route["nh_interface"]:
                output.append(route)
                continue

            # attempt to resolve next hop
            nh_lpms = resolve_nh(route["nh_ip"], route["nh_table"], parsed_routes)
            if not nh_lpms:
                self.log.error("Could not resolve next hop for %s", route)
                continue
            # for every lpm found create an entry in our table for this recursive
            # route
            for lpm in nh_lpms:
                resolved = deepcopy(route)
                resolved["nh_ip"] = lpm["nh_ip"]
                resolved["nh_interface"] = lpm["nh_interface"]
                resolved["mpls_label"].extend(lpm["mpls_label"])
                output.append(resolved)

        return output

    def get_facts(self) -> FactsDict:
        """
        Cleans up model number on napalm get_facts
        """

        results = super().get_facts()

        model = results["model"]
        m = re.match(r"Nexus(3|9)\d+ (\S+) (\(\d Slot\) )*Chassis$", model)

        # some models have the "N9K" or "N3K already in them, some don't.
        if m and re.match(r"N\dK", m.group(2)):
            results["model"] = m.group(2)
        elif m:
            results["model"] = f"N{m.group(1)}K-{m.group(2)}"

        return results

    def get_mpls_switching(self) -> List[MPLSDict]:
        """
        parses show mpls into a dict that outputs
        aggregate labels and
        """
        output = []

        raw_entries = self._send_command("show mpls switching detail")
        entries = textfsm_extractor(self, "sh_mpls_switching_detail", raw_entries)

        for entry in entries:
            # for aggregate labels the next hop is the VRF
            nh_interface = entry["vrf"] if entry["vrf"] else entry["nh_interface"]
            output.append(
                {
                    "in_label": str_to_type(entry["in_label"]),
                    "out_label": self._parse_label_value(entry["out_label"]),
                    "fec": str_to_type(entry["fec"]),
                    "nh_ip": str_to_type(entry["nh_ip"]),
                    "nh_interface": str_to_type(nh_interface),
                    "rd": str_to_type(entry["rd"]),
                    "aggregate": bool(entry["vrf"]),
                }
            )

        return output

    def get_inventory(self) -> List[InventoryDict]:
        """
        Parses "show inventory"
        """
        raw_inventory = self._send_command("show inventory all")
        inventory = textfsm_extractor(self, "sh_inventory_all", raw_inventory)

        output = []
        for entry in inventory:

            # removing quotes from name and description fields,
            # which are enquoted for certain types
            for key in ["name", "desc"]:
                entry[key] = entry[key].replace('"', "")

            inventory_type = self._get_nxos_inventory_type(entry["name"], entry["desc"])
            if not inventory_type:
                continue

            # if this is a linecard in slot 1 and the model number
            # doesn't look like a linecard, then this is a fixed config device
            # and the "lincard" is really the chassis and we want to ingore it
            if (
                inventory_type == "linecard"
                and entry["name"] == "Slot 1"
                and re.match(r"N[39]K-C", entry["pid"])
            ):
                continue

            output.append(
                {
                    "type": inventory_type,
                    "name": entry["name"],
                    "part_number": entry["pid"],
                    "serial_number": entry["sn"],
                    "parent": None,
                }
            )

        return output

    def get_ip_interfaces(self) -> List[IPInterfaceDict]:
        output = []

        # NOTE: because "get_interfaces" currently has a bug for loopback and mgmt IPs on Nexus,
        # we're going to do our own parsing. WE can actually get everything we need
        # with a combination of "show ip int vrf all" and the napalm get_interfaces
        # function
        raw_interfaces = self._send_command("show ip interface vrf all")
        ip_interfaces = textfsm_extractor(
            self, "sh_ip_interface_vrf_all", raw_interfaces
        )
        phy_interfaces = super().get_interfaces()

        for i in ip_interfaces:
            # some l3 interfaces don't have IP addresses (like EVPN L3VPN vrf SVIs)
            # we want to skip those.
            if not i["ip_address"]:
                continue
            phy_i = phy_interfaces.get(i["interface"], {})
            output.append(
                {
                    "ip_address": ip_interface(f'{i["ip_address"]}/{i["prefixlen"]}'),
                    "interface": abbr_interface(i["interface"]),
                    "description": phy_i.get("description", ""),
                    "mtu": int(i["mtu"]),
                    "admin_up": (i["admin_state"] == "admin-up"),
                    "oper_up": (i["protocol_state"] == "protocol-up"),
                    "vrf": i["vrf"],
                }
            )

        return output

    def get_vni_information(self) -> List[VNIDict]:
        """
        Runs "show nve vni" to get vni info
        """
        output = []
        raw_vnis = self._send_command("show nve vni")
        vnis = textfsm_extractor(self, "sh_nve_vni", raw_vnis)

        for vni in vnis:

            output.append(
                {
                    "vni": str_to_type(vni["vni"]),
                    "mcast_group": (
                        None
                        if vni["mcast_grp"] == "n/a"
                        else ip_address(vni["mcast_grp"])
                    ),
                    "vrf": vni["bd_vrf"] if vni["type"] == "L3" else None,
                    "vlan_id": (
                        vni["bd_vrf"]
                        if vni["type"] == "L2" and vni["bd_vrf"] != "UC"
                        else None
                    ),
                },
            )

        return output
