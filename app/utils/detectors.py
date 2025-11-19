import re
from typing import List, Optional

import pandas as pd
import pyarrow as pa
from fastapi import HTTPException
from sqlalchemy import Table

ID_KEY = "id"
VALUE_KEY = "value"
DATE_KEYS = ["date", "day", "time", "timestamp", "datetime", "dttm"]


def _norm(name: str) -> List[str]:
    name = str(name).lower().strip()
    return re.split(r"[^a-z0-9]+", name)


def _find_by_name(
    table: Table,
    keys: List[str],
    *,
    exclude: Optional[int] = None,
) -> List[int]:
    cols: List[int] = []
    for idx, name in enumerate(table.column_names):
        if exclude is not None and idx == exclude:
            continue
        tokens = _norm(name)
        if any(k in tokens for k in keys):
            cols.append(idx)
    return cols


def _resolve(cols: List[int], table: Table, label: str) -> Optional[int]:
    if len(cols) > 1:
        raise HTTPException(
            status_code=400,
            detail=f"Multiple {label}-like columns: {[table.column_names[i] for i in cols]}",
        )
    if len(cols) == 1:
        return cols[0]
    return None


def has_header_pacsv(table) -> bool:
    for name in table.column_names:
        s = str(name)
        if any(c.isalpha() for c in s):
            return True
    return False


def get_idx_id(table: Table) -> Optional[int]:
    cols_n = _find_by_name(table, [ID_KEY])
    res = _resolve(cols_n, table, "ID")
    if res is not None:
        return res

    cols_t: List[int] = []
    for idx, field in enumerate(table.schema):
        t = field.type

        if pa.types.is_integer(t) or pa.types.is_string(t):
            ser = table[idx].to_pandas()

            if not ser.empty and ser.is_unique:
                cols_t.append(idx)

    return _resolve(cols_t, table, "ID")


def get_idx_value(table: Table, id_idx: Optional[int]) -> Optional[int]:
    cols_n = _find_by_name(table, [VALUE_KEY], exclude=id_idx)
    res = _resolve(cols_n, table, "VALUE")
    if res is not None:
        return res

    cols_t: List[int] = []
    for idx, field in enumerate(table.schema):
        if idx == id_idx:
            continue

        t = field.type
        if pa.types.is_integer(t) or pa.types.is_floating(t):
            ser = table[idx].to_pandas()

            if not ser.empty:
                cols_t.append(idx)

    return _resolve(cols_t, table, "VALUE")


def get_idx_date(table: Table) -> Optional[int]:
    cols_n = _find_by_name(table, DATE_KEYS)
    res = _resolve(cols_n, table, "DATE")
    if res is not None:
        return res

    cols_t: List[int] = [
        idx
        for idx, field in enumerate(table.schema)
        if pa.types.is_date(field.type) or pa.types.is_timestamp(field.type)
    ]
    res = _resolve(cols_t, table, "DATE")
    if res is not None:
        return res

    cols_p: List[int] = []
    for idx, name in enumerate(table.column_names):
        arr = table[name]

        if pa.types.is_string(arr.type):
            ser = arr.to_pandas()

            parsed = pd.to_datetime(ser, errors="coerce", format="mixed")
            if parsed.notna().any():
                cols_p.append(idx)

    return _resolve(cols_p, table, "DATE")
