# # pylint: disable=no-member
from typing import List, Union
import re
from ipaddress import ip_network

from napalm.junos import JunOSDriver
from napalm.base.models import ARPTableDict

from lxml import etree

from ..base import UMnetNapalmError, UMnetNapalm
from ..models import RouteDict, MPLSDict, InventoryDict
from . import junos_views
from ..utils import age_to_datetime


XCVR_DESC_TO_INTERFACE_PREFIX = {
    r"QSFP": "et-",
    r"SFP\+": "xe-",
    r"SFP-": "ge-",
}

DEFAULT_ARP_AGING_TIMER = 1200


class Junos(UMnetNapalm, JunOSDriver):
    """
    Junos parser
    """

    # interfaces to ignore when doing 'show ip interfaces'
    IGNORE_INTERFACES = [
        "bme",
        "jsrv",
        "em1",
        "em0",
    ]

    # tables to ignore when doing 'show route'
    IGNORE_ROUTE_TABLES = [
        "bgp.l3vpn.0",
        "bgp.l3vpn-inet6.0",
        "inet.3",
        "inet6.3",
        "iso.0",
        "mpls.0",
        ":vxlan.inet.0",
        "__default_evpn__.evpn.0",
        "default-switch.evpn.0",
    ]

    # mapping of inventory name regex to their netbox types
    INVENTORY_TO_TYPE = {
        r"Fan Tray": "fan",
        r"(PIC|MIC|FPC)": "linecard",
        r"Xcvr": "optic",
        r"(PEM|Power Supply)": "psu",
        r"Routing Engine": "re",
        # don't care about these inventory items
        r"(CPU|PDM|FPM|Midplane|CB)": None,
    }

    def __init__(self, hostname: str, username: str, password: str, **kwargs):
        """
        overriding the napalm driver init class so we can keep internal state
        """
        super().__init__(hostname, username, password, **kwargs)
        self._config = None
        self.arp_aging_timer = DEFAULT_ARP_AGING_TIMER

    def _get_junos_inventory_type(self, name: str, model_number: str) -> str:
        """
        Maps the name and part number of the Junos inventory item to its type
        """
        # "Xcvr" parts are always optics
        if name.startswith("Xcvr"):
            return "optic"

        # non-optic parts should always have a model number, if not
        # we don't care about them
        if not (model_number):
            return None

        # EX switches and virtual chassis save their vc members and uplink modules
        # as FPC X and PIC X - we want to classify those correctly
        if re.match(r"EX[234]", model_number):
            if re.search(r"FPC \d+", name):
                return "stack-member"

            if re.search(r"PIC \d+", name):
                return None

        # uplink modules are also saved under PIC X, must classify based
        # on their model number
        if re.match(r"EX-UM", model_number):
            return "uplink-module"

        # otherwise we want to pattern-match based on the INVENTORY_TO_TYPE
        # dictionary
        return self._get_inventory_type(name)

    def _get_xcvr_interface_prefix(self, xcvr_desc: str) -> str:
        """
        Maps xcvr description from "show chassis hardware" to
        interface prefix
        """
        for pattern, prefix in XCVR_DESC_TO_INTERFACE_PREFIX.items():
            if re.match(pattern, xcvr_desc):
                return prefix

        raise UMnetNapalmError(f"{self.hostname}: Unknown xcvr type {xcvr_desc}")

    def _get_mod_number(self, mod_name: str) -> str:
        """
        Strips out "FPC|MIC|PIC" from a module name seen in "show chassis hardware"
        """
        return re.sub(r"(MIC|PIC|FPC) ", "", mod_name)

    def _send_command(self, view: str) -> str:
        """
        Uses junos views to send an RPC command and gets the results
        """
        view = getattr(junos_views, view)
        result = view(self.device)  # pylint: disable=no-member
        return result.get()

    def get_config(self):
        """
        If we run our nornir getters right we can pull the arp aging timer
        out of the config
        """
        self._config = super().get_config()
        return self._config

    def get_active_routes(self) -> List[RouteDict]:
        """
        Parses rpc call show route detail
        """
        result = self._send_command("junos_route_table")

        output = []

        for route in dict(result).values():
            if route.vrf in self.IGNORE_ROUTE_TABLES:
                continue

            prefix = ip_network(route.prefix)

            if route.vrf in ["inet.0", "inet6.0"]:
                vrf = "default"
            else:
                vrf = route.vrf.split(".")[0]

            # also skip link local prefixes
            if prefix.is_link_local:
                continue

            for entry in dict(route.rt_entry).values():
                for next_hop in dict(entry.next_hop).values():
                    if not next_hop.selected_next_hop:
                        continue

                    if entry.learned_from:
                        learned_from = entry.learned_from
                    elif next_hop.nh_ip:
                        learned_from = next_hop.nh_ip
                    elif entry.protocol in ["Direct", "Local", "Static"]:
                        learned_from = "self"
                    else:
                        raise UMnetNapalmError(
                            f"Could not determine learned from for {route}"
                        )
                    
                    mpls_label = self._parse_mpls_label(next_hop.mpls_label)

                    output.append(
                        RouteDict(
                            vrf=vrf,
                            prefix=prefix,
                            nh_interface=next_hop.nh_interface,
                            learned_from=learned_from,
                            protocol=entry.protocol,
                            age=age_to_datetime(entry.age),
                            nh_ip=next_hop.nh_ip,
                            mpls_label=mpls_label,
                            nh_table = "default" if mpls_label else vrf,

                            # not supporting junos VXLAN
                            vxlan_vni=None,
                            vxlan_endpoint=None,
                        )
                    )

        return output

    def get_inventory(self) -> List[InventoryDict]:
        """
        parses the get-chassis-inventory RPC call, which maps to "show chassis hardware"
        """
        result = self._send_command("junos_inventory")

        output = []
        for chassis in dict(result).values():

            # note that the chassis model and s/n are at this level, but
            # that doesn't count as an 'inventory item' so we're ignoring it

            # saving modules, sub-modules and sub-sub modules
            for module in dict(chassis.modules).values():
                self._save_inventory_item(output, module)

                for sub_module in dict(module.sub_modules).values():
                    self._save_inventory_item(output, sub_module, parent=module.name)

                    for sub_sub_module in dict(sub_module.sub_sub_modules).values():
                        self._save_inventory_item(
                            output,
                            sub_sub_module,
                            parent=sub_module.name,
                            grandparent=module.name,
                        )

        return output

    def _save_inventory_item(
        self, output: list, item: any, parent: str = None, grandparent: str = None
    ) -> bool:
        """
        Extracts data from a particular inventory item object.
        Returns whether we care aobut this item or not (so we know whether or not)
        to loop over its children
        """
        # skip builtin types, or parts without model numbers that aren't transcievers
        if item.part_number == "BUILTIN":
            return False

        # get inventory type based on item name and P/N
        inv_type = self._get_junos_inventory_type(item.name, item.model_number)

        if not inv_type:
            return False

        # for transcievers, change the name from Xcvr X to be the junos interface name
        # note that we expect transcievers to always be at the sub-sub module level
        # and thus to have a grandparent and parent
        m = re.search(r"Xcvr (\d+)", item.name)
        if m:
            if not (grandparent or parent):
                raise UMnetNapalmError(
                    f"{self.hostname}: No MIC and PIC found for {item.name}"
                )
            prefix = self._get_xcvr_interface_prefix(item.description)

            item_name = f"{prefix}{self._get_mod_number(grandparent)}/{self._get_mod_number(parent)}/{m.group(1)}"
        else:
            item_name = item.name

        output.append(
            {
                "type": inv_type,
                "name": item_name,
                "part_number": self._get_inventory_part_number(item),
                "serial_number": item.serial_number,
                "parent": parent,
            }
        )

        return True

    def _get_inventory_part_number(self, item: any) -> str:
        """
        Extracts the part number from an inventory item
        which, depending on the specific item, is stashed in
        the part number, model number, or description field
        """
        if item.model_number:
            return item.model_number
        return item.description

    def get_mpls_switching(self) -> List[MPLSDict]:
        """
        Parses 'show route active-path table mpls.0'
        """
        result = self._send_command("junos_mpls_table")

        output = []
        for label in dict(result).values():
            # in our network we can skip these 'label is not at the top
            # of the stack' entries - they're redundant
            # also labels 0-2 are junos-internal
            if "(S=0)" in label.prefix or label.prefix in ["0", "1", "2"]:
                continue

            for entry in dict(label.rt_entry).values():
                for next_hop in dict(entry.next_hop).values():

                    # next hop table is either in 'nh-table-receive' or 'nh-table'
                    nh_table = (
                        next_hop.nh_table
                        if next_hop.nh_table
                        else next_hop.nh_table_receive
                    )

                    (nh_interface, out_label, aggregate) = self._process_mpls_nh(
                        next_hop.nh_interface, next_hop.mpls_label, nh_table
                    )

                    # 'fec' and 'rd' aren't in the Junos mpls.0 table - this is a Cisco
                    # thing from "show mpls switching"
                    output.append(
                        {
                            "in_label": label.prefix,
                            "out_label": out_label,
                            "nh_interface": nh_interface,
                            "fec": None,
                            "nh_ip": next_hop.nh_ip,
                            "rd": None,
                            "aggregate": aggregate,
                        },
                    )

        return output

    def _parse_mpls_label(self, label_str) -> Union[List[int], None]:
        """
        Parses mpls-label parameter into a list of integers
        """
        if not label_str:
            return None

        m = re.match(r"Push (?P<inner>\d+)(, Push (?P<outer>\d+))*", label_str)
        if not m:
            raise UMnetNapalmError(f"Couldn't parse label op {label_str}")

        labels = [m.group("inner")]
        if m.group("outer"):
            labels.append(m.group("outer"))

        return labels

    def _process_mpls_nh(
        self, nh_interface: str, mpls_label: str, nh_table: str
    ) -> tuple:
        """
        Parses 'nh interface', 'mpls_label', and nh_table values
        into something our standardized outpur likes.
        Returns a tuple (nh_interface:str, out_label:list, aggregate:bool )
        """
        # when the next hop is a table, not an interface we're going to
        # classify it as an aggregate label
        if not nh_interface and nh_table:
            nh_vrf = re.sub(r".inet6?.0", "", nh_table)
            return (nh_vrf, ["pop"], True)

        # aggregate labels also show up as nh_interface "lsi.X (VRF_NAME)"
        m = re.match(r"^lsi.\d+ \((\S+)\)", nh_interface)
        if m:
            return (m.group(1), [], True)

        # 'pop' label has trailing whitespace
        if mpls_label and re.match(r"^Pop", mpls_label):
            return (nh_interface, ["pop"], False)

        # 'swap' with optional 'push'
        if mpls_label:
            m = re.match(r"^Swap (?P<inner>\d+)(, Push (?P<outer>\d+))*", mpls_label)
            if m:
                out_label = [m.group("inner")]
                if m.group("outer"):
                    out_label.append(m.group("outer"))

                return (nh_interface, out_label, False)

        raise UMnetNapalmError(
            f"Cannot parse MPLS route nh: {nh_interface} label: {mpls_label}"
        )

    def get_arp_table(self, vrf="") -> ARPTableDict:
        """
        Pulls ARP table - napalm does have get_arp_table for junos but it doesn't
        support VRFs :(

        Because we have to dynamically query every VPN on the device we can't use
        junos views for this since they're based on statically defined rpc calls.
        Instead we'll have to do our own rpc calls under the hood.
        """

        # figure out the ARP aging timer - no operational command appears to show this,
        # pulling it from the config.
        if not (self._config):
            self.get_config()
        m = re.search(r"system \{.+arp {\+aging-timer (\d+);", self._config["running"])
        if m:
            self.arp_aging_timer = int(m.group(1))

        # building the rpc call as an lxml element so we can dynamically add a vrf if we want
        # if no vrf is provided all ARP entries are returned
        arp_rpc = etree.Element("get-arp-table-information")
        etree.SubElement(arp_rpc, "no-resolve")
        etree.SubElement(arp_rpc, "expiration-time")
        if vrf:
            xml_vrf = etree.SubElement(arp_rpc, "vpn")
            xml_vrf.text = vrf

        rpc_result = self.device.execute(arp_rpc)

        results = []
        for xml_entry in rpc_result.iterfind("arp-table-entry"):

            interface = xml_entry.find("interface-name").text.strip("\n")

            # MX and EX9200 include the physical interface in brackets - stripping
            # that out so only the logical interface is shown
            interface = re.sub(r" \[.+\]$", "", interface)

            exp = xml_entry.find("time-to-expire")
            if exp is not None:
                age = self.arp_aging_timer - int(exp.text)
            else:
                age = 0

            results.append(
                {
                    "interface": interface,
                    "ip": xml_entry.find("ip-address").text.strip("\n"),
                    "mac": xml_entry.find("mac-address").text.strip("\n").upper(),
                    "age": age,
                }
            )

        return results
