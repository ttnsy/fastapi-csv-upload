import io
from pathlib import Path


def test_upload_csv_file(client, temp_upload_dir):
    with open("tests/sample.csv", "rb") as f:
        response = client.post(
            "/csv-file/", files={"file": ("sample.csv", f, "text/csv")}
        )
    assert response.status_code == 200
    saved_path = Path(response.json()["path"])
    assert saved_path.exists()
    assert saved_path.parent == temp_upload_dir


def test_upload_rejects_non_csv(client):
    fake_file = io.BytesIO(b"some content")
    response = client.post(
        "/csv-file/", files={"file": ("not_a_csv.txt", fake_file, "text/plain")}
    )
    assert response.status_code == 400


def test_download_uploaded_csv_file(client, temp_upload_dir):
    with open("tests/sample.csv", "rb") as f:
        response = client.post(
            "/csv-file/", files={"file": ("sample.csv", f, "text/csv")}
        )
    assert response.status_code == 200
    filename = Path(response.json()["path"]).name

    download_response = client.get(f"/csv-file/{filename}")
    assert download_response.status_code == 200
