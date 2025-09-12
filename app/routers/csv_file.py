import logging
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.crud import create_metadata
from app.dependencies import SessionDep, UploadDirDep
from app.utils.csv_files import extract_csv_metadata, save_uploaded_csv

logger = logging.getLogger(__name__)

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
    if file.filename is None:
        logger.warning("Upload attempt with missing filename")
        raise HTTPException(status_code=400, detail="Filename is missing")

    if not file.filename.endswith(".csv"):
        logger.warning(f"Rejected file {file.filename} (not .csv)")
        raise HTTPException(status_code=400, detail="Only accept .csv")

    logger.info(f"Uploading file {file.filename} to {upload_dir}")

    file_path = await save_uploaded_csv(file, dir=upload_dir)

    try:
        csv_metadata = extract_csv_metadata(
            file_path, name_original=Path(file.filename).stem
        )
        metadata = create_metadata(session=session, csv_metadata=csv_metadata)
        logger.info(f"Metadata created for {file.filename}: {metadata}")
    except Exception as e:
        logger.exception(f"Failed processing {file.filename}")  # logs stack trace
        if file_path.exists():
            file_path.unlink()
            logger.info(f"Deleted incomplete file {file_path}")
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    return {"message": "Success", "metadata": metadata}


@router.get("/{filename}")
async def download_csv(filename: str, upload_dir: UploadDirDep):
    file_path = upload_dir / filename

    if not file_path.exists():
        logger.warning(f"Download failed: {filename} not found in {upload_dir}")
        raise HTTPException(status_code=404, detail="File not found")

    logger.info(f"Serving file {filename} from {upload_dir}")
    return FileResponse(path=file_path, filename=filename, media_type="text/csv")
