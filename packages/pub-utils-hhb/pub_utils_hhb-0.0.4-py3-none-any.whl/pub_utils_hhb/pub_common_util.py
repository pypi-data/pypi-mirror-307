import json
import os.path
import sys
import time

from typing import Callable, TypeVar
from functools import wraps

from pub_utils_hhb.pub_time_util import TimeUnit, now

__all__ = [
    'pprint',
    'print_obj',
    'is_debugging',
    'accurate_sleep',
    'get_root_dir',
    'get_sub_dir',
    'singleton',
]

T = TypeVar('T')


def singleton(cls: T) -> Callable[..., T]:
    instances = {}

    @wraps(cls)
    def _singleton(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)

        return instances[cls]

    return _singleton


def pprint(*val, **kwargs) -> None:
    """
    Pretty print.
    """
    for v in val:
        try:
            if isinstance(v, dict):
                v = json.dumps(v, indent=2, ensure_ascii=False)
            if isinstance(v, str):
                v = json.loads(v).dumps(v, indent=2, ensure_ascii=False)
        except Exception:
            pass

        print(v, **kwargs, end=' ')

    print()


def print_obj(obj: object) -> None:
    for attr, value in vars(obj).items():
        print(f'attr: {attr}; type: {type(value)}; value: {value}')


def is_debugging() -> bool:
    return os.path.realpath(sys.argv[0]).endswith('py')


def accurate_sleep(s: float = 0, ms: int = 0) -> None:
    """
    Accurately sleep for seconds and milliseconds.

    :param s: second for sleep
    :param ms: millisecond for sleep
    :return: None
    """
    if s < 0 or ms < 0:
        raise Exception('param s or ms must not less than zero')

    sleep_duration_ms = s * 1000 + ms
    sleep_end_ms = now(unit=TimeUnit.MS) + sleep_duration_ms

    # Function time.sleep() usually sleeps more for 10 ~ 100 ms.
    # Therefore, use time.sleep() for rough sleep but shorten by 1 second.
    # And then use while-loop for the rest sleep duration.

    sleep_duration_s = (sleep_duration_ms // 1000) - 1
    sleep_duration_s = max(sleep_duration_s, 0)

    time.sleep(sleep_duration_s)

    while now(unit=TimeUnit.MS) < sleep_end_ms:
        pass


def get_root_dir() -> str:
    running_file = os.path.realpath(sys.argv[0])
    if running_file.endswith('py'):
        return os.path.dirname(os.path.dirname(running_file))
    else:
        return os.path.dirname(running_file)


def get_sub_dir(sub_name) -> str:
    return os.path.join(get_root_dir(), sub_name)
