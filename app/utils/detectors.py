import pandas as pd
import pyarrow as pa
from fastapi import HTTPException


def get_idx_id(table) -> int | None:
    cols = []

    for idx, field in enumerate(table.schema):
        col_type = field.type
        if not (pa.types.is_integer(col_type) or pa.types.is_string(col_type)):
            continue
        ser = table[idx].to_pandas()
        if ser.empty:
            continue
        if ser.is_unique:
            cols.append(idx)

    if len(cols) > 1:
        raise HTTPException(
            status_code=400,
            detail=f"CSV has multiple ID columns: "
            f"{[table.column_names[i] for i in cols]}",
        )

    if len(cols) == 1:
        return cols[0]

    return None


def get_idx_value(table, id_idx: int | None) -> int | None:
    cols = []
    for idx, field in enumerate(table.schema):
        if idx == id_idx:
            continue
        col_type = field.type
        if not (pa.types.is_integer(col_type) or pa.types.is_floating(col_type)):
            continue
        ser = table[idx].to_pandas()
        if ser.empty:
            continue
        cols.append(idx)

    if len(cols) > 1:
        raise HTTPException(
            status_code=400,
            detail=f"Multiple VALUE-like columns detected: "
            f"{[table.column_names[i] for i in cols]}",
        )
    if len(cols) == 1:
        return cols[0]
    return None


def get_idx_date(table) -> int | None:
    cols = []
    for idx, field in enumerate(table.schema):
        if pa.types.is_date(field.type) or pa.types.is_timestamp(field.type):
            cols.append(idx)
    if len(cols) > 1:
        raise HTTPException(
            status_code=400,
            detail=f"Multiple date columns detected: {[table.column_names[i] for i in cols]}",
        )
    if len(cols) == 1:
        return cols[0]

    for idx, name in enumerate(table.column_names):
        arr = table[name]
        if not pa.types.is_string(arr.type):
            continue
        ser = arr.to_pandas()
        parsed = pd.to_datetime(ser, format="mixed", errors="coerce")
        if parsed.notna().any():
            cols.append(idx)

    if len(cols) > 1:
        raise HTTPException(
            status_code=400,
            detail=f"Multiple date columns detected: {[table.column_names[i] for i in cols]}",
        )

    if len(cols) == 1:
        return cols[0]

    return None
