# umnet-napalm
This is a project that augments the [NAPALM](https://napalm.readthedocs.io/en/latest/) library in ways that are relevant to our interests.
More specifically, new [getter functions](https://napalm.readthedocs.io/en/latest/support/index.html#getters-support-matrix) have been implemented to pull
data from routers and parse it into a vender agnostic format.


Currently, the following NAPALM classes have been augmented:
* IOS
* NXOS-SSH
* Junos
* PANOS (from [napalm-panos](https://github.com/napalm-automation-community/napalm-panos))

The following "getter" methods have been added:
* `get_ip_interfaces`
* `get_active_routes`
* `get_mpls_switching`
* `get_vni_information`
