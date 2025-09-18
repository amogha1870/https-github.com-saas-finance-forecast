# tests/test_llm_integration.py
from app.llm_integration import parse_query

def test_example_1():
    q = "12 months, start w/2 sales reps, add 1 per month, 200k marketing spend."
    p, c, n = parse_query(q)
    assert p["duration_months"] == 12
    assert p["initial_salespeople"] == 2
    assert p["new_salespeople_per_month"] == 1
    assert p.get("marketing_spend_total") == 200000

def test_example_2():
    q = "6 months; 3 sales starting; $50k per month marketing; CAC 1200; conversion 35%."
    p, c, n = parse_query(q)
    assert p["duration_months"] == 6
    assert p["initial_salespeople"] == 3
    assert p["marketing_spend_per_month"] == 50000
    assert abs(p["smb_conversion_rate"] - 0.35) < 1e-6

