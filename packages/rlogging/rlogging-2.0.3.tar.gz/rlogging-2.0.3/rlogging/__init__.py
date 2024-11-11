from importlib import metadata as _metadata

from rlogging.extension.adapters import HttpLoggerAdapter, RsLoggerAdapter  # noqa: F401

try:
    __version__ = _metadata.version('rlogging')

except _metadata.PackageNotFoundError:
    __version__ = '0.0.0'
