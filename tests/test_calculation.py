# tests/test_calculation.py
import pandas as pd
from app.calculation_engine import generate_forecast

def test_forecast_shape():
    df = generate_forecast(10, 100, 5, 6)
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 6
    assert "Revenue" in df.columns

def test_forecast_growth():
    df = generate_forecast(10, 100, 10, 3)
    # Month 1 revenue = 10 * 100
    assert df.iloc[0]["Revenue"] == 1000
    # Customers should grow by 10% each month
    assert df.iloc[1]["Customers"] == 11
