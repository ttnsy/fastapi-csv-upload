import os
import uuid
from io import BytesIO

import pytest
from fastapi import UploadFile

from app.schemas import CSVMetadataCreate
from app.utils.csv_files import extract_csv_metadata, save_uploaded_csv


@pytest.mark.asyncio
async def test_save_uploaded_csv(tmp_path, sample_csv_path):
    sample_csv = sample_csv_path.read_bytes()
    uploaded_csv = UploadFile(filename="sample.csv", file=BytesIO(sample_csv))

    saved_path = await save_uploaded_csv(uploaded_csv, dir=tmp_path)
    saved_filename = saved_path.stem

    assert saved_path.exists()
    assert str(uuid.UUID(saved_filename)) == saved_filename


def test_extract_csv_metadata(sample_csv_path):
    metadata = extract_csv_metadata(sample_csv_path, name_original="new_file")

    assert isinstance(metadata, CSVMetadataCreate)
    assert metadata.name_stored == "sample"
    assert metadata.name_original == "new_file"
    assert metadata.nrows == 5
    assert metadata.ncols == 5
    assert metadata.size_bytes == os.path.getsize(sample_csv_path)
