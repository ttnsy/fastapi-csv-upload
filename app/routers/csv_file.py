import os
import uuid
from pathlib import Path

import pandas as pd
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from ..crud import create_metadata
from ..database import Session, get_session
from ..dependencies import get_upload_dir
from ..schemas import CSVMetadataCreate

router = APIRouter(
    prefix="/csv-file",
    tags=["CSV files"],
    dependencies=[Depends(get_upload_dir)],
    responses={404: {"description": "Not found"}},
)


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
        name_stored=Path(file_path).name,
        name_original=name_original,
        size_bytes=os.path.getsize(file_path),
        nrows=df.shape[0],
        ncols=df.shape[1],
    )


@router.post("/")
async def upload_csv(
    file: UploadFile = File(...),
    upload_dir: Path = Depends(get_upload_dir),
    session: Session = Depends(get_session),
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only accept .csv")

    file_path = await save_uploaded_csv(file, dir=upload_dir)

    try:
        csv_metadata = extract_csv_metadata(file_path, name_original=file.filename)
        metadata = create_metadata(session=session, csv_metadata=csv_metadata)
    except Exception as e:
        if os.path.exists(file_path):
            os.remove(file_path)
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    return {"message": "Success", "metadata": metadata}


@router.get("/{filename}")
async def download_csv(filename: str, upload_dir: Path = Depends(get_upload_dir)):
    file_path = upload_dir / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, filename=filename, media_type="text/csv")
