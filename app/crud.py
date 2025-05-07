from fastapi import Depends
from sqlmodel import Session

from app.database import engine
from app.dependencies import get_session
from app.models import CSVMetadata
from app.schemas import CSVMetadataCreate


def create_metadata(
    *, session: Session = Depends(get_session), csv_metadata: CSVMetadataCreate
):
    with Session(engine) as session:
        db_obj = CSVMetadata(**csv_metadata.model_dump())

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return csv_metadata
