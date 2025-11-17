import os
import uuid
from io import BytesIO

import pyarrow.csv as pacsv
import pytest
from fastapi import UploadFile

from app import crud
from app.schemas import CSVMetadataCreate
from app.utils.csv_files import create_and_save_metadata, save_uploaded_csv


def test_create_and_save_metadata(session, tmp_path, sample_csv_path, monkeypatch):
    table = pacsv.read_csv(sample_csv_path)

    parquet_path = tmp_path / "sample.parquet"
    parquet_path.write_bytes(b"dummy")

    upload = UploadFile(filename="new_file.csv", file=BytesIO(b""))
    monkeypatch.setattr(crud, "save_metadata", lambda *a, **k: None)

    metadata = create_and_save_metadata(session, upload, parquet_path, table)

    assert isinstance(metadata, CSVMetadataCreate)
    assert metadata.name_stored == "sample"
    assert metadata.name_original == "new_file"
    assert metadata.size_bytes == os.path.getsize(parquet_path)
    assert metadata.nrows == table.shape[0]
    assert metadata.ncols == table.shape[1]


@pytest.mark.asyncio
async def test_save_uploaded_csv(session, tmp_path, sample_csv_path, monkeypatch):
    table = pacsv.read_csv(sample_csv_path)
    content = sample_csv_path.read_bytes()
    upload = UploadFile(filename="sample.csv", file=BytesIO(content))

    monkeypatch.setattr(crud, "save_metadata", lambda s, m: None)

    metadata = await save_uploaded_csv(upload, session=session, dir=tmp_path)

    # parquet file exists
    parquet_file = (tmp_path / metadata.name_stored).with_suffix(".parquet")
    assert parquet_file.exists()

    # metadata structure correct
    assert isinstance(metadata, CSVMetadataCreate)
    assert metadata.nrows == table.shape[0]
    assert metadata.ncols == table.shape[1]

    # stored name is a UUID
    assert str(uuid.UUID(metadata.name_stored)) == metadata.name_stored
