from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class CSVMetadata(SQLModel, table=True):
    name_stored: str = Field(index=True, primary_key=True)
    name_original: str
    size_bytes: int
    nrows: int
    ncols: int
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
