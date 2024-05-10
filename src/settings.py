from secrets import token_urlsafe
from typing import Optional

from pydantic import Field, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class PostgresSettings(BaseSettings):
    host: str
    db: str
    password: str
    port: str
    user: str

    model_config = SettingsConfigDict(env_file_encoding="utf-8", env_prefix='postgres_')

    def build_dsn(self) -> str:
        return (
            "postgresql+psycopg://"
            f"{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.db}"
        )


class WebhooksSettings(BaseSettings):
    base: Optional[str]
    path: Optional[str]
    host: Optional[str]
    port: Optional[int]
    secret: Optional[str] = Field(default_factory=token_urlsafe)

    model_config = SettingsConfigDict(env_file_encoding="utf-8", env_prefix='webhook_')

    def build_url(self):
        return f'{self.base}{self.path}'


class LoggerSettings(BaseSettings):
    channel_id: int
    bot_token: str
    level: int

    model_config = SettingsConfigDict(env_file_encoding="utf-8", env_prefix='logging_')

    def build_url(self):
        return f'https://api.telegram.org/bot{self.bot_token}/sendMessage'


class Settings(BaseSettings):
    bot_token: str
    bot_url: str

    uri_prefix: str

    postgres: PostgresSettings = PostgresSettings()

    use_webhooks: bool = Field(default=False)
    webhooks: WebhooksSettings = WebhooksSettings()

    logger: LoggerSettings = LoggerSettings()

    model_config = SettingsConfigDict(env_file_encoding="utf-8")


settings = Settings()
print(settings.postgres.build_dsn())