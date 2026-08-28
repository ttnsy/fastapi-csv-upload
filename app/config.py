from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

UPLOAD_DIR = Path("data")


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore"
    )

    database_engine: Literal["sqlite", "postgres"] = Field(default="sqlite")
    database_host: str
    database_port: int
    database_user: str
    database_password: str
    database_db: str

    @property
    def database_url(self) -> str:
        if self.database_engine == "sqlite":
            return "sqlite:///:memory:"
        return (
            f"postgresql+psycopg://{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_db}"
        )


settings = DatabaseSettings()
