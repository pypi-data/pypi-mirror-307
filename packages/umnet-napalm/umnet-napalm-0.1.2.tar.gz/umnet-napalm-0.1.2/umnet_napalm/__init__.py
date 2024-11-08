from .nxos import NXOS
from .ios import IOS
from .junos import Junos
from .panos import PANOS
from .iosxr_netconf import IOSXRNetconf
from .mock import MockNXOS, MockIOS, MockJunos

PLATFORM_MAP = {
    "ios": IOS,
    "nxos_ssh": NXOS,
    "junos": Junos,
    "panos": PANOS,
    "iosxr_netconf": IOSXRNetconf,
}
MOCK_PLATFORM_MAP = {
    "ios": MockIOS,
    "nxos": MockNXOS,
    "junos": MockJunos,
}


def get_network_driver(platform: str):
    """
    Returns network driver based on platform string.
    """
    for valid_platform, driver in PLATFORM_MAP.items():
        if valid_platform == platform:
            return driver

    raise NotImplementedError(f"Unsupported platform {platform}")


def get_mock_driver(platform: str):
    """
    Returns mocked driver for testing
    """
    for valid_platform, driver in MOCK_PLATFORM_MAP.items():
        if valid_platform == platform:
            return driver

    raise NotImplementedError(f"Unsupported mock platform {platform}")
