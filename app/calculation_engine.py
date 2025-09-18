import pandas as pd

def generate_forecast(customers: int, price: float, growth: float, months: int = 12):
    """
    Simple revenue forecast model.
    customers: starting number of customers
    price: price per customer per month
    growth: monthly growth rate (%)
    months: forecast length
    """
    data = []
    current_customers = customers

    for m in range(1, months + 1):
        revenue = current_customers * price
        data.append({"Month": m, "Customers": current_customers, "Revenue": revenue})
        current_customers = int(current_customers * (1 + growth / 100))

    return pd.DataFrame(data)
