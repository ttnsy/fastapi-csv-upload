import io

from fastapi.testclient import TestClient


def test_upload_dataset_file_success(uploaded_dataset):
    assert uploaded_dataset


def test_upload_dataset_file_rejects_non_csv(client: TestClient, upload_url):
    fake_file = io.BytesIO(b"some content")
    response = client.post(
        upload_url, files={"file": ("not_a_csv.txt", fake_file, "text/plain")}
    )
    assert response.status_code == 400


def test_download_uploaded_csv_success(
    client: TestClient, uploaded_dataset, download_url
):
    metadata = uploaded_dataset
    assert metadata is not None

    download_response = client.get(download_url)
    assert download_response.status_code == 200
