# tests/test_api.py
import pytest
from app.main import app

@pytest.fixture
def client():
    return app.test_client()

def test_forecast_api(client):
    response = client.post(
        "/forecast",
        json={"customers": 5, "price": 50, "growth": 10, "months": 3}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "forecast" in data
    assert isinstance(data["forecast"], list)
    assert len(data["forecast"]) == 3
