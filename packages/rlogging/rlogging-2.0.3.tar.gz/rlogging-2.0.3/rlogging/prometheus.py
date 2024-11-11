import logging

from prometheus_client import Info

from rlogging import settings

__all__ = (
    'prometheus_info',
    'DEFAULT_BUCKETS',
)

logger = logging.getLogger('rlogging')

INF = float('inf')

DEFAULT_BUCKETS = (
    0.005,
    0.01,
    0.025,
    0.05,
    0.075,
    0.1,
    0.25,
    0.5,
    0.75,
    1.0,
    2.5,
    5.0,
    7.5,
    12.5,
    15.0,
    17.5,
    20.0,
    25.0,
    30.0,
    35.0,
    40.0,
    45.0,
    50.0,
    INF,
)

prometheus_info = Info('service', 'Service info')
prometheus_info.info(settings.APP.get_service_info())
