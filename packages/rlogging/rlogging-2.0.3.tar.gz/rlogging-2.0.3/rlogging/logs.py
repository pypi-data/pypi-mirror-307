import logging
import sys
from typing import Any

from logging_prometheus import PrometheusHandler

from rlogging import settings
from rlogging.extension.formatters import ElkFormatter, RsFormatter


def logging_setup():
    default_extra = {
        'service': settings.APP.get_service_info(),
    }

    # Создание объектов форматирования
    text_formatter = RsFormatter(fmt=settings.APP.LOGGING_TEXT_FORMAT)
    elk_formatter = ElkFormatter(default_extra=default_extra)

    # Создание объектов обработчиков
    main_handler = logging.StreamHandler(stream=sys.stdout)
    main_handler.setFormatter(text_formatter if settings.APP.DEVELOP else elk_formatter)

    prometheus_handler = PrometheusHandler(labels=['name', 'levelname', 'module'])

    logging.basicConfig(
        level=settings.APP.LOGGING_DEPS_LEVEL,
        handlers=[main_handler, prometheus_handler],
        force=True,
    )

    # Создание объектов логгеров
    for logger_name in settings.APP.LOGGING_MODULES:
        _logger = logging.getLogger(logger_name)
        _logger.setLevel(settings.APP.LOGGING_LEVEL)
        _logger.addHandler(main_handler)
        _logger.addHandler(prometheus_handler)
        _logger.propagate = False


def generate_logging_dict() -> dict[str, Any]:
    default_extra = {
        'service': settings.APP.get_service_info(),
    }

    loggers_dict = {
        '': {
            'handlers': ['console', 'prometheus_logs'],
            'level': settings.APP.LOGGING_DEPS_LEVEL,
            'propagate': True,
        },
        'root': {
            'handlers': ['console', 'prometheus_logs'],
            'level': settings.APP.LOGGING_DEPS_LEVEL,
            'propagate': True,
        },
    }

    for logger_name in settings.APP.LOGGING_MODULES:
        loggers_dict[logger_name] = {
            'handlers': ['console', 'prometheus_logs'],
            'level': settings.APP.LOGGING_LEVEL,
            'propagate': False,
        }

    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'text': {
                '()': 'rlogging.extension.formatters.RsFormatter',
                'fmt': settings.APP.LOGGING_TEXT_FORMAT,
            },
            'json': {
                '()': 'rlogging.extension.formatters.ElkFormatter',
                'default_extra': default_extra,
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
                'formatter': 'text' if settings.APP.DEVELOP else 'json',
            },
            'prometheus_logs': {
                'class': 'logging_prometheus.PrometheusHandler',
                'labels': ['name', 'levelname', 'module'],
            },
        },
        'loggers': loggers_dict,
    }
