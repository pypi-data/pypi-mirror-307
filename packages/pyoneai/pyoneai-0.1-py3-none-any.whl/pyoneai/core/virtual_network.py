__all__ = [
    "VirtualNetwork",
    "VirtualNetworkPool",
]

from typing import Any

from .bases import Entity, Pool
from .group import Group
from .user import User


class VirtualNetwork(Entity):
    __slots__ = ()

    @property
    def user(self) -> User:
        uid = int(self.get_data(decrypt_secrets=False)["UID"])
        return User(id=uid, session=self.session)

    @property
    def group(self) -> Group:
        guid = int(self.get_data(decrypt_secrets=False)["GID"])
        return Group(id=guid, session=self.session)

    def get_info(self, decrypt_secrets: bool = False) -> str:
        client = self.session.oned_client
        response = client.request("one.vn.info", self.id, decrypt_secrets)
        return response

    def get_data(self, decrypt_secrets: bool = False) -> dict[str, Any]:
        client = self.session.oned_client
        data = client("one.vn.info", self.id, decrypt_secrets)
        return data["VNET"]


class VirtualNetworkPool(Pool):
    __slots__ = ()

    def _get_system_ids(self) -> set[int]:
        client = self.session.oned_client
        data = client("one.vnpool.info", -2, -1, -1)["VNET_POOL"]["VNET"]
        if not isinstance(data, list):
            return {int(data["ID"])}
        return {int(entity_data["ID"]) for entity_data in data}

    def _get_entity(self, id: int) -> VirtualNetwork:
        return VirtualNetwork(session=self.session, id=id)
