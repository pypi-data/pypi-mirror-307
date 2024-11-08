# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from collections.abc import Collection

import numpy as np
import pytest
from pytest_mock import MockerFixture

from pyoneai import Session
from pyoneai.core import Entity, One
from pyoneai.core.host import Host, HostPool
from pyoneai.core.virtual_machine import VirtualMachinePool


class TestHost:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        def mock_entity_init(self, session: Session, id: int) -> None:
            self.session = session
            self.id = id

        self.mock_entity_init = mocker.patch(
            target="pyoneai.core.bases.Entity.__init__",
            autospec=True,
            side_effect=mock_entity_init,
        )
        pci_device_data = [
            {
                "ADDRESS": "0000:00:00:0",
                "BUS": "00",
                "CLASS": "0600",
                "CLASS_NAME": "Host bridge",
                "DEVICE": "29c0",
                "DEVICE_NAME": "82G33/G31/P35/P31 Express DRAM Controller",
                "DOMAIN": "0000",
                "FUNCTION": "0",
                "NUMA_NODE": "-",
                "SHORT_ADDRESS": "00:00.0",
                "SLOT": "00",
                "TYPE": "8086:29c0:0600",
                "VENDOR": "8086",
                "VENDOR_NAME": "Intel Corporation",
                "VMID": "-1",
            },
            {
                "ADDRESS": "0000:00:01:0",
                "BUS": "00",
                "CLASS": "0300",
                "CLASS_NAME": "VGA compatible controller",
                "DEVICE": "1050",
                "DEVICE_NAME": "Virtio GPU",
                "DOMAIN": "0000",
                "FUNCTION": "0",
                "NUMA_NODE": "-",
                "SHORT_ADDRESS": "00:01.0",
                "SLOT": "01",
                "TYPE": "1af4:1050:0300",
                "VENDOR": "1af4",
                "VENDOR_NAME": "Red Hat, Inc.",
                "VMID": "-1",
            },
        ]
        host_share_data = {"PCI_DEVICES": {"PCI": pci_device_data}}
        self.client = mocker.MagicMock(
            return_value={"HOST": {"ID": 10, "HOST_SHARE": host_share_data}}
        )
        self.client.request = mocker.MagicMock(return_value="test_response")
        self.mock_session = mocker.MagicMock(spec=Session)
        self.mock_session.oned_client = self.client
        self.host = Host(session=self.mock_session, id=10)
        self.host_vms = VirtualMachinePool(owner=self.host, ids=[0, 1])
        mocker.patch(
            "pyoneai.core.host.Host.vms",
            new_callable=mocker.PropertyMock,
            return_value=self.host_vms,
        )

    def test_init(self):
        assert isinstance(self.host, Host)
        self.mock_entity_init.assert_called_once_with(
            self.host, session=self.mock_session, id=10
        )
        assert hasattr(self.host, "session")
        assert self.host.session is self.mock_session
        assert hasattr(self.host, "id")
        assert self.host.id == 10
        assert hasattr(self.host, "vms")
        assert isinstance(self.host.vms, VirtualMachinePool)
        assert hasattr(self.host.vms, "owner")
        assert self.host.vms.owner is self.host
        assert hasattr(self.host.vms, "_ids")
        assert self.host.vms._ids == {0, 1}

    def test_latest_values(self, mocker: MockerFixture):
        mock_metric = mocker.MagicMock(to_array=lambda copy: np.array([10.0]))
        mock_metric_accessor = mocker.MagicMock()
        mock_metric_accessor.__getitem__.return_value = mock_metric
        mock_metric_collection = mocker.MagicMock()
        mock_metric_collection.__getitem__.return_value = mock_metric_accessor
        self.host.metrics = mock_metric_collection
        result = self.host.cpu_ratio
        mock_metric_collection.__getitem__.assert_called_once_with("cpu_ratio")
        mock_metric_accessor.__getitem__.assert_called_once_with("0")
        assert isinstance(result, float)
        assert result == 10.0

    def test_get_info(self):
        info = self.host.get_info(decrypt_secrets=False)
        self.client.request.assert_called_once_with("one.host.info", 10, False)
        assert info == "test_response"

    def test_get_data(self):
        data = self.host.get_data(decrypt_secrets=False)
        self.client.assert_called_once_with("one.host.info", 10, False)
        assert "ID" in data
        assert data["ID"] == 10

    def test_pci_devices(self, mocker: MockerFixture):
        mock_pci_device = mocker.patch(
            target="pyoneai.core.host.PCIDevice", autospec=True
        )
        mock_pci_device_pool = mocker.patch(
            target="pyoneai.core.host.PCIDevicePool", autospec=True
        )
        _ = self.host.pci_devices
        self.client.assert_called_once_with("one.host.info", 10, False)
        mock_pci_device.assert_called()
        mock_pci_device_pool.assert_called_once()


class TestHostPool:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        def mock_pool_init(
            self, owner: One | Entity, ids: Collection[int]
        ) -> None:
            self.owner = owner
            self._ids = set(ids)

        self.mock_pool_init = mocker.patch(
            target="pyoneai.core.bases.Pool.__init__",
            autospec=True,
            side_effect=mock_pool_init,
        )
        self.client = mocker.MagicMock(
            return_value={"HOST_POOL": {"HOST": [{"ID": 0}, {"ID": 1}]}}
        )
        self.mock_session = mocker.MagicMock(spec=Session)
        self.mock_session.oned_client = self.client
        self.mock_owner = mocker.MagicMock(spec=One)
        self.mock_owner.session = self.mock_session
        self.hosts = HostPool(owner=self.mock_owner, ids=[4, 5])

    def test_init(self):
        assert isinstance(self.hosts, HostPool)
        self.mock_pool_init.assert_called_once_with(
            self.hosts, owner=self.mock_owner, ids=[4, 5]
        )
        assert hasattr(self.hosts, "owner")
        assert self.hosts.owner is self.mock_owner
        assert hasattr(self.hosts, "session")
        assert self.hosts.session is self.mock_owner.session
        assert hasattr(self.hosts, "_ids")
        assert self.hosts._ids == {4, 5}

    def test_get_system_ids(self):
        ids = self.hosts._get_system_ids()
        self.client.assert_called_once_with("one.hostpool.info")
        assert isinstance(ids, set)
        assert ids == {0, 1}

    def test_get_entity(self, mocker: MockerFixture):
        mock_host = mocker.MagicMock(spec_set=Host)
        mock_host_class = mocker.patch(
            target="pyoneai.core.host.Host",
            autospec=True,
            return_value=mock_host,
        )
        host = self.hosts._get_entity(10)
        mock_host_class.assert_called_once_with(
            session=self.mock_session, id=10
        )
        assert host is mock_host
