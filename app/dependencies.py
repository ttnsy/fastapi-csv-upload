from pathlib import Path
from typing import Annotated, Generator

from fastapi import Depends
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
