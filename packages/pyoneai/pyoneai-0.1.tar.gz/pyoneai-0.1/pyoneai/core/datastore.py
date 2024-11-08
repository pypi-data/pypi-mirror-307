__all__ = [
    "Datastore",
    "DatastorePool",
]
from typing import Any

from .bases import Entity, LatestMetricValue, Pool
from .group import Group
from .image import ImagePool
from .user import User


class Datastore(Entity):
    __slots__ = ()

    @property
    def user(self) -> User:
        uid = int(self.get_data(decrypt_secrets=False)["UID"])
        return User(id=uid, session=self.session)

    @property
    def group(self) -> Group:
        guid = int(self.get_data(decrypt_secrets=False)["GID"])
        return Group(id=guid, session=self.session)

    @property
    def images(self) -> ImagePool:
        return ImagePool(owner=self)

    free_bytes = LatestMetricValue(float)
    used_bytes = LatestMetricValue(float)
    total_bytes = LatestMetricValue(float)

    def get_info(self, decrypt_secrets: bool = False) -> str:
        client = self.session.oned_client
        response = client.request(
            "one.datastore.info", self.id, decrypt_secrets
        )
        return response

    def get_data(self, decrypt_secrets: bool = False) -> dict[str, Any]:
        client = self.session.oned_client
        data = client("one.datastore.info", self.id, decrypt_secrets)
        return data["DATASTORE"]


class DatastorePool(Pool):
    __slots__ = ()

    def _get_system_ids(self) -> set[int]:
        client = self.session.oned_client
        data = client("one.datastorepool.info")["DATASTORE_POOL"]["DATASTORE"]
        if not isinstance(data, list):
            return {int(data["ID"])}
        return {int(entity_data["ID"]) for entity_data in data}

    def _get_entity(self, id: int) -> Datastore:
        return Datastore(session=self.session, id=id)
