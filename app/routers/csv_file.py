import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from ..dependencies import get_upload_dir

router = APIRouter(
    prefix="/csv-file",
    tags=["CSV files"],
    dependencies=[Depends(get_upload_dir)],
    responses={404: {"description": "Not found"}},
)


async def save_uploaded_csv(file: UploadFile, dir: Path):
    name = f"{uuid.uuid4()}_{file.filename}"
    path = dir / name

    content = await file.read()
    with open(path, "wb") as f:
        f.write(content)

    return str(path)


@router.post("/")
async def upload_csv(
    file: UploadFile = File(...), upload_dir: Path = Depends(get_upload_dir)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only accept .csv")

    file_path = await save_uploaded_csv(file, dir=upload_dir)
    return {"message": "Success", "path": file_path}


@router.get("/{filename}")
async def download_csv(filename: str, upload_dir: Path = Depends(get_upload_dir)):
    file_path = upload_dir / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, filename=filename, media_type="text/csv")
