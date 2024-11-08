import numpy as np
import pandas as pd

from ..core import Metric
from .utils.prediction_utils import compute_prediction_time_index


class PersistenceModel:

    def fit(self, train):
        return self

    def predict(self, series: Metric, n: int) -> Metric:
        # Repeat the last value n times to create predictions
        last_value = series.to_array()[-1]
        predictions = np.repeat(last_value, n)

        # Generate the new timestamps
        time_index = compute_prediction_time_index(series, n)

        # Create and return the new TimeSeries with predictions
        # TODO:TO BE CHANGED when add metric names property!!
        metric_name = series.to_dataframe().columns[0]
        predicted_series = Metric(time_index, {metric_name: predictions})
        return predicted_series
