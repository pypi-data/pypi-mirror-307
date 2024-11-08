from typing import List
import re
from ipaddress import ip_interface
import logging
from napalm.base import NetworkDriver

from .models import IPInterfaceDict, RouteDict, MPLSDict, VNIDict
from .utils import abbr_interface

# from .abstract_base import AbstractUMnetNapalm


class UMnetNapalmError(Exception):
    """
    Generic error class
    """


class UMnetNapalm(NetworkDriver):
    """
    Base class for um-specific (but also non-vendor specific)
    implementations.
    """

    log = logging.getLogger("nornir")

    # populate in child classes
    IGNORE_INTERFACES = []
    LABEL_VALUE_MAP = {}
    INVENTORY_TO_TYPE = {}

    def _get_inventory_type(self, name: str) -> str:
        """
        Maps the name of the inventory item to its type
        """
        for pattern, inv_type in self.INVENTORY_TO_TYPE.items():
            if re.search(pattern, name):
                return inv_type

        raise UMnetNapalmError(f"{self.hostname}: Unknown inventory item {name}")

    def get_ip_interfaces(self) -> List[IPInterfaceDict]:
        """
        Uses a series napalm getters to retrieve layer 3 ip address information.

        getter models reference:
        https://github.com/napalm-automation/napalm/blob/develop/napalm/base/base.py
        """
        phy_interfaces = self.get_interfaces()
        ip_interfaces = self.get_interfaces_ip()
        vrfs = self.get_network_instances()

        # rekeying the vrf data by interface to make our life easier
        vrf_interfaces = {}
        for vrf, vrf_data in vrfs.items():
            for i in vrf_data["interfaces"]["interface"]:
                vrf_interfaces[i] = vrf

        output = []
        for i, data in ip_interfaces.items():
            if self._ignore_interface(i):
                continue

            if i not in phy_interfaces or i not in vrf_interfaces:
                continue

            phy_i = phy_interfaces[i]
            vrf_i = vrf_interfaces[i]

            all_ips = data.get("ipv4", {})
            all_ips.update(data.get("ipv6", {}))

            for a, a_data in all_ips.items():
                ip = ip_interface(f'{a}/{a_data["prefix_length"]}')

                # skip link-local addresses
                if ip.is_link_local:
                    continue

                output.append(
                    {
                        "ip_address": ip,
                        "interface": abbr_interface(i),
                        "description": phy_i["description"],
                        "mtu": phy_i["mtu"],
                        "admin_up": phy_i["is_enabled"],
                        "oper_up": phy_i["is_up"],
                        "vrf": vrf_i,
                    }
                )
        return output

    def get_active_routes(self) -> List[RouteDict]:
        """get active routes"""
        return []

    def get_mpls_switching(self) -> List[MPLSDict]:
        """get mpls switching (the mpls forwarding table)"""
        return []

    def get_vni_information(self) -> List[VNIDict]:
        """get vni to vlan and VRF mapping"""
        return []

    def _ignore_interface(self, interface: str) -> bool:
        for ignore in self.IGNORE_INTERFACES:
            if re.search(ignore, interface):
                return True
        return False

    def _parse_label_value(self, label) -> list:
        """
        Parses mpls label value into normalized data
        """
        if label in self.LABEL_VALUE_MAP:
            return self.LABEL_VALUE_MAP[label]

        return [label]
