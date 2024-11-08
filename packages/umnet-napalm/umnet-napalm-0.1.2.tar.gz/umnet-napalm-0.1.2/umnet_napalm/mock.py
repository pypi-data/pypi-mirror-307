from unittest.mock import patch

from .ios import IOS
from .nxos import NXOS
from .junos import Junos, junos_views
from .iosxr_netconf import IOSXRNetconf
from .abstract_base import AbstractUMnetNapalm


class FixtureNotFoundError(FileNotFoundError):
    pass


class MockParser(AbstractUMnetNapalm):
    """
    Overloads the _send_command methods
    in the different parsers so that the data comes from
    a file instead of a live device
    """

    fixture_vendor = "mock"

    def __init__(self, fixture_path: str, hostname: str):
        self.fixture_path = fixture_path
        self.hostname = hostname

    def _send_command(self, command: str):
        """
        Retrieves command response from a file instead of a live device
        File must be saved at the path provided to the mock constructor, named
        based on the command with underscores instead of spaces.

        Note that for Junos the "command" is actually the junos view
        """
        fixture = command.replace(" ", "_")
        fixture_file = (
            f"{self.fixture_path}/{self.fixture_vendor}/{self.hostname}/{fixture}.txt"
        )
        print(fixture_file)
        try:
            with open(fixture_file, encoding="utf-8") as fh:
                result = fh.read()
        except FileNotFoundError as e:
            raise FixtureNotFoundError from e

        return result


class MockIOS(MockParser, IOS):
    """
    Mock class for testing the IOS parser.
    """

    fixture_vendor = "ios"


class MockIOSXRNetconf(MockParser, IOSXRNetconf):
    """
    Mock class for testing the IOS parser.
    """

    fixture_vendor = "iosxr"


class MockNXOS(MockParser, NXOS):
    """
    Mock class for testing the NXOS parser.
    """

    fixture_vendor = "nxos"


class MockJunos(MockParser, Junos):
    """
    Mock class for testing the Junos parser.
    """

    fixture_vendor = "junos"

    def _send_command(self, command: str):
        """
        You can pass a "path" attribute to the pyez View constructor
        instead of a device and it will read the data from a file - woot.
        """

        view = getattr(junos_views, command)
        fixture_file = f"{self.fixture_path}/{self.fixture_vendor}/{self.hostname}/{view.GET_RPC}.xml"
        result = view(path=fixture_file)  # pylint: disable=no-member
        return result.get()
