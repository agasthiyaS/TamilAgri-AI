# TamilAgri AI - Backend Service

FastAPI-powered backend providing REST APIs for:
* Weather forecast retrieval (Demo & Open-Meteo adapters)
* Rule-based Paddy climate risk evaluation across 5 growth stages
* Bilingual Tamil & English warning template generation
* Farmer registration with mobile validation in SQLite
* SMS early warning dispatch with 24-hour duplicate suppression

## Running the Backend

```bash
# Activate virtual environment
..\venv\Scripts\Activate.ps1

# Run with hot reload on port 8000
uvicorn app.main:app --reload --port 8000
```

* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

## Running Tests

```bash
pytest ../backend/tests -v
```
