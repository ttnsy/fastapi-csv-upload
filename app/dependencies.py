from app.config import UPLOAD_DIR


def get_upload_dir():
    if not UPLOAD_DIR.exists():
        raise RuntimeError(f"{UPLOAD_DIR} does not exist!")
    return UPLOAD_DIR
