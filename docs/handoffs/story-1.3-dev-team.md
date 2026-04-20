# Dev Team Handoff: Story 1.3 - Model Database

**Story:** Model Database  
**Story Points:** 8  
**Priority:** High  
**Blocked By:** Story 1.1 (Complete - Schema ready)

---

## Overview

Create a database to store and query AI model information. This is the central data store for the research team's model tracking system.

---

## Inputs from AI Agents

### 1. Schema Definition
**Location:** `docs/schemas/model-metadata.json`

```json
{
  "name": "GPT-4",
  "lab": "OpenAI",
  "release_date": "2023-03-14",
  "architecture": "dense-transformer",
  "parameters": "unknown",
  "context_window": 8192,
  "benchmarks": {
    "mmlu": 86.4,
    "humaneval": 67.0
  },
  "paper_url": "https://arxiv.org/abs/2303.08774",
  "announcement_url": "https://openai.com/blog/gpt-4",
  "tags": ["multimodal", "reasoning"]
}
```

**Required Fields:**
- `name` (string): Model name
- `lab` (string): Research lab
- `release_date` (ISO date): Release date
- `architecture` (enum): dense-transformer, moe, ssm, multimodal, reasoning, other
- `parameters` (number or "unknown"): Parameter count in billions
- `context_window` (number or "unknown"): Context window size
- `benchmarks` (object): Benchmark scores
- `paper_url` (string): Paper URL
- `announcement_url` (string): Announcement URL

**Optional Fields:**
- `tags` (array of strings): Categorization tags

### 2. Sample Data
**Location:** `data/sample-model.json`

### 3. Validation Script
**Location:** `scripts/validate-model-schema.py`

Run: `python scripts/validate-model-schema.py --test`

---

## Requirements

### Database Schema

**Table: models**
```sql
CREATE TABLE models (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    lab VARCHAR(255) NOT NULL,
    release_date DATE NOT NULL,
    architecture VARCHAR(50) NOT NULL,
    parameters VARCHAR(50),  -- 'unknown' or number as string
    context_window INTEGER,  -- NULL for unknown
    paper_url VARCHAR(500),
    announcement_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Table: benchmarks**
```sql
CREATE TABLE benchmarks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER NOT NULL,
    benchmark_name VARCHAR(100) NOT NULL,
    score FLOAT NOT NULL,
    metric VARCHAR(50),  -- e.g., 'accuracy', 'pass@1'
    FOREIGN KEY (model_id) REFERENCES models(id)
);
```

**Table: tags**
```sql
CREATE TABLE tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id INTEGER NOT NULL,
    tag_name VARCHAR(100) NOT NULL,
    FOREIGN KEY (model_id) REFERENCES models(id)
);
```

### API Endpoints

**FastAPI Application**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/models` | List all models (paginated) |
| GET | `/api/models/{id}` | Get specific model |
| POST | `/api/models` | Create new model |
| PUT | `/api/models/{id}` | Update model |
| DELETE | `/api/models/{id}` | Delete model |
| GET | `/api/models/search` | Search models by query params |

**Query Parameters for `/api/models`:**
- `page` (int): Page number (default: 1)
- `per_page` (int): Items per page (default: 20)
- `lab` (str): Filter by lab
- `architecture` (str): Filter by architecture
- `date_from` (date): Filter by release date (start)
- `date_to` (date): Filter by release date (end)

**Query Parameters for `/api/models/search`:**
- `q` (str): Search query (matches name, lab, tags)

### Response Format

```json
{
  "data": [
    {
      "id": 1,
      "name": "GPT-4",
      "lab": "OpenAI",
      "release_date": "2023-03-14",
      "architecture": "dense-transformer",
      "parameters": "unknown",
      "context_window": 8192,
      "benchmarks": {
        "mmlu": 86.4,
        "humaneval": 67.0
      },
      "tags": ["multimodal", "reasoning"],
      "paper_url": "https://arxiv.org/abs/2303.08774",
      "announcement_url": "https://openai.com/blog/gpt-4"
    }
  ],
  "pagination": {
    "page": 1,
    "per_page": 20,
    "total": 150,
    "total_pages": 8
  }
}
```

---

## Tech Stack

- **Framework:** FastAPI
- **ORM:** SQLAlchemy
- **Database:** SQLite (for now, PostgreSQL migration path)
- **Validation:** Pydantic
- **Testing:** pytest

---

## File Structure

```
src/
├── __init__.py
├── main.py              # FastAPI app entry point
├── database.py          # Database connection & models
├── models/
│   ├── __init__.py
│   └── model.py         # SQLAlchemy models
├── schemas/
│   ├── __init__.py
│   └── model.py         # Pydantic schemas
├── routers/
│   ├── __init__.py
│   └── models.py        # API endpoints
└── services/
    ├── __init__.py
    └── model_service.py # Business logic

tests/
├── __init__.py
├── conftest.py          # pytest fixtures
├── test_api.py          # API endpoint tests
└── test_models.py       # Database model tests
```

---

## Acceptance Criteria

- [ ] Database schema created (SQLite)
- [ ] API supports: list, get, create, update, delete
- [ ] Search by lab, architecture, date range
- [ ] Tests pass (pytest)
- [ ] Documentation updated (API docs via FastAPI)
- [ ] Sample data imports successfully
- [ ] Validation against JSON schema works

---

## Dependencies

```
fastapi
uvicorn
sqlalchemy
pydantic
pytest
httpx  # for testing
```

---

## Integration Points

### From AI Agents
- **Input:** `docs/schemas/model-metadata.json`
- **Input:** `data/sample-model.json`
- **Validation:** `scripts/validate-model-schema.py`

### To AI Agents
- **Output:** API endpoints for Literature Review Agent
- **Output:** Query interface for Data Analysis Agent

---

## Notes

- Use SQLite for initial implementation (simple, portable)
- Design for PostgreSQL migration (use SQLAlchemy properly)
- Include database migrations (Alembic optional)
- API documentation auto-generated at `/docs` (Swagger UI)
- Include CORS for frontend integration

---

## Questions?

Contact: Integration Agent or Scrum Master

**Status:** Ready for Development  
**Priority:** High (blocks Iteration 2)