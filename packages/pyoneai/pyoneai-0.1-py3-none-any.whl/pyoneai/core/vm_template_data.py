__all__ = ["VMTemplateData"]


import enum
from typing import Annotated

from pydantic import BaseModel, ByteSize, ConfigDict, Field
from pydantic.networks import IPvAnyAddress

from pyoneai.core.image import Image
from pyoneai.core.virtual_network import VirtualNetwork


# TODO: implement this Model as an Entity
class SecurityGroup(BaseModel):
    id: int


@enum.unique
class IOType(enum.StrEnum):
    THREADS = enum.auto()
    NATIVE = enum.auto()


@enum.unique
class DiskType(enum.StrEnum):
    BLOCK = enum.auto()
    CDROM = enum.auto()
    FILE = enum.auto()


@enum.unique
class DiscardPolicy(enum.StrEnum):
    IGNORE = enum.auto()
    DISCARD = enum.auto()


@enum.unique
class ImageFormat(enum.StrEnum):
    RAW = enum.auto()
    QCOW2 = enum.auto()


@enum.unique
class DevicePrefix(enum.StrEnum):
    HD = enum.auto()
    SD = enum.auto()
    VD = enum.auto()


@enum.unique
class CachePolicy(enum.StrEnum):
    NONE = enum.auto()
    WRITEBACK = enum.auto()
    WRITETHROUGH = enum.auto()
    DIRECTSYNC = enum.auto()
    UNSAFE = enum.auto()
    DEFAULT = enum.auto()


@enum.unique
class NetworkMode(enum.StrEnum):
    AUTO = enum.auto()


class Capacity(BaseModel):
    cpu: Annotated[float, Field(ge=0)] | None = None
    vcpu: Annotated[float, Field(ge=0)] = 1
    memory: ByteSize | None = None


class Disk(BaseModel):
    dev_prefix: DevicePrefix | None = None
    target: str | None = None
    driver: str | None = None
    cache: CachePolicy | None = None
    readonly: bool | None = None
    io: IOType | None = None
    total_bytes: int | None = None
    read_bytes: int | None = None
    write_bytes: int | None = None
    total_iops: int | None = None
    read_iops: int | None = None
    write_iops: int | None = None
    size_iops: int | None = None


class ImageDisk(Disk):
    image: Image
    iothread: int | None = None
    virtio_blk_queues: int | None = None
    total_bytes_max: int | None = None
    read_bytes_max: int | None = None
    write_bytes_max: int | None = None
    total_iops_max: int | None = None
    read_iops_max: int | None = None
    write_iops_max: int | None = None
    total_bytes_sex_max_lenght: int | None = None
    read_bytes_max_lenght: int | None = None
    write_bytes_max_lenght: int | None = None
    total_iops_max_lenght: int | None = None
    read_iops_max_lenght: int | None = None
    write_iops_max_lenght: int | None = None
    type: DiskType | None = None
    discard: DiscardPolicy | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class VolatileDisk(Disk):
    type: DiskType | None = None
    size: ByteSize | None = None
    image_format: ImageFormat | None = None


class Nic(BaseModel):
    name: str | None = None
    vnet: VirtualNetwork
    ip: IPvAnyAddress | None = None
    mac: str | None = None
    bridge: str | None = None
    target: str | None = None
    script: str | None = None
    model: str | None = None
    filtering: str | None = None
    security_groups: list[SecurityGroup] | None = None
    inbound_avg_bw: int | None = None
    inbound_peak_bw: int | None = None
    inbound_peak_kb: int | None = None
    outbound_avg_bw: int | None = None
    outbound_peak_bw: int | None = None
    outbound_peak_kb: int | None = None
    mode: NetworkMode | None = None
    sched_requirements: str | None = None
    sched_rank: str | None = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class NicAlias(Nic):
    parent: str


class NicDefault(Nic):
    vnet: VirtualNetwork | None = None  # optional for default nic


class VMTemplateData(BaseModel):
    name: str
    capacity: Capacity
    disks: list[VolatileDisk | ImageDisk] = None
    nics: list[Nic | NicAlias | NicDefault] = None
