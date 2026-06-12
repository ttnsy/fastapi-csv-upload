from pathlib import Path

from pydantic_settings import BaseSettings

UPLOAD_DIR = Path("data")


class Settings(BaseSettings):
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_host: str = "db"
    postgres_port: int = 5432


settings = Settings()
