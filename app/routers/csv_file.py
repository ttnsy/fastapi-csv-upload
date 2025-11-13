import io

import pyarrow.csv as pacsv
import pyarrow.parquet as pq
from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import StreamingResponse

from app.dependencies import SessionDep, UploadDirDep
from app.log_config import logger
from app.utils.csv_files import save_uploaded_csv

router = APIRouter(
    prefix="/csv-file",
    tags=["CSV files"],
    responses={404: {"description": "Not found"}},
)


@router.post("/")
async def upload_csv(
    session: SessionDep,
    upload_dir: UploadDirDep,
    file: UploadFile = File(...),
):
    if not file.filename.endswith(".csv"):
        logger.warning(f"Rejected file {file.filename} (not .csv)")
        raise HTTPException(status_code=400, detail="Only accept .csv")

    metadata = await save_uploaded_csv(file, session, dir=upload_dir)

    return {"message": "Success", "metadata": metadata}


@router.get("/{filename}")
async def download_csv(filename: str, upload_dir: UploadDirDep):
    parquet_path = (upload_dir / filename).with_suffix(".parquet")

    if not parquet_path.exists():
        logger.warning(
            f"Download failed: {parquet_path.name} not found in {upload_dir}"
        )
        raise HTTPException(status_code=404, detail="File not found")

    table = pq.read_table(parquet_path)
    parquet_path = (upload_dir / filename).with_suffix(".parquet")

    if not parquet_path.exists():
        logger.warning(
            f"Download failed: {parquet_path.name} not found in {upload_dir}"
        )
        raise HTTPException(status_code=404, detail="File not found")

    sink = io.BytesIO()
    pacsv.write_csv(table, sink)
    csv_bytes = sink.getvalue()

    logger.info(f"Serving CSV for {filename} from {upload_dir}")

    return StreamingResponse(
        io.BytesIO(csv_bytes),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}.csv"'},
    )
