import pytest
from pydantic import ValidationError
from pytest_mock import MockerFixture

from pyoneai import Session
from pyoneai.core import One
from pyoneai.core.image import Image
from pyoneai.core.virtual_network import VirtualNetwork
from pyoneai.core.vm_template_data import (
    Capacity,
    ImageDisk,
    Nic,
    NicAlias,
    NicDefault,
    SecurityGroup,
    VMTemplateData,
    VolatileDisk,
)


class TestVMTemplateData:
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        self.mock_session = mocker.MagicMock(spec=Session)
        self.mock_session.config = mocker.MagicMock()

    @pytest.fixture
    def vm_capacity(self):
        return Capacity(cpu=2.0, vcpu=2, memory="512 GB")

    @pytest.fixture
    def vm_image_disk(self):
        return ImageDisk(
            image=Image(id=101, session=self.mock_session),
            kind="block",
            discard="ignore",
            dev_prefix="sd",
            driver="qcow2",
            cache="writeback",
        )

    @pytest.fixture
    def vm_volatile_disk(self):
        return VolatileDisk(
            kind="file",
            size="8 GiB",
            image_format="qcow2",
            dev_prefix="sd",
            driver="qcow2",
            cache="writeback",
        )

    @pytest.fixture
    def vm_nic1(self):
        return Nic(
            name="eth0",
            vnet=VirtualNetwork(id=1, session=self.mock_session),
            ip="192.168.1.100",
            mac="00:11:22:33:44:55",
            bridge="br0",
        )

    @pytest.fixture
    def vm_nic2(self):
        return NicAlias(
            vnet=VirtualNetwork(id=2, session=self.mock_session),
            ip="2001:0db8:85a3:0000:0000:8a2e:0370:7334",
            mac="AA:BB:CC:DD:EE:01",
            bridge="br1",
            parent="eth0",
        )

    @pytest.fixture
    def vm_nic3(self):
        return NicDefault(
            model="virtio",
            security_groups=[SecurityGroup(id=1), SecurityGroup(id=2)],
        )

    def test_vm_template_valid(
        self,
        vm_capacity,
        vm_image_disk,
        vm_volatile_disk,
        vm_nic1,
        vm_nic2,
        vm_nic3,
    ):
        vm_template = VMTemplateData(
            name="Production VM",
            capacity=vm_capacity,
            disks=[vm_image_disk, vm_volatile_disk],
            nics=[vm_nic1, vm_nic2, vm_nic3],
        )

        # Assert general VM template attributes
        assert vm_template.name == "Production VM"
        assert vm_template.capacity.cpu == 2.0
        assert vm_template.capacity.memory == 512000000000

        # Assert Disk attributes
        assert len(vm_template.disks) == 2
        assert vm_template.disks[0].dev_prefix == "sd"
        assert vm_template.disks[0].image.id == 101
        assert vm_template.disks[1].driver == "qcow2"
        assert vm_template.disks[1].size == 8589934592

        # Assert NIC attributes
        assert len(vm_template.nics) == 3
        assert vm_template.nics[0].mac == "00:11:22:33:44:55"
        assert vm_template.nics[0].name == "eth0"
        assert str(vm_template.nics[0].ip) == "192.168.1.100"
        assert str(vm_template.nics[1].ip) == "2001:db8:85a3::8a2e:370:7334"
        assert vm_template.nics[1].parent == "eth0"
        assert vm_template.nics[2].model == "virtio"
        assert vm_template.nics[2].security_groups[0].id == 1
        assert vm_template.nics[2].security_groups[1].id == 2

    def test_vm_template_without_optional_fields(self, vm_capacity):
        vm_template = VMTemplateData(
            name="Minimal VM",
            capacity=vm_capacity,
        )

        assert vm_template.name == "Minimal VM"
        assert vm_template.capacity.cpu == 2.0
        assert vm_template.capacity.vcpu == 2
        assert vm_template.capacity.memory == 512000000000
        assert vm_template.disks is None
        assert vm_template.nics is None

    def test_invalid_capacity(self):
        with pytest.raises(ValueError):
            VMTemplateData(
                name="Invalid VM",
                capacity=Capacity(cpu=-1.0, vcpu=2, memory="4096 Gib"),
            )

    def test_invalid_disk(self, vm_capacity):
        with pytest.raises(ValueError):
            VMTemplateData(
                name="Invalid Disk VM",
                capacity=vm_capacity,
                disks=[
                    ImageDisk(
                        image="image",
                        kind="invalid",
                        dev_prefix="fake",
                    )
                ],
            )

    def test_invalid_nic(self, vm_capacity, vm_image_disk, vm_nic1):
        with pytest.raises(ValidationError):
            Nic(
                name="eth1",
                vnet=VirtualNetwork(id=2, session=self.mock_session),
                ip="999.999.999.999",
            )
        with pytest.raises(ValidationError):
            Nic(
                name="eth2",
                vnet=VirtualNetwork(id=3, session=self.mock_session),
                ip="abcd:efgh:ijkl:zzzz:mnop:qrst:uvwx:yz12",
            )
