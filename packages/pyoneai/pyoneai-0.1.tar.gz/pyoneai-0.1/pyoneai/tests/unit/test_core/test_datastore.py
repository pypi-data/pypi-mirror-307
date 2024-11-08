from collections.abc import Collection

import pytest
from pytest_mock import MockerFixture

from pyoneai import Session
from pyoneai.core import Entity, One
from pyoneai.core.datastore import Datastore, DatastorePool
from pyoneai.core.group import Group
from pyoneai.core.image import ImagePool
from pyoneai.core.user import User


class TestDatastore:
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
            return_value={"DATASTORE": {"ID": 10, "UID": 0, "GID": 1}}
        )
        self.client.request = mocker.MagicMock(return_value="test_response")
        self.mock_session = mocker.MagicMock(spec=Session)
        self.mock_session.oned_client = self.client
        self.datastore = Datastore(session=self.mock_session, id=10)
        self.datastore_images = ImagePool(owner=self.datastore, ids=[1, 2])
        mocker.patch(
            "pyoneai.core.datastore.Datastore.images",
            new_callable=mocker.PropertyMock,
            return_value=self.datastore_images,
        )

    def test_init(self):
        assert isinstance(self.datastore, Datastore)
        self.mock_entity_init.assert_called_once_with(
            self.datastore, session=self.mock_session, id=10
        )
        assert hasattr(self.datastore, "session")
        assert self.datastore.session is self.mock_session
        assert hasattr(self.datastore, "id")
        assert self.datastore.id == 10
        assert hasattr(self.datastore, "images")
        assert isinstance(self.datastore.images, ImagePool)
        assert hasattr(self.datastore.images, "owner")
        assert self.datastore.images.owner is self.datastore
        assert hasattr(self.datastore.images, "_ids")
        assert self.datastore.images._ids == {1, 2}
        assert hasattr(self.datastore, "group")
        assert isinstance(self.datastore.group, Group)
        assert self.datastore.group.id == 1
        assert hasattr(self.datastore, "user")
        assert isinstance(self.datastore.user, User)
        assert self.datastore.user.id == 0

    def test_get_info(self):
        info = self.datastore.get_info(decrypt_secrets=False)
        self.client.request.assert_called_once_with(
            "one.datastore.info", 10, False
        )
        assert info == "test_response"

    def test_get_data(self):
        data = self.datastore.get_data(decrypt_secrets=False)
        self.client.assert_called_once_with("one.datastore.info", 10, False)
        assert data == {"ID": 10, "UID": 0, "GID": 1}


class TestDatastorePool:
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
            return_value={
                "DATASTORE_POOL": {"DATASTORE": [{"ID": 0}, {"ID": 1}]}
            }
        )
        self.mock_session = mocker.MagicMock(spec=Session)
        self.mock_session.oned_client = self.client
        self.mock_owner = mocker.MagicMock(spec=One)
        self.mock_owner.session = self.mock_session
        self.datastores = DatastorePool(owner=self.mock_owner, ids=[4, 5])

    def test_init(self):
        assert isinstance(self.datastores, DatastorePool)
        self.mock_pool_init.assert_called_once_with(
            self.datastores, owner=self.mock_owner, ids=[4, 5]
        )
        assert hasattr(self.datastores, "owner")
        assert self.datastores.owner is self.mock_owner
        assert hasattr(self.datastores, "session")
        assert self.datastores.session is self.mock_session
        assert hasattr(self.datastores, "_ids")
        assert self.datastores._ids == {4, 5}

    def test_get_system_ids(self):
        ids = self.datastores._get_system_ids()
        self.client.assert_called_once_with("one.datastorepool.info")
        assert isinstance(ids, set)
        assert ids == {0, 1}

    def test_get_entity(self, mocker: MockerFixture):
        mock_datastore = mocker.MagicMock(spec_set=Datastore)
        mock_datastore_class = mocker.patch(
            target="pyoneai.core.datastore.Datastore",
            autospec=True,
            return_value=mock_datastore,
        )
        datastore = self.datastores._get_entity(10)
        mock_datastore_class.assert_called_once_with(
            session=self.mock_session, id=10
        )
        assert datastore is mock_datastore
