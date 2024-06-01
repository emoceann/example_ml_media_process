import sys
from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class CommonSettings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PASSWORD: str
    POSTGRES_USER: str
    POSTGRES_PORT: int

    PATH_TO_ML_MODEL: str
    PATH_TO_LABELS: str

    TEMP_MEDIA_FOLDER: str


class Settings(CommonSettings):
    REDIS_DSN: str


class TestSettings(CommonSettings):
    model_config = SettingsConfigDict(env_prefix="TEST_")


@cache
def get_settings() -> CommonSettings:
    if "pytest" in sys.modules:
        return TestSettings()
    return Settings()
