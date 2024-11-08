# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import pytest

from pyoneai.core.pci_device import PCIDevice, PCIDevicePool


class TestPCIDevice:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self):
        self.pci_devices = [
            PCIDevice(
                address="0000:00:00:0",
                short_address="00:00.0",
                vendor_id="8086",
                vendor_name="Intel Corporation",
                device_id="29c0",
                device_name="82G33/G31/P35/P31 Express DRAM Controller",
                class_id="0600",
                class_name="Host bridge",
                type_label="8086:29c0:0600",
                bus="00",
                slot="00",
                numa_node="-",
                domain="0000",
                function="0",
                vm_id=-1,
            ),
            PCIDevice(
                address="0000:00:01:0",
                short_address="00:01.0",
                vendor_id="1af4",
                vendor_name="Red Hat, Inc.",
                device_id="1050",
                device_name="Virtio GPU",
                class_id="0300",
                class_name="VGA compatible controller",
                type_label="1af4:1050:0300",
                bus="00",
                slot="01",
                numa_node="-",
                domain="0000",
                function="0",
                vm_id=0,
            ),
        ]

    def test_init(self):
        assert isinstance(self.pci_devices[0], PCIDevice)
        assert self.pci_devices[0].address == "0000:00:00:0"
        assert self.pci_devices[0].vendor_id == "8086"
        assert self.pci_devices[0].device_id == "29c0"
        assert self.pci_devices[0].class_id == "0600"
        assert self.pci_devices[0].vm_id == -1

        assert isinstance(self.pci_devices[1], PCIDevice)
        assert self.pci_devices[1].address == "0000:00:01:0"
        assert self.pci_devices[1].vendor_id == "1af4"
        assert self.pci_devices[1].device_id == "1050"
        assert self.pci_devices[1].class_id == "0300"
        assert self.pci_devices[1].vm_id == 0

    def test_allocated(self):
        assert not self.pci_devices[0].allocated
        assert self.pci_devices[1].allocated

    def test_compare_free(self):
        assert self.pci_devices[0].compare(free=True)
        assert self.pci_devices[0].compare(
            vendor_id="8086", device_id="29c0", class_id="0600", free=True
        )
        assert self.pci_devices[0].compare(vendor_id="8086", free=True)
        assert not self.pci_devices[0].compare(vendor_id="0", free=True)
        assert not self.pci_devices[1].compare(free=True)

    def test_compare_all(self):
        assert self.pci_devices[0].compare(
            vendor_id="8086", device_id="29c0", class_id="0600"
        )
        assert self.pci_devices[0].compare(vendor_id="8086")
        assert not self.pci_devices[0].compare(vendor_id="0")
        assert self.pci_devices[1].compare(
            vendor_id="1af4", device_id="1050", class_id="0300"
        )
        assert self.pci_devices[1].compare(device_id="1050", class_id="0300")
        assert not self.pci_devices[1].compare(device_id="0")


class TestPCIDevicePool:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self):
        self.pci_devices = [
            PCIDevice(
                address="0000:00:00:0",
                short_address="00:00.0",
                vendor_id="8086",
                vendor_name="Intel Corporation",
                device_id="29c0",
                device_name="82G33/G31/P35/P31 Express DRAM Controller",
                class_id="0600",
                class_name="Host bridge",
                type_label="8086:29c0:0600",
                bus="00",
                slot="00",
                numa_node="-",
                domain="0000",
                function="0",
                vm_id=-1,
            ),
            PCIDevice(
                address="0000:00:01:0",
                short_address="00:01.0",
                vendor_id="1af4",
                vendor_name="Red Hat, Inc.",
                device_id="1050",
                device_name="Virtio GPU",
                class_id="0300",
                class_name="VGA compatible controller",
                type_label="1af4:1050:0300",
                bus="00",
                slot="01",
                numa_node="-",
                domain="0000",
                function="0",
                vm_id=0,
            ),
        ]
        self.pci_device_pool = PCIDevicePool(self.pci_devices)

    def test_init(self):
        assert isinstance(self.pci_device_pool, PCIDevicePool)

    def test_contains(self):
        assert "0000:00:00:0" in self.pci_device_pool
        assert self.pci_devices[1] in self.pci_device_pool
        assert "0" not in self.pci_device_pool

    def test_iter(self):
        pci_device_iter = iter(self.pci_device_pool)
        assert next(pci_device_iter) is self.pci_devices[0]
        assert next(pci_device_iter) is self.pci_devices[1]

    def test_len(self):
        assert len(self.pci_device_pool) == 2

    def test_getitem(self):
        assert self.pci_device_pool["0000:00:00:0"] is self.pci_devices[0]
        assert self.pci_device_pool["0000:00:01:0"] is self.pci_devices[1]

    def test_getitem_with_wrong_key(self):
        with pytest.raises(KeyError):
            _ = self.pci_device_pool["0"]

    def test_get(self):
        assert self.pci_device_pool.get("0000:00:00:0") is self.pci_devices[0]
        assert self.pci_device_pool.get("0000:00:01:0") is self.pci_devices[1]

    def test_filter(self):
        new_pool = self.pci_device_pool.filter(vendor_id="8086")
        assert len(new_pool) == 1
        assert list(new_pool) == [self.pci_devices[0]]

        new_pool = self.pci_device_pool.filter(
            vendor_id="1af4", device_id="1050", class_id="0300"
        )
        assert len(new_pool) == 1
        assert list(new_pool) == [self.pci_devices[1]]

        new_pool = self.pci_device_pool.filter(vendor_id="0")
        assert len(new_pool) == 0
        assert list(new_pool) == []
