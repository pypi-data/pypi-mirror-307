from datetime import datetime

import numpy as np
import pandas as pd
import pytest

from pyoneai.core import Metric, Predictor, TimeIndex
from pyoneai.mlmodels import PersistenceModel


class TestPersistenceModel:
    @pytest.fixture(autouse=True)
    def setup(self):
        times = pd.date_range(
            start=datetime(2024, 7, 29), periods=1, freq="h", tz="UTC"
        )
        values = np.array([0.1234])
        self.timeseries = Metric(times, {"metric_name": values})
        self.model = PersistenceModel()

    def test_model_initialization(self):
        assert self.model.fit(self.timeseries) == self.model
        assert isinstance(self.model, PersistenceModel)

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

    def test_predict_results(self):
        predictions = self.model.predict(self.timeseries, n=3)

        # Check length, values and times
        assert len(predictions) == 3
        assert (predictions.to_array() == 0.1234).all()
        expected_times = pd.date_range(
            start=self.timeseries.time_index[-1] + self.timeseries.frequency,
            periods=3,
            freq=self.timeseries.frequency,
        )
        assert (predictions.time_index == expected_times).all()
