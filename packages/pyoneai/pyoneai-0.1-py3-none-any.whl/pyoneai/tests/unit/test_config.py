# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import os

import pytest
from pytest_mock import MockerFixture

from pyoneai import SessionConfig


class TestSessionConfig:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        mocker.patch(
            "builtins.open",
            mocker.mock_open(
                read_data=(
                    "one_xmlrpc: http://localhost:2633/RPC2\n"
                    "oneflow_server: http://localhost:2474\n"
                    "prometheus_server: http://localhost:9090\n"
                    "registry:\n"
                    "  config: /etc/one/registry.yaml\n"
                    "  models: /etc/one/models"
                )
            ),
        )
        mocker.patch(
            "yaml.safe_load",
            return_value={
                "one_xmlrpc": "http://localhost:2633/RPC2",
                "oneflow_server": "http://localhost:2474",
                "prometheus_server": "http://localhost:9090",
                "registry": {
                    "config": "/etc/one/registry.yaml",
                    "models": "/etc/one/models",
                },
                "mlops": {
                    "sequence_length": 24,
                    "batch_size": 5,
                    "num_workers": 0,
                    "epochs": 2,
                    "lr": 0.05,
                    "weight_decay": 0.001,
                },
                "plan_executor": {
                    "version": "v1",
                    "host": "localhost",
                    "port": 8080,
                },
            },
        )
        mocker.patch.dict(
            os.environ, {"ONE_AUTH": "/home/user/.one/one_auth"}, clear=True
        )
        mocker.patch(
            "builtins.open", mocker.mock_open(read_data="user:password")
        )
        mocker.patch("pyoneai.config.FileRegistry")
        self.config = SessionConfig()

    def test_load_default_paths_fixed(self, mocker):
        assert self.config.one_xmlrpc == "http://localhost:2633/RPC2"
        assert self.config.oned_session == "user:password"
        assert self.config.oneflow_server == "http://localhost:2474"
        assert self.config.oneflow_session == "user:password"
        assert self.config.prometheus_server == "http://localhost:9090"
