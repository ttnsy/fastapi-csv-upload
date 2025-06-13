from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

UPLOAD_DIR = Path("data")


class Settings(BaseSettings):
    db_path: str = "database.db"

    model_config = SettingsConfigDict(env_file=".env")  #' Optional


settings = Settings()
