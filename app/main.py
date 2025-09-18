from flask import Flask, request, jsonify
from app.calculation_engine import generate_forecast
from app.llm_integration import explain_forecast
from app.knowledge_base import get_large_customer_revenue, get_default_cac  # Import helper functions

app = Flask(__name__)

@app.route("/forecast", methods=["POST"])
def forecast():
    data = request.get_json()
    customers = data.get("customers", 10)
    price = data.get("price", 100.0)
    growth = data.get("growth", 5.0)
    months = data.get("months", 12)

    forecast_df = generate_forecast(customers, price, growth, months)
    return forecast_df.to_json(orient="records")

@app.route("/explain", methods=["POST"])
def explain():
    data = request.get_json()
    customers = data.get("customers", 10)
    price = data.get("price", 100.0)
    growth = data.get("growth", 5.0)
    months = data.get("months", 12)

    forecast_df = generate_forecast(customers, price, growth, months)
    explanation = explain_forecast(forecast_df)
    return jsonify({"explanation": explanation})

if __name__ == "__main__":
    # Print values when running this script directly
    print("Large customer revenue:", get_large_customer_revenue())
    print("CAC:", get_default_cac())

    app.run(debug=True)

