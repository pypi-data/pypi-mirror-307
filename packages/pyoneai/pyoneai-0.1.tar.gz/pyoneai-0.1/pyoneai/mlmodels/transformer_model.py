"""The module contains Transformer class using just PyTorch."""

__all__ = ("TransformerModel",)
import math
from typing import Self

import pandas as pd
import torch
import torch.nn as nn

from ..core import Metric
from .utils.prediction_utils import (
    compute_prediction_time_index,
    metric_to_batch,
    prepare_predictions,
)


# https://github.com/unit8co/darts/blob/master/darts/models/forecasting/transformer_model.py
def _generate_coder(
    d_model,
    dim_ff,
    dropout,
    nhead,
    num_layers,
    norm_layer,
    coder_cls,
    layer_cls,
    ffn_cls,
):
    """Generates an Encoder or Decoder with one of Darts' Feed-forward Network variants.
    Parameters
    ----------
    coder_cls
        Either `torch.nn.TransformerEncoder` or `...TransformerDecoder`
    layer_cls
        Either `darts.models.components.transformer.CustomFeedForwardEncoderLayer`,
        `...CustomFeedForwardDecoderLayer`, `nn.TransformerEncoderLayer`, or `nn.TransformerDecoderLayer`.
    ffn_cls
        One of Darts' Position-wise Feed-Forward Network variants `from darts.models.components.glu_variants`
    """

    ffn = (
        dict(ffn=ffn_cls(d_model=d_model, d_ff=dim_ff, dropout=dropout))
        if ffn_cls
        else dict()
    )
    layer = layer_cls(
        **ffn,
        dropout=dropout,
        d_model=d_model,
        nhead=nhead,
        dim_feedforward=dim_ff,
    )
    return coder_cls(
        layer,
        num_layers=num_layers,
        norm=norm_layer(d_model),
    )


# https://pytorch.org/tutorials/beginner/transformer_tutorial.html
class _PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout=0.1, max_len=500):
        """An implementation of positional encoding as described in 'Attention is All you Need' by Vaswani et al. (2017)

        Parameters
        ----------
        d_model
            The number of expected features in the transformer encoder/decoder inputs.
            Last dimension of the input.
        dropout
            Fraction of neurons affected by Dropout (default=0.1).
        max_len
            The dimensionality of the computed positional encoding array.
            Only its first "input_size" elements will be considered in the output.

        Inputs
        ------
        x of shape `(batch_size, input_size, d_model)`
            Tensor containing the embedded time series.

        Outputs
        -------
        y of shape `(batch_size, input_size, d_model)`
            Tensor containing the embedded time series enhanced with positional encoding.
        """
        super().__init__()
        self.dropout = nn.Dropout(p=dropout)

        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float()
            * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0).transpose(0, 1)
        self.register_buffer("pe", pe)

    def forward(self, x):
        x = x + self.pe[: x.size(0), :]
        return self.dropout(x)


class TransformerModel(nn.Module):
    """Transformer model for time series forecasting."""

    def __init__(
        self,
        input_size: int,
        output_size: int,
        in_sequence_length: int,
        nhead: int,
        num_encoder_layers: int,
        num_decoder_layers: int,
        dropout: float,
        hidden_dim: int,
        activation: str,
    ) -> None:
        super().__init__()
        self.input_size = input_size
        self.output_size = output_size
        self.in_sequence_length = in_sequence_length
        # NOTE: to enable any forecast horizon, we set out_sequence_length
        # to 1 and repeat prediction
        self.out_sequence_length = 1
        self.nhead = nhead
        self.num_encoder_layers = num_encoder_layers
        self.num_decoder_layers = num_decoder_layers
        self.dropout = dropout
        self.hidden_dim = hidden_dim

        self.encoder = nn.Linear(input_size, hidden_dim)
        self.positional_encoding = _PositionalEncoding(
            hidden_dim, dropout, self.in_sequence_length
        )
        custom_encoder = _generate_coder(
            hidden_dim,
            hidden_dim,
            dropout,
            nhead,
            num_encoder_layers,
            nn.LayerNorm,
            coder_cls=nn.TransformerEncoder,
            layer_cls=nn.TransformerEncoderLayer,
            ffn_cls=None,
        )

        custom_decoder = _generate_coder(
            hidden_dim,
            hidden_dim,
            dropout,
            nhead,
            num_decoder_layers,
            nn.LayerNorm,
            coder_cls=nn.TransformerDecoder,
            layer_cls=nn.TransformerDecoderLayer,
            ffn_cls=None,
        )

        self.transformer = nn.Transformer(
            d_model=hidden_dim,
            nhead=nhead,
            num_encoder_layers=num_encoder_layers,
            num_decoder_layers=num_decoder_layers,
            dim_feedforward=hidden_dim,
            dropout=dropout,
            activation=activation,
            custom_encoder=custom_encoder,
            custom_decoder=custom_decoder,
        )

        self.decoder = nn.Linear(
            hidden_dim, self.out_sequence_length * self.output_size
        )

    def _preprocess_input(self, x: torch.Tensor) -> torch.Tensor:
        """Preprocess input."""
        src = x.permute(1, 0, 2)
        tgt = src[-1:, :, :]
        return src, tgt

    def forward(self, x) -> torch.Tensor:
        """Run single step."""
        x, tgt = self._preprocess_input(x)
        x = self.encoder(x) * math.sqrt(self.hidden_dim)
        x = self.positional_encoding(x)

        tgt = self.encoder(tgt) * math.sqrt(self.hidden_dim)
        tgt = self.positional_encoding(tgt)

        x = self.transformer(src=x, tgt=tgt)
        out = self.decoder(x)
        predictions = out[0, :, :]
        return predictions

    def predict_raw(self, series: torch.Tensor, n: int) -> torch.Tensor:
        preds = []
        with torch.no_grad():
            load = series
            for _ in range(n):
                x = self.forward(load)
                preds.append(x)
                load = torch.cat((load, x.unsqueeze(0)), dim=1)[:, 1:, :]
        return torch.stack(preds)

    def predict(self, series: Metric, n: int) -> Metric:
        """Predict `n` steps ahead.

        Parameters
        ----------
        series : Metric
            Metric to predict from (the history).
        n : int
            Number of steps to predict.

        Returns
        -------
        Metric
            Predicted metric values.
        """
        self.eval()
        pred_ind = compute_prediction_time_index(series, n)
        metric = Metric(
            series.time_index[-self.in_sequence_length :],
            series.to_dataframe().iloc[-self.in_sequence_length :],
        )
        preds = self.predict_raw(metric_to_batch(metric), n)
        return prepare_predictions(metric, preds, pred_ind)

    @classmethod
    def load(cls, path: str) -> Self:
        """Load model from Kit4DL checkpoint.

        Parameters
        ----------
        path : str
            Path to the checkpoint.

        Returns
        -------
        TransformerModel
            The loaded model.
        """
        if torch.cuda.is_available():
            checkpoint = torch.load(path, weights_only=False)
        else:
            checkpoint = torch.load(
                path, weights_only=False, map_location="cpu"
            )
        model = cls(**checkpoint["hyper_parameters"])
        model.load_state_dict(checkpoint["state_dict"])
        model.eval()
        return model
