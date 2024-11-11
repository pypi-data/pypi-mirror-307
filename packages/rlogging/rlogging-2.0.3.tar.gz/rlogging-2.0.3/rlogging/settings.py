from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict

ENV_FILE = Path.cwd() / '.env'


class AppBaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix='APP_',
        extra='ignore',
    )

    DEBUG: bool = True
    DEVELOP: bool = True

    NAME: str = 'rlogging:stub'
    VERSION: str = '0.1.0'
    ENVIRONMENT: str = 'dev'

    LOGGING_TEXT_FORMAT: str = '%(levelname)-8s [%(name)s] %(message)s'

    LOGGING_MODULES: list[str] = ['app']
    LOGGING_LEVEL: str = 'DEBUG'
    LOGGING_DEPS_LEVEL: str = 'INFO'

    MODULE_PATH: str | None = None

    def get_service_info(self) -> dict[str, Any]:
        import rlogging

        return {
            'name': self.NAME,
            'version': self.VERSION,
            'environment': self.ENVIRONMENT,
            'rlogging': rlogging.__version__,
        }


APP = AppBaseSettings()
