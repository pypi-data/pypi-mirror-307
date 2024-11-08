from datetime import timedelta
import re
from ipaddress import ip_network, ip_interface, ip_address
from ipaddress import (
    IPv4Address,
    IPv6Address,
    IPv4Interface,
    IPv6Interface,
    IPv4Network,
    IPv6Network,
)
import json
from typing import List
from .models import RouteDict


# eventually want to pull this from a more central place
# as we've defined it in so many places already
INTERFACE_ABBRS = {
    # ios
    "Fastethernet": "Fa",
    "GigabitEthernet": "Gi",
    "TwoGigabitEthernet": "Tw",
    "TenGigabitEthernet": "Te",
    "TwentyFiveGigE": "Twe",
    "Port-channel": "Po",
    "Loopback": "Lo",
    # nxos
    "Ethernet": "Eth",
    "port-channel": "Po",
    "loopback": "Lo",
}


class UMnetNapalmJsonEncoder(json.JSONEncoder):
    """
    custom json encoder that handles types
    in our results that aren't encodable by default.
    Reference the "Extending JSONEncoder" section of: https://docs.python.org/3/library/json.html

    Currently ipaddress and timedelta types are the only non-encodable
    types among the results
    """

    def default(self, obj):
        if isinstance(
            obj,
            (
                IPv4Address,
                IPv6Address,
                IPv4Interface,
                IPv6Interface,
                IPv4Network,
                IPv6Network,
                timedelta,
            ),
        ):
            return str(obj)

        return super().default(obj)


def abbr_interface(interface: str) -> str:
    """
    Converts long version of interface name to short one
    if applicable
    """
    for long, short in INTERFACE_ABBRS.items():
        if interface.startswith(long):
            return interface.replace(long, short)

    return interface


def age_to_datetime(age: str) -> timedelta:
    """
    Across platforms age strings can be:
    10y5w, 5w4d, 05d04h, 01:10:12, 3w4d 01:02:03
    """
    days = 0
    hours = 0
    minutes = 0
    seconds = 0
    m = re.search(
        r"^((?P<years>\d+)y)*((?P<weeks>\d+)w)*((?P<days>\d+)d)*((?P<hours>\d+)h)*",
        age,
    )
    if m:
        if m.group("years"):
            days += int(m.group("years")) * 365
        if m.group("weeks"):
            days += int(m.group("weeks")) * 7
        if m.group("days"):
            days += int(m.group("days"))
        if m.group("hours"):
            hours += int(m.group("hours"))

    m = re.search(r"(?P<hours>\d+):(?P<minutes>\d+):(?P<seconds>\d+)$", age)
    if m:
        if m.group("hours"):
            hours += int(m.group("hours"))
        if m.group("minutes"):
            minutes += int(m.group("minutes"))
        if m.group("seconds"):
            seconds += int(m.group("seconds"))

    return timedelta(
        days=days,
        hours=hours,
        minutes=minutes,
        seconds=seconds,
    )


def resolve_nh(nh_ip: str, nh_table: str, routes: List[RouteDict]) -> List[RouteDict]:
    """
    Given a next hop IP and next hop table, search a list of
    routes for that next hop and return LPMs that have a next hop
    interface
    """
    nh_routes = [
        r
        for r in routes
        if r["vrf"] == nh_table
        and r["prefix"].version == ip_network(nh_ip).version
        and r["prefix"].supernet_of(ip_network(nh_ip))
        and r["nh_interface"]
    ]

    if not nh_routes:
        return []

    nh_routes.sort(key=lambda x: x["prefix"].prefixlen, reverse=True)

    # the first entry is a longest prefix match because of our sort,
    # but with ECMP there could be more than one!
    # we'll peel routes off the front with matching lengths to find
    # the rest.
    lpms = [nh_routes[0]]
    if len(nh_routes) > 1:
        for nh_route in nh_routes[1::]:
            if nh_route["prefix"].prefixlen == nh_routes[0]["prefix"].prefixlen:
                lpms.append(nh_route)

    return lpms


def str_to_type(string: str) -> object:
    """
    Converts string output to obvious types.
    empty quote is converted to "None".
    ip_address, ip_interface, and ip_network are converted to their appropriate objecst
    integers are converted to int
    """
    if string in ["", "None"]:
        return None
    if re.match(r"^\d+$", string):
        return int(string)

    for ip_type in [ip_network, ip_interface, ip_address]:
        try:
            return ip_type(string)
        except ValueError:
            pass

    return string
