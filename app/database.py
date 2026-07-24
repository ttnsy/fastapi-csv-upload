from sqlalchemy.pool import StaticPool
from sqlmodel import create_engine

from app.config import settings

if settings.engine == "sqlite":
    engine = create_engine(
        settings.database_url,
        echo=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
else:
    engine = create_engine(
        settings.database_url,
        echo=True,
    )
