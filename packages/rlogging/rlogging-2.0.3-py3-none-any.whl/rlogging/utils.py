import datetime
import traceback
import types
import uuid
from collections.abc import Callable
from typing import Any


class LazyStrCallable(object):
    def __init__(self, target_func: Callable[[Any], Any], *args: Any, **kwargs: Any) -> None:
        self.target = target_func
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return self.target(*self.args, **self.kwargs)

    def __str__(self) -> str:
        return str(self())


def custom_json_default(obj: Any) -> str:
    if isinstance(obj, str):
        return obj

    if isinstance(obj, datetime.date | datetime.time | datetime.datetime):
        return obj.isoformat()

    if isinstance(obj, uuid.UUID):
        return str(obj)

    if isinstance(obj, BaseException):
        return ''.join(traceback.format_exception(obj)).strip()

    if isinstance(obj, types.TracebackType):
        return ''.join(traceback.format_tb(obj)).strip()

    return str(obj)


def flatten_dict(dict_data: dict, parent_key: str = '', sep: str = '.'):
    items = []

    for k, v in dict_data.items():
        new_key = f'{parent_key}{sep}{k}' if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())

        else:
            items.append((new_key, v))

    return dict(items)
