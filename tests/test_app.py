import io
import os

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_csv_path():
    return "tests/sample.csv"


def test_upload_csv_file(client, sample_csv_path):
    with open(sample_csv_path, "rb") as f:
        response = client.post(
            "/upload-csv/", files={"file": ("sample.csv", f, "text/csv")}
        )
    assert response.status_code == 200
    data = response.json()
    assert "path" in data
    saved_path = data["path"]
    assert os.path.exists(saved_path)
    os.remove(saved_path)


def test_upload_rejects_non_csv(client):
    fake_file = io.BytesIO(b"some content")
    response = client.post(
        "/upload-csv/", files={"file": ("not_a_csv.txt", fake_file, "text/plain")}
    )
    assert response.status_code == 400
