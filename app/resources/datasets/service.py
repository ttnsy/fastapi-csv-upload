import io
import os
import uuid
from pathlib import Path

import pyarrow.csv as pacsv
import pyarrow.parquet as pq
from fastapi import HTTPException, UploadFile
from sqlmodel import Session

from app.api.annotations import SessionDep, UploadDirDep
from app.log_config import logger
from app.resources.datasets.crud import (
    get_all_datasets,
    get_metadata_by_name,
    save_metadata,
)
from app.resources.datasets.detectors import (
    get_idx_date,
    get_idx_id,
    get_idx_value,
    has_header_pacsv,
)
from app.resources.datasets.schema import CSVMetadataCreate


async def save_uploaded_csv(
    session: Session,
    file: UploadFile,
    dir: Path,
    stored_name: str | None = None,
) -> CSVMetadataCreate:
    name = stored_name or str(uuid.uuid4())
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
        name_original=Path(file.filename or "unknown").stem,
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


def get_dataset(stored_name: str, session: SessionDep, upload_dir: UploadDirDep):
    metadata = get_metadata_by_name(session, stored_name)
    if not metadata:
        raise HTTPException(404, "Dataset not found")
    path = (upload_dir / metadata.name_stored).with_suffix(".parquet")
    if not path.exists():
        logger.error(f"Metadata exists but file missing: {path}")
        raise HTTPException(500, "Dataset file is missing")
    return metadata, path


def get_datasets(session: SessionDep):
    metadata = get_all_datasets(session)
    if not metadata:
        raise HTTPException(404, "No datasets found")
    return metadata
