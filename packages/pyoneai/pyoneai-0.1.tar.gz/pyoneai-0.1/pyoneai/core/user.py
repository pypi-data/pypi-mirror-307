__all__ = [
    "User",
    "UserPool",
]

from typing import Any

from .bases import Entity, Pool


class User(Entity):
    __slots__ = ()

    def get_info(self, decrypt_secrets: bool = False) -> str:
        client = self.session.oned_client
        response = client.request("one.user.info", self.id, decrypt_secrets)
        return response

    def get_data(self, decrypt_secrets: bool = False) -> dict[str, Any]:
        client = self.session.oned_client
        data = client("one.user.info", self.id, decrypt_secrets)
        return data["USER"]


class UserPool(Pool):
    __slots__ = ()

    def _get_system_ids(self) -> set[int]:
        client = self.session.oned_client
        data = client("one.userpool.info")["USER_POOL"]["USER"]
        if not isinstance(data, list):
            return {int(data["ID"])}
        return {int(entity_data["ID"]) for entity_data in data}

    def _get_entity(self, id: int) -> User:
        return User(session=self.session, id=id)
