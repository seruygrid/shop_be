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
    ALLOWED_ORIGINS: str = 'http://localhost http://localhost:3002'
    DEBUG: bool = True
    ENV: Env = Env.LOCAL
    LOG_LEVEL: str = 'INFO'

    DB_PORT: int = 5432
    DB_USER: str = 'g50'
    DB_PASS: str = '12345'
    DB_NAME: str = 'g50'
    DB_HOST: str = 'localhost'
    DB_DRIVER: str = 'postgresql+asyncpg'

    WEB_URL: AnyHttpUrl = 'https://example.com'

    AWS_DEFAULT_REGION: str = 'eu-west-1'
    COGNITO_POOL_ID: str = 'eu-west-1_eTaEzgpNJ'
    S3_BUCKET_NAME: str = 'harvest-images'
    COGNITO_CLIENT_ID: str = '3t5hbnb5fp41sao37prmgpo8pm'
    COGNITO_CLIENT_SECRET: str = 'v1eoabj26u4mbojq3qifuagp9is0uq6vsg056bu6ab9amas41cu'

    @property
    def sqlalchemy_database_uri(self) -> str:
        return f'{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}'


settings = Settings()
