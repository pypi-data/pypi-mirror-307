__all__ = ["One"]

from ..session import Session
from .bases import MetricBase
from .cluster import ClusterPool
from .datastore import DatastorePool
from .group import GroupPool
from .host import HostPool
from .image import ImagePool
from .user import UserPool
from .virtual_machine import VirtualMachinePool
from .virtual_network import VirtualNetworkPool


class One(MetricBase):
    __slots__ = ()

    def __init__(self, session: Session | None = None) -> None:
        if session is None:
            session = Session()
        super().__init__(session=session)

    @property
    def clusters(self) -> ClusterPool:
        return ClusterPool(owner=self)

    @property
    def datastores(self) -> DatastorePool:
        return DatastorePool(owner=self)

    @property
    def groups(self) -> GroupPool:
        return GroupPool(owner=self)

    @property
    def hosts(self) -> HostPool:
        return HostPool(owner=self)

    @property
    def images(self) -> ImagePool:
        return ImagePool(owner=self)

    @property
    def users(self) -> UserPool:
        return UserPool(owner=self)

    @property
    def vms(self) -> VirtualMachinePool:
        return VirtualMachinePool(owner=self)

    @property
    def vnets(self) -> VirtualNetworkPool:
        return VirtualNetworkPool(owner=self)
