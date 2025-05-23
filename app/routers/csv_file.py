from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.crud import create_metadata
from app.dependencies import SessionDep, UploadDirDep
from app.utils.csv_files import extract_csv_metadata, save_uploaded_csv

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
        raise HTTPException(status_code=400, detail="Filename is missing")

    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only accept .csv")

    file_path = await save_uploaded_csv(file, dir=upload_dir)

    try:
        csv_metadata = extract_csv_metadata(
            file_path, name_original=Path(file.filename).stem
        )
        metadata = create_metadata(session=session, csv_metadata=csv_metadata)
    except Exception as e:
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    return {"message": "Success", "metadata": metadata}


@router.get("/{filename}")
async def download_csv(filename: str, upload_dir: UploadDirDep):
    file_path = upload_dir / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, filename=filename, media_type="text/csv")
