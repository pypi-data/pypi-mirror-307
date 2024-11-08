from datetime import datetime, timedelta
from typing import Literal, Self, TypeAlias, TypeVar

import numpy as np
import numpy.typing as npt
import pandas as pd

_DateTimeT = TypeVar("_DateTimeT", bound=str | datetime | np.datetime64)
_TimeDeltaT = TypeVar("_TimeDeltaT", bound=str | timedelta | np.timedelta64)
_TimeIndexT: TypeAlias = _DateTimeT | _TimeDeltaT | npt.ArrayLike | slice

_DATE_TIME_END = frozenset(map(str, range(10))) | {"Z", "z"}
_TIME_DELTA_END = frozenset({"W", "w", "D", "d", "h", "m", "s"})


class TimeIndex:
    __slots__ = ("_time_index", "_start", "_stop", "_step", "_init_time")

    _DEFAULT_STEP = pd.Timedelta("60s")

    def __init__(self, value: _TimeIndexT = "0") -> None:
        self._init_time = pd.Timestamp.now(tz="UTC")

        if isinstance(value, slice):
            self._start = self._time_stamp(value.start)
            self._stop = self._time_stamp(value.stop)
            if value.step is None:
                self._step = self._DEFAULT_STEP
            else:
                self._step = pd.Timedelta(value.step)
            self._time_index = pd.date_range(
                self._start, self._stop, freq=self._step
            )
        elif isinstance(
            value, (str, datetime, np.datetime64, timedelta, np.timedelta64)
        ):
            time_stamp = self._time_stamp(value)
            self._start = time_stamp
            self._stop = time_stamp
            self._step = freq = self._DEFAULT_STEP
            self._time_index = pd.DatetimeIndex([time_stamp], freq=freq)
        else:
            idx = pd.DatetimeIndex(value, freq="infer")
            match idx.size:
                case 0:
                    self._start = self._stop = pd.NaT
                    if idx.freq is None:
                        idx.freq = self._DEFAULT_STEP
                        self._step = self._DEFAULT_STEP
                    else:
                        self._step = pd.Timedelta(idx.freq)
                case 1:
                    time_stamp = self._assure_time_zone(idx[0])
                    self._start = self._stop = time_stamp
                    if idx.freq is None:
                        idx.freq = self._DEFAULT_STEP
                        self._step = self._DEFAULT_STEP
                    else:
                        self._step = pd.Timedelta(idx.freq)
                case 2:
                    self._start, self._stop = idx[0], idx[-1]
                    if idx.freq is None:
                        diff = self._stop - self._start
                        idx.freq = diff
                        self._step = diff
                    else:
                        self._step = pd.Timedelta(idx.freq)
                case _:
                    self._start, self._stop = idx[0], idx[-1]
                    if idx.freq is None:
                        raise ValueError("'value' is not a monotonic sequence")
                    self._step = pd.Timedelta(idx.freq)
            self._time_index = idx

        if self._start > self._stop:
            raise ValueError("'value' is incorrect")

    @staticmethod
    def _assure_time_zone(time_stamp: pd.Timestamp) -> pd.Timestamp:
        if time_stamp.tz is not None:
            return time_stamp
        raise ValueError(
            "'time' is passed as a datetime-like object and must contain a "
            "time zone information"
        )

    def _time_stamp(
        self, value: _DateTimeT | _TimeDeltaT | Literal[0] | None
    ) -> pd.Timestamp:
        match value:
            case None | 0 | "0":
                return self._init_time
            case datetime() | np.datetime64():
                time_stamp = pd.Timestamp(value)
                return self._assure_time_zone(time_stamp)
            case timedelta() | np.timedelta64():
                return self._init_time + value
            case str():
                # TODO: Use `dateutil` for better checks.
                # (value[-1].isdigit or value.endswith(('Z', 'z'), -1))
                last = value[-1]
                if last in _DATE_TIME_END and len(value) >= 14:
                    time_stamp = pd.Timestamp(value)
                    return self._assure_time_zone(time_stamp)
                if last in _TIME_DELTA_END:
                    time_delta = pd.Timedelta(value)
                    return self._init_time + time_delta
                raise ValueError("'value' is an incorrect string")
            case _:
                raise TypeError(
                    "'value' must be a datetime-like or timedelta-like object"
                )

    @property
    def values(self) -> pd.DatetimeIndex:
        # TODO: Consider renaming this property.
        return self._time_index

    @property
    def start(self) -> pd.Timestamp:
        return self._start

    @property
    def stop(self) -> pd.Timestamp:
        return self._stop

    @property
    def resolution(self) -> pd.Timedelta:
        return self._step

    def split(self, when: _DateTimeT | None = None) -> tuple[Self, Self]:
        if when is None:
            time_stamp = self._init_time
        else:
            time_stamp = self._assure_time_zone(pd.Timestamp(when))
        time_idx = self._time_index
        sep_idx = np.searchsorted(time_idx, time_stamp, side="right")
        cls_ = type(self)
        return (cls_(time_idx[:sep_idx]), cls_(time_idx[sep_idx:]))


class _TimeIndexer:
    __slots__ = ()

    def __getitem__(self, key: _TimeIndexT) -> TimeIndex:
        return TimeIndex(key)


time = _TimeIndexer()
