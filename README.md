# Natural Language to SQL Analytics Agent

A constrained analytics API mapping a small set of natural-language intents to approved SQL templates over a local sample SQLite database.

## Supported questions
- "Show total sales by region"
- "Show total sales by product"
- "What is the average sale?"
- "List all sales"

## Run
```bash
pip install -r requirements.txt
uvicorn app:app --reload
```
Open http://127.0.0.1:8000/docs and use `POST /query`.

## Safety choices
- Predefined SELECT templates instead of arbitrary model-generated SQL
- Read-only SQLite connection for query execution
- Maximum 100 returned rows
- Unsupported intents return HTTP 400

## Limitations
Intent parsing is keyword-based, not an LLM. The local sample database is created at startup for demonstration. A real deployment needs authentication, schema-level authorization, audit logs, timeouts, and tenant isolation.

## Stack
Python, FastAPI, SQLite, pytest.
