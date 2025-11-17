from pydantic import BaseModel


class CSVMetadataCreate(BaseModel):
    name_stored: str
    name_original: str
    size_bytes: int
    nrows: int
    ncols: int
    idx_id: int | None
    idx_date: int | None
    idx_value: int | None
