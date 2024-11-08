import warnings

import numpy as np
from statsmodels.tsa.arima.model import ARIMA

from ..core import Metric
from .utils.prediction_utils import compute_prediction_time_index


class ArimaModel:
    def __init__(
        self,
        order: tuple[int, int, int] = (0, 0, 0),
        seasonal_order: tuple[int, int, int, int] = (0, 0, 0, 0),
        enforce_stationarity: bool = True,
        enforce_invertibility: bool = True,
        concentrate_scale: bool = False,
        trend_offset: int = 1,
    ):
        self.order = order
        self.seasonal_order = seasonal_order
        self.enforce_stationarity = enforce_stationarity
        self.enforce_invertibility = enforce_invertibility
        self.concentrate_scale = concentrate_scale
        self.trend_offset = trend_offset

    def fit(self, train):
        return self

    def predict(self, series: Metric, n: int) -> Metric:
        series_values = series.to_array()

        if len(series_values) == 1:
            warnings.warn(
                "Only one historical step is used. Returning the latest value for the prediction."
            )
            last_value = series.to_array()[-1]
            forecast = np.repeat(
                last_value, n
            )  # Repeat the latest value 'n' times
        else:
            model = ARIMA(
                series_values,
                order=self.order,
                seasonal_order=self.seasonal_order,
                enforce_stationarity=self.enforce_stationarity,
                concentrate_scale=self.concentrate_scale,
                trend_offset=self.trend_offset,
            )
            self.model = model.fit()

            forecast = self.model.forecast(steps=n)

        pred_ind = compute_prediction_time_index(series, n)

        metric_name = series.to_dataframe().columns[0]
        predicted_series = Metric(pred_ind, {metric_name: forecast})

        return predicted_series
