from app.main import app

def test_forecast_api():
    client = app.test_client()
    response = client.post("/forecast", json={"customers": 5, "price": 50, "growth": 10, "months": 3})
    assert response.status_code == 200
