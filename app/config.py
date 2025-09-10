from pathlib import Path

from pydantic import field_validator
from pydantic_settings import BaseSettings

UPLOAD_DIR = Path("data")

# Used to catch missing DB_PATH.
# If this value is still set, it means DB_PATH wasn't configured.
DEFAULT_DB_PLACEHOLDER = "__MISSING_DB_PATH__"


class Settings(BaseSettings):
    db_path: str = DEFAULT_DB_PLACEHOLDER

    @field_validator("db_path", mode="before")
    @classmethod
    def validate_db_path(cls, value):
        if value == DEFAULT_DB_PLACEHOLDER:
            raise ValueError("You must set DB_PATH in your environment or .env file.")
        return value


settings = Settings()
