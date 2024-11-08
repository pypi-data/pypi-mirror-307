import os
from collections.abc import Sequence
from importlib import import_module
from typing import Any

import pandas as pd

from .metric import Metric
from .time_index import TimeIndex


def _get_class(name: str) -> type:
    module_name, _, cls_name = name.rpartition(".")
    module = import_module(module_name)
    cls_ = getattr(module, cls_name)
    return cls_


def _get_model(
    full_class_name: str,
    args: tuple | list = (),
    kwargs: dict | None = None,
    path: str = "",
    model_path: str = "",
    train: Metric | None = None,
):
    # Import `model` module and class.
    cls_ = _get_class(full_class_name)
    # Load a pre-trained model and return it, if it exists.
    if path:
        print("pre-trained model found, loading")
        return cls_.load(os.path.join(model_path, path))

    # Instantiate a model, fit it, and return it.
    if train is None or not len(train):
        # Raise an error if there is no pre-trained model nor training data.
        raise ValueError("'train' must be a non-empty time series object")
    if not kwargs:
        return cls_(*args).fit(train)
    if "model" not in kwargs:
        return cls_(*args, **kwargs).fit(train)
    model_kwargs = kwargs.copy()
    submodel_data = model_kwargs.pop("model", None)
    submodel_cls = _get_class(submodel_data["class"])
    submodel_args = submodel_data["args"]
    submodel_kwargs = submodel_data["kwargs"]
    submodel = submodel_cls(*submodel_args, **submodel_kwargs)
    return cls_(*args, **model_kwargs, model=submodel).fit(train)


def _prepare_model(
    entity, metric_name: str, time_index: TimeIndex
) -> tuple[Any, Metric]:
    hist_accessor = entity.metrics[metric_name]._hist
    kwa = (
        entity.registry[metric_name].get("prediction")
        or entity.registry_default["prediction"]
    )
    kwa = kwa.copy()
    model_cls = kwa.pop("class")

    if "historical_steps" in kwa:
        n_periods = int(kwa.pop("historical_steps"))
    else:
        historical_period_str = kwa.pop("historical_period")
        try:
            historical_period = pd.Timedelta(historical_period_str)
        except ValueError:
            raise ValueError(
                f"Invalid historical_period format: {historical_period_str}"
            )
        if time_index.resolution > -historical_period:
            raise ValueError(
                "'historical_period' must be less than 'resolution'"
            )
        if historical_period == pd.Timedelta(0):
            n_periods = 1
        else:
            n_periods = round(-historical_period / time_index.resolution)

    hist_time_idx = pd.date_range(
        end=time_index.start - time_index.resolution,
        periods=n_periods,
        freq=time_index.resolution,
    )
    series = hist_accessor[hist_time_idx].fill_missing_values()
    model_path = entity.session.config.model_path
    model = _get_model(model_cls, **kwa, model_path=model_path, train=series)
    return model, series


class Predictor:
    """
    Generate forecasts using time series models.

    Parameters
    ----------
    entity : Union[OnedEntity, OneFlowEntity]
        Entity associated with the predictor.
    metric_name : str
        Metric name.
    time_index : TimeIndex
        Time index for generating forecasts.

    Methods
    -------
    predict: Generate forecasts using the trained model.

    """

    __slots__ = ("_model", "_series", "_forecast_horizon")

    def __init__(
        self, entity, metric_name: str, time_index: TimeIndex
    ) -> None:
        self._forecast_horizon = time_index.values.size
        self._model, self._series = _prepare_model(
            entity, metric_name, time_index
        )

    def predict(self) -> Metric:
        """
        Generate forecasts using the trained model.

        Returns
        -------
        Metric
            The forecasted time series.

        """
        return self._model.predict(
            n=self._forecast_horizon, series=self._series
        )
