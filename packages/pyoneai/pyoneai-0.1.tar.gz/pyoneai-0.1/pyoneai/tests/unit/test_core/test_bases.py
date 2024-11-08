# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import numpy as np
import pandas as pd
import pytest
from pytest_mock import MockerFixture

from pyoneai import Session
from pyoneai.core import MetricCollection, One, PoolMetricCollection
from pyoneai.core.bases import (
    Entity,
    LatestMetricValue,
    MetricBase,
    Pool,
    SessionBase,
)


class TestSessionBase:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        # pylint: disable=abstract-class-instantiated
        mocker.patch.object(
            target=SessionBase,
            attribute="__abstractmethods__",
            new=frozenset(),
        )
        self.mock_session = mocker.MagicMock(spec_set=Session)
        self.session_base = SessionBase(
            # type: ignore[abstract]
            session=self.mock_session
        )

    def test_init(self):
        assert isinstance(self.session_base, SessionBase)
        assert hasattr(self.session_base, "session")
        assert self.session_base.session is self.mock_session


class TestMetricBase:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        # pylint: disable=abstract-class-instantiated
        mocker.patch.object(
            target=MetricBase, attribute="__abstractmethods__", new=frozenset()
        )
        self.mock_session_base_init = mocker.patch(
            target="pyoneai.core.bases.SessionBase.__init__",
            autospec=True,
            side_effect=lambda self, session: setattr(
                self, "session", session
            ),
        )
        self.mock_metric_collection_class = mocker.patch(
            target="pyoneai.core.bases.MetricCollection", autospec=True
        )
        self.mock_session = mocker.MagicMock(spec=Session)
        self.mock_session.config = mocker.MagicMock()
        self.mock_session.config.registry = mocker.MagicMock()
        self.metric_base = MetricBase(
            # type: ignore[abstract]
            session=self.mock_session
        )

    def test_init(self):
        assert isinstance(self.metric_base, MetricBase)
        self.mock_session_base_init.assert_called_once_with(
            self.metric_base, self.mock_session
        )
        assert hasattr(self.metric_base, "session")
        assert self.metric_base.session is self.mock_session
        self.mock_metric_collection_class.assert_called_once_with(
            self.metric_base
        )
        assert hasattr(self.metric_base, "metrics")
        assert isinstance(self.metric_base.metrics, MetricCollection)
        self.mock_session.config.registry.__getitem__.assert_called_with(
            "default"
        )
        assert hasattr(self.metric_base, "registry")
        assert hasattr(self.metric_base, "registry_default")
        assert self.metric_base.session is self.mock_session


class TestEntity:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        # pylint: disable=abstract-class-instantiated
        mocker.patch.object(
            target=Entity, attribute="__abstractmethods__", new=frozenset()
        )
        self.mock_metric_base_init = mocker.patch(
            target="pyoneai.core.bases.MetricBase.__init__",
            autospec=True,
            side_effect=lambda self, session: setattr(
                self, "session", session
            ),
        )
        self.mock_session = mocker.MagicMock(spec_set=Session)
        self.entity = Entity(
            # type: ignore[abstract]
            session=self.mock_session,
            id=5,
        )

    def test_init(self):
        assert isinstance(self.entity, Entity)
        self.mock_metric_base_init.assert_called_once_with(
            self.entity, self.mock_session
        )
        assert hasattr(self.entity, "id")
        assert self.entity.id == 5


class TestLatestMetricValue:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        mock_metric = mocker.MagicMock(to_array=lambda copy: np.array([10.0]))
        mock_metric_accessor = mocker.MagicMock()
        mock_metric_accessor.__getitem__.return_value = mock_metric
        mock_metric_collection = mocker.MagicMock()
        mock_metric_collection.__getitem__.return_value = mock_metric_accessor

        class MockEntity:
            metrics = mock_metric_collection
            cpu_usage = LatestMetricValue(float)

        self.mock_entity_class = MockEntity

    def test_init(self):
        value = LatestMetricValue(float)
        assert isinstance(value, LatestMetricValue)
        assert value._type is float

    def test_get(self):
        mock_entity = self.mock_entity_class()
        assert mock_entity.cpu_usage == 10.0


class TestPool:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        # pylint: disable=abstract-class-instantiated
        self.mock_pool_get_system_ids = mocker.patch.object(
            target=Pool,
            attribute="_get_system_ids",
            autospec=True,
            return_value={0, 1, 2},
        )
        self.mock_pool_get_entity = mocker.patch.object(
            target=Pool,
            attribute="_get_entity",
            autospec=True,
            side_effect=lambda self, id: mocker.MagicMock(id=id),
        )
        self.mock_pool_metric_collection_class = mocker.patch(
            target="pyoneai.core.bases.PoolMetricCollection", autospec=True
        )
        self.mock_session = mocker.MagicMock(spec=Session)
        self.mock_owner = mocker.MagicMock(spec=One)
        self.mock_owner.session = self.mock_session
        self.pool = Pool(
            # type: ignore[abstract, var-annotated]
            owner=self.mock_owner,
            ids={1, 2, 3, 4, 5},
        )

    def test_init_with_ids_inside_set(self):
        assert isinstance(self.pool, Pool)
        assert hasattr(self.pool, "session")
        assert self.pool.session is self.mock_session
        self.mock_pool_metric_collection_class.assert_called_once_with(
            self.pool
        )
        assert hasattr(self.pool, "metrics")
        assert isinstance(self.pool.metrics, PoolMetricCollection)
        assert hasattr(self.pool, "_ids")
        assert isinstance(self.pool._ids, set)
        assert self.pool._ids == {1, 2, 3, 4, 5}
        assert hasattr(self.pool, "owner")
        assert self.pool.owner is self.mock_owner

    def test_init_with_ids_inside_list(self):
        # pylint: disable=abstract-class-instantiated
        pool = Pool(
            # type: ignore[abstract, var-annotated]
            owner=self.mock_owner,
            ids=[1, 2, 3, 4, 5],
        )
        assert isinstance(pool._ids, set)
        assert pool._ids == {1, 2, 3, 4, 5}

    def test_init_without_ids(self):
        # pylint: disable=abstract-class-instantiated
        pool = Pool(
            # type: ignore[abstract, var-annotated]
            owner=self.mock_owner
        )
        assert pool._ids is None

    def test_ids_for_defined_pool(self):
        ids = self.pool.ids
        assert isinstance(ids, set)
        assert ids == self.pool._ids

    def test_ids_for_undefined_pool(self):
        # pylint: disable=abstract-class-instantiated
        pool = Pool(
            # type: ignore[abstract, var-annotated]
            owner=self.mock_owner
        )
        ids = pool.ids
        self.mock_pool_get_system_ids.assert_called_once_with(pool)
        assert isinstance(ids, set)
        assert ids == {0, 1, 2}
        assert ids is pool._get_system_ids()

    def test_len(self):
        assert len(self.pool) == len(self.pool.ids)

    def test_iter(self):
        assert len(list(self.pool)) == len(self.pool)

        entities = iter(self.pool)
        ids = iter(self.pool._ids)
        while True:
            try:
                entity = next(entities)
                id_ = next(ids)
                self.mock_pool_get_entity.assert_called_with(self.pool, id_)
                assert entity.id == id_
            except StopIteration:
                break

        for entity in self.pool:
            self.mock_pool_get_entity.assert_called_with(self.pool, entity.id)

    def test_contains_for_determined_pool(self):
        assert 5 in self.pool
        assert 50 not in self.pool

    def test_contains_for_undetermined_pool(self):
        # pylint: disable=abstract-class-instantiated
        pool = Pool(
            # type: ignore[abstract, var-annotated]
            owner=self.mock_owner
        )
        assert 1 in pool
        assert 10 not in pool

    @pytest.mark.parametrize("id", [5, 5.0, np.array([5])[0]])
    def test_getitem_with_existent_id(self, id):
        entity = self.pool[id]
        self.mock_pool_get_entity.assert_called_with(self.pool, id)
        assert entity.id == 5

    @pytest.mark.parametrize("id", [50, 50.0, np.array([50])[0]])
    def test_getitem_with_nonexistent_id(self, id):
        message = f"'key' {int(id)} not in the pool"
        with pytest.raises(KeyError, match=message):
            _ = self.pool[id]

    @pytest.mark.parametrize("ids", [{4, 5}, [4.0, 5.0], np.array([4, 5])])
    def test_getitem_with_existent_id_collection(self, ids):
        pool = self.pool[ids]
        assert pool.session is self.mock_session
        assert isinstance(pool._ids, set)
        assert pool._ids == {4, 5}

    @pytest.mark.parametrize("ids", [{0, 1}, [0.0, 1.0], np.array([0, 1])])
    def test_getitem_with_nonexistent_id_collection(self, ids):
        message = r"'key' contains ids that are not in the pool: \[0\]"
        with pytest.raises(KeyError, match=message):
            _ = self.pool[ids]

    def test_getitem_with_id_mask(self):
        mask = pd.Series(
            data=np.array([False, True, False, True, True], dtype=bool),
            index=np.arange(1, 6, dtype=np.int32),
        )
        pool = self.pool[mask]
        assert pool.session is self.mock_session
        assert isinstance(pool._ids, set)
        assert pool._ids == {2, 4, 5}

    @pytest.mark.parametrize("ids", ["5", ["4", "5"], None])
    def test_getitem_with_wrong_id_type(self, ids):
        message = "'key' must be int-like, collection, or series mask"
        with pytest.raises(TypeError, match=message):
            _ = self.pool[ids]

    def test_get_with_existent_id(self):
        entity = self.pool.get(5, default=50)
        self.mock_pool_get_entity.assert_called_with(self.pool, 5)
        assert entity.id == 5

    def test_get_with_nonexistent_id(self):
        entity = self.pool.get(10, default=20)
        self.mock_pool_get_entity.assert_not_called()
        assert entity == 20

    def test_owner(self, mocker: MockerFixture):
        self.mock_owner_ = mocker.MagicMock(spec=Entity)
        self.mock_owner_.session = self.mock_session
        self.mock_owner_.id = 0
        self.pool_ = Pool(
            # type: ignore[abstract, var-annotated]
            owner=self.mock_owner_,
            ids={1, 2, 3, 4, 5},
        )
        assert isinstance(self.pool.owner, One)
        assert self.pool.owner is self.mock_owner
        assert self.pool.owner_id is None
        assert isinstance(self.pool_.owner, Entity)
        assert self.pool_.owner is self.mock_owner_
        assert self.pool_.owner_id is 0
