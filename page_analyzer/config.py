from functools import lru_cache

from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

ASYNC_SCHEME = "postgresql+asyncpg://"
PLAIN_SCHEMES = ("postgres://", "postgresql://")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str
    secret_key: SecretStr

    @field_validator("database_url", mode="before")
    @classmethod
    def use_async_driver(cls, value: str) -> str:
        for scheme in PLAIN_SCHEMES:
            if value.startswith(scheme):
                return ASYNC_SCHEME + value.removeprefix(scheme)
        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()
