from pydantic import BaseModel

from app.resources.datasets.analyses.service import AggFunc, AggPeriod


class AnalysisParams(BaseModel):
    agg_period: AggPeriod
    agg_func: AggFunc
    group_by_id: bool = False
