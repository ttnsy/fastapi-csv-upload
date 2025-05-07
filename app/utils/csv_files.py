import os
import uuid
from pathlib import Path

import pandas as pd
from fastapi import UploadFile

from app.schemas import CSVMetadataCreate


async def save_uploaded_csv(file: UploadFile, dir: Path):
    name = uuid.uuid4().hex
    path = dir / name

    content = await file.read()
    with open(path, "wb") as f:
        f.write(content)

    return str(path)


def extract_csv_metadata(file_path: str, name_original: str):
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        raise ValueError(f"Failed to read CSV: {e}")

    return CSVMetadataCreate(
        name_stored=Path(file_path).stem,
        name_original=name_original,
        size_bytes=os.path.getsize(file_path),
        nrows=df.shape[0],
        ncols=df.shape[1],
    )
