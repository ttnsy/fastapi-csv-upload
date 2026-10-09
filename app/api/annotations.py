from pathlib import Path
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.api.dependencies import get_session, get_upload_dir

SessionDep = Annotated[Session, Depends(get_session)]
UploadDirDep = Annotated[Path, Depends(get_upload_dir)]
