from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class CSVMetadata(SQLModel, table=True):
    name_stored: str = Field(index=True, primary_key=True)
    name_original: str
    size_bytes: int
    nrows: int
    ncols: int
    idx_id: int | None
    idx_date: int | None
    idx_value: int | None
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def field_names(cls) -> set[str]:
        return set(cls.model_fields.keys())
