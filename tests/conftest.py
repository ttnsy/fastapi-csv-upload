import logging
import os
from pathlib import Path

import alembic.config
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.database import engine
from app.dependencies import get_session, get_upload_dir
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def disable_logging():
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)


# -------------------------------------------------------------
# DATABASE SETUP
# -------------------------------------------------------------


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    alembic.config.main(argv=["--raiseerr", "upgrade", "head"])
    yield
    Path(os.getenv("DB_PATH")).unlink(missing_ok=True)


@pytest.fixture
def session():
    with Session(engine) as session:
        yield session


# -------------------------------------------------------------
# FASTAPI CLIENT SETUP WITH DEPENDENCY OVERRIDES
# -------------------------------------------------------------


@pytest.fixture
def client(session, tmp_path):
    def override_get_session():
        return session

    def override_get_upload_dir():
        return tmp_path

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_upload_dir] = override_get_upload_dir

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


# -------------------------------------------------------------
# SAMPLE CSV
# -------------------------------------------------------------


@pytest.fixture
def sample_csv_path() -> Path:
    return Path("tests/sample.csv")
