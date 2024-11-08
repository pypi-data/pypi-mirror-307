import numpy as np
import pandas as pd
import pytest


class TestTransformerModel:

    @pytest.fixture(autouse=True)
    def setup(self):
        from pyoneai.mlmodels.transformer_model import TransformerModel

        self.model = TransformerModel(
            input_size=1,
            output_size=1,
            in_sequence_length=5,
            nhead=2,
            num_encoder_layers=3,
            num_decoder_layers=3,
            dropout=0.1,
            hidden_dim=100,
            activation="relu",
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
            time_index=self.generate_time_index(100),
            data={"dummy_data": self.generate_data(100)},
        )
        predictions = self.model.predict(metric, n=10)
        assert isinstance(predictions, Metric)

    @pytest.mark.parametrize("n", [1, 10, 1000])
    def test_predict_returns_metric_correct_length(self, n):
        from pyoneai.core import Metric

        metric = Metric(
            time_index=self.generate_time_index(100),
            data={"dummy_data": self.generate_data(100)},
        )
        predictions = self.model.predict(metric, n=n)
        assert len(predictions) == n
