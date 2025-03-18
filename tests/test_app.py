import io
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_upload_dir
from app.main import app


@pytest.fixture
def temp_upload_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        app.dependency_overrides[get_upload_dir] = lambda: Path(tmpdir)
        yield Path(tmpdir)
        app.dependency_overrides.clear()


@pytest.fixture
def client():
    return TestClient(app)


def test_upload_csv_file(client, temp_upload_dir):
    with open("tests/sample.csv", "rb") as f:
        response = client.post(
            "/upload-csv/", files={"file": ("sample.csv", f, "text/csv")}
        )
    assert response.status_code == 200
    saved_path = Path(response.json()["path"])
    assert saved_path.exists()
    assert saved_path.parent == temp_upload_dir


def test_upload_rejects_non_csv(client):
    fake_file = io.BytesIO(b"some content")
    response = client.post(
        "/upload-csv/", files={"file": ("not_a_csv.txt", fake_file, "text/plain")}
    )
    assert response.status_code == 400
