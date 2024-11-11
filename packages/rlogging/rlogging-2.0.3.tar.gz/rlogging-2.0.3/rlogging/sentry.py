import sentry_sdk
from pydantic_settings import BaseSettings, SettingsConfigDict

from rlogging.settings import ENV_FILE, AppBaseSettings


class SentrySettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix='SENTRY_',
        extra='ignore',
    )

    DSN: str | None = None

    SAMPLE_RATE: float = 1.0
    TRACES_SAMPLE_RATE: float = 0
    PROFILES_SAMPLE_RATE: float = 0


def init():
    APP_SETTINGS = AppBaseSettings()
    SENTRY_SETTINGS = SentrySettings()

    sentry_sdk.init(
        dsn=SENTRY_SETTINGS.DSN,
        #
        release=f'{APP_SETTINGS.NAME}@{APP_SETTINGS.VERSION}',
        environment=APP_SETTINGS.ENVIRONMENT,
        #
        sample_rate=SENTRY_SETTINGS.SAMPLE_RATE,
        traces_sample_rate=SENTRY_SETTINGS.TRACES_SAMPLE_RATE,
        profiles_sample_rate=SENTRY_SETTINGS.PROFILES_SAMPLE_RATE,
    )
