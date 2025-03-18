from pathlib import Path


def get_upload_dir():
    upload_dir = Path(__file__).resolve().parent / "files"
    upload_dir.mkdir(parents=True, exist_ok=True)
    return upload_dir
