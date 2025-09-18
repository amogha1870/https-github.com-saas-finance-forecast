# app/llm_integration.py
import os, json, re
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

try:
    import openai
    openai.api_key = OPENAI_API_KEY
except Exception:
    openai = None

# Simple fallback parsers
from app.fallback_utils import (
    parse_amount, parse_duration, parse_initial_salespeople,
    parse_new_sales_per_month, parse_marketing
)

# Default values if missing
KB_DEFAULTS = {
    "company_type": "SaaS",
    "revenue_per_large_customer_per_month": 16500,
    "avg_cac": 1500,
    "smb_conversion_rate": 0.45,
    "revenue_per_smb_customer_per_month": 1500
}

SYSTEM_PROMPT = (
    "You are an assistant that MUST extract forecasting parameters from a short natural language "
    "query and output JSON ONLY. Use numeric types. Units: USD for currency, months for duration. "
    "If a field is unknown, omit it or set null. Always include \"company_type\": \"SaaS\"."
)

FEW_SHOT_EXAMPLES = [
    {
        "user": "Forecast for 6 months: start with 3 sales execs, add 1 every month, $50k/month marketing, CAC 1200, conversion 35%.",
        "assistant": {
            "company_type": "SaaS",
            "duration_months": 6,
            "initial_salespeople": 3,
            "new_salespeople_per_month": 1,
            "marketing_spend_per_month": 50000,
            "avg_cac": 1200,
            "smb_conversion_rate": 0.35
        }
    },
    {
        "user": "12 months. 2 sales starting. 200k marketing total. Add one sales person every month. revenue per enterprise customer $16,500.",
        "assistant": {
            "company_type": "SaaS",
            "duration_months": 12,
            "initial_salespeople": 2,
            "new_salespeople_per_month": 1,
            "marketing_spend_total": 200000,
            "revenue_per_large_customer_per_month": 16500
        }
    }
]

def call_llm_for_params(query):
    if openai is None or not OPENAI_API_KEY:
        return None
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for ex in FEW_SHOT_EXAMPLES:
        messages.append({"role": "user", "content": ex["user"]})
        messages.append({"role": "assistant", "content": json.dumps(ex["assistant"])})
    messages.append({"role": "user", "content": query + "\nReturn JSON only."})
    try:
        resp = openai.ChatCompletion.create(
            model=MODEL,
            messages=messages,
            temperature=0.0,
            max_tokens=400
        )
        return resp["choices"][0]["message"]["content"]
    except Exception as e:
        print("LLM call error:", e)
        return None

def try_extract_json(txt):
    if not txt:
        return None
    m = re.search(r'(\{.*\})', txt, flags=re.DOTALL)
    if not m:
        return None
    jtxt = m.group(1)
    try:
        return json.loads(jtxt)
    except Exception:
        jtxt = re.sub(r',\s*}', '}', jtxt)
        jtxt = re.sub(r',\s*\]', ']', jtxt)
        try:
            return json.loads(jtxt)
        except Exception:
            return None

def fallback_parse(query):
    params = {}
    if dur := parse_duration(query):
        params["duration_months"] = dur
    if isp := parse_initial_salespeople(query):
        params["initial_salespeople"] = isp
    if newspm := parse_new_sales_per_month(query):
        params["new_salespeople_per_month"] = newspm
    if mkt := parse_marketing(query):
        if re.search(r'per month|/month|monthly', query, re.I):
            params["marketing_spend_per_month"] = mkt
        else:
            params["marketing_spend_total"] = mkt
    if m := re.search(r'(enterprise|large).*customer.*\$?([\d,\.kmKM]+)', query, re.I):
        params["revenue_per_large_customer_per_month"] = int(parse_amount(m.group(2)))
    if m2 := re.search(r'CAC\s*\$?([\d,\.kmKM]+)', query, re.I):
        params["avg_cac"] = int(parse_amount(m2.group(1)))
    if m3 := re.search(r'conversion.*?([\d\.]+)\s*%', query, re.I):
        params["smb_conversion_rate"] = float(m3.group(1)) / 100.0
    return params

def validate_and_fill_defaults(params, source):
    notes = []
    for k, v in KB_DEFAULTS.items():
        if k not in params or params.get(k) is None:
            params[k] = v
            notes.append(k)
    if "duration_months" in params:
        params["duration_months"] = int(params["duration_months"])
    conf = 0.9 if source == "llm" else 0.6
    if len(notes) >= 3:
        conf -= 0.3
    conf = max(conf, 0.2)
    return params, conf, f"default fields filled: {notes}" if notes else ""

def parse_query(query):
    llm_txt = call_llm_for_params(query)
    params = try_extract_json(llm_txt) if llm_txt else None
    source = "llm" if params else "fallback"
    if not params:
        params = fallback_parse(query)
    params, conf, notes = validate_and_fill_defaults(params, source)
    return params, conf, notes

# Alias for main.py
parse_user_query = parse_query
