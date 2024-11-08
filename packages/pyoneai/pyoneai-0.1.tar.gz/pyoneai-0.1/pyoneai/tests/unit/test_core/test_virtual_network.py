from collections.abc import Collection

import pytest
from pytest_mock import MockerFixture

from pyoneai import Session
from pyoneai.core import Entity, One
from pyoneai.core.group import Group
from pyoneai.core.user import User
from pyoneai.core.virtual_network import VirtualNetwork, VirtualNetworkPool


class TestVirtualNetwork:
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
            return_value={"VNET": {"ID": 10, "UID": 0, "GID": 1}}
        )
        self.client.request = mocker.MagicMock(return_value="test_response")
        self.mock_session = mocker.MagicMock(spec=Session)
        self.mock_session.oned_client = self.client
        self.vnet = VirtualNetwork(session=self.mock_session, id=10)

    def test_init(self):
        assert isinstance(self.vnet, VirtualNetwork)
        self.mock_entity_init.assert_called_once_with(
            self.vnet, session=self.mock_session, id=10
        )
        assert hasattr(self.vnet, "session")
        assert self.vnet.session is self.mock_session
        assert hasattr(self.vnet, "id")
        assert self.vnet.id == 10
        assert hasattr(self.vnet, "user")
        assert isinstance(self.vnet.user, User)
        assert self.vnet.user.id == 0
        assert hasattr(self.vnet, "group")
        assert isinstance(self.vnet.group, Group)
        assert self.vnet.group.id == 1

    def test_get_info(self):
        info = self.vnet.get_info(decrypt_secrets=False)
        self.client.request.assert_called_once_with("one.vn.info", 10, False)
        assert info == "test_response"

    def test_get_data(self):
        data = self.vnet.get_data(decrypt_secrets=False)
        self.client.assert_called_once_with("one.vn.info", 10, False)
        assert data == {"ID": 10, "UID": 0, "GID": 1}


class TestVirtualNetworkPool:
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
            return_value={"VNET_POOL": {"VNET": [{"ID": 0}, {"ID": 1}]}}
        )
        self.mock_session = mocker.MagicMock(spec=Session)
        self.mock_session.oned_client = self.client
        self.mock_owner = mocker.MagicMock(spec=One)
        self.mock_owner.session = self.mock_session
        self.vnets = VirtualNetworkPool(owner=self.mock_owner, ids=[4, 5])

    def test_init(self):
        assert isinstance(self.vnets, VirtualNetworkPool)
        self.mock_pool_init.assert_called_once_with(
            self.vnets, owner=self.mock_owner, ids=[4, 5]
        )
        assert hasattr(self.vnets, "owner")
        assert self.vnets.owner is self.mock_owner
        assert hasattr(self.vnets, "session")
        assert self.vnets.session is self.mock_session
        assert hasattr(self.vnets, "_ids")
        assert self.vnets._ids == {4, 5}

    def test_get_system_ids(self):
        ids = self.vnets._get_system_ids()
        self.client.assert_called_once_with("one.vnpool.info", -2, -1, -1)
        assert isinstance(ids, set)
        assert ids == {0, 1}

    def test_get_entity(self, mocker: MockerFixture):
        mock_vnet = mocker.MagicMock(spec_set=VirtualNetwork)
        mock_vnet_class = mocker.patch(
            target="pyoneai.core.virtual_network.VirtualNetwork",
            autospec=True,
            return_value=mock_vnet,
        )
        vnet = self.vnets._get_entity(10)
        mock_vnet_class.assert_called_once_with(
            session=self.mock_session, id=10
        )
        assert vnet is mock_vnet
