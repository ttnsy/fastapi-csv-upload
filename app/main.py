import uuid
from pathlib import Path

from fastapi import Depends, FastAPI, File, HTTPException, UploadFile

from app.dependencies import get_upload_dir

app = FastAPI()


async def save_uploaded_csv(file: UploadFile, dir: Path):
    name = f"{uuid.uuid4()}_{file.filename}"
    path = dir / name

    content = await file.read()
    with open(path, "wb") as f:
        f.write(content)

    return str(path)


@app.post("/upload-csv/")
async def create_upload_csv(
    file: UploadFile = File(...), upload_dir: Path = Depends(get_upload_dir)
):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only accept .csv")

    file_path = await save_uploaded_csv(file, dir=upload_dir)
    return {"message": "Success", "path": file_path}
