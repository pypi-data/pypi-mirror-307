# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import pytest
from prometheus_api_client.prometheus_connect import PrometheusConnect
from pytest_mock import MockerFixture

from pyoneai import Session
from pyoneai.drivers.xmlrpc import OnedServerProxy
from pyoneai.session import OneFlowClient


class TestSession:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        self.mock_config = mocker.MagicMock(
            one_xmlrpc="http://localhost:2633/RPC2",
            oned_session="oneadmin:oneadmin",
            oneflow_server="http://localhost:2474",
            oneflow_session="oneadmin:oneadmin",
            prometheus_server="http://localhost:9090",
            registry=mocker.MagicMock(),
            model_path=mocker.MagicMock(),
        )
        self.mock_session_config_class = mocker.patch(
            target="pyoneai.session.SessionConfig",
            autospec=True,
            return_value=self.mock_config,
        )
        self.session = Session(config_path="oneaiops.conf")

    def test_init(self):
        self.mock_session_config_class.assert_called_once_with("oneaiops.conf")
        assert isinstance(self.session, Session)
        assert self.session.config is self.mock_config
        assert isinstance(self.session.oned_client, OnedServerProxy)
        assert (
            self.session.oned_client._server_proxy._ServerProxy__host
            == "localhost:2633"
        )
        assert (
            self.session.oned_client._server_proxy._ServerProxy__handler
            == "/RPC2"
        )
        assert self.session.oned_client._session == "oneadmin:oneadmin"
        assert isinstance(self.session.oneflow_client, OneFlowClient)
        assert self.session.oneflow_client.url == "http://localhost:2474"
        assert self.session.oneflow_client.session == "oneadmin:oneadmin"
        assert isinstance(self.session.prometheus_client, PrometheusConnect)
        assert self.session.prometheus_client.url == "http://localhost:9090"
