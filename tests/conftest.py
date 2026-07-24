import logging
import os
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel

from app.config import settings
from app.database import engine
from app.dependencies import get_session, get_upload_dir
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def test_setup():
    assert settings.engine == "sqlite", (
        f"Tests must use SQLite, got engine: {settings.engine}"
    )
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)


# -------------------------------------------------------------
# DATABASE SETUP
# -------------------------------------------------------------


@pytest.fixture(scope="session")
def test_engine(tmp_path_factory):
    SQLModel.metadata.create_all(engine)
    yield engine
    engine.dispose()
    if os.path.exists("test.db"):
        os.remove("test.db")


@pytest.fixture
def session(test_engine):
    with Session(test_engine) as s:
        yield s


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
