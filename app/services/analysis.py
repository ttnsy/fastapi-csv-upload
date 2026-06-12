import pandas as pd

from app.models import CSVMetadata
from app.schemas import AggFunc, AggPeriod, AnalysisParams


def aggregate_dataframe(
    df: pd.DataFrame, metadata: CSVMetadata, params: AnalysisParams
) -> pd.DataFrame:
    if metadata.idx_date is None or metadata.idx_value is None:
        raise ValueError("metadata.idx_date and metadata.idx_value must be set")

    date_col = df.columns[metadata.idx_date]
    value_col = df.columns[metadata.idx_value]

    id_col = None
    if params.group_by_id:
        if metadata.idx_id is None:
            raise ValueError("metadata.idx_id must be set when group_by_id is True")
        id_col = df.columns[metadata.idx_id]

    df[date_col] = pd.to_datetime(df[date_col])

    if params.agg_period == AggPeriod.daily:
        df["period"] = df[date_col].dt.date
    elif params.agg_period == AggPeriod.weekly:
        df["period"] = df[date_col].dt.strftime("%Y-%W")
    elif params.agg_period == AggPeriod.monthly:
        df["period"] = df[date_col].dt.strftime("%Y-%m")

    group_cols = ["period"]
    if params.group_by_id and id_col is not None:
        group_cols.append(id_col)

    agg_func_map = {
        AggFunc.sum: "sum",
        AggFunc.avg: "mean",
        AggFunc.median: "median",
    }
    agg_func = agg_func_map[params.agg_func]

    result = df.groupby(group_cols)[value_col].agg(agg_func).reset_index()
    return result
