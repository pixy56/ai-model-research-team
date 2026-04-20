# Model Database API

FastAPI application for managing AI model metadata with SQLite database.

## Structure

```
src/
├── main.py              # FastAPI app entry point
├── database.py          # Database connection and session management
├── models/
│   └── model.py         # SQLAlchemy models (Model, Benchmark, Tag)
├── schemas/
│   └── model.py         # Pydantic schemas for request/response validation
├── routers/
│   └── models.py        # API endpoints
└── services/
    └── model_service.py # Business logic

tests/
├── conftest.py          # Pytest fixtures
├── test_api.py          # API endpoint tests
└── test_models.py       # Service layer tests
```

## Installation

```bash
pip install -r requirements-api.txt
```

## Running the API

```bash
# Development mode with auto-reload
./start-api.sh

# Or directly
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| GET | `/api/models` | List models (paginated) |
| GET | `/api/models/search?q={query}` | Search models |
| GET | `/api/models/{id}` | Get specific model |
| POST | `/api/models` | Create model |
| PUT | `/api/models/{id}` | Update model |
| DELETE | `/api/models/{id}` | Delete model |

## Running Tests

```bash
pytest tests/
```

## Database Schema

### models table
- `id`: Primary key
- `name`: Model name
- `lab`: Research lab/organization
- `release_date`: ISO 8601 date string
- `architecture`: Model architecture type
- `parameters`: Number of parameters (or "unknown")
- `context_window`: Context window size (or "unknown")
- `paper_url`: URL to research paper
- `announcement_url`: URL to announcement
- `created_at`: Timestamp
- `updated_at`: Timestamp

### benchmarks table
- `id`: Primary key
- `model_id`: Foreign key to models
- `benchmark_name`: Name of benchmark
- `score`: Score value
- `metric`: Metric type (default: "score")

### tags table
- `id`: Primary key
- `model_id`: Foreign key to models
- `tag_name`: Tag value
