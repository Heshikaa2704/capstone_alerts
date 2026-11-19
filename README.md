# Alert Explainer API

## Purpose

A FastAPI service for creating and retrieving alerts and generating human-readable alert explanations. Explanations use fixed rules based on severity and the metric value relative to its threshold.

## Project Structure

```text
alert_explainer_api/
├── database.py          # SQLite engine, session factory, and DB dependency
├── main.py              # FastAPI app and root health endpoint
├── models.py            # SQLAlchemy Alert model
├── requirements.txt     # Runtime dependencies
├── schemas.py           # Request and response models
├── test_alerts.py       # API tests
├── routers/
│   └── alerts.py        # Alert endpoints
├── services/
│   └── explainer.py     # Rule-based explanation generation
└── docs/
    └── adr/             # Architecture Decision Records
```

The SQLite database file, `alerts.db`, is created in the working directory when the application starts.

## Alert Fields

Create an alert with these required JSON fields:

| Field | Type | Details |
| --- | --- | --- |
| `title` | string | Alert title |
| `severity` | string | One of `critical`, `warning`, or `info` |
| `source` | string | Alert source |
| `metric_name` | string | Name of the measured metric |
| `metric_value` | number | Current metric value |
| `threshold` | number | Comparison threshold |

Alert responses also include the database-generated `id` and `created_at` timestamp. Explanation responses include `alert_id`, `explanation`, and `generated_at`.

## API Endpoints

| Method | Path | Status codes | Description |
| --- | --- | --- | --- |
| `GET` | `/` | `200` | Health check |
| `POST` | `/alerts/` | `201`, `422` | Create an alert; `422` for invalid request data |
| `GET` | `/alerts/` | `200` | List alerts |
| `GET` | `/alerts/{alert_id}` | `200`, `404`, `422` | Get an alert; `404` if it does not exist, `422` if the ID is not an integer |
| `POST` | `/alerts/{alert_id}/explain` | `200`, `404`, `422` | Generate an explanation; `404` if the alert does not exist, `422` if the ID is not an integer |

FastAPI's interactive API documentation is available at `/docs` while the service is running; the alternative documentation UI is at `/redoc`.

## Install and Run on Windows (PowerShell)

From the project directory:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
uvicorn main:app --reload
```

The API is available at `http://127.0.0.1:8000`. Open `http://127.0.0.1:8000/docs` to try the endpoints interactively. Keep the server running in this terminal; use a separate PowerShell terminal for tests.

## Run Tests

The test runner and HTTP client are not included in `requirements.txt`. Install them in the activated virtual environment, then run the test suite:

```powershell
python -m pip install pytest httpx
python -m pytest -v
```

## Architecture Decision Records

- [ADR 0001: Rule-Based Explanations](docs/adr/0001-rule-based-explanations.md)
- [ADR 0002: Human Approval for Alert Summaries](docs/adr/0002-human-approval-for-alert-summaries.md)
