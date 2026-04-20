# Dev Team Handoff: Story 2.6 - Comparison Dashboard

**Story:** Build interactive web dashboard for comparing model benchmarks  
**Points:** 13  
**Priority:** Medium  
**Dependencies:** Story 2.4 (Complete - normalized scores available)

---

## Overview

Create an interactive web dashboard that allows users to compare AI model performance across benchmarks. The dashboard should integrate with our existing FastAPI backend and provide visual comparisons.

---

## Data Sources

### Primary Data
- **File:** `data/processed/normalized_scores.json`
- **Size:** 830 normalized scores
- **Models:** 179 unique models
- **Benchmarks:** 12 (MMLU, MMLU-Pro, GPQA, MATH, HumanEval, BBH, IFEval, MUSR, GSM8K, etc.)

### Data Schema (normalized_scores.json)
```json
{
  "metadata": {
    "total_scores": 830,
    "unique_models": 179,
    "benchmarks": ["mmlu", "mmlu-pro", "gpqa", ...],
    "sources": ["hf_leaderboard", "paperswithcode", "papers", "lab_announcements", "manual"]
  },
  "scores": [
    {
      "model": "model-name",
      "benchmark": "mmlu-pro",
      "raw_score": 70.03,
      "normalized_score": 70.03,
      "original_range": "0-100",
      "evaluation_setup": "0-shot",
      "source": "paperswithcode",
      "date": "2025-04"
    }
  ],
  "models": {
    "model-name": {
      "lab": "Organization",
      "architecture": "Dense Transformer",
      "parameters": "70B",
      "release_date": "2025-01"
    }
  }
}
```

---

## Requirements

### Functional Requirements

1. **Model Comparison Table**
   - Display models in sortable table
   - Columns: Model name, Lab, Architecture, Parameters, Benchmark scores
   - Sort by any column
   - Filter by lab, architecture, date range

2. **Benchmark Filtering**
   - Select which benchmarks to display
   - Toggle between normalized and raw scores
   - Filter by score range

3. **Visualizations**
   - Bar chart: Model comparison for selected benchmark
   - Radar chart: Multi-benchmark comparison for selected models
   - Distribution histogram: Score distribution across models

4. **Leaderboard View**
   - Rank models by selected benchmark
   - Show top N (configurable: 10, 25, 50, 100)
   - Highlight new releases (last 30 days)

5. **Export**
   - Export filtered data to CSV
   - Export to JSON
   - Export charts as PNG/SVG

### Non-Functional Requirements

- **Performance:** Page load < 2s, table render < 500ms for 100 rows
- **Responsive:** Works on desktop and tablet
- **Accessibility:** WCAG 2.1 AA compliant
- **Browser Support:** Chrome, Firefox, Safari (last 2 versions)

---

## Technical Stack

**Backend:**
- Existing FastAPI (`src/api/main.py`)
- SQLite database (can migrate normalized_scores.json)

**Frontend:**
- React or Vue.js (recommend React with TypeScript)
- Chart library: Chart.js or Recharts
- UI library: Tailwind CSS or Material-UI

**API Endpoints Needed:**
```
GET /api/models - List all models with metadata
GET /api/models/{id}/scores - Get scores for specific model
GET /api/benchmarks - List available benchmarks
GET /api/scores?benchmark=X&lab=Y - Filtered scores
GET /api/leaderboard?benchmark=X&limit=N - Ranked leaderboard
```

---

## Acceptance Criteria

- [ ] Dashboard with model comparison tables
- [ ] Benchmark filtering and sorting
- [ ] Charts for benchmark distributions
- [ ] Leaderboard rankings view
- [ ] Export to CSV/JSON
- [ ] Responsive design
- [ ] Integration tests pass

---

## Files to Reference

- `data/processed/normalized_scores.json` - Main data source
- `src/api/main.py` - Existing API (extend this)
- `docs/normalization_methodology.md` - Understanding the data
- `scripts/normalize_benchmarks.py` - Reference for data processing

---

## Notes

- The normalized scores are already cleaned and ready for display
- Consider caching leaderboard queries (data updates weekly)
- Model metadata is in the "models" section of normalized_scores.json
- Some models may have missing scores for certain benchmarks (handle gracefully)

---

**Created:** April 20, 2025  
**Handoff By:** AI Research Team
