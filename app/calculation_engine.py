# app/calculation_engine.py

import pandas as pd
import random

def generate_full_forecast(
    months: int = 12,
    # Large customer GTM
    sales_executives: int = 2,
    new_executives_per_month: int = 1,
    customers_per_exec_min: int = 1,
    customers_per_exec_max: int = 2,
    revenue_per_large: float = 16500,
    # SMB GTM
    marketing_spend_smb: float = 20000,
    cac_smb: float = 1500,
    conversion_smb: float = 0.45,
    revenue_per_smb: float = 1500
):
    """
    Revenue forecast based on GTM strategy (row-wise format).
    """
    data = []
    total_large_customers = 0

    for m in range(1, months + 1):
        # --- Large customer logic ---
        new_large_customers = sum(
            random.randint(customers_per_exec_min, customers_per_exec_max)
            for _ in range(sales_executives)
        )
        total_large_customers += new_large_customers
        rev_large = total_large_customers * revenue_per_large

        # Ramp up sales team
        sales_executives += new_executives_per_month

        # --- SMB customer logic ---
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
    """
    Generate forecast in matrix format (metrics as rows, months as columns).
    """
    df = generate_full_forecast(**kwargs)

    # Set "Month" as index so that months become columns
    df_matrix = df.set_index("Month").T

    # Rename month columns to M1, M2, ...
    df_matrix.columns = [f"M{m}" for m in df_matrix.columns]

    # Add a proper index name for clarity
    df_matrix.index.name = "Tasks"

    return df_matrix



def export_to_excel(df: pd.DataFrame, filename="forecast.xlsx"):
    """
    Export forecast DataFrame to Excel (readable version).
    """
    with pd.ExcelWriter(filename, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Forecast")

        # Auto-adjust column width
        worksheet = writer.sheets["Forecast"]
        for col in worksheet.columns:
            max_length = 0
            col_letter = col[0].column_letter
            for cell in col:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
            worksheet.column_dimensions[col_letter].width = max_length + 2

    return filename



def export_to_csv(df: pd.DataFrame, filename="forecast.csv"):
    """
    Export forecast DataFrame to CSV.
    """
    df.to_csv(filename, index=True)
    return filename


# --- Standalone test ---
if __name__ == "__main__":
    # Generate matrix forecast
    df_matrix = generate_matrix_forecast(
        months=12,
        sales_executives=2,
        new_executives_per_month=1,
        customers_per_exec_min=1,
        customers_per_exec_max=2,
        revenue_per_large=16500,
        marketing_spend_smb=20000,
        cac_smb=1500,
        conversion_smb=0.45,
        revenue_per_smb=1500
    )

    # Display in console
    print(df_matrix)

    # Export to Excel & CSV
    export_to_excel(df_matrix, "matrix_forecast.xlsx")
    export_to_csv(df_matrix, "matrix_forecast.csv")
    print("Forecast exported in matrix format to Excel and CSV.")
