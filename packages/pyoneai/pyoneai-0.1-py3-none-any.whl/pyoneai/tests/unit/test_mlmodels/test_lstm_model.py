import numpy as np
import pandas as pd
import pytest


class TestLSTMModel:

    @pytest.fixture(autouse=True)
    def setup(self):
        from pyoneai.mlmodels.lstm_model import ConvLSTMModel

        self.model_conv = ConvLSTMModel(
            input_size=1, hidden_size=100, num_layers=3, conv=True
        )
        self.model_nconv = ConvLSTMModel(
            input_size=1, hidden_size=100, num_layers=3, conv=False
        )

    def generate_time_index(self, n, tz: str = "UTC"):
        return pd.date_range(
            "2024-07-12T01:00:10", periods=n, freq="10s", tz=tz.upper()
        )

    def generate_data(self, n):
        return np.random.random((n,))

    def test_predict_returns_metric(self):
        from pyoneai.core import Metric

        metric = Metric(
            time_index=self.generate_time_index(10),
            data={"dummy_data": self.generate_data(10)},
        )
        predictions = self.model_conv.predict(metric, n=10)
        assert isinstance(predictions, Metric)

        predictions = self.model_nconv.predict(metric, n=10)
        assert isinstance(predictions, Metric)

    @pytest.mark.parametrize("n", [1, 10, 1000])
    def test_predict_returns_metric_correct_length(self, n):
        from pyoneai.core import Metric

        metric = Metric(
            time_index=self.generate_time_index(10),
            data={"dummy_data": self.generate_data(10)},
        )
        predictions = self.model_conv.predict(metric, n=n)
        assert len(predictions) == n

        predictions = self.model_nconv.predict(metric, n=n)
        assert len(predictions) == n

    def test_keep_original_metric_name(self):
        from pyoneai.core import Metric

        metric = Metric(
            time_index=self.generate_time_index(10),
            data={"dummy_data": self.generate_data(10)},
        )
        predictions = self.model_conv.predict(metric, n=1)
        assert predictions.to_dataframe().columns[0] == "dummy_data"
