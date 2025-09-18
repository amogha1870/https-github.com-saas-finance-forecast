# app/calculation_engine.py

import pandas as pd
import random

def generate_forecast(
    months: int = 12,
    sales_executives: int = 2,
    new_executives_per_month: int = 1,
    customers_per_exec_min: int = 1,
    customers_per_exec_max: int = 2,
    revenue_per_large: float = 16500,
    marketing_spend_smb: float = 20000,
    cac_smb: float = 1500,
    conversion_smb: float = 0.45,
    revenue_per_smb: float = 1500
):
    """Generate row-wise forecast DataFrame."""
    data = []
    total_large_customers = 0

    for m in range(1, months + 1):
        new_large_customers = sum(random.randint(customers_per_exec_min, customers_per_exec_max) 
                                  for _ in range(sales_executives))
        total_large_customers += new_large_customers
        rev_large = total_large_customers * revenue_per_large

        # Ramp up sales team
        sales_executives += new_executives_per_month

        # SMB logic
        potential_smb_customers = marketing_spend_smb / cac_smb
        paying_smb_customers = int(potential_smb_customers * conversion_smb)
        rev_smb = paying_smb_customers * revenue_per_smb

        total_rev = rev_large + rev_smb

        data.append({
            "Month": m,
            "Sales People": sales_executives,
            "Large Customers": total_large_customers,
            "Large Revenue": rev_large,
            "SMB Customers": paying_smb_customers,
            "SMB Revenue": rev_smb,
            "Total Revenue": total_rev
        })

    return pd.DataFrame(data)

def generate_matrix_forecast(**kwargs):
    """Generate forecast in matrix format (metrics as rows, months as columns)."""
    df = generate_forecast(**kwargs)
    df_matrix = df.set_index("Month").T
    df_matrix.columns = [f"M{m}" for m in df_matrix.columns]
    df_matrix.index.name = "Metrics"
    return df_matrix

def export_to_excel(df: pd.DataFrame, filename="forecast.xlsx"):
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Forecast")
    return filename

def export_to_csv(df: pd.DataFrame, filename="forecast.csv"):
    df.to_csv(filename, index=True)
    return filename
