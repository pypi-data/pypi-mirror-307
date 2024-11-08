__all__ = ["SessionConfig"]

import os

import yaml

from .registry import FileRegistry


class SessionConfig:
    one_xmlrpc: str
    oned_session: str
    oneflow_server: str
    oneflow_session: str
    prometheus_server: str
    model_path: str
    registry: FileRegistry

    def __init__(self, config_path: os.PathLike[str] | str = "") -> None:
        env = os.environ

        # Reading the configuration file.
        # The configuration file path is given in the environment
        # variable `ONEAIOPS_CONFIG_PATH` if exists, otherwise it is
        # `/etc/one/oneaiops/oneaiops.conf`.
        config_path = (
            config_path
            or env.get("ONEAIOPS_CONFIG_PATH")
            or "/etc/one/aiops/aiops.conf"
        )
        with open(config_path, mode="rb") as config_file:
            config = yaml.safe_load(config_file)

        # Reading the `one_auth` file.
        # The `one_auth` file path is given in the environment variable
        # `ONE_AUTH` if exists, otherwise it is `$HOME/.one/one_auth`.
        auth_path = env.get("ONE_AUTH") or os.path.join(
            env["HOME"], ".one", "one_auth"
        )
        with open(auth_path, mode="r") as auth_file:
            session = auth_file.readlines()[0].strip()
        config |= {"oned_session": session, "oneflow_session": session}

        # Reading the environment variables, see:
        # * https://docs.opennebula.io/6.8/management_and_operations/references/cli.html#shell-environment
        # * https://docs.opennebula.io/6.8/installation_and_configuration/opennebula_services/oneflow.html#configure-cli
        # Environment variable `ONE_XMLRPC` superseeds the configuration
        # file entry.
        if "ONE_XMLRPC" in env:
            config["one_xmlrpc"] = env["ONE_XMLRPC"]
        # Environment variable `ONEFLOW_URL` superseeds the
        # configuration file entry.
        if "ONEFLOW_URL" in env:
            config["oneflow_server"] = env["ONEFLOW_URL"]
        # Environment variables `ONEFLOW_USER` and `ONEFLOW_PASSWORD`
        # superseeds the `one_auth` file entry.
        if "ONEFLOW_USER" in env and "ONEFLOW_PASSWORD" in env:
            user = env["ONEFLOW_USER"]
            password = env["ONEFLOW_PASSWORD"]
            config["oneflow_session"] = f"{user}:{password}"

        self.one_xmlrpc = config["one_xmlrpc"]
        self.oned_session = config["oned_session"]
        self.oneflow_server = config["oneflow_server"]
        self.oneflow_session = config["oneflow_session"]
        self.prometheus_server = config["prometheus_server"]
        self.registry = FileRegistry(config["registry"]["config"])
        self.model_path = config["registry"]["models"]
