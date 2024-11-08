"""The module contains Transformer class using just PyTorch."""

__all__ = ("ConvLSTMModel",)
from typing import Self

import torch
import torch.nn as nn

from ..core import Metric
from .utils.prediction_utils import (
    compute_prediction_time_index,
    metric_to_batch,
    prepare_predictions,
)


class ConvLSTMModel(nn.Module):
    """ConvLSTM neural network model."""

    def __init__(
        self,
        input_size: int,
        hidden_size: int,
        num_layers: int,
        dropout: float = 0.0,
        conv: bool = False,
    ) -> None:
        super().__init__()
        self.run_conv = conv
        if conv:
            self.conv = nn.Sequential(
                nn.Conv1d(
                    in_channels=input_size,
                    out_channels=hidden_size,
                    kernel_size=3,
                ),
                nn.ReLU(),
                nn.BatchNorm1d(hidden_size),
                nn.Conv1d(
                    in_channels=hidden_size,
                    out_channels=hidden_size,
                    kernel_size=3,
                ),
                nn.ReLU(),
                nn.BatchNorm1d(hidden_size),
            )
        self.lstm = nn.LSTM(
            input_size=hidden_size if conv else input_size,
            hidden_size=hidden_size,
            num_layers=num_layers,
            dropout=dropout,
            batch_first=True,
        )
        self.cls = nn.Sequential(
            nn.Linear(in_features=hidden_size, out_features=1),
        )

    def forward(self, x) -> torch.Tensor:
        """Run single step."""
        if self.run_conv:
            x = self.conv(x.permute(0, 2, 1))
            x, _ = self.lstm(x.permute(0, 2, 1))
        else:
            x, _ = self.lstm(x)
        x = self.cls(x[:, -1, :])
        return x.squeeze()

    def predict_raw(self, series: torch.Tensor, n: int) -> torch.Tensor:
        preds = []
        with torch.no_grad():
            load = series
            for _ in range(n):
                x = self.forward(load)
                preds.append(x)
                load = torch.cat((load, x.view(1, 1, 1)), dim=1)[:, 1:, :]
        return torch.stack(preds)

    def predict(self, series: Metric, n: int) -> Metric:
        """Predict `n` steps ahead.

        Parameters
        ----------
        series : Metric
            Time series to predict from (the history).
        n : int
            Number of steps to predict.

        Returns
        -------
        Metric
            Predicted time series.
        """
        self.eval()
        pred_ind = compute_prediction_time_index(series, n)
        preds = self.predict_raw(metric_to_batch(series), n)
        return prepare_predictions(series, preds, pred_ind)

    @classmethod
    def load(cls, path: str) -> Self:
        """Load model from checkpoint.

        Parameters
        ----------
        path : str
            Path to the checkpoint.

        Returns
        -------
        ConvLSTMModel
            The loaded model.
        """
        if torch.cuda.is_available():
            checkpoint = torch.load(path, weights_only=True)
        else:
            checkpoint = torch.load(
                path, weights_only=True, map_location="cpu"
            )
        model = cls(**checkpoint["hyper_parameters"])
        model.load_state_dict(checkpoint["state_dict"])
        model.eval()
        return model
