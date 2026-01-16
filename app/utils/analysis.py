from enum import Enum

import pandas as pd


class AggPeriod(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"


class AggFunc(str, Enum):
    sum = "sum"
    avg = "avg"
    median = "median"


def aggregate_dataframe(df: pd.DataFrame, metadata, params) -> pd.DataFrame:
    date_col = df.columns[metadata.idx_date]
    value_col = df.columns[metadata.idx_value]
    id_col = df.columns[metadata.idx_id] if params.group_by_id else None

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
