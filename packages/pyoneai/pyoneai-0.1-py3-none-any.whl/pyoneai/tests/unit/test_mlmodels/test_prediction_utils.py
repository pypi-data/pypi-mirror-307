import numpy as np
import pandas as pd
import pytest
from torch import Value


class TestPredictionUtils:

    @pytest.mark.parametrize(
        "time_index, n, expected",
        [
            (
                pd.date_range("2024-07-12", periods=3, freq="2d", tz="UTC"),
                3,
                [
                    pd.Timestamp("2024-07-18", tz="UTC"),
                    pd.Timestamp("2024-07-20", tz="UTC"),
                    pd.Timestamp("2024-07-22", tz="UTC"),
                ],
            ),
        ],
    )
    def test_compute_several_prediction_time_indices(
        self, time_index, n, expected
    ):
        from pyoneai.core import Metric
        from pyoneai.mlmodels.utils.prediction_utils import (
            compute_prediction_time_index,
        )

        DUMMY_DATA = {"dummy_data": np.random.random((len(time_index),))}
        metric = Metric(time_index, DUMMY_DATA)

        prediction_index = compute_prediction_time_index(metric, n)
        assert prediction_index.to_list() == expected

    def test_metric_to_batch_returns_tensor(self):
        import torch

        from pyoneai.core import Metric
        from pyoneai.mlmodels.utils.prediction_utils import metric_to_batch

        DUMMY_DATA = {"dummy_data": np.random.random((6,))}
        batch = metric_to_batch(
            Metric(
                time_index=pd.date_range(
                    "2024-07-12T14Z", periods=6, freq="2h"
                ),
                data=DUMMY_DATA,
            )
        )
        assert isinstance(batch, torch.Tensor)

    @pytest.mark.parametrize("n", [1, 2, 10, 100])
    def test_univariate_metric_to_batch(self, n):
        import torch

        from pyoneai.core import Metric
        from pyoneai.mlmodels.utils.prediction_utils import metric_to_batch

        DUMMY_DATA = {"dummy_data": np.random.random((n,))}
        batch = metric_to_batch(
            Metric(
                time_index=pd.date_range(
                    "2024-07-12T14Z", periods=n, freq="2h"
                ),
                data=DUMMY_DATA,
            )
        )
        assert batch.shape == torch.Size([1, n, 1])

    @pytest.mark.parametrize("n", [1, 2, 10, 100])
    def test_multivariate_metric_to_batch(self, n):
        import torch

        from pyoneai.core import Metric
        from pyoneai.mlmodels.utils.prediction_utils import metric_to_batch

        DUMMY_DATA = {
            "dummy_data": np.random.random((n,)),
            "dummy_data_2": np.random.random((n,)),
        }
        batch = metric_to_batch(
            Metric(
                time_index=pd.date_range(
                    "2024-07-12T14Z", periods=n, freq="2h"
                ),
                data=DUMMY_DATA,
            )
        )
        assert batch.shape == torch.Size([1, n, 2])

    def test_prepare_predictions_keep_single_metric_name(self):
        import torch

        from pyoneai.core import Metric
        from pyoneai.mlmodels.utils.prediction_utils import prepare_predictions

        DUMMY_DATA = {
            "dummy_data": np.random.random((10,)),
        }
        PREDICTIONS = (torch.randn(10),)
        PRED_TIME_INDEX = pd.date_range(
            "2024-08-01T14Z", periods=10, freq="2h"
        )
        metric = Metric(
            time_index=pd.date_range("2024-07-12T14Z", periods=10, freq="2h"),
            data=DUMMY_DATA,
        )
        metric = prepare_predictions(
            metric, predictions=PREDICTIONS, pred_index=PRED_TIME_INDEX
        )
        assert metric.to_dataframe().columns[0] == "dummy_data"

    def test_prepare_predictions_keep_two_metric_names(self):
        import torch

        from pyoneai.core import Metric
        from pyoneai.mlmodels.utils.prediction_utils import prepare_predictions

        DUMMY_DATA = {
            "dummy_data": np.random.random((10,)),
            "dummy_data2": np.random.random((10,)),
        }
        PREDICTIONS = (torch.randn(10), torch.randn(10))
        PRED_TIME_INDEX = pd.date_range(
            "2024-08-01T14Z", periods=10, freq="2h"
        )
        metric = Metric(
            time_index=pd.date_range("2024-07-12T14Z", periods=10, freq="2h"),
            data=DUMMY_DATA,
        )
        metric = prepare_predictions(
            metric, predictions=PREDICTIONS, pred_index=PRED_TIME_INDEX
        )
        assert len(metric.to_dataframe().columns) == 2
        assert metric.to_dataframe().columns[0] == "dummy_data"
        assert metric.to_dataframe().columns[1] == "dummy_data2"

    def test_prepare_predictions_returns_metric(self):
        import torch

        from pyoneai.core import Metric
        from pyoneai.mlmodels.utils.prediction_utils import prepare_predictions

        DUMMY_DATA = {
            "dummy_data": np.random.random((10,)),
            "dummy_data2": np.random.random((10,)),
        }
        PREDICTIONS = (torch.randn(10), torch.randn(10))
        PRED_TIME_INDEX = pd.date_range(
            "2024-08-01T14Z", periods=10, freq="2h"
        )
        metric = Metric(
            time_index=pd.date_range("2024-07-12T14Z", periods=10, freq="2h"),
            data=DUMMY_DATA,
        )
        metric = prepare_predictions(
            metric, predictions=PREDICTIONS, pred_index=PRED_TIME_INDEX
        )
        assert isinstance(metric, Metric)

    def test_prepare_predictions_returns_predictions(self):
        import torch

        from pyoneai.core import Metric
        from pyoneai.mlmodels.utils.prediction_utils import prepare_predictions

        DUMMY_DATA = {
            "dummy_data": np.random.random((10,)),
            "dummy_data2": np.random.random((10,)),
        }
        PREDICTIONS = (torch.randn(10), torch.randn(10))
        PRED_TIME_INDEX = pd.date_range(
            "2024-08-01T14Z", periods=10, freq="2h"
        )
        metric = Metric(
            time_index=pd.date_range("2024-07-12T14Z", periods=10, freq="2h"),
            data=DUMMY_DATA,
        )
        metric = prepare_predictions(
            metric, predictions=PREDICTIONS, pred_index=PRED_TIME_INDEX
        )
        assert all(metric.time_index == PRED_TIME_INDEX)
        assert all(
            metric.to_dataframe()
            == pd.DataFrame(
                {
                    "dummy_data": PREDICTIONS[0].detach().numpy(),
                    "dummy_data2": PREDICTIONS[1].detach().numpy(),
                },
                index=PRED_TIME_INDEX,
            )
        )

    def test_raise_on_prediction_multivariate_mismatch(self):
        import torch

        from pyoneai.core import Metric
        from pyoneai.mlmodels.utils.prediction_utils import prepare_predictions

        DUMMY_DATA = {
            "dummy_data": np.random.random((10,)),
            "dummy_data2": np.random.random((10,)),
            "dummy_data3": np.random.random((10,)),
        }
        PREDICTIONS = (torch.randn(10), torch.randn(10))
        PRED_TIME_INDEX = pd.date_range(
            "2024-08-01T14Z", periods=10, freq="2h"
        )
        metric = Metric(
            time_index=pd.date_range("2024-07-12T14Z", periods=10, freq="2h"),
            data=DUMMY_DATA,
        )
        with pytest.raises(ValueError, match=r"Expected 3 predictions, got 2"):
            _ = prepare_predictions(
                metric, predictions=PREDICTIONS, pred_index=PRED_TIME_INDEX
            )

    def test_prepapre_prediction_pass_single_tensor(self):
        import torch

        from pyoneai.core import Metric
        from pyoneai.mlmodels.utils.prediction_utils import prepare_predictions

        DUMMY_DATA = {
            "dummy_data": np.random.random((10,)),
        }
        PREDICTIONS = torch.randn(10)
        PRED_TIME_INDEX = pd.date_range(
            "2024-08-01T14Z", periods=10, freq="2h"
        )
        metric = Metric(
            time_index=pd.date_range("2024-07-12T14Z", periods=10, freq="2h"),
            data=DUMMY_DATA,
        )
        assert prepare_predictions(
            metric, predictions=PREDICTIONS, pred_index=PRED_TIME_INDEX
        ) == prepare_predictions(
            metric, predictions=(PREDICTIONS,), pred_index=PRED_TIME_INDEX
        )
