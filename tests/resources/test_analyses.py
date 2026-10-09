from fastapi.testclient import TestClient


def test_analysis_daily_sum(client: TestClient, analysis_url):
    response = client.get(
        analysis_url,
        params={"agg_period": "daily", "agg_func": "sum"},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

    for record in data:
        assert "period" in record
        assert "VALUE" in record


def test_analysis_weekly_sum(client: TestClient, analysis_url):
    response = client.get(
        analysis_url,
        params={"agg_period": "weekly", "agg_func": "sum"},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_analysis_monthly_sum(client: TestClient, analysis_url):
    response = client.get(
        analysis_url,
        params={"agg_period": "monthly", "agg_func": "sum"},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


def test_analysis_daily_avg(client: TestClient, analysis_url):
    response = client.get(
        analysis_url,
        params={"agg_period": "daily", "agg_func": "avg"},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_analysis_daily_median(client: TestClient, analysis_url):
    response = client.get(
        analysis_url,
        params={"agg_period": "daily", "agg_func": "median"},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_analysis_with_group_by_id(client: TestClient, analysis_url):
    response = client.get(
        analysis_url,
        params={"agg_period": "monthly", "agg_func": "sum", "group_by_id": True},
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

    for record in data:
        assert "period" in record
        assert "VALUE" in record
        assert "ID" in record
