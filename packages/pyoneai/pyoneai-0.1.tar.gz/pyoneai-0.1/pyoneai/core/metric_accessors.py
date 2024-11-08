import abc
import os
import warnings
from collections.abc import Collection, Sequence
from importlib import import_module
from string import Template
from typing import Literal

import numpy as np
import pandas as pd
from prometheus_api_client.metric_range_df import MetricRangeDataFrame

from .metric import Metric, PoolMetric
from .predictor import Predictor
from .time_index import TimeIndex, _DateTimeT, _TimeDeltaT


class BaseMetricAccessor(abc.ABC):
    __slots__ = ("_entity", "_metric_name")

    def __init__(self, entity, metric_name: str) -> None:
        self._entity = entity
        self._metric_name = metric_name

    @abc.abstractmethod
    def get_timeseries(self, time_index: TimeIndex) -> Metric:
        raise NotImplementedError()

    def __getitem__(
        self, key: _DateTimeT | _TimeDeltaT | Literal[0] | slice | TimeIndex
    ) -> Metric:
        time_index = key if isinstance(key, TimeIndex) else TimeIndex(key)
        return self.get_timeseries(time_index)


class PredictorMetricAccessor(BaseMetricAccessor):
    __slots__ = ()

    def get_timeseries(self, time_index: TimeIndex) -> Metric:
        predictor = Predictor(
            entity=self._entity,
            metric_name=self._metric_name,
            time_index=time_index,
        )
        return predictor.predict()


class PrometheusMetricAccessor(BaseMetricAccessor):
    __slots__ = ("_query",)

    def _prepare_query(self, metric_name: str) -> str:
        registry = self._entity.registry
        query = registry[metric_name]["accessor"]["kwargs"]["query"]

        if Template.delimiter not in query:
            return query

        template = Template(query)
        kwa = {}
        for name in template.get_identifiers():
            attr_name = name.lower()
            if hasattr(self._entity, attr_name):
                kwa[name] = getattr(self._entity, attr_name)
            elif name == "PERIOD":
                kwa[name] = f"{Template.delimiter}PERIOD"
            else:
                raise ValueError(f"'{name}' identifier is not allowed")
        return template.substitute(**kwa)

    def _prepare_period_query(self, period: pd.Timedelta) -> str:
        if f"{Template.delimiter}PERIOD" not in self._query:
            return self._query
        period_s = f"{round(period.total_seconds())}s"
        return Template(self._query).substitute({"PERIOD": period_s})

    def _prepare_time_index_query(self, time_index: TimeIndex) -> str:
        if time_index.values.size == 1:
            period = time_index.resolution
        else:
            period = time_index.stop - time_index.start
        return self._prepare_period_query(period)

    def __init__(self, entity, metric_name: str) -> None:
        super().__init__(entity=entity, metric_name=metric_name)
        self._query = self._prepare_query(metric_name)

    @property
    def client(self):
        return self._entity.session.prometheus_client

    def _get_query_result(self, time_index: TimeIndex) -> list[dict]:
        return self.client.custom_query_range(
            query=self._prepare_time_index_query(time_index),
            start_time=time_index.start.to_pydatetime(),
            end_time=time_index.stop.to_pydatetime(),
            step=f"{round(time_index.resolution.total_seconds())}s",
        )

    def _get_metric_df(
        self, query_result: list[dict], row_idx: slice | None = None
    ) -> pd.DataFrame:
        if query_result:
            metric_df = MetricRangeDataFrame(query_result)
            return metric_df if row_idx is None else metric_df.iloc[row_idx, :]
        warnings.warn(f"'query_result' for '{self._metric_name}' is empty")
        return pd.DataFrame(data={"value": []}, index=pd.DatetimeIndex([]))

    def get_timeseries(self, time_index: TimeIndex) -> Metric:
        metric = self._get_query_result(time_index)
        # TODO: Check if the returned data are always related to UTC.
        metric_df = self._get_metric_df(metric).tz_localize("UTC")
        if metric_df.index.freq is None:
            # TODO: Consider moving this functionality to `Metric`.
            duplicates = metric_df.index.duplicated(keep='last')
            if duplicates.any():
                metric_df = metric_df.loc[~duplicates, :]
            metric_df = metric_df.asfreq(time_index.resolution)
        if metric_df.isna().any(axis=None):
            # NOTE: This is the case when Prometheus omits a value.
            # TODO: Consider moving this functionality to `Metric`.
            metric_df = metric_df.interpolate(
                method="linear", axis=0, limit_direction="both"
            )
        return Metric(
            time_index=metric_df.index,
            data={self._metric_name: metric_df["value"].to_numpy(copy=False)},
        )


class MetricAccessor(BaseMetricAccessor):
    __slots__ = ("_hist", "_pred")

    def _get_history(self, metric_name: str):
        class_name = (
            self._entity.registry[metric_name]["accessor"].get("class")
            or self._entity.registry_default["accessor"]["class"]
        )
        module_name, _, class_name = class_name.rpartition(".")
        module = import_module(module_name)
        cls_ = getattr(module, class_name)
        return cls_(self._entity, metric_name)

    def __init__(self, entity, metric_name: str) -> None:
        super().__init__(entity=entity, metric_name=metric_name)
        self._hist = self._get_history(metric_name)
        self._pred = PredictorMetricAccessor(entity, metric_name)

    def get_timeseries(self, time_index: TimeIndex) -> Metric:
        now = pd.Timestamp.now(tz="UTC")
        past_start = time_index.start <= now
        past_end = time_index.stop <= now
        if past_start and past_end:
            # in this case we access only Prometheus Metrics
            return self._hist.get_timeseries(time_index)
        if past_start and not past_end:
            # in this case we access Prometheus Metrics and Metrics Prediction
            # period.start -> prometheus
            # period.end -> predictor
            hist_idx, pred_idx = time_index.split(now)
            hist = self._hist.get_timeseries(hist_idx)
            pred = self._pred.get_timeseries(pred_idx)
            return hist.append(pred)
        if not past_start and not past_end:
            # in this case we use only Metrics Prediction
            # period.start & period.end -> Predictor
            return self._pred.get_timeseries(time_index)
        raise ValueError("'time_index' contains incorrect data")


class DerivedMetricAccessor(BaseMetricAccessor):
    __slots__ = ("_covariates", "_model")

    def __init__(
        self, entity, metric_name: str, covariate_names: Sequence[str]
    ) -> None:
        super().__init__(entity=entity, metric_name=metric_name)
        self._covariates = list(covariate_names)
        self._model = None

    def _load_model(self):
        if self._model is not None:
            return self._model

        derived = (
            self._entity.registry[self._metric_name].get("derived")
            or self._entity.registry_default["derived"]
        )
        class_name = derived.get("class")
        module_name, _, class_name = class_name.rpartition(".")
        module = import_module(module_name)
        cls_ = getattr(module, class_name)
        kwa = derived.get("kwargs", {})
        if model_rel_path := derived.get("path"):
            model_base_path = self._entity.session.config.model_path
            model_abs_path = os.path.join(model_base_path, model_rel_path)
            self._model = cls_(**kwa).load(model_abs_path)
            return self._model
        else:
            return cls_()

    def get_timeseries(self, time_index: TimeIndex) -> Metric:

        metrics = self._entity.metrics
        covar_accessor = metrics[
            self._covariates[0]
        ]  # this works for the moment only with 1 input
        covar_data_ = covar_accessor[time_index].to_dataframe()
        covar_data = Metric.from_dataframe(covar_data_.tz_localize(None))
        # TODO: data should be built and passed as arguments in the same sequence from the user
        # TODO: we need a loop on time that builds the Darts timeseries
        new_values = np.empty(
            len(covar_data.time_index),
            dtype=covar_data.values(copy=False).dtype,
        )
        for i, t in enumerate(covar_data.time_index):
            new_values[i] = self._load_model().predict(
                covar_data[t].values(copy=False).item()
            )
        result = Metric.from_series(
            pd.Series(data=new_values, index=covar_data.time_index)
        )

        return Metric.from_dataframe(
            result.pd_dataframe().tz_localize(covar_data_.index.tz)
        )


class MetricAccessors(BaseMetricAccessor):
    __slots__ = ("_accessors",)

    def __init__(self, entity, metric_name: Collection[str]) -> None:
        super().__init__(entity, list(metric_name))
        metrics = entity.metrics
        self._accessors = [metrics[name] for name in metric_name]

    def get_timeseries(self, time_index: TimeIndex) -> Metric:
        metrics = [accessor[time_index] for accessor in self._accessors]
        return Metric.multivariate(metrics)


# TODO: Consider refactoring the accessor classes so that `PoolMetricAccessor`
# can inherit `BaseMetricAccessor`.
class PoolMetricAccessor:
    __slots__ = ("_pool", "_metric_name")

    def __init__(self, pool, metric_name: str | Collection[str]) -> None:
        self._pool = pool
        self._metric_name = metric_name

    def get_timeseries(self, time_index: TimeIndex) -> PoolMetric:
        names = self._metric_name
        metrics = [entity.metrics[names][time_index] for entity in self._pool]
        return PoolMetric(pool=self._pool, metrics=metrics)

    def __getitem__(
        self, key: _DateTimeT | _TimeDeltaT | Literal[0] | slice | TimeIndex
    ) -> PoolMetric:
        time_index = key if isinstance(key, TimeIndex) else TimeIndex(key)
        return self.get_timeseries(time_index)
