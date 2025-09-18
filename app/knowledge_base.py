import json
import os

# Load the knowledge base JSON file safely
BASE_DIR = os.path.dirname(__file__)
with open(os.path.join(BASE_DIR, "knowledge_base.json"), "r") as f:
    kb = json.load(f)

# Example helper functions
def get_large_customer_revenue():
    return kb["units"]["large"]["arpu_monthly"]

def get_default_cac():
    return kb["units"]["smb"]["cac"]

def get_conversion_rate():
    return kb["units"]["smb"]["conversion_demo_to_paid"]

def get_default_value(key: str):
    """
    Retrieve default values from knowledge_base.json.
    """
    defaults = kb.get("defaults", {})
    return defaults.get(key, None)

# Run tests if this file is executed directly
if __name__ == "__main__":
    print("Revenue per large customer:", get_large_customer_revenue())
    print("Default CAC:", get_default_cac())
    print("Conversion rate:", get_conversion_rate())
    print("Default months:", get_default_value("forecast_months"))
