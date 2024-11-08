from abc import ABCMeta, abstractmethod
from typing import Dict, List

import napalm.base.models as napalm_models
from . import models as umnet_models


class AbstractUMnetNapalm(metaclass=ABCMeta):
    """
    Abstract definition of umnet_napalm class.
    Some of these methods are expected to be inherited from
    NAPALM. Extensions to NAPALM are defined in vendor-specific child classes

    """

    @abstractmethod
    def __init__(self, hostname: str) -> str:
        """at minimum we need a hostname for mock"""
        self.hostname = hostname

    @abstractmethod
    def get_facts(self) -> napalm_models.FactsDict:
        """get basic device facts"""

    @abstractmethod
    def get_lldp_neighbors(self) -> Dict[str, List[napalm_models.LLDPNeighborDict]]:
        """get lldp neighbors"""

    @abstractmethod
    def get_ip_interfaces(self) -> List[umnet_models.IPInterfaceDict]:
        """get IP interface information"""

    @abstractmethod
    def get_arp_table(self) -> List[napalm_models.ARPTableDict]:
        """get IP interface information"""

    @abstractmethod
    def get_active_routes(self) -> List[umnet_models.RouteDict]:
        """get active routes"""

    @abstractmethod
    def get_mpls_switching(self) -> List[umnet_models.MPLSDict]:
        """get mpls switching (the mpls forwarding table)"""

    @abstractmethod
    def get_vni_information(self) -> List[umnet_models.VNIDict]:
        """get vni to vlan and VRF mapping"""

    @abstractmethod
    def get_inventory(self) -> List[umnet_models.InventoryDict]:
        """get inventory items"""
