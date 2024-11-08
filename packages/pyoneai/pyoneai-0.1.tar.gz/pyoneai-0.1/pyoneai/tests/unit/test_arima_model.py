from datetime import datetime

import numpy as np
import pandas as pd
import pytest

from pyoneai.core import Metric, Predictor, TimeIndex
from pyoneai.mlmodels import ArimaModel


class TestArimaModel:
    @pytest.fixture(autouse=True)
    def setup(self):
        times = pd.date_range(
            start=datetime(2024, 7, 29), periods=2, freq="h", tz="UTC"
        )
        values = np.array([0.1234, 0.1234])
        self.timeseries = Metric(times, {"metric_name": values})
        self.model = ArimaModel(
            order=(0, 0, 0),
            seasonal_order=(0, 0, 0, 0),
            enforce_stationarity=False,
            enforce_invertibility=False,
            concentrate_scale=False,
            trend_offset=1,
        )

    def test_model_initialization(self):
        assert self.model.fit(self.timeseries) == self.model
        assert isinstance(self.model, ArimaModel)

    def test_predict(self, mocker):
        mock_entity = mocker.MagicMock()
        mock_prepare_model = mocker.patch(
            "pyoneai.core.predictor._prepare_model"
        )
        mock_prepare_model.return_value = (self.model, self.timeseries)

        # Check the prepared model
        t_i = TimeIndex(slice("0", "2m", "1m"))
        predictor = Predictor(
            entity=mock_entity, metric_name="cpu_usage", time_index=t_i
        )
        model, series = predictor._model, predictor._series
        assert model == self.model
        assert series == self.timeseries
        mock_prepare_model.assert_called_once_with(
            mock_entity, "cpu_usage", t_i
        )

    def test_predict_returns_metric(self):
        predictions = self.model.predict(self.timeseries, n=1)
        assert isinstance(predictions, Metric)

    def test_predict_one_result(self):
        predictions = self.model.predict(self.timeseries, n=1)

        # Check length, values and times
        assert len(predictions) == 1
        expected_times = pd.date_range(
            start=self.timeseries.time_index[-1] + self.timeseries.frequency,
            periods=1,
            freq=self.timeseries.frequency,
        )
        assert (predictions.time_index == expected_times).all()

    def test_predict_multiple_results(self):
        predictions = self.model.predict(self.timeseries, n=5)

        # Check length, values and times
        assert len(predictions) == 5
        expected_times = pd.date_range(
            start=self.timeseries.time_index[-1] + self.timeseries.frequency,
            periods=5,
            freq=self.timeseries.frequency,
        )
        assert (predictions.time_index == expected_times).all()

    def test_predict_from_one_historical_step_return(self):
        times = pd.date_range(
            start=datetime(2024, 7, 29), periods=1, freq="h", tz="UTC"
        )
        values = np.array([0.5678])
        one_step_series = Metric(times, {"metric_name": values})

        # Make predictions with only one historical data point
        with pytest.warns(
            UserWarning,
            match="Only one historical step is used. Returning the latest value for the prediction.",
        ):
            predictions = self.model.predict(one_step_series, n=3)

        # Check that all predictions are equal to the latest value
        assert len(predictions) == 3
        assert (predictions.to_array() == values[-1]).all()

        # Ensure that times are correctly forecasted
        expected_times = pd.date_range(
            start=one_step_series.time_index[-1] + one_step_series.frequency,
            periods=3,
            freq=one_step_series.frequency,
        )
        assert (predictions.time_index == expected_times).all()
