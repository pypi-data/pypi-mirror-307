import logging


class RFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return True
