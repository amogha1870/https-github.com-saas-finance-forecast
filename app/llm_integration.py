def explain_forecast(forecast_df):
    """
    Fake LLM explanation for now.
    Replace with OpenAI API call during hackathon.
    """
    avg_revenue = forecast_df["Revenue"].mean()
    return f"The forecast shows steady growth, with an average monthly revenue of {avg_revenue:.2f}."
