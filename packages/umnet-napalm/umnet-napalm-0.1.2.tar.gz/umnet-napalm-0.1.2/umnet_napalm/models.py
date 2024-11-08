from ipaddress import ip_network, ip_interface, ip_address
from typing import Optional

from datetime import timedelta

from typing_extensions import TypedDict


# using TypedDict to model our standardized output because that's
# what nampalm does and I like it - ref
# https://github.com/napalm-automation/napalm/blob/develop/napalm/base/models.py
VNIDict = TypedDict(
    "VNIDict",
    {
        "vni": int,
        "mcast_group": Optional[ip_address],
        "vrf": Optional[str],
        "vlan_id": Optional[int],
    },
)

RouteDict = TypedDict(
    "RouteDict",
    {
        "vrf": str,
        "prefix": ip_network,
        "nh_interface": str,
        "learned_from": str,
        "protocol": str,
        "age": timedelta,
        "nh_table": str,
        "nh_ip": Optional[ip_address],
        "mpls_label": Optional[list[str]],
        "vxlan_vni": Optional[int],
        "vxlan_endpoint": Optional[ip_address],
    },
)

MPLSDict = TypedDict(
    "MPLSDict",
    {
        "in_label": str,
        "out_label": list,
        "nh_interface": Optional[str],
        "fec": Optional[ip_network],
        "nh_ip": Optional[ip_address],
        "rd": Optional[str],
        "aggregate": bool,
    },
)

IPInterfaceDict = TypedDict(
    "IPInterfaceDict",
    {
        "ip_address": ip_interface,
        "interface": str,
        "description": str,
        "mtu": int,
        "admin_up": bool,
        "oper_up": bool,
        "vrf": str,
    },
)

VersionDict = TypedDict(
    "VersionDict",
    {
        "ip": ip_address,
        "version": str,
        "vendor": str,
        "model": str,
        "serial": str,
    },
)

NeighborsDict = TypedDict(
    "NeighborsDict",
    {
        "port": str,
        "remote_device": str,
        "remote_port": str,
    },
)

InventoryDict = TypedDict(
    "InventoryDict",
    {
        "type": str,
        "name": str,
        "part_number": str,
        "serial_number": str,
        "parent": str,
    },
)
