from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_ENV_PATH = '.env'


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=DEFAULT_ENV_PATH,
        env_file_encoding='utf-8',
        extra='allow',
    )

    APP_HOST: str = '127.0.0.1'
    APP_PORT: int = 8080

    DB_HOST: str = '127.0.0.1'
    DB_PORT: int = 5432
    DB_BASENAME: str = ''
    DB_USERNAME: str = ''
    DB_PASSWORD: str = ''
    DB_PROTOCOL: str = 'postgresql+asyncpg'

    @property
    def dsn(self) -> str:
        return f"{self.DB_PROTOCOL}://{self.DB_USERNAME}:{self.DB_PASSWORD}@" \
               f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_BASENAME}"


settings = Settings()
