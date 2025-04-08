import io


def test_upload_csv_file(upload_csv_path):
    assert upload_csv_path.exists()


def test_upload_rejects_non_csv(client):
    fake_file = io.BytesIO(b"some content")
    response = client.post(
        "/csv-file/", files={"file": ("not_a_csv.txt", fake_file, "text/plain")}
    )
    assert response.status_code == 400


def test_download_uploaded_csv_file(upload_csv_path, client):
    filename = upload_csv_path.name

    download_response = client.get(f"/csv-file/{filename}")
    assert download_response.status_code == 200
