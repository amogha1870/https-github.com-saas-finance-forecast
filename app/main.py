from flask import Flask, request, jsonify, send_file
import os
import tempfile
from dotenv import load_dotenv

# Local imports (no need for "app." prefix since main.py is already inside app/)
from llm_integration import parse_user_query   # TM3
from knowledge_base import get_default_value   # TM2
from calculation_engine import (
    generate_matrix_forecast,
    export_to_excel,
    export_to_csv
)  # TM4

# Load environment variables
load_dotenv()

app = Flask(__name__)

@app.route("/forecast", methods=["POST"])
def forecast():
    try:
        data = request.get_json()

        # If natural language query is provided → send to LLM (TM3)
        if "query" in data:
            params = parse_user_query(data["query"])
        else:
            # Otherwise use direct params (fallback)
            params = {
                "months": data.get("months", get_default_value("months")),
                "sales_executives": data.get("sales_executives", get_default_value("sales_executives")),
                "new_executives_per_month": data.get("growth", get_default_value("new_executives_per_month")),
                "marketing_spend_smb": data.get("marketing_spend", get_default_value("marketing_spend_smb")),
            }

        # Generate forecast (TM4)
        df_matrix = generate_matrix_forecast(**params)

        # Check response format
        response_format = data.get("format", "json").lower()

        if response_format == "json":
            return df_matrix.to_json(orient="split")

        elif response_format == "excel":
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
            export_to_excel(df_matrix, temp_file.name)
            return send_file(temp_file.name, as_attachment=True, download_name="forecast.xlsx")

        elif response_format == "csv":
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
            export_to_csv(df_matrix, temp_file.name)
            return send_file(temp_file.name, as_attachment=True, download_name="forecast.csv")

        else:
            return jsonify({"error": "Unsupported format. Use json, excel, or csv"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))


