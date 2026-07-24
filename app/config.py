from pathlib import Path
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

UPLOAD_DIR = Path("data")


class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="POSTGRES_", extra="ignore"
    )

    engine: Literal["sqlite", "postgres"] = Field(default="sqlite")
    host: str
    port: int
    user: str
    password: str
    db: str

    @property
    def database_url(self) -> str:
        if self.engine == "sqlite":
            return "sqlite:///:memory:"
        return (
            f"postgresql+psycopg://{self.user}:{self.password}"
            f"@{self.host}:{self.port}/{self.db}"
        )


settings = DatabaseSettings()
