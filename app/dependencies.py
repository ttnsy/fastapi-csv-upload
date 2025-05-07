from sqlmodel import Session

from app.config import UPLOAD_DIR
from app.database import engine


def get_session():
    with Session(engine) as session:
        yield session


def get_upload_dir():
    if not UPLOAD_DIR.exists():
        raise RuntimeError(f"{UPLOAD_DIR} does not exist!")
    return UPLOAD_DIR
