import time
import datetime

from enum import Enum, auto

__all__ = [
    'now',
    'now_str',
    'datetime_to_timestamp',
    'timestamp_to_datetime',
    'TimeUnit',
    'TimePoint',
]


class TimeUnit(Enum):
    S = auto()
    MS = auto()


def now(unit: TimeUnit = TimeUnit.S) -> int:
    """
    Get current timestamp.

    :param unit: TimeUnit (default: TimeUnit.S)
    :return: current timestamp
    """
    if unit not in TimeUnit:
        raise TypeError('arguments "unit" must be enum value of TimeUnit')

    if unit == TimeUnit.S:
        return int(time.time())
    if unit == TimeUnit.MS:
        return int(time.time() * 1000)


def now_str(fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Get formatted datetime string of current timestamp.

    :param fmt: format of datetime (default '%Y-%m-%d %H:%M:%S')
    :return: formatted datetime string
    """
    return datetime.datetime.now().strftime(fmt)


def datetime_to_timestamp(dt: str, fmt: str = '%Y-%m-%d %H:%M:%S') -> int:
    """
    Convert formatted datetime string to timestamp(unit: s).

    :param dt: datetime string
    :param fmt: format of datetime (default: '%Y-%m-%d %H:%M:%S')
    :return: timestamp(unit: s)
    """
    time_array = time.strptime(dt, fmt)
    return int(time.mktime(time_array))


def timestamp_to_datetime(ts: int, fmt: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    Convert timestamp(unit: s) to formatted datetime string.

    :param ts: timestamp(unit: s)
    :param fmt: format of datetime
    :return: formatted datetime string
    """
    time_local = time.localtime(ts)
    return time.strftime(fmt, time_local)


class TimePoint:
    C_DEFAULT_TIMESTAMP = -1

    def __init__(self, ts_ms: int = C_DEFAULT_TIMESTAMP):
        self._ts_ms = ts_ms
        if ts_ms < 0:
            self.set_timestamp_to_now()

    def get_timestamp(self, unit: TimeUnit = TimeUnit.MS) -> int:
        """
        Get self timestamp.

        :param unit: TimeUnit (default: TimeUnit.MS)
        :return: self timestamp
        """
        if unit not in TimeUnit:
            raise TypeError('arguments "unit" must be enum value of TimeUnit')

        if unit == TimeUnit.MS:
            return self._ts_ms
        if unit == TimeUnit.S:
            return self._ts_ms // 1000

        return TimePoint.C_DEFAULT_TIMESTAMP

    def set_timestamp(self, ts_ms: int) -> None:
        """
        Set self timestamp.

        :param ts_ms: timestamp(unit: ms)
        """
        if ts_ms < 0:
            raise Exception('arguments "ts_ms" cannot be negative')

        self._ts_ms = ts_ms

    def set_timestamp_to_now(self) -> None:
        """
        Set self timestamp to current timestamp.
        """
        self._ts_ms = now(unit=TimeUnit.MS)

    def clear_timestamp(self) -> None:
        """
        Clear self timestamp to default value.
        """
        self._ts_ms = self.C_DEFAULT_TIMESTAMP

    def calc_elapsed(self, unit: TimeUnit = TimeUnit.MS) -> int:
        """
        Calculate elapsed time from self timestamp.

        :param unit: TimeUnit (default: TimeUnit.MS)
        :return: elapsed time
        """
        if unit not in TimeUnit:
            raise TypeError('arguments "unit" must be enum value of TimeUnit')

        if self._ts_ms == self.C_DEFAULT_TIMESTAMP:
            raise Exception('self "timestamp" is unset')

        return now(unit) - self.get_timestamp(unit)
