from datetime import datetime

from pydantic import BaseModel

from app.utils.analysis import AggFunc, AggPeriod


class CSVMetadataCreate(BaseModel):
    name_stored: str
    name_original: str
    size_bytes: int
    nrows: int
    ncols: int
    idx_id: int | None
    idx_date: int | None
    idx_value: int | None
    uploaded_at: datetime | None = None


class AnalysisParams(BaseModel):
    agg_period: AggPeriod
    agg_func: AggFunc
    group_by_id: bool = False
