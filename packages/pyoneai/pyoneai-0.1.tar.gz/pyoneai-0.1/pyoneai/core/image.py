from typing import Any

from .bases import Entity, Pool
from .group import Group
from .user import User


class Image(Entity):
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
        response = client.request("one.image.info", self.id, decrypt_secrets)
        return response

    def get_data(self, decrypt_secrets: bool = False) -> dict[str, Any]:
        client = self.session.oned_client
        data = client("one.image.info", self.id, decrypt_secrets)
        return data["IMAGE"]


class ImagePool(Pool):
    __slots__ = ()

    def _get_system_ids(self) -> set[int]:
        from .datastore import Datastore

        client = self.session.oned_client
        # Get Images from the owner datastore
        if isinstance(self.owner, Datastore):
            data = client("one.datastore.info", self.owner_id)["DATASTORE"][
                "IMAGES"
            ]
            if data is None:
                return set()
            return {int(id_) for id_ in data["ID"]}
        # Get all system Images
        else:
            data = client("one.imagepool.info", -2, -1, -1)["IMAGE_POOL"][
                "IMAGE"
            ]
            if not isinstance(data, list):
                return {int(data["ID"])}
            return {int(entity_data["ID"]) for entity_data in data}

    def _get_entity(self, id: int) -> Image:
        return Image(session=self.session, id=id)
