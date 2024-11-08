# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import numpy as np
import pandas as pd
import pytest
from pytest_mock import MockerFixture

from pyoneai.core import Metric, Pool, PoolMetric


class TestMetric:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self):
        self.data_x = {"x": np.arange(6, dtype=np.float32)}
        self.index_x = pd.date_range(
            "2024-07-05T12Z", "2024-07-05T22Z", freq="2h"
        )
        self.metric_x = Metric(time_index=self.index_x, data=self.data_x)
        self.data_y = {"y": np.full(6, 2, dtype=np.float32)}
        self.index_y = self.index_x
        self.metric_y = Metric(time_index=self.index_y, data=self.data_y)

        vals_1 = np.arange(6, dtype=np.float32).reshape(3, 2)
        self.metric_1 = Metric(
            time_index=pd.date_range("2024-07-12T14Z", periods=3, freq="2h"),
            data={"x_1": vals_1[:, 0], "y_1": vals_1[:, 1]},
        )
        vals_2 = np.array([[1, 1, np.nan], [np.nan, 10, 0]], dtype=np.float32)
        self.metric_2 = Metric(
            time_index=pd.date_range("2024-07-12T15Z", periods=2, freq="2h"),
            data={"x_2": vals_2[:, 0], "y_2": vals_2[:, 1]},
        )
        vals_3 = np.arange(8, dtype=np.float32).reshape(4, 2)
        self.metric_3 = Metric(
            time_index=pd.date_range("2024-07-12T16Z", periods=4, freq="2h"),
            data={"x_3": vals_3[:, 0], "y_3": vals_3[:, 1]},
        )
        self.metric_e = Metric(time_index=[], data={"x_e": []})

    def test_init(self):
        assert np.all(self.metric_x.time_index == self.index_x)
        assert self.metric_x.time_zone == str(self.index_x.tz)
        assert self.metric_x.frequency == pd.Timedelta(self.index_x.freq)
        assert np.allclose(
            self.metric_x.to_array().reshape(-1), self.data_x["x"]
        )

    def test_to_dataframe(self):
        df = self.metric_x.to_dataframe()
        assert np.all(self.metric_x.time_index == df.index)
        assert np.allclose(self.metric_x.to_array(), df.to_numpy())

    def test_to_series(self):
        ser = self.metric_x.to_series()[0]
        assert np.all(self.metric_x.time_index == ser.index)
        assert np.allclose(
            self.metric_x.to_array().reshape(-1), ser.to_numpy()
        )

    def test_multivariate(self):
        metric = Metric.multivariate([self.metric_x, self.metric_y])
        assert np.all(metric.time_index == self.index_x)
        assert np.allclose(
            metric["x"].to_array().reshape(-1), self.data_x["x"]
        )
        assert np.allclose(
            metric["y"].to_array().reshape(-1), self.data_y["y"]
        )

    def test_comparison_univariate(self):
        metric_x = self.metric_2["x_2"]
        metric_y = self.metric_2["y_2"]

        assert np.all((metric_x == metric_y) == np.array([[True], [False]]))
        assert np.all((metric_x != metric_y) == np.array([[False], [True]]))
        assert np.all((metric_x < metric_y) == np.array([[False], [False]]))
        assert np.all((metric_x > metric_y) == np.array([[False], [False]]))

    def test_comparison_multivariate(self):
        assert not np.any(self.metric_1 == self.metric_2)
        assert np.all(self.metric_1 != self.metric_2)
        assert not np.any(self.metric_1 <= self.metric_2)
        assert not np.any(self.metric_1 >= self.metric_2)

    def test_comparison_empty(self):
        assert len(self.metric_1["x_1"] == self.metric_e) == 3
        assert not np.any(self.metric_1["x_1"] == self.metric_e)
        assert np.all(self.metric_1["x_1"] != self.metric_e)
        assert not np.any(self.metric_1["x_1"] <= self.metric_e)
        assert not np.any(self.metric_1["x_1"] >= self.metric_e)

    def test_arithmetics(self):
        result = np.array(self.metric_1 + self.metric_3)
        correct = np.full((5, 2), np.nan)
        correct[1:3, :] = [[2, 4], [6, 8]]
        assert np.allclose(result, correct, equal_nan=True)
        assert np.allclose(result + 2, correct + 2, equal_nan=True)
        assert np.allclose(2 + result, 2 + correct, equal_nan=True)
        assert np.allclose(result - 2, correct - 2, equal_nan=True)
        assert np.allclose(2 - result, 2 - correct, equal_nan=True)
        assert np.allclose(result * 2, correct * 2, equal_nan=True)
        assert np.allclose(2 * result, 2 * correct, equal_nan=True)

        result = np.array(self.metric_1 - self.metric_3)
        correct = np.full((5, 2), np.nan)
        correct[1:3, :] = 2
        assert np.allclose(result, correct, equal_nan=True)

    def test_arithmetics_empty(self):
        sum_ = self.metric_1["x_1"] + self.metric_e
        assert len(sum_) == 3
        assert np.count_nonzero(np.isnan(sum_)) == 3

    def test_rename(self):
        new_metric = self.metric_1.rename(names={"x_1": "x_2", "y_1": "y_2"})
        assert new_metric.names.to_list() == ["x_2", "y_2"]
        assert np.all(self.metric_1.time_index == new_metric.time_index)
        assert np.allclose(self.metric_1.to_array(), new_metric.to_array())


class TestPoolMetric:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        vals_1 = np.arange(6, dtype=np.float32).reshape(3, 2)
        self.metric_1 = Metric(
            time_index=pd.date_range("2024-07-12T14Z", periods=3, freq="2h"),
            data={"x_1": vals_1[:, 0], "y_1": vals_1[:, 1]},
        )
        vals_2 = np.array([[1, 1, np.nan], [np.nan, 10, 0]], dtype=np.float32)
        self.metric_2 = Metric(
            time_index=pd.date_range("2024-07-12T15Z", periods=2, freq="2h"),
            data={"x_2": vals_2[:, 0], "y_2": vals_2[:, 1]},
        )
        vals_3 = np.arange(8, dtype=np.float32).reshape(4, 2)
        self.metric_3 = Metric(
            time_index=pd.date_range("2024-07-12T16Z", periods=4, freq="2h"),
            data={"x_3": vals_3[:, 0], "y_3": vals_3[:, 1]},
        )
        self.metric_e = Metric(time_index=[], data={"x_e": []})

        self.metrics = [self.metric_1, self.metric_2, self.metric_3]
        self.pool_metric = self._create_pool_metric(self.metrics, mocker)

    @staticmethod
    def _create_pool_metric(
        metrics: int | list[Metric], mocker: MockerFixture
    ) -> PoolMetric:
        if isinstance(metrics, int):
            size = metrics
            metrics = [mocker.MagicMock(spec_set=Metric) for _ in range(size)]
        else:
            size = len(metrics)

        def create_mock_pool(ids: int | list[int]) -> mocker.MagicMock:
            if isinstance(ids, int):
                ids = [ids]
            mock_pool = mocker.MagicMock(spec_set=Pool, ids=ids)
            mock_pool.__iter__.side_effect = lambda: iter(
                mocker.MagicMock(id=id_) for id_ in ids
            )
            mock_pool.__getitem__.side_effect = lambda key: create_mock_pool(
                ids=key
            )
            return mock_pool

        ids = list(range(size))
        pool_metric = PoolMetric(pool=create_mock_pool(ids), metrics=metrics)

        return pool_metric

    def test_init(self):
        assert isinstance(self.pool_metric, PoolMetric)
        assert isinstance(self.pool_metric._pool, Pool)
        assert isinstance(self.pool_metric._metrics, dict)
        for i, (id_, metric) in enumerate(self.pool_metric._metrics.items()):
            assert i == id_
            assert self.metrics[i] is metric
        assert len(self.pool_metric) == len(self.metrics)

    def test_comparison(self, mocker):
        mock_metrics = self.metrics + [self.metric_e]
        pool_metric = self._create_pool_metric(mock_metrics, mocker)

        cmp = pool_metric == self.metric_1
        assert isinstance(cmp, pd.Series)
        assert cmp.dtype is np.dtype(bool)
        assert cmp.index.dtype.kind == "i"
        assert np.all(cmp.index == np.arange(4))
        assert np.all(cmp == pd.Series(data=[True, False, False, False]))
        assert set(cmp[cmp].index) == {0}

        cmp = pool_metric != self.metric_1
        assert cmp.dtype is np.dtype(bool)
        assert cmp.index.dtype.kind == "i"
        assert np.all(cmp.index == np.arange(4))
        assert np.all(cmp == pd.Series(data=[False, False, False, False]))
        assert set(cmp[cmp].index) == set()

        cmp = pool_metric <= self.metric_1
        assert cmp.dtype is np.dtype(bool)
        assert cmp.index.dtype.kind == "i"
        assert np.all(cmp.index == np.arange(4))
        assert np.all(cmp == pd.Series(data=[True, False, False, False]))
        assert set(cmp[cmp].index) == {0}

        cmp = pool_metric >= self.metric_1
        assert cmp.dtype is np.dtype(bool)
        assert cmp.index.dtype.kind == "i"
        assert np.all(cmp.index == np.arange(4))
        assert np.all(cmp == pd.Series(data=[True, False, False, False]))
        assert set(cmp[cmp].index) == {0}

    def test_comparison_empty(self, mocker):
        mock_metrics = [self.metric_1, self.metric_e]
        pool_metric = self._create_pool_metric(mock_metrics, mocker)
        cmp = pool_metric == self.metric_e
        assert cmp.dtype is np.dtype(bool)
        assert cmp.index.dtype.kind == "i"
        assert np.all(cmp.index == np.arange(2))
        assert np.all(cmp == pd.Series(data=[False, False]))
        assert set(cmp[cmp].index) == set()

    def test_getitem_with_correct_name(self, mocker):
        metrics = [self.metric_1, self.metric_1]
        original_pool_metric = self._create_pool_metric(metrics, mocker)
        pool_metric = original_pool_metric["x_1"]
        assert isinstance(pool_metric, PoolMetric)
        assert original_pool_metric.ids == pool_metric.ids
        assert isinstance(pool_metric._metrics, dict)
        for id_, metric in pool_metric._metrics.items():
            original = original_pool_metric._metrics[id_]
            assert id_ in original_pool_metric._metrics
            assert metric.names.to_list() == ["x_1"]
            assert np.all(metric.time_index == original.time_index)
            assert metric == original["x_1"]

    def test_getitem_with_incorrect_name(self):
        with pytest.raises(KeyError):
            _ = self.pool_metric["x_1"]

    def test_getitem_with_correct_names(self, mocker):
        metrics = [self.metric_1, self.metric_1]
        original_pool_metric = self._create_pool_metric(metrics, mocker)
        pool_metric = original_pool_metric[["x_1", "y_1"]]
        assert isinstance(pool_metric, PoolMetric)
        assert original_pool_metric.ids == pool_metric.ids
        assert isinstance(pool_metric._metrics, dict)
        for id_, metric in pool_metric._metrics.items():
            original = original_pool_metric._metrics[id_]
            assert id_ in original_pool_metric._metrics
            assert metric.names.to_list() == ["x_1", "y_1"]
            assert np.all(metric.time_index == original.time_index)
            assert metric["x_1"] == original["x_1"]
            assert metric["y_1"] == original["y_1"]

    def test_getitem_with_incorrect_names(self):
        with pytest.raises(KeyError):
            _ = self.pool_metric[["x_1", "y_2"]]

    def test_getitem_with_correct_id(self):
        metric = self.pool_metric[1]
        assert isinstance(metric, Metric)
        assert metric is self.metrics[1]

    def test_getitem_with_incorrect_id(self):
        with pytest.raises(KeyError):
            _ = self.pool_metric[10]

    _correct_ids = [
        [1, 2],
        np.array([1, 2]),
        pd.Series(data=[False, True, True], index=[0, 1, 2]),
    ]

    @pytest.mark.parametrize("key", _correct_ids)
    def test_getitem_with_correct_ids(self, key):
        pool_metric = self.pool_metric[key]
        assert isinstance(pool_metric, PoolMetric)
        assert len(pool_metric._pool.ids) == 2
        assert set(pool_metric._pool.ids) == {1, 2}
        assert isinstance(pool_metric._metrics, dict)
        assert set(pool_metric._metrics) == {1, 2}
        assert pool_metric._metrics[1] is self.metrics[1]
        assert pool_metric._metrics[2] is self.metrics[2]

    _incorrect_ids = [
        [1, 10],
        np.array([1, 10]),
        pd.Series(data=[False, True, True], index=[0, 1, 10]),
    ]

    @pytest.mark.parametrize("key", _incorrect_ids)
    def test_getitem_with_incorrect_ids(self, key):
        with pytest.raises(KeyError):
            _ = self.pool_metric[key]

    def test_getitem_with_tuple(self, mocker):
        metrics = [self.metric_1, self.metric_1, self.metric_1]
        original_pool_metric = self._create_pool_metric(metrics, mocker)
        pool_metric = original_pool_metric[[1, 2], ["x_1"]]
        assert isinstance(pool_metric, PoolMetric)
        assert len(pool_metric._pool.ids) == 2
        assert set(pool_metric._pool.ids) == {1, 2}
        assert isinstance(pool_metric._metrics, dict)
        assert set(pool_metric._metrics) == {1, 2}
        for id_, metric in pool_metric._metrics.items():
            original = original_pool_metric._metrics[id_]
            assert id_ in self.pool_metric._metrics
            assert metric.names.to_list() == ["x_1"]
            assert np.all(metric.time_index == original.time_index)
            assert metric == original["x_1"]
