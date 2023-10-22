from enum import Enum

from pydantic import AnyHttpUrl
from pydantic_settings import BaseSettings


class Env(str, Enum):
    LOCAL = 'LOCAL'
    TESTING = 'TESTING'
    STAGING = 'STAGING'
    PRODUCTION = 'PRODUCTION'


class Settings(BaseSettings):
    PORT: int = 4000
    ALLOWED_ORIGINS: str = 'http://localhost http://localhost:3003'
    DEBUG: bool = True
    ENV: Env = Env.LOCAL

    DB_PORT: int = 5432
    DB_USER: str = 'g50'
    DB_PASS: str = '12345'
    DB_NAME: str = 'g50'
    DB_HOST: str = 'localhost'
    DB_DRIVER: str = 'postgresql+asyncpg'

    WEB_URL: AnyHttpUrl = 'https://example.com'

    @property
    def sqlalchemy_database_uri(self) -> str:
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


settings = Settings()
