from __future__ import annotations

import json

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = Field(alias="APP_NAME")
    api_host: str = Field(alias="API_HOST")
    api_port: int = Field(alias="API_PORT")

    postgres_db: str = Field(alias="POSTGRES_DB")
    postgres_user: str = Field(alias="POSTGRES_USER")
    postgres_password: str = Field(alias="POSTGRES_PASSWORD")
    postgres_host: str = Field(alias="POSTGRES_HOST")
    postgres_port: int = Field(alias="POSTGRES_PORT")
    secret: str = Field(alias="SECRET")
    version: str = Field(alias="VERSION")
    description: str = Field(alias="DESCRIPTION")
    mongo_uri: str = Field(default="mongodb://mongo:27017", alias="MONGO_URI")
    mongo_db: str = Field(default="opepic_sync", alias="MONGO_DB")
    cors_allowed_origins_raw: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000,null",
        alias="CORS_ALLOWED_ORIGINS",
    )
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    debug_mode: bool = Field(default=False, alias="DEBUG_MODE")

    def __init__(self) -> None:
        super().__init__()

    @property
    def cors_allowed_origins(self) -> list[str]:
        text = self.cors_allowed_origins_raw.strip()
        if not text:
            return []
        if text.startswith("["):
            parsed = json.loads(text)
            if not isinstance(parsed, list):
                raise ValueError("CORS_ALLOWED_ORIGINS must be a list of strings")
            return [str(item) for item in parsed]
        return [item.strip() for item in text.split(",") if item.strip()]

    @property
    def sqlalchemy_database_uri(self) -> str:
        return (
            "postgresql+psycopg2://"
            f"{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )


settings = Settings()
