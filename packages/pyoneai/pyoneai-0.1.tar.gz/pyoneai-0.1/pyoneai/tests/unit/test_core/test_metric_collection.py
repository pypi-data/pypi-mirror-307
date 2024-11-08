# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import pytest

from pyoneai.core import MetricCollection, PoolMetricCollection


class TestMetricCollection:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        self.mock_entity = mocker.MagicMock()
        self.mock_entity.registry = {
            "test_metric": None,
            "x": None,
            "y": None,
        }
        self.mock_metric_accessor = mocker.patch(
            "pyoneai.core.metric_collection.MetricAccessor", autospec=True
        )
        self.mock_derived_metric_accessor = mocker.patch(
            "pyoneai.core.metric_collection.DerivedMetricAccessor",
            autospec=True,
        )
        self.mock_metric_accessors = mocker.patch(
            "pyoneai.core.metric_collection.MetricAccessors", autospec=True
        )
        self.metric_collection = MetricCollection(entity=self.mock_entity)

    def test_init(self):
        assert self.metric_collection._entity is self.mock_entity
        # pylint: disable=use-implicit-booleaness-not-comparison
        assert self.metric_collection._data == {}

    def test_getitem_with_simple_key(self):
        metric = self.metric_collection["test_metric"]
        self.mock_metric_accessor.assert_called_once_with(
            self.mock_entity, "test_metric"
        )
        self.mock_derived_metric_accessor.assert_not_called()
        self.mock_metric_accessors.assert_not_called()
        assert len(self.metric_collection._data) == 1
        assert set(self.metric_collection._data) == {"test_metric"}
        assert self.metric_collection._data["test_metric"] is metric

    def test_getitem_with_composite_key(self):
        metric = self.metric_collection["test_metric(x, y)"]
        self.mock_metric_accessor.assert_not_called()
        self.mock_derived_metric_accessor.assert_called_once_with(
            self.mock_entity, "test_metric", ["x", "y"]
        )
        self.mock_metric_accessors.assert_not_called()
        assert len(self.metric_collection._data) == 1
        assert set(self.metric_collection._data) == {"test_metric(x, y)"}
        assert self.metric_collection._data["test_metric(x, y)"] is metric

    def test_getitem_with_sequence_key(self):
        # pylint: disable=pointless-statement
        self.metric_collection["test_metric", "x", "y"]
        self.mock_metric_accessor.assert_not_called()
        self.mock_derived_metric_accessor.assert_not_called()
        self.mock_metric_accessors.assert_called_once_with(
            self.mock_entity, ("test_metric", "x", "y")
        )

    def test_getitem_with_wrong_key(self):
        with pytest.raises(KeyError):
            # pylint: disable=pointless-statement
            self.metric_collection["wrong_name"]


class TestPoolMetricCollection:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        self.mock_pool = mocker.MagicMock()
        self.mock_accessor = mocker.MagicMock()
        self.mock_pool_metric_accessor = mocker.patch(
            "pyoneai.core.metric_collection.PoolMetricAccessor",
            autospec=True,
            return_value=self.mock_accessor,
        )
        self.pool_metric_collection = PoolMetricCollection(pool=self.mock_pool)

    def test_init(self):
        assert self.pool_metric_collection._pool is self.mock_pool

    def test_getitem(self):
        metric = self.pool_metric_collection["test_metric"]
        self.mock_pool_metric_accessor.assert_called_once_with(
            self.mock_pool, "test_metric"
        )
        assert metric is self.mock_accessor
