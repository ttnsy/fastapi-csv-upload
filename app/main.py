import os
import uuid

from fastapi import FastAPI, File, HTTPException, UploadFile

app = FastAPI()

UPLOAD_DIR = "files"
os.makedirs(UPLOAD_DIR, exist_ok=True)


async def save_uploaded_csv(file: UploadFile, dir: str):
    name = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(dir, name)

    with open(path, "wb") as f:
        content = await file.read()
        f.write(content)

    return path


@app.post("/upload-csv/")
async def create_upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only accept .csv")

    file_path = await save_uploaded_csv(file, dir=UPLOAD_DIR)

    return {"message": "Success", "path": file_path}
