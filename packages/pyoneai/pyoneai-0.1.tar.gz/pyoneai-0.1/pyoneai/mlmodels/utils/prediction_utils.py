__all__ = (
    "compute_prediction_time_index",
    "metric_to_batch",
)
import pandas as pd

try:
    import torch
except ImportError:
    _HAS_TORCH = False
else:
    _HAS_TORCH = True

from ...core import Metric


def compute_prediction_time_index(metric: Metric, n: int) -> pd.DatetimeIndex:
    """Compute the time index for predictions.

    Parameters
    ----------
    metric : Metric
        Time series to predict from (the history).
    n : int
        Number of steps to predict.

    Returns
    -------
    pd.DatetimeIndex
        Time index for predictions.
    """
    return pd.date_range(
        metric.time_index[-1],
        periods=n + 1,
        freq=metric.time_index.freq,
        inclusive="right",
    )


if _HAS_TORCH:

    def metric_to_batch(metric: Metric) -> torch.Tensor:
        """Convert metric to tensor batch ready for feeding to model.

        Parameters
        ----------
        metric : Metric
            Time series to convert to batch

        Returns
        -------
        torch.Tensor
            Tensor batch
        """
        return torch.tensor(metric.to_array()).float().unsqueeze(0)

    def prepare_predictions(
        metric: Metric,
        predictions: torch.Tensor | tuple[torch.Tensor, ...],
        pred_index: pd.DatetimeIndex,
    ) -> Metric:
        """Prepare Metric with predictions for given historical Metric.

        Parameters
        ----------
        metric : Metric
            Historical Metric
        predictions : torch.Tensor | tuple[torch.Tensor, ...]
            Predictions
        pred_index : pd.DatetimeIndex
            Time index for predictions

        Returns
        -------
        Metric
            Metric with predictions
        """
        # TODO: to be changed when metrics name(s) could be easily accessed
        # with e.g. `metric.name` or `metric.names`
        if isinstance(predictions, torch.Tensor):
            predictions = (predictions,)
        metric_names = metric.to_dataframe().columns
        if len(metric_names) != len(predictions):
            raise ValueError(
                f"Expected {len(metric_names)} predictions, got {len(predictions)}"
            )
        return Metric(
            pred_index,
            data={
                metric_name: prediction.squeeze().cpu().numpy()
                for metric_name, prediction in zip(metric_names, predictions)
            },
        )
