from sqlmodel import Session

from app.models import CSVMetadata
from app.schemas import CSVMetadataCreate


def create_metadata(session: Session, csv_metadata: CSVMetadataCreate):
    db_obj = CSVMetadata.model_validate(csv_metadata)

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
