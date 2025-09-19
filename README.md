GrowthGrid

This project is a Flask-based web application that integrates a Large Language Model (LLM) with a custom calculation engine to perform forecasting from natural language queries.

Project Structure
my_flask_app/
│
├─ app/
│  ├─ templates/
│  │  └─ index.html          # Frontend HTML page
│  ├─ main.py                # Flask backend
│  ├─ llm_integration.py     # LLM query parsing & OpenAI API calls
│  ├─ calculation_engine.py  # Forecasting logic
│  └─ fallback_utils.py      # Parsers for natural language fallback
│
├─ tests/                    # test files are added for testing and checking
│
├─ .env                      # Environment variables (API keys, etc.)
├─ requirements.txt          # Python dependencies
└─ README.md                 # Project documentation

 Setup Instructions
1) Clone the repository
git clone https://github.com/amogha1870/https-github.com-saas-finance-forecast

cd my_flask_app

2️) Create & activate a virtual environment
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows

3) Install dependencies
pip install -r requirements.txt

4) Set environment variables

Create a .env file in the project root:

OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4

5) Running the App

Start the Flask app:

python -m app.main
Then open your browser at: http://127.0.0.1:5000

Frontend
The app includes a simple HTML frontend (index.html) under app/templates/.
It allows users to:

Enter a natural language query (e.g., "Forecast the revenue growth for the next 3 months")
Submit the query to the backend
Display results from the LLM + calculation engine

📡 API Endpoints
POST /forecast

Accepts natural language queries and returns AI + calculation engine response.

Request JSON Example:

{
  "query": "What will be the sales trend for the next 6 months?"
}


Response Example:

{
  "response": "Based on the calculation engine, the projected sales will increase by ~12% over the next 6 months."
}


 Features

- LLM Integration with OpenAI
- Custom Forecasting Engine
- REST API + Frontend
- Unit & Integration Tests
 - Environment variable-based configuration
 - Deployment

You can deploy the app on cloud platforms like Render, Heroku, or Azure.

Example: Deploy on Render

Push your repo to GitHub

Connect GitHub repo to Render

Add environment variables (OPENAI_API_KEY, OPENAI_MODEL) in Render dashboard

Set Start Command:

gunicorn app.main:app
