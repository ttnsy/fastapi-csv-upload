import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel

from app.dependencies import get_upload_dir
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def create_test_tables(engine):
    SQLModel.metadata.create_all(engine)


@pytest.fixture
def temp_upload_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        app.dependency_overrides[get_upload_dir] = lambda: Path(tmpdir)
        yield Path(tmpdir)
        app.dependency_overrides.clear()


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_csv_path() -> Path:
    return Path("tests/sample.csv")
