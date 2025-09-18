from flask import Flask, request,   render_template, jsonify, send_file
import tempfile, os
from dotenv import load_dotenv

from app.calculation_engine import generate_matrix_forecast, export_to_excel, export_to_csv
from app.llm_integration import parse_user_query

load_dotenv()
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/forecast", methods=["POST"])
def forecast():
    data = request.get_json() or {}

    # If natural language query is provided
    if "query" in data:
        params, conf, notes = parse_user_query(data["query"])
    else:
        params = data

    # Map params to calculation engine args
    mapped_params = {
        "months": params.get("duration_months", data.get("months", 6)),
        "sales_executives": params.get("initial_salespeople", data.get("sales_executives", 2)),
        "new_executives_per_month": params.get("new_salespeople_per_month", data.get("new_executives_per_month", 1)),
        "customers_per_exec_min": data.get("customers_per_exec_min", 1),
        "customers_per_exec_max": data.get("customers_per_exec_max", 2),
        "revenue_per_large": params.get("revenue_per_large_customer_per_month", data.get("revenue_per_large", 16500)),
        "marketing_spend_smb": params.get("marketing_spend_per_month", data.get("marketing_spend_smb", 20000)),
        "cac_smb": params.get("avg_cac", data.get("cac_smb", 1500)),
        "conversion_smb": params.get("smb_conversion_rate", data.get("conversion_smb", 0.45)),
        "revenue_per_smb": params.get("revenue_per_smb_customer_per_month", data.get("revenue_per_smb", 1500))
    }

    try:
        df_matrix = generate_matrix_forecast(**mapped_params)
        response_format = data.get("format", "json").lower()

        if response_format == "json":
            return jsonify(df_matrix.to_dict())
        elif response_format == "excel":
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            export_to_excel(df_matrix, temp_file.name)
            return send_file(temp_file.name, as_attachment=True, download_name="forecast.xlsx")
        elif response_format == "csv":
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
            export_to_csv(df_matrix, temp_file.name)
            return send_file(temp_file.name, as_attachment=True, download_name="forecast.csv")
        else:
            return jsonify({"error": "Unsupported format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
