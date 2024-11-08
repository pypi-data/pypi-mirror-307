# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
import numpy as np
import pandas as pd
import pytest
from pytest_mock import MockerFixture

import pyoneai.core.predictor
from pyoneai.core import TimeIndex


class TestPredictor:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker: MockerFixture):
        self.mock_entity = mocker.MagicMock()
        self.time_index = TimeIndex(slice("0", "2m", "1m"))
        predicted_ts = pd.DataFrame(
            data={"gaussian": np.random.normal(loc=10.0, scale=0.1, size=3)},
            index=pd.date_range(
                pd.Timestamp("2010-02-01 00:00:00"), periods=3, freq="1D"
            ),
        )
        self.predicted_df = predicted_ts.tz_localize("UTC")
        self.mock_model = mocker.MagicMock()
        self.mock_model.predict.return_value = predicted_ts
        self.mock_series = mocker.MagicMock()
        self.mock_series.time_zone = "UTC"
        self.mock_series.to_dataframe.return_value = pd.DataFrame(
            data={"value": [1, 2, 3]},
            index=TimeIndex(slice("-2m", "0", "1m")).values,
        )
        self.mock_prepare_model = mocker.patch.object(
            pyoneai.core.predictor,
            "_prepare_model",
            autospec=True,
            return_value=(self.mock_model, self.mock_series),
        )
        self.predictor = pyoneai.core.predictor.Predictor(
            entity=self.mock_entity,
            metric_name="test_metric",
            time_index=self.time_index,
        )

    def test_init(self):
        assert self.predictor._forecast_horizon == self.time_index.values.size
        assert self.predictor._model == self.mock_model
        assert self.predictor._series == self.mock_series
        self.mock_prepare_model.assert_called_once_with(
            self.mock_entity, "test_metric", self.time_index
        )

    def test_predict(self):
        predictions = self.predictor.predict()
        self.mock_model.predict.assert_called_once()
        # assert predictions == self.predicted_df
