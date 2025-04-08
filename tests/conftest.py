import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_upload_dir
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def temp_upload_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        app.dependency_overrides[get_upload_dir] = lambda: Path(tmpdir)
        yield Path(tmpdir)
        app.dependency_overrides.clear()


@pytest.fixture
def upload_csv_path(client):
    with open("tests/sample.csv", "rb") as f:
        response = client.post(
            "/csv-file/", files={"file": ("sample.csv", f, "text/csv")}
        )
    assert response.status_code == 200
    return Path(response.json()["path"])
