from collections.abc import Collection

import pytest
from pytest_mock import MockerFixture

from pyoneai import Session
from pyoneai.core import Entity, One
from pyoneai.core.group import Group, GroupPool
from pyoneai.core.user import UserPool


class TestGroup:
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
        self.client = mocker.MagicMock(return_value={"GROUP": {"ID": 10}})
        self.client.request = mocker.MagicMock(return_value="test_response")
        self.mock_session = mocker.MagicMock(spec=Session)
        self.mock_session.oned_client = self.client
        self.group = Group(session=self.mock_session, id=10)
        self.group_users = UserPool(owner=self.group, ids=[1, 2])
        mocker.patch(
            "pyoneai.core.group.Group.users",
            new_callable=mocker.PropertyMock,
            return_value=self.group_users,
        )

    def test_init(self):
        assert isinstance(self.group, Group)
        self.mock_entity_init.assert_called_once_with(
            self.group, session=self.mock_session, id=10
        )
        assert hasattr(self.group, "session")
        assert self.group.session is self.mock_session
        assert hasattr(self.group, "id")
        assert self.group.id == 10
        assert hasattr(self.group, "users")
        assert isinstance(self.group.users, UserPool)
        assert hasattr(self.group.users, "owner")
        assert self.group.users.owner is self.group
        assert hasattr(self.group.users, "_ids")
        assert self.group.users._ids == {1, 2}

    def test_get_info(self):
        info = self.group.get_info(decrypt_secrets=False)
        self.client.request.assert_called_once_with(
            "one.group.info", 10, False
        )
        assert info == "test_response"

    def test_get_data(self):
        data = self.group.get_data(decrypt_secrets=False)
        self.client.assert_called_once_with("one.group.info", 10, False)
        assert data == {"ID": 10}


class TestGroupPool:
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
            return_value={"GROUP_POOL": {"GROUP": [{"ID": 0}, {"ID": 1}]}}
        )
        self.mock_session = mocker.MagicMock(spec=Session)
        self.mock_session.oned_client = self.client
        self.mock_owner = mocker.MagicMock(spec=One)
        self.mock_owner.session = self.mock_session
        self.groups = GroupPool(owner=self.mock_owner, ids=[4, 5])

    def test_init(self):
        assert isinstance(self.groups, GroupPool)
        self.mock_pool_init.assert_called_once_with(
            self.groups, owner=self.mock_owner, ids=[4, 5]
        )
        assert hasattr(self.groups, "owner")
        assert self.groups.owner is self.mock_owner
        assert hasattr(self.groups, "session")
        assert self.groups.session is self.mock_session
        assert hasattr(self.groups, "_ids")
        assert self.groups._ids == {4, 5}

    def test_get_system_ids(self):
        ids = self.groups._get_system_ids()
        self.client.assert_called_once_with("one.grouppool.info")
        assert isinstance(ids, set)
        assert ids == {0, 1}

    def test_get_entity(self, mocker: MockerFixture):
        mock_group = mocker.MagicMock(spec_set=Group)
        mock_group_class = mocker.patch(
            target="pyoneai.core.group.Group",
            autospec=True,
            return_value=mock_group,
        )
        group = self.groups._get_entity(10)
        mock_group_class.assert_called_once_with(
            session=self.mock_session, id=10
        )
        assert group is mock_group
