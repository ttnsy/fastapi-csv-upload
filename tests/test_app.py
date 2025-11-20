import io
from pathlib import Path

from fastapi.testclient import TestClient


def test_upload_csv_file_success(
    client: TestClient, sample_csv_path: Path, tmp_path: Path
):
    with sample_csv_path.open("rb") as f:
        response = client.post(
            "/csv-file/",
            files={"file": ("sample.csv", f, "text/csv")},
        )
    assert response.status_code == 200
    assert "metadata" in response.json()


def test_upload_csv_file_rejects_non_csv(client: TestClient):
    fake_file = io.BytesIO(b"some content")
    response = client.post(
        "/csv-file/", files={"file": ("not_a_csv.txt", fake_file, "text/plain")}
    )
    assert response.status_code == 400


def test_download_uploaded_csv_success(client: TestClient, sample_csv_path: Path):
    with sample_csv_path.open("rb") as f:
        response = client.post(
            "/csv-file/", files={"file": ("sample.csv", f, "text/csv")}
        )
    assert response.status_code == 200

    metadata = response.json().get("metadata")
    assert metadata is not None

    download_response = client.get(f"/csv-file/{metadata.get('name_stored')}")
    assert download_response.status_code == 200
