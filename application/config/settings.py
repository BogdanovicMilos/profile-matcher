from __future__ import annotations

from dotenv import load_dotenv
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv(Path(__file__).resolve().parents[2] / ".env")


class Settings(BaseSettings):
    app_name: str = "Profile Matcher API"
    api_url: str = ""
    postgres_user: str = ""
    postgres_password: str = ""
    postgres_host: str = ""
    postgres_database: str = ""
    postgres_port: str = ""
    ssl_enabled: bool = False
    env: str = ""
    allowed_origins: str = ""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
