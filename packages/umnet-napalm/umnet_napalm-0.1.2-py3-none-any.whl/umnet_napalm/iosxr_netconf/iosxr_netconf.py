from typing import List
from ipaddress import ip_interface, ip_network
from datetime import timedelta
from copy import deepcopy



from lxml import etree

from napalm.iosxr_netconf import IOSXRNETCONFDriver
from ncclient.xml_ import to_ele

from ..base import UMnetNapalm
from ..models import RouteDict, IPInterfaceDict
from ..utils import resolve_nh, str_to_type

from .constants import IP_INT_RPC_REQ, IP_ROUTE_RPC_REQ, NS


class IOSXRNetconf(IOSXRNETCONFDriver, UMnetNapalm):
    """
    IOSXR Class
    """

    # Helper xml methods that always pass in our namespaces by default
    def _text(self, xml_tree, path, default=None, namespaces=NS):
        return super()._find_txt(xml_tree, path, default, namespaces=namespaces)

    def _xpath(self, xml_tree, path, namespaces=NS):
        return getattr(xml_tree, "xpath")(path, namespaces=namespaces)

    def _find(self, xml_tree, element, namespaces=NS):
        return getattr(xml_tree, "find")(element, namespaces=namespaces)

    def _iterfind(self, xml_tree, element, namespaces=NS):
        return getattr(xml_tree, "iterfind")(element, namespaces=namespaces)

    def get_ip_interfaces(self) -> List[IPInterfaceDict]:
        """
        Gets IP interfaces
        """
        rpc_reply = self.device.dispatch(to_ele(IP_INT_RPC_REQ)).xml
        xml_result = etree.fromstring(rpc_reply)
        results = []

        # looking at every interface and pulling operation state and description
        for i in self._xpath(xml_result, "//int:interfaces/int:interface"):

            i_name = self._text(i, "int:interface-name")
            i_data = {
                "interface": i_name,
                "description": self._text(i, "int:description"),
                "admin_up": self._text(i, "int:state") != "im-state-admin-down",
                "oper_up": self._text(i, "int:line-state") == "im-state-up",
            }

            # pulling primary IPv4 for the interface. Note that though we're looping,
            # we only expect the xpath query to return a single entry.
            for pri_ipv4 in self._xpath(
                xml_result,
                f"//int4:vrf/int4:details/int4:detail[int4:interface-name='{i_name}']",
            ):
                ip = self._text(pri_ipv4, "int4:primary-address")

                prefixlen = self._text(pri_ipv4, "int4:prefix-length")

                i_data.update(
                    {
                        "vrf": self._text(pri_ipv4, "../../int4:vrf-name"),
                        "mtu": self._text(pri_ipv4, "int4:mtu"),
                    }
                )
                if ip != "0.0.0.0":
                    i_data.update(
                        {
                            "ip_address": ip_interface(f"{ip}/{prefixlen}"),
                            "mtu": self._text(pri_ipv4, "int4:mtu"),
                        }
                    )
                    results.append(i_data.copy())

                # ipv4 secondaries
                for sec_ipv4 in self._iterfind(pri_ipv4, "int4:secondary-address"):
                    ip = self._text(sec_ipv4, "int4:address")
                    prefixlen = self._text(sec_ipv4, "int4:prefix-length")
                    i_data["ip_address"] = ip_interface(f"{ip}/{prefixlen}")
                    results.append(i_data.copy())

            # ipv6 addresses
            for ipv6 in self._xpath(
                xml_result,
                f"//int6:global-detail[int6:interface-name='{i_name}']/int6:address",
            ):
                i_data["mtu"] = self._text(ipv6, "../int6:mtu")
                ip = self._text(ipv6, "int6:address")
                prefixlen = self._text(ipv6, "int6:prefix-length")
                i_data["ip_address"] = ip_interface(f"{ip}/{prefixlen}")
                results.append(i_data.copy())

        return results

    def get_active_routes(self) -> List[RouteDict]:
        """
        Pulls active routes from the rib
        """
        rpc_reply = self.device.dispatch(to_ele(IP_ROUTE_RPC_REQ)).xml
        xml_result = etree.fromstring(rpc_reply)

        parsed_routes = []

        # ipv4 rib and ipv6 rib yang models are similar enough that we can
        # use the same logic for both
        for v in ["4", "6"]:
            for route in self._xpath(
                xml_result,
                f"//rib{v}:ip-rib-route-table-name/rib{v}:routes/rib{v}:route",
            ):
                vrf = self._text(route, f"../../../../../../../../rib{v}:vrf-name")

                subnet = self._text(route, f"rib{v}:address")
                prefixlen = self._text(route, f"rib{v}:prefix-length")
                protocol = self._text(route, f"rib{v}:protocol-name")
                age = self._text(route, f"rib{v}:route-age")
                prefix = ip_network(f"{subnet}/{prefixlen}")



                for nh in self._xpath(
                    route, f"rib{v}:route-path/rib{v}:ipv{v}-rib-edm-path"
                ):
                    learned_from = self._text(nh, f"rib{v}:information-source")
                    if learned_from == "0.0.0.0":
                        learned_from = "self"

                    # not currently dealing with enapsulation (where the next hop
                    # could be in a different table), but we do have some PBR
                    # that shows up under 'next-hop-vrf-name
                    if self._text(nh, f"rib{v}:next-hop-vrf-name"):
                        nh_table = self._text(nh, f"rib{v}:next-hop-vrf-name")
                    else:
                        nh_table = vrf

                    parsed_routes.append(
                        {
                            "vrf": vrf,
                            "prefix": prefix,
                            "nh_interface": str_to_type(self._text(nh, f"rib{v}:interface-name")),
                            "learned_from": learned_from,
                            "protocol": protocol,
                            "nh_ip": self._text(nh, f"rib{v}:address"),
                            "age": timedelta(seconds=int(age)),
                            "mpls_label": [],
                            "vxlan_vni": None,
                            "nh_table": nh_table,
                        }
                    )

        # second pass to resolve next hops
        output = []
        for route in parsed_routes:
            if route["nh_interface"]:
                output.append(route)
                continue

            # attempt to resolve next hop
            nh_table = (
                "default" if route["mpls_label"] or route["vxlan_vni"] else route["vrf"]
            )
            nh_lpms = resolve_nh(route["nh_ip"], nh_table, parsed_routes)
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
