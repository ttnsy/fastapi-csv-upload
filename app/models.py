from datetime import datetime, timezone

from sqlmodel import Field, SQLModel


class CSVMetadata(SQLModel, table=True):
    name_stored: str = Field(index=True, primary_key=True)
    name_original: str
    size_bytes: int
    nrows: int
    ncols: int
    idx_id: int
    idx_date: int
    idx_value: int
    uploaded_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def schema(cls) -> dict[str, type]:
        return {name: field.annotation for name, field in cls.model_fields.items()}
