import logging
from logging import config as logging_config


def test():
    LOGGING = {
        'version': 1,
        'formatters': {
            'text': {
                '()': 'rlogging.extension.formatters.RsFormatter',
            },
            'elk': {
                '()': 'rlogging.extension.formatters.ElkFormatter',
                'default_extra': {
                    'version': '0.1.0',
                },
            },
        },
        'handlers': {
            'main_handler': {
                'class': 'logging.StreamHandler',
                'formatter': 'elk',
                'stream': 'ext://sys.stdout',
            },
        },
        'loggers': {
            'test': {
                'handlers': ['main_handler'],
                'level': 'DEBUG',
                'propagate': False,
            },
        },
        'root': {
            'handlers': ['main_handler'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }

    logging_config.dictConfig(LOGGING)

    logger = logging.getLogger('test')

    logger.debug('debug message')
    logger.info('info message')
    logger.warning('warning message')
    logger.error('error message')
    logger.critical('critical message')

    try:
        raise Exception('exception message')
    except Exception as ex:
        logger.exception(ex)

    #

    logger.debug('debug message: %s', 'lorem')

    try:
        raise Exception('exception message: %s')
    except Exception as ex:
        logger.exception(ex, 'lorem')

    #

    logger.debug('debug message: %s | %s', 'lorem')

    try:
        raise Exception('exception message: %s | %s')
    except Exception as ex:
        logger.exception(ex, 'lorem')

    logger.debug(
        'debug message',
        extra={
            'key': 'value',
        },
    )
