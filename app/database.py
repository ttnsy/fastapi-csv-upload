from sqlalchemy import URL
from sqlmodel import create_engine

from app.config import settings

url = URL.create(
    drivername = "postgresql+psycopg",
    username = settings.postgres_user,
    password = settings.postgres_password,
    host = settings.postgres_host,
    port = settings.postgres_port,
    database = settings.postgres_db
)

engine = create_engine(url, echo=True)
