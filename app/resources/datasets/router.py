import io

import pyarrow.csv as pacsv
import pyarrow.parquet as pq
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import Response

from app.api.annotations import SessionDep, UploadDirDep
from app.log_config import logger
from app.resources.datasets.service import get_dataset, get_datasets, save_uploaded_csv

router = APIRouter(prefix="/datasets", tags=["datasets"])


@router.post("/", status_code=201)
async def upload_csv(
    session: SessionDep,
    upload_dir: UploadDirDep,
    file: UploadFile = File(...),
):
    if not file.filename or not file.filename.endswith(".csv"):
        logger.warning(f"Rejected file {file.filename} (not .csv)")
        raise HTTPException(status_code=400, detail="Only accept .csv")

    metadata = await save_uploaded_csv(session, file, dir=upload_dir)

    return {"message": "Success", "metadata": metadata}


@router.get("/")
def list_datasets(session: SessionDep):
    datasets = get_datasets(session)
    return datasets


@router.get("/{stored_name}")
def get_dataset_info(stored_name: str, session: SessionDep, upload_dir: UploadDirDep):
    metadata, _ = get_dataset(stored_name, session, upload_dir)
    return metadata


@router.get("/{stored_name}/content")
async def download_csv(stored_name: str, session: SessionDep, upload_dir: UploadDirDep):
    metadata, path = get_dataset(stored_name, session, upload_dir)
    sink = io.BytesIO()
    pacsv.write_csv(pq.read_table(path), sink)
    csv_content = sink.getvalue()

    logger.info(f"Serving CSV for {stored_name} from {upload_dir}")

    return Response(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{stored_name}.csv"'},
    )
