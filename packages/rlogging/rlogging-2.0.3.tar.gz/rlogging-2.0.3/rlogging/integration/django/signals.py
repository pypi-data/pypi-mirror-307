import logging
from typing import Any

from django.core.signals import got_request_exception, request_finished, request_started, setting_changed
from django.db.models.signals import (
    class_prepared,
    m2m_changed,
    post_delete,
    post_init,
    post_migrate,
    post_save,
    pre_delete,
    pre_init,
    pre_migrate,
    pre_save,
)

from rlogging.extension import namespaces

logger = logging.getLogger(namespaces.DB)

SIGNALS = [
    request_started,
    request_finished,
    got_request_exception,
    setting_changed,
    class_prepared,
    pre_init,
    post_init,
    pre_save,
    post_save,
    pre_delete,
    post_delete,
    m2m_changed,
    pre_migrate,
    post_migrate,
]


def signal_handler(sender: Any, *args: Any, **kwargs: Any):
    logger.info(
        f'received django signal: {sender}',
        extra={
            'djang_signal': {
                'sender': sender,
                'args': args,
                'kwargs': kwargs,
            }
        },
    )


# Connect the handler to all signals
for signal in SIGNALS:
    signal.connect(signal_handler)
