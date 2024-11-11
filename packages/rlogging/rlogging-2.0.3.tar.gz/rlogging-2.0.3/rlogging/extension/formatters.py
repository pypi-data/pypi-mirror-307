import json
import logging
from typing import Any

from rlogging import utils


class RsFormatter(logging.Formatter):
    """Кастомный форматер модуля."""


class JsonFormatter(RsFormatter):
    """Форматер в json."""

    DEFAULT_EXCLUDE_FIELDS = {
        'msecs',
        'relativeCreated',
        'filename',
        'exc_info',
        'stack_info',
        'exc_text',
        'thread',
        'msg',
    }

    def __init__(
        self,
        include_fields: set[str] | None = None,
        exclude_fields: set[str] | None = None,
        default_extra: dict[str, Any] | None = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args)

        self.include_fields = set(include_fields) if include_fields is not None else None
        self.exclude_fields = set(exclude_fields) if exclude_fields is not None else None
        self.default_extra = default_extra if default_extra is not None else {}

        if self.include_fields is None and self.exclude_fields is None:
            self.exclude_fields = self.DEFAULT_EXCLUDE_FIELDS

        assert not (self.include_fields and self.exclude_fields), 'Only one of include_fields/exclude_fields'

        self.json_serializer = kwargs.pop('json_serializer', json.dumps)
        self.json_default = kwargs.pop('json_default', None)
        self.json_cls = kwargs.pop('json_cls', None)

        if self.json_default is None:
            self.json_default = utils.custom_json_default

    def get_data_from_record(self, record: logging.LogRecord) -> dict:
        try:
            record.message = record.msg % record.args

        except BaseException:
            record.message = record.msg

        if isinstance(record.msg, BaseException):
            record.exception = record.msg
            record.message = str(record.msg)

        record_data = {}
        record_data.update(self.default_extra)
        record_data.update(record.__dict__)

        if self.exclude_fields:
            return {k: v for k, v in record_data.items() if k not in self.exclude_fields}

        if self.include_fields:
            return {k: v for k, v in record_data.items() if k in self.include_fields}

        return record_data

    def format(self, record: logging.LogRecord):
        record_data = self.get_data_from_record(record)
        return self.json_serializer(record_data, default=self.json_default, cls=self.json_cls)


class ElkFormatter(JsonFormatter):
    def get_data_from_record(self, record: logging.LogRecord) -> dict:
        return utils.flatten_dict(super().get_data_from_record(record))
