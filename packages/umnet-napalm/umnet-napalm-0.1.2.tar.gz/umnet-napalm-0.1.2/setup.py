# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['umnet_napalm',
 'umnet_napalm.ios',
 'umnet_napalm.iosxr_netconf',
 'umnet_napalm.junos',
 'umnet_napalm.nxos',
 'umnet_napalm.panos']

package_data = \
{'': ['*'],
 'umnet_napalm.ios': ['utils/textfsm_templates/*'],
 'umnet_napalm.nxos': ['utils/textfsm_templates/*']}

install_requires = \
['napalm-panos>=0.6.2,<0.7.0', 'napalm>=4.0.0,<5.0.0']

setup_kwargs = {
    'name': 'umnet-napalm',
    'version': '0.1.2',
    'description': 'A custom version of NAPALM for UMnet',
    'long_description': '# umnet-napalm\nThis is a project that augments the [NAPALM](https://napalm.readthedocs.io/en/latest/) library in ways that are relevant to our interests.\nMore specifically, new [getter functions](https://napalm.readthedocs.io/en/latest/support/index.html#getters-support-matrix) have been implemented to pull\ndata from routers and parse it into a vender agnostic format.\n\n\nCurrently, the following NAPALM classes have been augmented:\n* IOS\n* NXOS-SSH\n* Junos\n* PANOS (from [napalm-panos](https://github.com/napalm-automation-community/napalm-panos))\n\nThe following "getter" methods have been added:\n* `get_ip_interfaces`\n* `get_active_routes`\n* `get_mpls_switching`\n* `get_vni_information`\n',
    'author': 'Amy Liebowitz',
    'author_email': 'amylieb@umich.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<3.12',
}


setup(**setup_kwargs)
