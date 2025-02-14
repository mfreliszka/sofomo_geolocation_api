"""Module containing project configuration."""

from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApplicationEnvironment(str, Enum):
    """Enum representing all possible application environments."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"


class Settings(BaseSettings):
    """Project settings overritable by environment variables."""

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    environment: ApplicationEnvironment = ApplicationEnvironment.DEVELOPMENT
    application_url: str = "http://127.0.0.1:8000"

    ipstack_access_key: str = Field(
        default="db1d75027952e614f174dd222ffeb857", alias="IPSTACK_ACCESS_KEY"
    )
    ipstack_api_url: str = Field(
        default="http://api.ipstack.com/", alias="IPSTACK_API_URL"
    )
    database_url: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/GeolocationAPI",
        alias="DATABASE_URL",
    )
    ipstack_timeout: int = Field(default=10, alias="IPSTACK_TIMEOUT")


settings = Settings()
