import logging
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel

from app.api.dependencies import get_session, get_upload_dir
from app.config import settings
from app.database import engine
from app.main import app


@pytest.fixture(scope="session", autouse=True)
def test_setup():
    assert settings.database_engine == "sqlite", (
        f"Tests must use SQLite, got engine: {settings.engine}"
    )
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)


# -------------------------------------------------------------
# DATABASE SETUP
# -------------------------------------------------------------


@pytest.fixture(scope="session")
def test_engine(tmp_path_factory):
    SQLModel.metadata.create_all(engine)
    yield engine


@pytest.fixture
def session(test_engine):
    with Session(test_engine) as s:
        yield s


@pytest.fixture
def client(session, tmp_path):
    def override_get_session():
        return session

    def override_get_upload_dir():
        return tmp_path

    app.dependency_overrides[get_session] = override_get_session
    app.dependency_overrides[get_upload_dir] = override_get_upload_dir

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


# -------------------------------------------------------------
# URL
# -------------------------------------------------------------
@pytest.fixture
def upload_url():
    return app.url_path_for("upload_dataset")


@pytest.fixture
def uploaded_dataset(client: TestClient, sample_csv_path, upload_url):
    with sample_csv_path.open("rb") as f:
        response = client.post(
            upload_url,
            files={"file": ("sample.csv", f, "text/csv")},
        )
    assert response.status_code == 201
    return response.json()["metadata"]


@pytest.fixture
def analysis_url(uploaded_dataset):
    return app.url_path_for(
        "analyse_dataset", stored_name=uploaded_dataset["name_stored"]
    )


@pytest.fixture
def download_url(uploaded_dataset):
    return app.url_path_for(
        "download_dataset", stored_name=uploaded_dataset["name_stored"]
    )


# -------------------------------------------------------------
# SAMPLE CSV
# -------------------------------------------------------------


@pytest.fixture
def sample_csv_path() -> Path:
    return Path("tests/sample.csv")
