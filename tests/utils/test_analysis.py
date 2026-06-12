from datetime import date
from unittest.mock import MagicMock

import pandas as pd
import pytest

from app.utils.analysis import AggFunc, AggPeriod, aggregate_dataframe


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
def metadata_mock():
    mock = MagicMock()
    mock.idx_id = 0
    mock.idx_date = 1
    mock.idx_value = 2
    return mock


@pytest.fixture
def params_mock():
    mock = MagicMock()
    mock.agg_period = AggPeriod.daily
    mock.agg_func = AggFunc.sum
    mock.group_by_id = False
    return mock


# --- AggPeriod and AggFunc Enum tests ---
def test_agg_period_values():
    assert AggPeriod.daily.value == "daily"
    assert AggPeriod.weekly.value == "weekly"
    assert AggPeriod.monthly.value == "monthly"


def test_agg_func_values():
    assert AggFunc.sum.value == "sum"
    assert AggFunc.avg.value == "avg"
    assert AggFunc.median.value == "median"


# --- daily aggregation tests ---
def test_aggregate_daily_sum(sample_dataframe, metadata_mock, params_mock):
    params_mock.agg_period = AggPeriod.daily
    params_mock.agg_func = AggFunc.sum
    params_mock.group_by_id = False

    result = aggregate_dataframe(sample_dataframe, metadata_mock, params_mock)

    assert "period" in result.columns
    assert "VALUE" in result.columns
    assert len(result) == 4
    assert result[result["period"] == date(2025, 1, 1)]["VALUE"].values[0] == 40.0


def test_aggregate_daily_avg(sample_dataframe, metadata_mock, params_mock):
    params_mock.agg_period = AggPeriod.daily
    params_mock.agg_func = AggFunc.avg
    params_mock.group_by_id = False

    result = aggregate_dataframe(sample_dataframe, metadata_mock, params_mock)

    assert result[result["period"] == date(2025, 1, 1)]["VALUE"].values[0] == 20.0


def test_aggregate_daily_median(sample_dataframe, metadata_mock, params_mock):
    params_mock.agg_period = AggPeriod.daily
    params_mock.agg_func = AggFunc.median
    params_mock.group_by_id = False

    result = aggregate_dataframe(sample_dataframe, metadata_mock, params_mock)

    assert result[result["period"] == date(2025, 1, 1)]["VALUE"].values[0] == 20.0


# --- weekly aggregation tests ---
def test_aggregate_weekly_sum(sample_dataframe, metadata_mock, params_mock):
    params_mock.agg_period = AggPeriod.weekly
    params_mock.agg_func = AggFunc.sum
    params_mock.group_by_id = False

    result = aggregate_dataframe(sample_dataframe, metadata_mock, params_mock)

    assert "period" in result.columns


def test_aggregate_weekly_avg(sample_dataframe, metadata_mock, params_mock):
    params_mock.agg_period = AggPeriod.weekly
    params_mock.agg_func = AggFunc.avg
    params_mock.group_by_id = False

    result = aggregate_dataframe(sample_dataframe, metadata_mock, params_mock)

    assert len(result) > 0
    assert "VALUE" in result.columns


# --- monthly aggregation tests ---
def test_aggregate_monthly_sum(sample_dataframe, metadata_mock, params_mock):
    params_mock.agg_period = AggPeriod.monthly
    params_mock.agg_func = AggFunc.sum
    params_mock.group_by_id = False

    result = aggregate_dataframe(sample_dataframe, metadata_mock, params_mock)

    assert "period" in result.columns
    assert len(result) == 2
    assert result[result["period"] == "2025-01"]["VALUE"].values[0] == 100.0
    assert result[result["period"] == "2025-02"]["VALUE"].values[0] == 50.0


def test_aggregate_monthly_avg(sample_dataframe, metadata_mock, params_mock):
    params_mock.agg_period = AggPeriod.monthly
    params_mock.agg_func = AggFunc.avg
    params_mock.group_by_id = False

    result = aggregate_dataframe(sample_dataframe, metadata_mock, params_mock)

    assert result[result["period"] == "2025-01"]["VALUE"].values[0] == 25.0


def test_aggregate_monthly_median(sample_dataframe, metadata_mock, params_mock):
    params_mock.agg_period = AggPeriod.monthly
    params_mock.agg_func = AggFunc.median
    params_mock.group_by_id = False

    result = aggregate_dataframe(sample_dataframe, metadata_mock, params_mock)

    assert result[result["period"] == "2025-01"]["VALUE"].values[0] == 25.0


# --- group by id tests ---
def test_aggregate_daily_sum_grouped_by_id(
    sample_dataframe, metadata_mock, params_mock
):
    params_mock.agg_period = AggPeriod.daily
    params_mock.agg_func = AggFunc.sum
    params_mock.group_by_id = True

    result = aggregate_dataframe(sample_dataframe, metadata_mock, params_mock)

    assert "period" in result.columns
    assert "ID" in result.columns
    assert "VALUE" in result.columns
    assert len(result) == 5


def test_aggregate_monthly_sum_grouped_by_id(
    sample_dataframe, metadata_mock, params_mock
):
    params_mock.agg_period = AggPeriod.monthly
    params_mock.agg_func = AggFunc.sum
    params_mock.group_by_id = True

    result = aggregate_dataframe(sample_dataframe, metadata_mock, params_mock)

    # ID 1 in Jan: 10 + 20 = 30
    # ID 2 in Jan: 30 + 40 = 70
    # ID 3 in Feb: 50
    assert len(result) == 3
    jan_id1 = result[(result["period"] == "2025-01") & (result["ID"] == 1)]
    assert jan_id1["VALUE"].values[0] == 30.0
    jan_id2 = result[(result["period"] == "2025-01") & (result["ID"] == 2)]
    assert jan_id2["VALUE"].values[0] == 70.0


def test_aggregate_weekly_avg_grouped_by_id(
    sample_dataframe, metadata_mock, params_mock
):
    params_mock.agg_period = AggPeriod.weekly
    params_mock.agg_func = AggFunc.avg
    params_mock.group_by_id = True

    result = aggregate_dataframe(sample_dataframe, metadata_mock, params_mock)

    assert "period" in result.columns
    assert "ID" in result.columns
    assert len(result) > 0
