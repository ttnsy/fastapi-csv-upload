import pyarrow as pa
import pytest
from fastapi import HTTPException

from app.utils.detectors import (
    DATE_KEYS,
    ID_KEY,
    VALUE_KEY,
    get_idx_date,
    get_idx_id,
    get_idx_value,
    has_header_pacsv,
)


# --- check if csv has header ---
def test_has_header_true():
    table = pa.table({"user_id": [1, 2], "value": [3, 4]})
    assert has_header_pacsv(table) is True


def test_has_header_false_numeric_column_names():
    table = pa.table({"1": [1, 2], "2": [3, 4]})
    assert has_header_pacsv(table) is False


# --- get_idx_id tests ---
@pytest.mark.parametrize("key", [ID_KEY])
@pytest.mark.parametrize(
    "name_func",
    [
        lambda k: k,
        lambda k: f"{k}_col",
        lambda k: f"col_{k}",
        lambda k: f"col.{k}",
        lambda k: f"record{k}",
        lambda k: f"{k}record",
        lambda k: k.upper(),
    ],
)
def test_get_idx_id_name_based_detects_key(key, name_func):
    colname = name_func(key)
    table = pa.table({colname: [1, 2], "value": [3, 4]})
    assert get_idx_id(table) == 0


def test_get_idx_id_unique_integer():
    table = pa.table({"col1": [1, 2, 3], "col2": [10.0, 20.0, 30.0]})
    assert get_idx_id(table) == 0


def test_get_idx_id_unique_integer_ambiguous():
    table = pa.table({"col1": [1, 2, 3], "col2": [10, 20, 30]})
    with pytest.raises(HTTPException):
        get_idx_id(table)


def test_get_idx_id_unique_string():
    table = pa.table({"col1": ["A", "B", "C"], "col2": [1.1, 2.2, 3.3]})
    assert get_idx_id(table) == 0


def test_get_idx_id_not_found():
    table = pa.table({"a": [1, 1, 1], "b": ["x", "x", "x"]})
    assert get_idx_id(table) is None


# -- get_idx_value tests ---
@pytest.mark.parametrize("key", [VALUE_KEY])
@pytest.mark.parametrize(
    "name_func",
    [
        lambda k: k,
        lambda k: f"{k}_col",
        lambda k: f"col_{k}",
        lambda k: f"col.{k}",
        lambda k: f"record{k}",
        lambda k: f"{k}record",
        lambda k: k.upper(),
    ],
)
def test_get_idx_value_name_based_detects_key(key, name_func):
    colname = name_func(key)
    table = pa.table({"id": [1, 2], colname: [3, 4]})
    assert get_idx_value(table) == 1


def test_get_idx_value_name_ignore_id():
    table = pa.table({"id": [1, 2], "value": [3, 4]})
    assert get_idx_value(table, id_idx=0) == 1


def test_get_idx_value_numeric_fallback_float():
    table = pa.table({"id": [1, 2, 3], "amount": [30.1, 20.5, 30.5]})
    assert get_idx_value(table, id_idx=0) == 1


def test_get_idx_value_multiple_candidates_raises():
    table = pa.table({"id": [1, 2, 3], "a": [10, 20, 30], "b": [100.0, 200.0, 300.0]})

    with pytest.raises(HTTPException):
        get_idx_value(table)


# --- get_idx_date tests ---
@pytest.mark.parametrize("key", DATE_KEYS)
@pytest.mark.parametrize(
    "name_func",
    [
        lambda k: k,
        lambda k: f"{k}_col",
        lambda k: f"col_{k}",
        lambda k: f"col.{k}",
        lambda k: f"record{k}",
        lambda k: f"{k}record",
        lambda k: f"{k}Stamp",
    ],
)
def test_get_idx_date_name_based_detects_keys(key, name_func):
    colname = name_func(key)
    table = pa.table({"id": [1, 2], colname: ["2024-01-01", "2024-01-02"]})
    assert get_idx_date(table) == 1


def test_get_idx_date_parse_based_mixed_formats():
    table = pa.table(
        {
            "id": [1, 2, 3],
            "event_dttm": ["2024-01-01", "01/02/2024", "2024-03-04T12:30:00Z"],
        }
    )
    assert get_idx_date(table) == 1


def test_get_idx_date_multiple_candidates_raises():
    table = pa.table(
        {
            "id": [1, 2],
            "d1": ["2024-01-01", "2024-01-02"],
            "d2": ["2023-01-01", "2023-01-02"],
        }
    )
    with pytest.raises(HTTPException):
        get_idx_date(table)
