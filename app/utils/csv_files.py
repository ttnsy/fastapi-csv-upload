import io
import os
import uuid
from pathlib import Path

import pyarrow.csv as csv
import pyarrow.parquet as pq
from fastapi import HTTPException, UploadFile
from sqlmodel import Session

from app.crud import create_metadata
from app.log_config import logger
from app.schemas import CSVMetadataCreate


async def save_uploaded_csv(
    file: UploadFile, session: Session, dir: Path
) -> CSVMetadataCreate:
    name = str(uuid.uuid4())
    path = (dir / name).with_suffix(".parquet")

    content = await file.read()
    table = csv.read_csv(io.BytesIO(content))

    try:
        pq.write_table(table, path)
    except Exception as e:
        logger.error(f"Failed to write parquet file: {e}")
        raise

    metadata = CSVMetadataCreate(
        name_stored=path.stem,
        name_original=file.filename,
        size_bytes=os.path.getsize(path),
        nrows=table.shape[0],
        ncols=table.shape[1],
    )

    try:
        create_metadata(session=session, csv_metadata=metadata)
    except Exception:
        logger.exception(
            "Metadata insert failed, cleaning up parquet file",
            extra={"stored_path": str(path)},
        )
        path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail="Failed to save metadata")

    return metadata
