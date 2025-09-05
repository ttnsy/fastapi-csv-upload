from sqlmodel import create_engine

from app.config import settings

connect_args = {"check_same_thread": False}
engine = create_engine(
    f"sqlite:///{settings.db_path}", echo=True, connect_args=connect_args
)
