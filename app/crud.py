from sqlmodel import Session

from app.models import CSVMetadata
from app.schemas import CSVMetadataCreate


def save_metadata(session: Session, metadata: CSVMetadataCreate):
    db_obj = CSVMetadata.model_validate(metadata)

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
