import re
from typing import List, Dict
from ipaddress import ip_network
import logging

from napalm.ios import IOSDriver
from napalm.base.helpers import textfsm_extractor

from ..models import RouteDict, MPLSDict, InventoryDict
from ..base import UMnetNapalmError, UMnetNapalm
from ..utils import age_to_datetime, str_to_type, resolve_nh

IOS_PROTOCOLS = {
    "L": "local",
    "C": "connected",
    "S": "static",
    "i": "ISIS",
    "B": "BGP",
    "O": "OSPF",
}

IOS_LABEL_VALUES = {
    "": [],
    "No Label": [],
    "Pop Label": ["pop"],
}

IOS_MPLS_INTERFACES = {"Vl": "Vlan"}

logging.getLogger(__name__)


class IOS(UMnetNapalm, IOSDriver):
    """
    IOS Parser
    """

    LABEL_VALUE_MAP = {
        "": [],
        "No Label": [],
        "Pop Label": ["pop"],
    }

    INVENTORY_TO_TYPE = {
        r"Supervisor": "re",
        r"WS-": "linecard",
        r"Transceiver": "optic",
        r"Fan Module": "fan",
        r"[Pp]ower [Ss]upply": "psu",
        r"Uplink Module": "uplink-module",
        r"^Switch \d+$": "stack-member",
        r"StackPort": "optic",
        # on catalyst the optics show up as interface names
        # sometimes the names are abbreviated and sometimes they
        # are not (sigh)
        r"^(Twe|Te|Gi|Two).+\d$": "optic",
        # don't care about these inventory items
        r"(Clock FRU|Daughterboard|Feature Card|Forwarding Card)": None,
        # this is the chassis id of the master of the stack,
        # we
        r"Stack": None,
    }

    def _parse_protocol_abbr(self, abbr) -> str:
        if abbr in IOS_PROTOCOLS:
            return IOS_PROTOCOLS[abbr]

        raise UMnetNapalmError(f"Unknown IOS protocol abbr {abbr}")

    def _parse_label_value(self, label) -> list:
        """
        Parses mpls label value into normalized data
        """
        if label in IOS_LABEL_VALUES:
            return IOS_LABEL_VALUES[label]

        return [label]

    def _get_route_labels(self) -> Dict[tuple, str]:
        """
        Runs "show bgp vpnv4 unicast labels" and parses the result.

        The output is a dictionary with (vrf, prefix) as key
        and the outbound label as a value, eg
        output[ ("vrf_VOIP_NGFW", "0.0.0.0/0") ] = "12345"
        """

        raw_labels = self._send_command("show bgp vpnv4 unicast all labels")
        labels = textfsm_extractor(self, "sh_bgp_vpnv4_unicast_all_labels", raw_labels)

        # default route shows up as '0.0.0.0' so we have to munge that
        output = {}
        for l in labels:
            prefix = "0.0.0.0/0" if l["prefix"] == "0.0.0.0" else l["prefix"]
            output[(l["vrf"], ip_network(prefix))] = l["out_label"]

        return output

    def get_active_routes(self) -> List[RouteDict]:
        """
        Parses "show ip route vrf *" for IOS. Will also run
        "show bgp vpnv4 unicast labels" to get label bindings
        """

        parsed_routes = []
        output = []

        raw_routes = self._send_command("show ip route vrf *")
        routes = textfsm_extractor(self, "sh_ip_route_vrf_all", raw_routes)

        for route in routes:
            protocol = self._parse_protocol_abbr(route["proto_1"])

            # "learned from" is one of the keys in our route table that determines
            # uniqueness, as such we need to make sure it's set. Usually it's
            # the IP of the advertising router, but for local/direct/static it should
            # get set to 'self'
            if route["nh_ip"]:
                learned_from = route["nh_ip"]
            elif protocol in ["local", "connected", "static"]:
                learned_from = "self"
            else:
                raise UMnetNapalmError(f"Could not determine learned from for {route}")

            parsed_routes.append(
                {
                    "vrf": route["vrf"] if route["vrf"] else "default",
                    "prefix": str_to_type(route["prefix"]),
                    "nh_interface": route["nh_interface"],
                    "learned_from": learned_from,
                    "protocol": self._parse_protocol_abbr(route["proto_1"]),
                    "age": age_to_datetime(route["age"]),
                    "nh_ip": str_to_type(route["nh_ip"]),
                    "mpls_label": None,
                    "vxlan_vni": None,
                    "vxlan_endpoint": None,
                    "nh_table": route["vrf"] if route["vrf"] else "default",
                }
            )

        # Second pass to resolve recursive routes
        labels = self._get_route_labels()
        for route in parsed_routes:
            # routes that were already resolved can be skipped
            if route["nh_interface"]:
                output.append(route)
                continue

            # if we found an integer label mapping for this route we will save the label.
            # note that the way our old core is architected, there is only ever one label
            # in the stack
            if re.match(r"^\d+$", labels.get((route["vrf"], route["prefix"]), "")):
                route["mpls_label"] = [int(labels[(route["vrf"], route["prefix"])])]
                # also making an assumption that we need to resolve the next hop in
                # our default table
                nh_table = "default"

            # if we didn't find a label, assume this is vrf lite and the next hop
            # is in our local vrf
            else:
                nh_table = route["vrf"]

            # attempt to resolve next hop
            nh_lpms = resolve_nh(route["nh_ip"], nh_table, parsed_routes)
            if not nh_lpms:
                logging.error(f"Could not resolve next hop for {route}")
                continue

            # for every lpm found, create an entry for this recursive route
            for lpm in nh_lpms:
                resolved = route.copy()
                resolved["nh_ip"] = lpm["nh_ip"]
                resolved["nh_interface"] = lpm["nh_interface"]
                output.append(resolved)

        return output

    def get_inventory(self) -> list[InventoryDict]:
        """
        Parses "show inventory" for IOS
        """
        raw_inventory = self._send_command("show inventory")
        inventory = textfsm_extractor(self, "sh_inventory", raw_inventory)

        output = []
        for entry in inventory:
            inventory_type = self._get_inventory_type(entry["name"])

            if not inventory_type:
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

    def get_mpls_switching(self) -> List[MPLSDict]:
        """
        Parses "show mpls forwarding table" for IOS
        """
        raw_labels = self._send_command("show mpls forwarding-table")
        labels = textfsm_extractor(self, "sh_mpls_forwarding_table", raw_labels)

        output = []
        for entry in labels:
            # extract RD from 'FEC'
            m = re.match(r"([\d\.]+:\d+):(\d+.\d+.\d+.\d+\/\d+)", entry["fec"])
            if m:
                rd = m.group(1)
                fec = m.group(2)
            else:
                rd = None
                fec = entry["fec"]

            aggregate = bool(entry["vrf"])
            nh_interface = entry["vrf"] if entry["vrf"] else entry["nh_interface"]

            output.append(
                {
                    "in_label": str_to_type(entry["in_label"]),
                    "fec": str_to_type(fec),
                    "out_label": self._parse_label_value(entry["out_label"]),
                    "nh_ip": str_to_type(entry["nh_ip"]),
                    "nh_interface": str_to_type(nh_interface),
                    "rd": rd,
                    "aggregate": aggregate,
                }
            )

        return output
