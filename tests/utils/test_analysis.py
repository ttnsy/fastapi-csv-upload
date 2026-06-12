from datetime import date
from types import SimpleNamespace

import pandas as pd
import pytest

from app.schemas import AggFunc, AggPeriod, AnalysisParams
from app.services.analysis import aggregate_dataframe


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame(
        {
            "ID": [1, 1, 2, 2, 3],
            "DATE": [
                "2025-01-01",
                "2025-01-08",
                "2025-01-01",
                "2025-01-15",
                "2025-02-01",
            ],
            "VALUE": [10.0, 20.0, 30.0, 40.0, 50.0],
        }
    )


@pytest.fixture
def metadata():
    return SimpleNamespace(idx_id=0, idx_date=1, idx_value=2)


def make_params(agg_period, agg_func, group_by_id=False):
    return AnalysisParams(
        agg_period=agg_period, agg_func=agg_func, group_by_id=group_by_id
    )


# --- non-grouped aggregation: value checks ---
@pytest.mark.parametrize(
    "agg_period, agg_func, period_key, expected_value",
    [
        (AggPeriod.daily, AggFunc.sum, date(2025, 1, 1), 40.0),
        (AggPeriod.daily, AggFunc.avg, date(2025, 1, 1), 20.0),
        (AggPeriod.daily, AggFunc.median, date(2025, 1, 1), 20.0),
        (AggPeriod.monthly, AggFunc.sum, "2025-01", 100.0),
        (AggPeriod.monthly, AggFunc.avg, "2025-01", 25.0),
        (AggPeriod.monthly, AggFunc.median, "2025-01", 25.0),
    ],
)
def test_aggregate_value(
    sample_dataframe, metadata, agg_period, agg_func, period_key, expected_value
):
    params = make_params(agg_period, agg_func)
    result = aggregate_dataframe(sample_dataframe, metadata, params)

    assert "period" in result.columns
    assert "VALUE" in result.columns
    assert result[result["period"] == period_key]["VALUE"].values[0] == expected_value


def test_aggregate_monthly_row_count(sample_dataframe, metadata):
    params = make_params(AggPeriod.monthly, AggFunc.sum)
    result = aggregate_dataframe(sample_dataframe, metadata, params)
    assert len(result) == 2


# --- weekly aggregation tests ---
@pytest.mark.parametrize("agg_func", [AggFunc.sum, AggFunc.avg])
def test_aggregate_weekly_runs(sample_dataframe, metadata, agg_func):
    params = make_params(AggPeriod.weekly, agg_func)
    result = aggregate_dataframe(sample_dataframe, metadata, params)

    assert "period" in result.columns
    assert "VALUE" in result.columns
    assert len(result) > 0


# --- group by id tests ---
def test_aggregate_daily_sum_grouped_by_id(sample_dataframe, metadata):
    params = make_params(AggPeriod.daily, AggFunc.sum, group_by_id=True)
    result = aggregate_dataframe(sample_dataframe, metadata, params)

    assert "period" in result.columns
    assert "ID" in result.columns
    assert "VALUE" in result.columns
    assert len(result) == 5


def test_aggregate_monthly_sum_grouped_by_id(sample_dataframe, metadata):
    params = make_params(AggPeriod.monthly, AggFunc.sum, group_by_id=True)
    result = aggregate_dataframe(sample_dataframe, metadata, params)

    # ID 1 in Jan: 10 + 20 = 30
    # ID 2 in Jan: 30 + 40 = 70
    # ID 3 in Feb: 50
    assert len(result) == 3
    jan_id1 = result[(result["period"] == "2025-01") & (result["ID"] == 1)]
    assert jan_id1["VALUE"].values[0] == 30.0
    jan_id2 = result[(result["period"] == "2025-01") & (result["ID"] == 2)]
    assert jan_id2["VALUE"].values[0] == 70.0


def test_aggregate_weekly_avg_grouped_by_id(sample_dataframe, metadata):
    params = make_params(AggPeriod.weekly, AggFunc.avg, group_by_id=True)
    result = aggregate_dataframe(sample_dataframe, metadata, params)

    assert "period" in result.columns
    assert "ID" in result.columns
    assert len(result) > 0