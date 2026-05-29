from datetime import datetime
from enum import Enum

from pydantic import BaseModel


class AggPeriod(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"


class AggFunc(str, Enum):
    sum = "sum"
    avg = "avg"
    median = "median"


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
