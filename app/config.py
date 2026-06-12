from pathlib import Path

from pydantic_settings import BaseSettings

UPLOAD_DIR = Path("data")


class Settings(BaseSettings):
    database_url: str


settings = Settings()
