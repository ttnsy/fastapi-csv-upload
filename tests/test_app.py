import io


def test_upload_csv_file(client, sample_csv_path, tmp_path):
    with sample_csv_path.open("rb") as f:
        response = client.post(
            "/csv-file/", files={"file": ("sample.csv", f, "text/csv")}
        )
    assert response.status_code == 200

    res = response.json()
    assert "metadata" in res
    metadata = res["metadata"]
    assert "name_stored" in metadata
    assert metadata["name_original"] == "sample"

    text = sample_csv_path.read_text().strip().splitlines()
    header = text[0]
    rows = text[1:]
    nrows = len(rows)
    ncols = len(header.split(","))

    assert metadata["nrows"] == nrows
    assert metadata["ncols"] == ncols

    assert (tmp_path / metadata["name_stored"]).with_suffix(".parquet").exists()


def test_upload_rejects_non_csv(client):
    fake_file = io.BytesIO(b"some content")
    response = client.post(
        "/csv-file/", files={"file": ("not_a_csv.txt", fake_file, "text/plain")}
    )
    assert response.status_code == 400


def test_download_uploaded_csv_file(client, sample_csv_path):
    with sample_csv_path.open("rb") as f:
        response = client.post(
            "/csv-file/", files={"file": ("sample.csv", f, "text/csv")}
        )
    assert response.status_code == 200
    metadata = response.json()["metadata"]
    filename = metadata["name_stored"]

    download_response = client.get(f"/csv-file/{filename}")
    assert download_response.status_code == 200
