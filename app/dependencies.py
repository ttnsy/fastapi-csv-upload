from pathlib import Path
from typing import Annotated, Generator

from fastapi import Depends, HTTPException
from sqlmodel import Session

from app.config import UPLOAD_DIR
from app.database import engine


def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def get_upload_dir() -> Path:
    if not UPLOAD_DIR.exists():
        raise RuntimeError(f"{UPLOAD_DIR} does not exist!")
    return UPLOAD_DIR


SessionDep = Annotated[Session, Depends(get_session)]
UploadDirDep = Annotated[Path, Depends(get_upload_dir)]


def get_parquet_path(stored_name: str, upload_dir: UploadDirDep) -> Path:
    parquet_path = (upload_dir / stored_name).with_suffix(".parquet")
    if not parquet_path.exists():
        raise HTTPException(status_code=404, detail="Data file not found")
    return parquet_path


ParquetPathDep = Annotated[Path, Depends(get_parquet_path)]
