from aiogram import Bot, Dispatcher
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env-non-dev')

    TOKEN: str

    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: str


settings = Settings()

DATABASE_URL = f'postgresql+asyncpg://{settings.DB_USER}:' \
               f'{settings.DB_PASS}@{settings.DB_HOST}:' \
               f'{settings.DB_PORT}/{settings.DB_NAME}'

REDIS_URL = f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/0'

bot = Bot(settings.TOKEN, parse_mode='HTML')
dp = Dispatcher()

