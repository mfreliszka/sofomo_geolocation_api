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
    # database_url: str = Field(
    #     default="postgresql://postgres:postgres@localhost:5432/GeolocationAPI",
    #     alias="DATABASE_URL",
    # )
    ipstack_timeout: int = Field(default=10, alias="IPSTACK_TIMEOUT")

    # database settings
    db_user: str = Field(default="postgres", alias="DB_USER")
    db_password: str = Field(default="postgres", alias="DB_PASSWORD")
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = Field(default=5432, alias="DB_PORT")
    db_name: str = Field(default="GeolocationAPI", alias="DB_NAME")

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()
print(settings.db_port)
print(settings.database_url)
