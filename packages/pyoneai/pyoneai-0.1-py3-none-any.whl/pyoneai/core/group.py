__all__ = [
    "Group",
    "GroupPool",
]

from typing import Any

from .bases import Entity, Pool
from .user import UserPool


class Group(Entity):
    __slots__ = ()

    @property
    def users(self) -> UserPool:
        return UserPool(owner=self)

    def get_info(self, decrypt_secrets: bool = False) -> str:
        client = self.session.oned_client
        response = client.request("one.group.info", self.id, decrypt_secrets)
        return response

    def get_data(self, decrypt_secrets: bool = False) -> dict[str, Any]:
        client = self.session.oned_client
        data = client("one.group.info", self.id, decrypt_secrets)
        return data["GROUP"]


class GroupPool(Pool):
    __slots__ = ()

    def _get_system_ids(self) -> set[int]:
        client = self.session.oned_client
        data = client("one.grouppool.info")["GROUP_POOL"]["GROUP"]
        if not isinstance(data, list):
            return {int(data["ID"])}
        return {int(entity_data["ID"]) for entity_data in data}

    def _get_entity(self, id: int) -> Group:
        return Group(session=self.session, id=id)
