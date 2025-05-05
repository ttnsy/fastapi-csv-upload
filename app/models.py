from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class CSVMetadata(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name_stored: str = Field(index=True)
    name_original: str
    size_bytes: int
    nrows: int
    ncols: int
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
