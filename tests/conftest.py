from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine

from app.dependencies import get_session, get_upload_dir
from app.main import app

# -------------------------------------------------------------
# DATABASE SETUP
# -------------------------------------------------------------

# Create a temporary SQLite database for testing
test_engine = create_engine(
    "sqlite:///./test.db", connect_args={"check_same_thread": False}
)


@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    SQLModel.metadata.create_all(test_engine)
    yield
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture
def session():
    with Session(test_engine) as session:
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
