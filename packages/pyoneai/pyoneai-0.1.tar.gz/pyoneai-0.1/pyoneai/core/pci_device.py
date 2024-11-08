__all__ = ["PCIDevice", "PCIDevicePool"]

from collections.abc import Collection, Iterator
from dataclasses import dataclass
from typing import Any, Self


@dataclass(frozen=True, slots=True)
class PCIDevice:
    address: str
    short_address: str
    vendor_id: str
    vendor_name: str
    device_id: str
    device_name: str
    class_id: str
    class_name: str
    type_label: str
    bus: str
    slot: str
    numa_node: str
    domain: str
    function: str
    profiles: str | None = None
    uu_id: str | None = None
    vm_id: int = -1

    @property
    def allocated(self) -> bool:
        return self.vm_id >= 0

    def compare(
        self,
        vendor_id: str = "*",
        device_id: str = "*",
        class_id: str = "*",
        free: bool = False,
    ) -> bool:
        if free and self.allocated:
            return False
        return (
            vendor_id in {"*", self.vendor_id}
            and device_id in {"*", self.device_id}
            and class_id in {"*", self.class_id}
        )


class PCIDevicePool:
    __slots__ = ("_pci_devices",)

    def __init__(self, pci_devices: Collection[PCIDevice]) -> None:
        self._pci_devices = {device.address: device for device in pci_devices}

    def __contains__(self, item: str | PCIDevice) -> bool:
        if isinstance(item, PCIDevice):
            return item.address in self._pci_devices
        return item in self._pci_devices

    def __iter__(self) -> Iterator[PCIDevice]:
        return iter(self._pci_devices.values())

    def __len__(self) -> int:
        return len(self._pci_devices)

    def __bool__(self) -> bool:
        return bool(self._pci_devices)

    def __getitem__(self, key: str) -> PCIDevice:
        return self._pci_devices[key]

    def get(self, key: str, default: Any = None) -> Any:
        return self._pci_devices.get(key, default)

    def filter(
        self,
        vendor_id: str = "*",
        device_id: str = "*",
        class_id: str = "*",
        free: bool = False,
    ) -> Self:
        devices = [
            device
            for device in self._pci_devices.values()
            if device.compare(vendor_id, device_id, class_id, free)
        ]
        return type(self)(devices)
