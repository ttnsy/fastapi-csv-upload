import uuid
from io import BytesIO

import pytest
from fastapi import UploadFile

from app.utils.csv_files import save_uploaded_csv

# def test_create_and_save_metadata(sample_csv_path, session):
#     metadata = create_and_save_metadata(sample_csv_path)

#     assert isinstance(metadata, CSVMetadataCreate)
#     assert metadata.name_stored == "sample"
#     assert metadata.name_original == "new_file"
#     assert metadata.nrows == 5
#     assert metadata.ncols == 5
#     assert metadata.size_bytes == os.path.getsize(sample_csv_path)


@pytest.mark.asyncio
async def test_save_uploaded_csv(session, tmp_path, sample_csv_path):
    sample_csv = sample_csv_path.read_bytes()
    uploaded_csv = UploadFile(filename="sample.csv", file=BytesIO(sample_csv))

    metadata = await save_uploaded_csv(uploaded_csv, session=session, dir=tmp_path)

    assert (tmp_path / metadata.name_stored).with_suffix(".parquet").exists()
    assert str(uuid.UUID(metadata.name_stored)) == metadata.name_stored
