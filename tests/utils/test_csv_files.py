import os
from io import BytesIO

import pyarrow.csv as pacsv
import pyarrow.parquet as pq
import pytest
from fastapi import HTTPException, UploadFile

from app import crud
from app.models import CSVMetadata
from app.schemas import CSVMetadataCreate
from app.utils.csv_files import create_and_save_metadata, save_uploaded_csv


def test_create_and_save_metadata_success(
    session, tmp_path, sample_csv_path, monkeypatch
):
    table = pacsv.read_csv(sample_csv_path)
    parquet_path = tmp_path / "stored.parquet"
    parquet_path.write_bytes(b"dummy")

    upload = UploadFile(filename="sample.csv", file=BytesIO(b""))
    monkeypatch.setattr(crud, "save_metadata", lambda *a, **k: None)
    metadata = create_and_save_metadata(session, upload, parquet_path, table)

    assert isinstance(metadata, CSVMetadataCreate)
    assert metadata.name_stored == "stored"
    assert metadata.name_original == "sample"
    assert metadata.nrows == table.shape[0]
    assert metadata.ncols == table.shape[1]
    assert metadata.size_bytes == os.path.getsize(parquet_path)
    assert metadata.idx_id == 0
    assert metadata.idx_date == 1
    assert metadata.idx_value == 2


def test_create_and_save_metadata_db_failure(
    session, tmp_path, sample_csv_path, monkeypatch
):
    table = pacsv.read_csv(sample_csv_path)

    parquet_path = tmp_path / "file123.parquet"
    parquet_path.write_bytes(b"dummy parquet data")

    upload = UploadFile(filename="sample.csv", file=BytesIO(b""))

    def _save_error(*a, **k):
        raise Exception("DB ERROR")

    monkeypatch.setattr("app.utils.csv_files.save_metadata", _save_error)

    with pytest.raises(HTTPException) as exc:
        create_and_save_metadata(session, upload, parquet_path, table)

    assert exc.value.status_code == 500
    assert not parquet_path.exists()


@pytest.mark.parametrize(
    "csv_content",
    [
        # Missing ID column
        """
        date,value
        2024-01-01,10
        """,
        # Missing DATE column
        """
        id,value
        1,10
        """,
        # Missing VALUE column
        """
        id,date
        1,2024-01-01
        """,
    ],
)
def test_create_and_save_metadata_missing_columns(session, tmp_path, csv_content):
    cleaned = "\n".join(line.strip() for line in csv_content.strip().splitlines())
    table = pacsv.read_csv(BytesIO(cleaned.encode()))

    parquet_path = tmp_path / "bad.parquet"
    parquet_path.write_bytes(b"dummy")

    upload = UploadFile(filename="bad.csv", file=BytesIO(b""))

    with pytest.raises(HTTPException) as exc:
        create_and_save_metadata(session, upload, parquet_path, table)

    assert exc.value.status_code == 400
    assert not parquet_path.exists()


@pytest.mark.asyncio
async def test_save_uploaded_csv_rejects_missing_header(session, tmp_path):
    content = b"1,2,3\n4,5,6\n"
    upload = UploadFile(filename="bad.csv", file=BytesIO(content))

    with pytest.raises(HTTPException) as err:
        await save_uploaded_csv(session, upload, dir=tmp_path)

    assert err.value.status_code == 400


@pytest.mark.asyncio
async def test_save_uploaded_csv_success(
    session, tmp_path, sample_csv_path, monkeypatch
):
    content = sample_csv_path.read_bytes()
    upload = UploadFile(filename="sample.csv", file=BytesIO(content))
    stored_name = "testfile"

    monkeypatch.setattr(crud, "save_metadata", lambda s, m: None)

    metadata = await save_uploaded_csv(
        session, upload, dir=tmp_path, stored_name=stored_name
    )
    assert (tmp_path / f"{stored_name}.parquet").exists()
    assert isinstance(metadata, CSVMetadataCreate)
    assert set(metadata.model_dump().keys()) == set(CSVMetadata.schema().keys())


@pytest.mark.asyncio
async def test_save_uploaded_csv_parquet_write_failure(
    session, tmp_path, sample_csv_path, monkeypatch
):
    upload = UploadFile(
        filename="sample.csv", file=BytesIO(sample_csv_path.read_bytes())
    )
    stored_name = "testfile"

    monkeypatch.setattr(
        pq,
        "write_table",
        lambda *a, **k: (_ for _ in ()).throw(Exception("write error")),
    )

    with pytest.raises(Exception):
        await save_uploaded_csv(session, upload, dir=tmp_path, stored_name=stored_name)
    assert not (tmp_path / f"{stored_name}.parquet").exists()
