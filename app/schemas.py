from datetime import datetime

from pydantic import BaseModel


class CSVMetadataCreate(BaseModel):
    name_stored: str
    name_original: str
    size_bytes: int
    nrows: int
    ncols: int
    idx_id: int
    idx_date: int
    idx_value: int
    uploaded_at: datetime | None = None
