from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env-non-dev')

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    TOKEN: str


settings = Settings()

DATABASE_URL = f'postgresql+asyncpg://{settings.DB_USER}:' \
               f'{settings.DB_PASS}@{settings.DB_HOST}:' \
               f'{settings.DB_PORT}/{settings.DB_NAME}'
