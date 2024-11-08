# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

from collections.abc import Collection

import numpy as np
import pytest
from pytest_mock import MockerFixture

from pyoneai import Session
from pyoneai.core import Entity, One
from pyoneai.core.errors import VMMethodError
from pyoneai.core.group import Group
from pyoneai.core.host import Host
from pyoneai.core.user import User
from pyoneai.core.virtual_machine import (
    VirtualMachine,
    VirtualMachineMigration,
    VirtualMachinePool,
)
from pyoneai.drivers.xmlrpc import _OneXMLRPCError


class TestVirtualMachine:
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
        self.vm_template_data = {
            "UID": 0,
            "GID": 1,
            "TEMPLATE": {
                "PCI": [
                    {
                        "CLASS": "0403",
                        "DEVICE": "293e",
                        "NAME": "PCI0",
                        "PCI_ID": "0",
                        "VENDOR": "8086",
                        "VM_ADDRESS": "01:01.0",
                        "VM_BUS": "0x01",
                        "VM_DOMAIN": "0x0000",
                        "VM_FUNCTION": "0",
                        "VM_SLOT": "0x01",
                    },
                    {
                        "CLASS": "0300",
                        "DEVICE": "1050",
                        "NAME": "PCI1",
                        "PCI_ID": "1",
                        "VENDOR": "1af4",
                        "VM_ADDRESS": "01:02.0",
                        "VM_BUS": "0x01",
                        "VM_DOMAIN": "0x0000",
                        "VM_FUNCTION": "0",
                        "VM_SLOT": "0x02",
                    },
                ]
            },
            "USER_TEMPLATE": {"SCHED_REQUIREMENTS": 'ID="0"|ID="1"'},
        }
        self.client = mocker.MagicMock(
            return_value={"VM": {"ID": 10, **self.vm_template_data}}
        )
        self.client.request = mocker.MagicMock(return_value="test_response")
        self.mock_session = mocker.MagicMock(spec=Session)
        self.mock_session.oned_client = self.client
        self.vm = VirtualMachine(session=self.mock_session, id=10)

    def test_init(self):
        assert isinstance(self.vm, VirtualMachine)
        self.mock_entity_init.assert_called_once_with(
            self.vm, session=self.mock_session, id=10
        )
        assert hasattr(self.vm, "session")
        assert self.vm.session is self.mock_session
        assert hasattr(self.vm, "id")
        assert self.vm.id == 10
        assert hasattr(self.vm, "user")
        assert isinstance(self.vm.user, User)
        assert self.vm.user.id == 0
        assert hasattr(self.vm, "group")
        assert isinstance(self.vm.group, Group)
        assert self.vm.group.id == 1

    def test_latest_values(self, mocker: MockerFixture):
        mock_metric = mocker.MagicMock(to_array=lambda copy: np.array([1.0]))
        mock_metric_accessor = mocker.MagicMock()
        mock_metric_accessor.__getitem__.return_value = mock_metric
        mock_metric_collection = mocker.MagicMock()
        mock_metric_collection.__getitem__.return_value = mock_metric_accessor
        self.vm.metrics = mock_metric_collection
        result = self.vm.host_id
        mock_metric_collection.__getitem__.assert_called_once_with("host_id")
        mock_metric_accessor.__getitem__.assert_called_once_with("0")
        assert isinstance(result, int)
        assert result == 1

    def test_get_info(self):
        info = self.vm.get_info(decrypt_secrets=False)
        self.client.request.assert_called_once_with("one.vm.info", 10, False)
        assert info == "test_response"

    def test_get_data(self):
        data = self.vm.get_data(decrypt_secrets=False)
        self.client.assert_called_once_with("one.vm.info", 10, False)
        assert isinstance(data, dict)
        assert {"ID", "UID", "GID", "TEMPLATE", "USER_TEMPLATE"} <= data.keys()
        assert data["ID"] == 10
        assert data["UID"] == 0
        assert data["GID"] == 1
        assert data["TEMPLATE"] == self.vm_template_data["TEMPLATE"]
        assert data["USER_TEMPLATE"] == self.vm_template_data["USER_TEMPLATE"]

    def test_pci_devices(self):
        pci_devices = self.vm.pci_devices
        self.client.assert_called_once_with("one.vm.info", 10, False)
        assert isinstance(pci_devices, list)
        assert len(pci_devices) == 2
        assert pci_devices == self.vm_template_data["TEMPLATE"]["PCI"]

    def test_scheduling_requirements(self):
        scheduling = self.vm.scheduling_requirements
        self.client.assert_called_once_with("one.vm.info", 10, False)
        assert len(scheduling) == 2
        assert scheduling.ids == {0, 1}

    @pytest.mark.parametrize(
        "method, kwargs",
        [
            ("terminate", {"hard": False}),
            ("terminate", {"hard": True}),
            ("undeploy", {"hard": False}),
            ("undeploy", {"hard": True}),
            ("poweroff", {"hard": False}),
            ("poweroff", {"hard": True}),
            ("reboot", {"hard": False}),
            ("reboot", {"hard": True}),
            ("stop", {}),
            ("suspend", {}),
            ("resume", {}),
            ("resched", {}),
            ("unresched", {}),
        ],
    )
    def test_vm_actions(self, method, kwargs):
        action = f"{method}-hard" if kwargs.get("hard") else method
        method = getattr(self.vm, method)
        method(**kwargs)
        self.client.assert_called_once_with(
            "one.vm.action", action, self.vm.id
        )
        self.vm.session.oned_client.side_effect = _OneXMLRPCError("")
        with pytest.raises(VMMethodError):
            method(**kwargs)

    @pytest.mark.parametrize(
        "method, kwargs",
        [
            ("rename", {"name": "Valid VM Name"}),
            ("recover", {"operation": 0}),
            ("lock", {"level": 3}),
            ("unlock", {}),
            ("recover", {"operation": np.float64(2)}),
            (
                "migrate",
                {
                    "host": 7,
                    "live": True,
                    "overcommit": True,
                    "data_store": 0,
                    "kind": VirtualMachineMigration.SAVE,
                },
            ),
        ],
    )
    def test_vm_methods(self, method, kwargs):
        action = method
        method = getattr(self.vm, method)
        method(**kwargs)
        if action == "migrate":
            kwargs["kind"] = VirtualMachineMigration.SAVE.value
            kwargs["overcommit"] = False
        self.client.assert_called_once_with(
            f"one.vm.{action}", self.vm.id, *kwargs.values()
        )
        self.vm.session.oned_client.side_effect = _OneXMLRPCError("")
        with pytest.raises(VMMethodError):
            method(**kwargs)

    def test_vm_resize(self):
        self.vm.resize(cpu=2, vcpu=3, memory=4, overcommit=True)
        expected_template = (
            "<TEMPLATE>"
            "<CPU>2</CPU>"
            "<VCPU>3</VCPU>"
            "<MEMORY>4</MEMORY>"
            "</TEMPLATE>"
        )
        self.client.assert_called_once_with(
            "one.vm.resize", self.vm.id, expected_template, False
        )
        self.vm.session.oned_client.side_effect = _OneXMLRPCError("")
        with pytest.raises(VMMethodError):
            self.vm.resize(cpu=2, vcpu=3, memory=4, overcommit=True)


class TestVirtualMachinePool:
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
            return_value={"VM_POOL": {"VM": [{"ID": 0}, {"ID": 1}]}}
        )
        self.mock_session = mocker.MagicMock(spec=Session)
        self.mock_session.oned_client = self.client
        # VM Pool of One
        self.mock_owner = mocker.MagicMock(spec=One)
        self.mock_owner.session = self.mock_session
        self.vms = VirtualMachinePool(owner=self.mock_owner, ids=[4, 5])
        # VM Pool of Host
        self.mock_host = mocker.MagicMock(spec=Host)
        self.mock_host.id = 0
        self.mock_host.session = self.mock_session
        self.host_vms = VirtualMachinePool(owner=self.mock_host, ids=[0, 1])

    def test_init(self, mocker: MockerFixture):
        assert isinstance(self.vms, VirtualMachinePool)
        assert isinstance(self.host_vms, VirtualMachinePool)
        self.mock_pool_init.assert_has_calls(
            [
                mocker.call(self.vms, owner=self.mock_owner, ids=[4, 5]),
                mocker.call(self.host_vms, owner=self.mock_host, ids=[0, 1]),
            ]
        )
        assert hasattr(self.vms, "owner")
        assert self.vms.owner is self.mock_owner
        assert hasattr(self.vms, "session")
        assert self.vms.session is self.mock_owner.session
        assert hasattr(self.vms, "_ids")
        assert self.vms._ids == {4, 5}
        assert hasattr(self.host_vms, "owner")
        assert self.host_vms.owner is self.mock_host
        assert hasattr(self.host_vms, "_ids")
        assert self.host_vms._ids == {0, 1}

    def test_get_system_ids(self):
        ids = self.vms._get_system_ids()
        self.client.assert_called_once_with("one.vmpool.info", -2, -1, -1, -2)
        assert isinstance(ids, set)
        assert ids == {0, 1}

    def test_get_owner_ids(self):
        self.client.return_value = {"HOST": {"VMS": {"ID": ["2", "3"]}}}
        ids = self.host_vms._get_system_ids()
        self.client.assert_called_once_with("one.host.info", 0)
        assert isinstance(ids, set)
        assert ids == {2, 3}

    def test_get_entity(self, mocker: MockerFixture):
        mock_vm = mocker.MagicMock(spec_set=VirtualMachine)
        mock_vm_class = mocker.patch(
            target="pyoneai.core.virtual_machine.VirtualMachine",
            autospec=True,
            return_value=mock_vm,
        )
        vm = self.vms._get_entity(10)
        mock_vm_class.assert_called_once_with(session=self.mock_session, id=10)
        assert vm is mock_vm
