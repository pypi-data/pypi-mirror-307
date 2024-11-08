# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import numpy as np
import pandas as pd
import pytest

from pyoneai.core import time_index

_IDX = pd.date_range("2024-07-04T10Z", "2024-07-04T15Z", freq="30min")
_ARGS = {
    "timestamps": [
        "2024-07-04T10Z",
        pd.Timestamp("2024-07-04T10Z"),
        "2024-07-04T12:00:00.0+02:00",
        pd.Timestamp("2024-07-04T12:00:00.0+02:00"),
    ],
    "timedeltas": ["-150m", pd.Timedelta("-150m")],
    "slices": [
        slice("2024-07-04T10Z", "2024-07-04T15Z", "30m"),
        slice("-150m", "150m", "30m"),
    ],
    "array_like": [
        _IDX,
        [
            "2024-07-04T10Z",
            "2024-07-04T10:30Z",
            "2024-07-04T11Z",
            "2024-07-04T11:30Z",
            "2024-07-04T12Z",
            "2024-07-04T12:30Z",
            "2024-07-04T13Z",
            "2024-07-04T13:30Z",
            "2024-07-04T14Z",
            "2024-07-04T14:30Z",
            "2024-07-04T15Z",
        ],
    ],
}


class TestTimeIndex:
    # pylint: disable=protected-access, attribute-defined-outside-init
    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        self.now = pd.Timestamp("2024-07-04T12:30Z")
        self.mock_now = mocker.patch.object(
            time_index.pd.Timestamp,
            "now",
            autospec=True,
            return_value=self.now,
        )
        self.time_index = time_index.TimeIndex(_IDX)

    @pytest.mark.parametrize("value", _ARGS["timestamps"])
    def test_init_from_timestamp(self, value):
        time_idx = time_index.TimeIndex(value)
        assert isinstance(time_idx._init_time, pd.Timestamp)
        assert time_idx._init_time == self.now
        assert isinstance(time_idx.start, pd.Timestamp)
        assert time_idx.start == pd.Timestamp(value)
        assert isinstance(time_idx.stop, pd.Timestamp)
        assert time_idx.stop == pd.Timestamp(value)
        assert isinstance(time_idx.resolution, pd.Timedelta)
        assert time_idx.resolution == time_idx._DEFAULT_STEP
        assert isinstance(time_idx.values, pd.DatetimeIndex)
        assert pd.Timedelta(time_idx.values.freq) == time_idx.resolution
        assert np.all(
            time_idx.values
            == pd.DatetimeIndex([value], freq=time_idx._DEFAULT_STEP)
        )

    @pytest.mark.parametrize("value", _ARGS["timedeltas"])
    def test_init_from_timedelta(self, value):
        timestamp = self.now + pd.Timedelta(value)
        time_idx = time_index.TimeIndex(value)
        assert isinstance(time_idx._init_time, pd.Timestamp)
        assert time_idx._init_time == self.now
        assert isinstance(time_idx.start, pd.Timestamp)
        assert time_idx.start == timestamp
        assert isinstance(time_idx.stop, pd.Timestamp)
        assert time_idx.stop == timestamp
        assert isinstance(time_idx.resolution, pd.Timedelta)
        assert time_idx.resolution == time_idx._DEFAULT_STEP
        assert isinstance(time_idx.values, pd.DatetimeIndex)
        assert pd.Timedelta(time_idx.values.freq) == time_idx.resolution
        assert np.all(
            time_idx.values
            == pd.DatetimeIndex([timestamp], freq=time_idx._DEFAULT_STEP)
        )

    @pytest.mark.parametrize("value", _ARGS["slices"])
    def test_init_from_slice(self, value):
        time_idx = time_index.TimeIndex(value)
        assert isinstance(time_idx._init_time, pd.Timestamp)
        assert time_idx._init_time == self.now
        assert isinstance(time_idx.start, pd.Timestamp)
        assert time_idx.start == self.time_index.start
        assert isinstance(time_idx.stop, pd.Timestamp)
        assert time_idx.stop == self.time_index.stop
        assert isinstance(time_idx.resolution, pd.Timedelta)
        assert time_idx.resolution == self.time_index.resolution
        assert isinstance(time_idx.values, pd.DatetimeIndex)
        assert pd.Timedelta(time_idx.values.freq) == time_idx.resolution
        assert np.all(time_idx.values == self.time_index.values)

    def test_init_from_slice_default(self):
        value = slice(None)
        time_idx = time_index.TimeIndex(value)
        assert isinstance(time_idx._init_time, pd.Timestamp)
        assert time_idx._init_time == self.now
        assert isinstance(time_idx.start, pd.Timestamp)
        assert time_idx.start == self.now
        assert isinstance(time_idx.stop, pd.Timestamp)
        assert time_idx.stop == self.now
        assert isinstance(time_idx.resolution, pd.Timedelta)
        assert time_idx.resolution == time_idx._DEFAULT_STEP
        assert isinstance(time_idx.values, pd.DatetimeIndex)
        assert pd.Timedelta(time_idx.values.freq) == time_idx.resolution
        assert np.all(
            time_idx.values
            == pd.DatetimeIndex([self.now], freq=time_idx._DEFAULT_STEP)
        )

    @pytest.mark.parametrize("value", _ARGS["array_like"])
    def test_init_from_array_like(self, value):
        time_idx = time_index.TimeIndex(value)
        assert isinstance(time_idx._init_time, pd.Timestamp)
        assert time_idx._init_time == self.now
        assert isinstance(time_idx.start, pd.Timestamp)
        assert time_idx.start == self.time_index.start
        assert isinstance(time_idx.stop, pd.Timestamp)
        assert time_idx.stop == self.time_index.stop
        assert isinstance(time_idx.resolution, pd.Timedelta)
        assert time_idx.resolution == self.time_index.resolution
        assert isinstance(time_idx.values, pd.DatetimeIndex)
        assert pd.Timedelta(time_idx.values.freq) == time_idx.resolution
        assert np.all(time_idx.values == self.time_index.values)

    def test_init_from_empty_sequence(self):
        value = []
        time_idx = time_index.TimeIndex(value)
        assert isinstance(time_idx._init_time, pd.Timestamp)
        assert time_idx._init_time == self.now
        assert pd.isna(time_idx.start)
        assert pd.isna(time_idx.stop)
        assert isinstance(time_idx.resolution, pd.Timedelta)
        assert time_idx.resolution == self.time_index._DEFAULT_STEP
        assert isinstance(time_idx.values, pd.DatetimeIndex)
        assert pd.Timedelta(time_idx.values.freq) == time_idx.resolution
        assert not time_idx.values.size

    def test_init_from_start_greater_than_stop(self):
        value = slice("2024-07-04T15Z", "2024-07-04T10Z", "30m")
        with pytest.raises(ValueError):
            # pylint: disable=unused-variable
            time_idx = time_index.TimeIndex(value)  # noqa: F841

    def test_split(self):
        past, future = self.time_index.split("2024-07-04T14:15Z")
        assert past.start == self.time_index.start
        assert past.stop == pd.Timestamp("2024-07-04T14Z")
        assert past.resolution == self.time_index.resolution
        assert pd.Timedelta(past.values.freq) == past.resolution
        assert np.all(past.values == self.time_index.values[:9])
        assert future.start == pd.Timestamp("2024-07-04T14:30Z")
        assert future.stop == self.time_index.stop
        assert future.resolution == self.time_index.resolution
        assert pd.Timedelta(future.values.freq) == future.resolution
        assert np.all(future.values == self.time_index.values[9:])

    def test_split_default(self):
        past, future = self.time_index.split()
        assert past.start == self.time_index.start
        assert past.stop == pd.Timestamp("2024-07-04T12:30Z")
        assert past.resolution == self.time_index.resolution
        assert pd.Timedelta(past.values.freq) == past.resolution
        assert np.all(past.values == self.time_index.values[:6])
        assert future.start == pd.Timestamp("2024-07-04T13Z")
        assert future.stop == self.time_index.stop
        assert future.resolution == self.time_index.resolution
        assert pd.Timedelta(future.values.freq) == future.resolution
        assert np.all(future.values == self.time_index.values[6:])
