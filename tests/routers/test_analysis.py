import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def uploaded_dataset(client: TestClient, sample_csv_path):
    with sample_csv_path.open("rb") as f:
        response = client.post(
            "/csv-file/",
            files={"file": ("sample.csv", f, "text/csv")},
        )
    return response.raise_for_status().json()["metadata"]


@pytest.mark.parametrize(
    "agg_period, agg_func",
    [
        ("daily", "sum"),
        ("daily", "avg"),
        ("daily", "median"),
        ("weekly", "sum"),
        ("monthly", "sum"),
    ],
)
def test_analysis(client: TestClient, uploaded_dataset, agg_period, agg_func):
    data = client.get(
        f"/analysis/{uploaded_dataset['name_stored']}",
        params={"agg_period": agg_period, "agg_func": agg_func},
    ).raise_for_status().json()

    assert isinstance(data, list)
    assert len(data) > 0

    for record in data:
        assert "period" in record
        assert "VALUE" in record


def test_analysis_with_group_by_id(client: TestClient, uploaded_dataset):
    data = client.get(
        f"/analysis/{uploaded_dataset['name_stored']}",
        params={"agg_period": "monthly", "agg_func": "sum", "group_by_id": True},
    ).raise_for_status().json()

    assert isinstance(data, list)

    for record in data:
        assert "period" in record
        assert "VALUE" in record
        assert "ID" in record