# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import numpy as np
import pandas as pd
import pytest
from pytest_mock import MockerFixture

from pyoneai.core import (
    BaseMetricAccessor,
    MetricAccessor,
    MetricAccessors,
    Pool,
    PoolMetric,
    PoolMetricAccessor,
    PredictorMetricAccessor,
    PrometheusMetricAccessor,
    TimeIndex,
    metric_accessors,
)
from pyoneai.core.metric_collection import MetricCollection


class TestBaseMetricAccessor:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        self.mock_entity = mocker.MagicMock()
        mocker.patch.object(
            BaseMetricAccessor, "__abstractmethods__", frozenset()
        )
        self.mock_timeseries = mocker.MagicMock()
        self.mock_get_timeseries = mocker.patch.object(
            BaseMetricAccessor,
            "get_timeseries",
            autospec=True,
            return_value=self.mock_timeseries,
        )
        # pylint: disable=abstract-class-instantiated
        self.accessor = BaseMetricAccessor(
            entity=self.mock_entity, metric_name="test_metric"
        )  # type: ignore

    def test_init(self):
        assert self.accessor._entity is self.mock_entity
        assert self.accessor._metric_name == "test_metric"

    def test_getitem_with_time_index_key(self):
        time_idx = TimeIndex(slice("2024-07-04T12Z", "2024-07-04T14Z", "15s"))
        result = self.accessor[time_idx]
        # NOTE: In this case, `self.mock_get_timeseries` acts as a class method
        # because of the ways it is patched.
        self.mock_get_timeseries.assert_called_once_with(
            self.accessor, time_idx
        )
        assert result is self.mock_timeseries

    def test_getitem_with_slice_key(self):
        time_idx = slice("2024-07-04T12Z", "2024-07-04T14Z", "15s")
        result = self.accessor[time_idx]
        self.mock_get_timeseries.assert_called_once()
        assert result is self.mock_timeseries


class TestPredictionMetricAccessor:
    # pylint: disable=attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        self.mock_entity = mocker.MagicMock()
        self.accessor = PredictorMetricAccessor(
            entity=self.mock_entity, metric_name="test_metric"
        )

    def test_get_timeseries(self, mocker: MockerFixture):
        time_idx = TimeIndex(slice("2024-07-04T12Z", "2024-07-04T14Z", "15s"))
        mock_predictor = mocker.patch(
            "pyoneai.core.metric_accessors.Predictor", autospec=True
        )
        self.accessor.get_timeseries(time_idx)
        mock_predictor.assert_called_once_with(
            entity=self.mock_entity,
            metric_name="test_metric",
            time_index=time_idx,
        )


class TestPrometheusMetricAccessor:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        self.mock_entity = mocker.MagicMock()
        self.mock_entity.registry = {
            "test_metric": {"accessor": {"kwargs": {"query": "test_query"}}}
        }
        mock_prometheus = mocker.MagicMock()
        mock_prometheus.custom_query_range.return_value = [
            {
                "metric": {},
                "values": [
                    [1720105725, "4"],
                    [1720105740, "18"],
                    [1720105755, "32"],
                    [1720105770, "46"],
                    [1720105785, "61"],
                    [1720105800, "75"],
                ],
            }
        ]
        mocker.patch.object(
            PrometheusMetricAccessor,
            "client",
            spec=True,
            new_callable=mocker.PropertyMock,
            return_value=mock_prometheus,
        )
        self.time_index = pd.date_range(
            "2024-07-04T15:08:45Z", "2024-07-04T15:10:00Z", freq="15s"
        )
        self.values = np.array([4, 18, 32, 46, 61, 75], dtype=np.float64)
        self.accessor = PrometheusMetricAccessor(
            entity=self.mock_entity, metric_name="test_metric"
        )

    def test_init(self):
        assert self.accessor._entity is self.mock_entity
        assert self.accessor._metric_name == "test_metric"
        assert self.accessor._query == "test_query"

    def test_get_timeseries(self):
        time_idx = TimeIndex(self.time_index)
        metric = self.accessor.get_timeseries(time_idx)
        assert metric.time_index.freq == self.time_index.freq
        assert np.all(metric.time_index == self.time_index)
        assert np.allclose(metric.to_array().reshape(-1), self.values)

    def test_prepare_period_query_without_period(self):
        self.accessor._query = "opennebula_vm_state{one_vm_id='1'}"
        period = pd.Timedelta("60s")
        result = self.accessor._prepare_period_query(period)
        assert result == self.accessor._query

    def test_prepare_period_query_with_period(self):
        self.accessor._query = (
            "sum by (one_vm_id) "
            "(rate(opennebula_libvirt_cpu_seconds_total{one_vm_id='1'}"
            "[$PERIOD]))"
        )
        period = pd.Timedelta("60s")
        result = self.accessor._prepare_period_query(period)
        result_ = (
            "sum by (one_vm_id) "
            "(rate(opennebula_libvirt_cpu_seconds_total{one_vm_id='1'}[60s]))"
        )
        assert result == result_

    def test_prepare_time_index_query_without_period(self):
        self.accessor._query = "opennebula_vm_state{one_vm_id='1'}"
        time_idx = TimeIndex(slice("-300s", "0", "60s"))
        result = self.accessor._prepare_time_index_query(time_idx)
        assert result == self.accessor._query

    def test_prepare_time_index_query_with_period(self):
        self.accessor._query = (
            "sum by (one_vm_id) "
            "(rate(opennebula_libvirt_cpu_seconds_total{one_vm_id='1'}"
            "[$PERIOD]))"
        )
        time_idx = TimeIndex(slice("-300s", "-120s", "60s"))
        result = self.accessor._prepare_time_index_query(time_idx)
        result_ = (
            "sum by (one_vm_id) "
            "(rate(opennebula_libvirt_cpu_seconds_total{one_vm_id='1'}[180s]))"
        )
        assert result == result_


class TestMetricAccessor:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        self.mock_entity = mocker.MagicMock()
        self.mock_entity.registry = {
            "test_metric": {
                "accessor": {
                    "class": "pyoneai.core.PrometheusMetricAccessor",
                    "kwargs": {"query": "test_query"},
                }
            }
        }
        self.mock_prometheus_get_timeseries = mocker.patch.object(
            PrometheusMetricAccessor, "get_timeseries", autospec=True
        )
        self.mock_predictor_get_timeseries = mocker.patch.object(
            PredictorMetricAccessor, "get_timeseries", autospec=True
        )
        self.accessor = MetricAccessor(self.mock_entity, "test_metric")

    def test_init(self):
        # pylint: disable=pointless-statement
        assert self.accessor._entity is self.mock_entity
        assert self.accessor._metric_name == "test_metric"
        assert isinstance(self.accessor._hist, PrometheusMetricAccessor)
        assert self.accessor._hist._entity is self.mock_entity
        assert self.accessor._hist._metric_name == "test_metric"
        assert isinstance(self.accessor._pred, PredictorMetricAccessor)
        assert self.accessor._pred._entity is self.mock_entity
        assert self.accessor._pred._metric_name == "test_metric"

    def test_get_history(self):
        accessor = self.accessor._get_history("test_metric")
        assert isinstance(accessor, PrometheusMetricAccessor)
        assert accessor._entity is self.mock_entity
        assert accessor._metric_name == "test_metric"

    def test_get_timeseries_history(self):
        time_idx = TimeIndex(slice("-2m", "-1m", "15s"))
        self.accessor.get_timeseries(time_idx)
        self.mock_prometheus_get_timeseries.assert_called_once_with(
            self.accessor._hist, time_idx
        )
        self.mock_predictor_get_timeseries.assert_not_called()

    def test_get_timeseries_prediction(self):
        time_idx = TimeIndex(slice("1m", "2m", "15s"))
        self.accessor.get_timeseries(time_idx)
        self.mock_prometheus_get_timeseries.assert_not_called()
        self.mock_predictor_get_timeseries.assert_called_once_with(
            self.accessor._pred, time_idx
        )

    def test_get_timeseries_both(self):
        time_idx = TimeIndex(slice("-2m", "2m", "15s"))
        self.accessor.get_timeseries(time_idx)
        self.mock_prometheus_get_timeseries.assert_called_once()
        self.mock_predictor_get_timeseries.assert_called_once()


class TestDerivedMetricAccessor:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        self.mock_entity = mocker.MagicMock()
        self.mock_entity.registry = {
            "test_metric": None,
            "x": None,
            "y": None,
        }
        self.mock_entity.metrics = MetricCollection(self.mock_entity)
        self.accessor = metric_accessors.DerivedMetricAccessor(
            entity=self.mock_entity,
            metric_name="test_metric",
            covariate_names=["x", "y"],
        )

    def test_init(self):
        # pylint: disable=pointless-statement
        assert self.accessor._entity is self.mock_entity
        assert self.accessor._entity.metrics._entity is self.mock_entity
        assert self.accessor._entity.metrics._data == {}
        assert self.accessor._metric_name == "test_metric"
        assert self.accessor._covariates == ["x", "y"]
        assert self.accessor._model is None


class TestMetricAccessors:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        metrics = {name: mocker.MagicMock() for name in ["x", "y", "z"]}
        self.mock_entity = mocker.MagicMock()
        self.mock_metrics = mocker.MagicMock()
        self.mock_metrics.__getitem__.side_effect = lambda name: metrics[name]

    def test_init(self):
        accessors = MetricAccessors(self.mock_entity, ("x", "y", "z"))
        assert accessors._entity is self.mock_entity
        assert isinstance(accessors._metric_name, list)
        assert accessors._metric_name == ["x", "y", "z"]
        assert isinstance(accessors._accessors, list)


class TestPoolMetricAccessor:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        self.mock_metrics = [mocker.MagicMock() for _ in range(5)]

        self.mock_accessors = []
        for i in range(5):
            mock_accessor = mocker.MagicMock()
            mock_accessor.__getitem__.return_value = self.mock_metrics[i]
            self.mock_accessors.append(mock_accessor)

        self.mock_entities = []
        for i in range(5):
            entity = mocker.MagicMock()
            entity.id = i
            entity.metrics.__getitem__.return_value = self.mock_accessors[i]
            self.mock_entities.append(entity)

        self.mock_pool = mocker.MagicMock(spec_set=Pool)
        self.mock_pool.__iter__.side_effect = lambda: iter(self.mock_entities)
        self.accessor = PoolMetricAccessor(
            pool=self.mock_pool, metric_name="test_metric"
        )

    def test_init(self):
        assert isinstance(self.accessor, PoolMetricAccessor)
        assert self.accessor._pool is self.mock_pool
        assert self.accessor._metric_name == "test_metric"

    def test_get_timeseries(self):
        time_idx = TimeIndex(slice("-2m", "2m", "15s"))
        time_series = self.accessor.get_timeseries(time_idx)
        assert isinstance(time_series, PoolMetric)
        assert isinstance(time_series._pool, Pool)
        assert time_series._pool is self.accessor._pool
        assert isinstance(time_series._metrics, dict)
        assert len(time_series) == 5
        for i, (entity, metric) in enumerate(time_series):
            self.mock_entities[i].metrics.__getitem__.assert_called_once_with(
                "test_metric"
            )
            self.mock_accessors[i].__getitem__.assert_called_once_with(
                time_idx
            )
            assert entity.id == i
            assert entity is self.mock_entities[i]
            assert metric is self.mock_metrics[i]
