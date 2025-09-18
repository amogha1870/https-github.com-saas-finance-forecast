import json

# Load the knowledge base JSON file
with open("knowledge_base.json", "r") as f:
    kb = json.load(f)

# Example helper functions
def get_large_customer_revenue():
    return kb["units"]["large"]["arpu_monthly"]

def get_default_cac():
    return kb["units"]["smb"]["cac"]

def get_conversion_rate():
    return kb["units"]["smb"]["conversion_demo_to_paid"]

# Run tests if this file is executed directly
if __name__ == "__main__":
    print("Revenue per large customer:", get_large_customer_revenue())
    print("Default CAC:", get_default_cac())
    print("Conversion rate:", get_conversion_rate())
