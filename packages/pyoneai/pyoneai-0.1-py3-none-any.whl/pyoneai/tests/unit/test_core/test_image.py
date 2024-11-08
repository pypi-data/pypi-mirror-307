from collections.abc import Collection

import pytest
from pytest_mock import MockerFixture

from pyoneai import Session
from pyoneai.core import One
from pyoneai.core.bases import Entity
from pyoneai.core.datastore import Datastore
from pyoneai.core.group import Group
from pyoneai.core.image import Image, ImagePool
from pyoneai.core.user import User


class TestImage:
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        def mock_entity_init(self, session: Session, id: int) -> None:
            self.session = session
            self.id = id

        self.mock_entity_init = mocker.patch(
            target="pyoneai.core.bases.Entity.__init__",
            autospec=True,
            side_effect=mock_entity_init,
        )
        self.client = mocker.MagicMock(
            return_value={"IMAGE": {"ID": 10, "UID": 0, "GID": 1}}
        )
        self.client.request = mocker.MagicMock(return_value="test_response")
        self.mock_session = mocker.MagicMock(spec=Session)
        self.mock_session.oned_client = self.client
        self.image = Image(session=self.mock_session, id=10)

    def test_init(self):
        assert isinstance(self.image, Image)
        self.mock_entity_init.assert_called_once_with(
            self.image, session=self.mock_session, id=10
        )
        assert hasattr(self.image, "session")
        assert self.image.session is self.mock_session
        assert hasattr(self.image, "id")
        assert self.image.id == 10
        assert hasattr(self.image, "user")
        assert isinstance(self.image.user, User)
        assert self.image.user.id == 0
        assert hasattr(self.image, "group")
        assert isinstance(self.image.group, Group)
        assert self.image.group.id == 1

    def test_get_info(self):
        info = self.image.get_info(decrypt_secrets=False)
        print(info)
        self.client.request.assert_called_once_with(
            "one.image.info", 10, False
        )
        assert info == "test_response"

    def test_get_data(self):
        data = self.image.get_data(decrypt_secrets=False)
        self.client.assert_called_once_with("one.image.info", 10, False)
        assert data == {"ID": 10, "UID": 0, "GID": 1}


class TestImagePool:
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        def mock_pool_init(
            self, owner: One | Entity, ids: Collection[int]
        ) -> None:
            self.owner = owner
            self._ids = set(ids)

        self.mock_pool_init = mocker.patch(
            target="pyoneai.core.bases.Pool.__init__",
            autospec=True,
            side_effect=mock_pool_init,
        )
        self.client = mocker.MagicMock(
            return_value={"IMAGE_POOL": {"IMAGE": [{"ID": 0}, {"ID": 1}]}}
        )
        self.mock_session = mocker.MagicMock(spec=Session)
        self.mock_session.oned_client = self.client
        # Images of One
        self.mock_owner = mocker.MagicMock(spec=One)
        self.mock_owner.session = self.mock_session
        self.images = ImagePool(owner=self.mock_owner, ids=[4, 5])
        # Images of Datastore
        self.mock_ds = mocker.MagicMock(spec=Datastore)
        self.mock_ds.id = 0
        self.mock_ds.session = self.mock_session
        self.ds_images = ImagePool(owner=self.mock_ds, ids=[0, 1])

    def test_init(self, mocker: MockerFixture):
        assert isinstance(self.images, ImagePool)
        assert isinstance(self.ds_images, ImagePool)
        self.mock_pool_init.assert_has_calls(
            [
                mocker.call(self.images, owner=self.mock_owner, ids=[4, 5]),
                mocker.call(self.ds_images, owner=self.mock_ds, ids=[0, 1]),
            ]
        )
        assert hasattr(self.images, "owner")
        assert self.images.owner is self.mock_owner
        assert hasattr(self.images, "session")
        assert self.images.session is self.mock_session
        assert hasattr(self.images, "_ids")
        assert self.images._ids == {4, 5}
        assert hasattr(self.ds_images, "owner")
        assert self.ds_images.owner is self.mock_ds
        assert hasattr(self.ds_images, "_ids")
        assert self.ds_images._ids == {0, 1}

    def test_get_system_ids(self):
        ids = self.images._get_system_ids()
        self.client.assert_called_once_with("one.imagepool.info", -2, -1, -1)
        assert isinstance(ids, set)
        assert ids == {0, 1}

    def test_get_owner_ids(self):
        self.client.return_value = {
            "DATASTORE": {"IMAGES": {"ID": ["2", "3"]}}
        }
        ids = self.ds_images._get_system_ids()
        self.client.assert_called_once_with("one.datastore.info", 0)
        assert isinstance(ids, set)
        assert ids == {2, 3}

    def test_get_entity(self, mocker: MockerFixture):
        mock_image = mocker.MagicMock(spec=Image)
        mock_image_class = mocker.patch(
            target="pyoneai.core.image.Image",
            autospec=True,
            return_value=mock_image,
        )
        image = self.images._get_entity(10)
        mock_image_class.assert_called_once_with(
            session=self.mock_session, id=10
        )
        assert image is mock_image
