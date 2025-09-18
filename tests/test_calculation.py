from app.calculation_engine import generate_forecast

def test_forecast_shape():
    df = generate_forecast(10, 100, 5, 6)
    assert df.shape[0] == 6
    assert "Revenue" in df.columns
