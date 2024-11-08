# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import pytest
from pytest_mock import MockerFixture

from pyoneai import Session
from pyoneai.core import (
    ClusterPool,
    DatastorePool,
    GroupPool,
    HostPool,
    ImagePool,
    One,
    UserPool,
    VirtualMachinePool,
    VirtualNetworkPool,
)


class TestOne:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        self.mock_metric_base_init = mocker.patch(
            target="pyoneai.core.bases.MetricBase.__init__",
            autospec=True,
            side_effect=lambda self, session: setattr(
                self, "session", session
            ),
        )
        self.mock_cluster_pool_class = mocker.patch(
            target="pyoneai.core.one.ClusterPool", autospec=True
        )
        self.mock_host_pool_class = mocker.patch(
            target="pyoneai.core.one.HostPool", autospec=True
        )
        self.mock_vm_pool_class = mocker.patch(
            target="pyoneai.core.one.VirtualMachinePool", autospec=True
        )
        self.mock_vnet_pool_class = mocker.patch(
            target="pyoneai.core.one.VirtualNetworkPool", autospec=True
        )
        self.mock_user_pool_class = mocker.patch(
            target="pyoneai.core.one.UserPool", autospec=True
        )
        self.mock_group_pool_class = mocker.patch(
            target="pyoneai.core.one.GroupPool", autospec=True
        )
        self.mock_datastore_pool_class = mocker.patch(
            target="pyoneai.core.one.DatastorePool", autospec=True
        )
        self.mock_image_pool_class = mocker.patch(
            target="pyoneai.core.one.ImagePool", autospec=True
        )
        self.mock_session = mocker.MagicMock(spec_set=Session)
        self.one = One(session=self.mock_session)

    def test_init_with_default_session(self, mocker: MockerFixture):
        mock_session_class = mocker.patch(
            target="pyoneai.core.one.Session",
            autospec=True,
            return_value=self.mock_session,
        )
        one = One()
        mock_session_class.assert_called_once_with()
        assert isinstance(one, One)
        assert self.one.session is self.mock_session

    def test_init_with_specified_session(self):
        self.mock_metric_base_init.assert_called_once_with(
            self.one, session=self.mock_session
        )
        assert isinstance(self.one, One)
        assert self.one.session is self.mock_session

    def test_clusters(self):
        pass
        # TODO: Uncomment the code below and delete the line above when
        # the class `ClusterPool` is implemented.
        # clusters = self.one.clusters
        # self.mock_cluster_pool_class.assert_called_once_with(
        #     session=self.mock_session
        # )
        # assert isinstance(clusters, ClusterPool)

    def test_hosts(self):
        hosts = self.one.hosts
        self.mock_host_pool_class.assert_called_once_with(owner=self.one)
        assert isinstance(hosts, HostPool)

    def test_vms(self):
        vms = self.one.vms
        self.mock_vm_pool_class.assert_called_once_with(owner=self.one)
        assert isinstance(vms, VirtualMachinePool)

    def test_vnets(self):
        vms = self.one.vnets
        self.mock_vnet_pool_class.assert_called_once_with(owner=self.one)
        assert isinstance(vms, VirtualNetworkPool)

    def test_users(self):
        users = self.one.users
        self.mock_user_pool_class.assert_called_once_with(owner=self.one)
        assert isinstance(users, UserPool)

    def test_groups(self):
        groups = self.one.groups
        self.mock_group_pool_class.assert_called_once_with(owner=self.one)
        assert isinstance(groups, GroupPool)

    def test_datastores(self):
        datastores = self.one.datastores
        self.mock_datastore_pool_class.assert_called_once_with(owner=self.one)
        assert isinstance(datastores, DatastorePool)

    def test_images(self):
        images = self.one.images
        self.mock_image_pool_class.assert_called_once_with(owner=self.one)
        assert isinstance(images, ImagePool)
