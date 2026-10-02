from sqlmodel import Session, select

from app.resources.datasets.model import CSVMetadata
from app.resources.datasets.schema import CSVMetadataCreate


def save_metadata(session: Session, metadata: CSVMetadataCreate):
    db_obj = CSVMetadata(**metadata.model_dump())

    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)


def get_metadata_by_name(session: Session, stored_name: str):
    statement = select(CSVMetadata).where(CSVMetadata.name_stored == stored_name)
    result = session.exec(statement).first()
    return result


def get_all_datasets(session: Session):
    statement = select(
        CSVMetadata.name_stored, CSVMetadata.name_original, CSVMetadata.uploaded_at
    )
    result = session.exec(statement).all()
    return [
        {"name_stored": r[0], "name_original": r[1], "uploaded_at": r[2]}
        for r in result
    ]
