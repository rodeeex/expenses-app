from pydantic_settings import BaseSettings, SettingsConfigDict


# TODO: move KEY_DEFAULT to env file and rename
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    DB_ECHO: bool = False
    KEY_DEFAULT: str = "ya-samy-krutoy-razrabotchik"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    @property
    def DATABASE_URL_SYNC(self) -> str:
        return self.DATABASE_URL.replace("+aiosqlite", "")


settings = Settings()
