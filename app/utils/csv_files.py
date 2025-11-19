import io
import os
import uuid
from pathlib import Path

import pyarrow.csv as pacsv
import pyarrow.parquet as pq
from fastapi import HTTPException, UploadFile
from sqlmodel import Session

from app.crud import save_metadata
from app.log_config import logger
from app.schemas import CSVMetadataCreate
from app.utils.detectors import (
    get_idx_date,
    get_idx_id,
    get_idx_value,
    has_header_pacsv,
)


async def save_uploaded_csv(
    file: UploadFile, session: Session, dir: Path
) -> CSVMetadataCreate:
    name = str(uuid.uuid4())
    path = (dir / name).with_suffix(".parquet")

    content = await file.read()
    table = pacsv.read_csv(io.BytesIO(content))

    if not has_header_pacsv(table):
        raise HTTPException(400, "Missing header row")

    try:
        pq.write_table(table, path)
    except Exception as e:
        logger.error(f"Failed to write parquet file: {e}")
        raise

    metadata = create_and_save_metadata(session, file, path, table)
    return metadata


def create_and_save_metadata(
    session: Session, file: UploadFile, path: Path, table
) -> CSVMetadataCreate:
    idx_id = get_idx_id(table)
    idx_date = get_idx_date(table)
    idx_value = get_idx_value(table, idx_id)

    missing = []
    if idx_id is None:
        missing.append("ID")
    if idx_date is None:
        missing.append("DATE")
    if idx_value is None:
        missing.append("VALUE")

    if missing:
        path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=400,
            detail=f"Missing required column(s): {', '.join(missing)}",
        )

    metadata = CSVMetadataCreate(
        name_stored=path.stem,
        name_original=Path(file.filename).stem,
        size_bytes=os.path.getsize(path),
        nrows=table.shape[0],
        ncols=table.shape[1],
        idx_id=idx_id,
        idx_date=idx_date,
        idx_value=idx_value,
    )
    try:
        save_metadata(session, metadata)
    except Exception:
        logger.exception(
            "Metadata insert failed, cleaning up parquet file",
            extra={"stored_path": str(path)},
        )
        path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail="Failed to save metadata")
    return metadata
