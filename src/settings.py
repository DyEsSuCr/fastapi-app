import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AnyUrl, BeforeValidator
from typing import Literal, Annotated
from pydantic import computed_field
from pydantic_core import MultiHostUrl

from src.utils import parse_to_list


class Settings(BaseSettings):
    ENVIRONMENT: Literal['dev', 'prod', 'staging'] = 'dev'

    DB_PORT: int
    DB_HOST: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    DB_MOTOR: Literal['mysql+aiomysql', 'postgresql+asyncpg']

    REDIS_HOST: str
    REDIS_PORT: int
    JTI_EXPIRY_SECONDS: int = 3600

    APP_PORT: int
    APP_HOST: str
    APP_NAME: str
    APP_DESCRIPTION: str

    JWT_ALGORITHM: str
    JWT_SECRET_KEY: str
    REFRESH_TOKEN_EXPIRY_DAYS: int = 2
    ACCESS_TOKEN_EXPIRY_SECONDS: int = 3600

    ENABLE_RATE_LIMIT: bool = False

    TRUSTED_HOSTS: Annotated[list[str] | str, BeforeValidator(parse_to_list)] = Field(
        default_factory=list
    )

    CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_to_list)] = Field(
        default_factory=list
    )

    @computed_field
    @property
    def REDIS_URL(self) -> str:
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'

    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return str(
            MultiHostUrl.build(
                scheme=self.DB_MOTOR,
                username=self.DB_USER,
                password=self.DB_PASSWORD,
                host=self.DB_HOST,
                port=self.DB_PORT,
                path=self.DB_NAME,
            )
        )

    model_config = SettingsConfigDict(
        env_file=f'.env.{os.getenv("ENV", "dev")}',
        env_file_encoding='utf-8',
        extra='ignore',
    )


settings = Settings()
