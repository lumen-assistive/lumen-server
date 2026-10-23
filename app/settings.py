"""Runtime configuration read from the environment."""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings.

    Values are read from environment variables, falling back to a local
    SQLite database so the app and its tests run without external
    services configured.
    """

    model_config = SettingsConfigDict(env_prefix="LUMEN_SERVER_")

    database_url: str = "sqlite:///./lumen_server.db"


settings = Settings()
