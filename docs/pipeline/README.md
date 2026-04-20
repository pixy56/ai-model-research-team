# Data Pipeline Documentation

Automated data pipeline for ingesting AI model and benchmark data into the database.

## Overview

The pipeline provides automated ingestion of:
- **Lab Announcements** (47 models): From `data/raw/lab_announcements.json`
- **Benchmark Scores** (69 scores): From `data/processed/benchmark_scores.json`

## Components

```
scripts/pipeline/
├── validate_data.py       # Data validation module
├── ingest_lab_data.py     # Lab announcements ingestion
├── ingest_benchmarks.py   # Benchmark scores ingestion
├── scheduler.py           # Automated scheduling
└── run_pipeline.sh        # Master orchestration script
```

## Quick Start

### Prerequisites

1. API running at `localhost:8000`:
   ```bash
   ./start-api.sh
   ```

2. Python dependencies installed:
   ```bash
   pip install -r requirements-api.txt
   pip install requests
   ```

### Run the Pipeline

```bash
# Navigate to pipeline directory
cd scripts/pipeline

# Run full pipeline (validate + ingest)
./run_pipeline.sh run

# Preview changes without ingesting
./run_pipeline.sh dry-run

# Validate data only
./run_pipeline.sh validate

# Check status
./run_pipeline.sh status
```

## Pipeline Steps

### 1. Data Validation

Validates data before ingestion:
- Schema compliance
- Required fields
- Date formats
- Architecture values
- Benchmark score ranges

```bash
python validate_data.py --type lab data/raw/lab_announcements.json
python validate_data.py --type benchmark data/processed/benchmark_scores.json
```

### 2. Lab Data Ingestion

Ingests 47 models from lab announcements:

```bash
python ingest_lab_data.py --input data/raw/lab_announcements.json
```

**Features:**
- Auto-extracts parameters from model names (e.g., "7B")
- Extracts context window from key features
- Converts key_features to tags
- Handles duplicates (update vs create)
- Transforms benchmark claims to database format

### 3. Benchmark Ingestion

Ingests 69 benchmark scores and links to models:

```bash
python ingest_benchmarks.py --input data/processed/benchmark_scores.json
```

**Features:**
- Extracts model names from context
- Links scores to existing models
- Adds new benchmarks to models
- Skips extractions without scores

## Scheduler

### Configuration

Configuration stored in `scripts/pipeline/scheduler_config.json`:

```json
{
  "schedule": {
    "enabled": true,
    "frequency": "weekly",
    "day_of_week": 0,
    "hour": 2,
    "minute": 0
  },
  "pipeline": {
    "validate_before_ingest": true,
    "dry_run_first": false,
    "stop_on_error": true,
    "api_base_url": "http://localhost:8000"
  }
}
```

### Commands

```bash
# Check scheduler status
./run_pipeline.sh status

# Enable/disable scheduling
./run_pipeline.sh enable
./run_pipeline.sh disable

# Manual scheduled run
./run_pipeline.sh schedule
```

### Cron Setup

Add to crontab for weekly runs:

```bash
# Edit crontab
crontab -e

# Add line for weekly run (Monday 2:00 AM)
0 2 * * 1 cd /path/to/project && ./scripts/pipeline/run_pipeline.sh schedule
```

## API Integration

The pipeline integrates with the FastAPI endpoints:

- `GET /api/models` - List all models
- `GET /api/models/search?q={name}` - Search for model
- `POST /api/models` - Create new model
- `PUT /api/models/{id}` - Update existing model

## Data Transformation

### Lab Announcements → Model Schema

| Source Field | Target Field | Transformation |
|--------------|--------------|----------------|
| `name` | `name` | Direct mapping |
| `lab` | `lab` | Lab name |
| `announcement_date` | `release_date` | Direct mapping |
| `architecture` | `architecture` | Validated against allowed values |
| `name` (parsed) | `parameters` | Extract "7B" → 7.0 |
| `key_features` | `context_window` | Extract "128K" → 128000 |
| `url` | `announcement_url` | Direct mapping |
| `benchmark_claims` | `benchmarks` | Convert dict format |
| `key_features` | `tags` | Split by comma |

### Benchmark Scores → Model Benchmarks

- Extract model name from context
- Match to existing model in database
- Add benchmark score to model's benchmarks dict

## Error Handling

### Validation Errors

- Missing required fields
- Invalid architecture values
- Malformed dates
- Invalid benchmark scores

### Ingestion Errors

- API connection failures
- Duplicate model conflicts
- Missing referenced models
- Database constraint violations

### Logging

All scripts log to stdout with timestamps:
```
2025-04-20 12:00:00 - INFO - Starting ingestion...
2025-04-20 12:00:01 - ERROR - Failed to create model: ...
```

## Health Checks

```bash
# Check pipeline health
./run_pipeline.sh health

# Expected output:
{
  "status": "healthy",
  "checks": {
    "api": "healthy",
    "data_lab_announcements": "exists",
    "data_benchmark_scores": "exists",
    "last_run": "2025-04-20T10:00:00",
    "next_run": "2025-04-27T02:00:00"
  }
}
```

## Testing

### Dry Run Mode

Preview changes without modifying database:

```bash
./run_pipeline.sh dry-run
```

### Validation Only

Check data without ingestion:

```bash
./run_pipeline.sh validate
```

## Monitoring

### Acceptance Criteria

- [x] Pipeline ingests 47 lab models
- [x] Pipeline ingests 69 benchmark scores
- [x] Data validation enforced
- [x] Scheduler configured
- [x] Tests pass
- [x] Documentation complete

### Metrics

Track pipeline performance:
- Total models processed
- Created vs updated
- Failed operations
- Processing duration
- Validation errors

## Troubleshooting

### API Not Running

```
Error: API is not running at http://localhost:8000
```

**Solution:**
```bash
./start-api.sh
```

### Validation Failed

```
Error: Data validation failed
```

**Solution:** Check validation output for specific errors, fix source data.

### Model Not Found

```
Warning: Could not link benchmark - model not found
```

**Solution:** Ensure lab data is ingested before benchmark data.

## File Locations

```
ai-model-research-team/
├── data/
│   ├── raw/
│   │   └── lab_announcements.json      # 47 models
│   └── processed/
│       └── benchmark_scores.json        # 69 scores
├── scripts/
│   └── pipeline/
│       ├── validate_data.py
│       ├── ingest_lab_data.py
│       ├── ingest_benchmarks.py
│       ├── scheduler.py
│       ├── run_pipeline.sh
│       └── scheduler_config.json        # Auto-generated
└── docs/
    └── pipeline/
        └── README.md                    # This file
```

## Development

### Adding New Validators

1. Edit `validate_data.py`
2. Add validation method to `DataValidator` class
3. Update CLI in `main()` function

### Adding New Data Sources

1. Create new ingestion script (e.g., `ingest_papers.py`)
2. Follow pattern from existing ingesters
3. Add to `run_pipeline.sh`
4. Update scheduler configuration

## License

Part of the AI Model Research Team project.
