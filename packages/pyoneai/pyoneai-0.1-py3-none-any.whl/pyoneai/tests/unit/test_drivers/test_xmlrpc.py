# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from xmlrpc.client import ServerProxy

import pytest
from pytest_mock import MockerFixture

from pyoneai.drivers.xmlrpc import OnedServerProxy, OneXMLRPCAPIError


class TestOnedServerProxy:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        self.xml_response = (
            "<HOST_POOL>"
            "    <HOST>"
            "        <ID>1</ID>"
            "        <NAME>host01</NAME>"
            "        <STATE>3</STATE>"
            "        <HOST_SHARE>"
            "            <TOTAL_MEM>2015440</TOTAL_MEM>"
            "            <TOTAL_CPU>200</TOTAL_CPU>"
            "        </HOST_SHARE>"
            "    </HOST>"
            "    <HOST>"
            "        <ID>2</ID>"
            "        <NAME>host02</NAME>"
            "        <STATE>3</STATE>"
            "        <HOST_SHARE>"
            "            <TOTAL_MEM>2015440</TOTAL_MEM>"
            "            <TOTAL_CPU>800</TOTAL_CPU>"
            "        </HOST_SHARE>"
            "    </HOST>"
            "</HOST_POOL>"
        )
        self.result = {
            "HOST_POOL": {
                "HOST": [
                    {
                        "ID": "1",
                        "NAME": "host01",
                        "STATE": "3",
                        "HOST_SHARE": {
                            "TOTAL_MEM": "2015440",
                            "TOTAL_CPU": "200",
                        },
                    },
                    {
                        "ID": "2",
                        "NAME": "host02",
                        "STATE": "3",
                        "HOST_SHARE": {
                            "TOTAL_MEM": "2015440",
                            "TOTAL_CPU": "800",
                        },
                    },
                ]
            }
        }
        self.mock_method_int_success = mocker.MagicMock(
            side_effect=lambda session, *args: [True, 5, 0]
        )
        self.mock_method_xml_success = mocker.MagicMock(
            side_effect=lambda session, *args: [True, self.xml_response, 0]
        )
        self.mock_method_fail = mocker.MagicMock(
            side_effect=lambda session, *args: [False, "Failed", 0x1000, 10]
        )
        self.mock_server_proxy = mocker.MagicMock(
            set=ServerProxy,
            test_method_int_success=self.mock_method_int_success,
            test_method_xml_success=self.mock_method_xml_success,
            test_method_fail=self.mock_method_fail,
        )
        self.mock_server_proxy_class = mocker.patch(
            target="pyoneai.drivers.xmlrpc.ServerProxy",
            autospec=True,
            side_effect=lambda uri: self.mock_server_proxy,
        )
        self.client = OnedServerProxy(
            uri="http://localhost:2633/RPC2", session="oneadmin:oneadmin"
        )

    def test_init(self):
        self.mock_server_proxy_class.assert_called_once_with(
            uri="http://localhost:2633/RPC2"
        )
        assert isinstance(self.client, OnedServerProxy)
        assert self.client._server_proxy is self.mock_server_proxy
        assert self.client._session == "oneadmin:oneadmin"

    def test_call_with_int_response(self):
        result = self.client("test_method_int_success", 1, 2)
        self.mock_method_int_success.assert_called_once_with(
            self.client._session, 1, 2
        )
        assert result == 5

    def test_call_with_xml_response(self):
        result = self.client("test_method_xml_success", 1, 2)
        self.mock_method_xml_success.assert_called_once_with(
            self.client._session, 1, 2
        )
        assert isinstance(result, dict)
        assert result == self.result

    def test_call_fail(self):
        with pytest.raises(OneXMLRPCAPIError):
            _ = self.client("test_method_fail", 1, 2)

    def test_request_with_int_response(self):
        response = self.client.request("test_method_int_success", 1, 2)
        self.mock_method_int_success.assert_called_once_with(
            self.client._session, 1, 2
        )
        assert response == 5

    def test_request_with_xml_response(self):
        response = self.client.request("test_method_xml_success", 1, 2)
        self.mock_method_xml_success.assert_called_once_with(
            self.client._session, 1, 2
        )
        assert response == self.xml_response

    def test_request_fail(self):
        with pytest.raises(OneXMLRPCAPIError):
            _ = self.client.request("test_method_fail", 1, 2)
