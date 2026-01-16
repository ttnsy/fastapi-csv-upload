from sqlmodel import Session, select

from app.models import CSVMetadata
from app.schemas import CSVMetadataCreate


def save_metadata(session: Session, metadata: CSVMetadataCreate):
    db_obj = CSVMetadata(**metadata.model_dump())

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)


def get_metadata_by_name(session: Session, stored_name: str):
    statement = select(CSVMetadata).where(CSVMetadata.name_stored == stored_name)
    result = session.exec(statement).first()
    return result
