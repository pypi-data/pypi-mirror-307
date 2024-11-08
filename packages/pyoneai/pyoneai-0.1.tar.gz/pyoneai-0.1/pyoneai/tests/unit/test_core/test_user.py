from collections.abc import Collection

import pytest
from pytest_mock import MockerFixture

from pyoneai import Session
from pyoneai.core import One
from pyoneai.core.bases import Entity
from pyoneai.core.user import User, UserPool


class TestUser:
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
        self.client = mocker.MagicMock(return_value={"USER": {"ID": 10}})
        self.client.request = mocker.MagicMock(return_value="test_response")
        self.mock_session = mocker.MagicMock(spec=Session)
        self.mock_session.oned_client = self.client
        self.user = User(session=self.mock_session, id=10)

    def test_init(self):
        assert isinstance(self.user, User)
        self.mock_entity_init.assert_called_once_with(
            self.user, session=self.mock_session, id=10
        )
        assert hasattr(self.user, "session")
        assert self.user.session is self.mock_session
        assert hasattr(self.user, "id")
        assert self.user.id == 10

    def test_get_info(self):
        info = self.user.get_info(decrypt_secrets=False)
        print(info)
        self.client.request.assert_called_once_with("one.user.info", 10, False)
        assert info == "test_response"

    def test_get_data(self):
        data = self.user.get_data(decrypt_secrets=False)
        self.client.assert_called_once_with("one.user.info", 10, False)
        assert data == {"ID": 10}


class TestUserPool:
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
            return_value={"USER_POOL": {"USER": [{"ID": 0}, {"ID": 1}]}}
        )
        self.mock_session = mocker.MagicMock(spec=Session)
        self.mock_session.oned_client = self.client
        self.mock_owner = mocker.MagicMock(spec=One)
        self.mock_owner.session = self.mock_session
        self.users = UserPool(owner=self.mock_owner, ids=[4, 5])

    def test_init(self, mocker: MockerFixture):
        assert isinstance(self.users, UserPool)
        self.mock_pool_init.assert_called_once_with(
            self.users, owner=self.mock_owner, ids=[4, 5]
        )
        assert hasattr(self.users, "owner")
        assert self.users.owner is self.mock_owner
        assert hasattr(self.users, "session")
        assert self.users.session is self.mock_session
        assert hasattr(self.users, "_ids")
        assert self.users._ids == {4, 5}

    def test_get_system_ids(self):
        ids = self.users._get_system_ids()
        self.client.assert_called_once_with("one.userpool.info")
        assert isinstance(ids, set)
        assert ids == {0, 1}

    def test_get_entity(self, mocker: MockerFixture):
        mock_user = mocker.MagicMock(spec=User)
        mock_user_class = mocker.patch(
            target="pyoneai.core.user.User",
            autospec=True,
            return_value=mock_user,
        )
        user = self.users._get_entity(10)
        mock_user_class.assert_called_once_with(
            session=self.mock_session, id=10
        )
        assert user is mock_user
