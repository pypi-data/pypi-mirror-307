from pydantic_settings import BaseSettings, SettingsConfigDict

from rlogging.settings import ENV_FILE, AppBaseSettings

try:
    from storages.backends.s3boto3 import S3Boto3Storage

except ImportError as ex:
    raise ImportError(f'Import error "{ex}". Do "poetry add django-storages[s3]"') from ex

APP_SETTINGS = AppBaseSettings()


class StaticDjangoStorageSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix='ENV_S3_DJANGO_STATICFILES__',
        extra='ignore',
    )

    # TODO: Added dynamic default value
    ACCESS_KEY: str
    SECRET_KEY: str
    BUCKET_NAME: str

    LOCATION: str | None = None

    ENDPOINT_URL: str = 'https://storage.yandexcloud.net'
    DEFAULT_ACL: str = 'public-read'
    QUERYSTRING_AUTH: bool = False
    OBJECT_PARAMETERS: dict[str, str] = {'CacheControl': 'max-age=86400'}

    def get_location(self):
        if self.LOCATION is not None:
            return self.LOCATION

        return f'{APP_SETTINGS.ENVIRONMENT}/{APP_SETTINGS.NAME}/'


class MediaDjangoStorageSettings(StaticDjangoStorageSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_prefix='ENV_S3_DJANGO_MEDIA__',
        extra='ignore',
    )


STATIC_DJANGO_STORAGE_SETTINGS = StaticDjangoStorageSettings()
MEDIA_DJANGO_STORAGE_SETTINGS = MediaDjangoStorageSettings()


class StaticS3Storage(S3Boto3Storage):
    access_key = STATIC_DJANGO_STORAGE_SETTINGS.ACCESS_KEY
    secret_key = STATIC_DJANGO_STORAGE_SETTINGS.SECRET_KEY
    location = STATIC_DJANGO_STORAGE_SETTINGS.get_location()

    bucket_name = STATIC_DJANGO_STORAGE_SETTINGS.BUCKET_NAME
    endpoint_url = STATIC_DJANGO_STORAGE_SETTINGS.ENDPOINT_URL
    object_parameters = STATIC_DJANGO_STORAGE_SETTINGS.OBJECT_PARAMETERS
    default_acl = STATIC_DJANGO_STORAGE_SETTINGS.DEFAULT_ACL
    querystring_auth = STATIC_DJANGO_STORAGE_SETTINGS.QUERYSTRING_AUTH


class MediaS3Storage(S3Boto3Storage):
    access_key = MEDIA_DJANGO_STORAGE_SETTINGS.ACCESS_KEY
    secret_key = MEDIA_DJANGO_STORAGE_SETTINGS.SECRET_KEY
    location = MEDIA_DJANGO_STORAGE_SETTINGS.get_location()

    bucket_name = MEDIA_DJANGO_STORAGE_SETTINGS.BUCKET_NAME
    endpoint_url = MEDIA_DJANGO_STORAGE_SETTINGS.ENDPOINT_URL
    object_parameters = MEDIA_DJANGO_STORAGE_SETTINGS.OBJECT_PARAMETERS
    default_acl = MEDIA_DJANGO_STORAGE_SETTINGS.DEFAULT_ACL
    querystring_auth = MEDIA_DJANGO_STORAGE_SETTINGS.QUERYSTRING_AUTH
