import uuid
from pathlib import Path

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse

from app.dependencies import get_upload_dir

app = FastAPI()


async def save_uploaded_csv(file: UploadFile, dir: Path):
    name = f"{uuid.uuid4()}_{file.filename}"
    path = dir / name

    content = await file.read()
    with open(path, "wb") as f:
        f.write(content)

    return str(path)


@app.post("/csv-file/")
async def upload_csv(
    file: UploadFile = File(...), upload_dir: Path = Depends(get_upload_dir)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only accept .csv")

    file_path = await save_uploaded_csv(file, dir=upload_dir)
    return {"message": "Success", "path": file_path}


@app.get("/csv-file/{filename}")
async def download_csv(filename: str, upload_dir: Path = Depends(get_upload_dir)):
    file_path = upload_dir / filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(path=file_path, filename=filename, media_type="text/csv")
