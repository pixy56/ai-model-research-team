# Iteration 1 Backlog: Foundation

**Dates:** April 19 - May 2, 2025 (2 weeks)  
**Goal:** Set up infrastructure and start model tracking  
**Sprint Capacity:** 5 stories

---

## Stories

### Story 1.1: Model Metadata Schema
**Assignee:** Literature Review Agent  
**Points:** 3  
**Status:** Ready

**Description:**
Create a standardized schema for AI model metadata to ensure consistent data across the research team.

**Tasks:**
- [ ] Define JSON schema for model metadata
- [ ] Fields: name, lab, release_date, architecture, parameters, context_window, benchmarks, paper_url, announcement_url
- [ ] Create validation script
- [ ] Document schema in wiki

**Acceptance Criteria:**
- [ ] Schema documented in `docs/schemas/model-metadata.json`
- [ ] Validation script passes sample data
- [ ] Wiki updated with schema documentation

**Agent Context:**
```
Create a JSON schema for AI model metadata with these fields:
- name: string (model name, e.g., "GPT-4", "Claude 3")
- lab: string (research lab, e.g., "OpenAI", "Anthropic")
- release_date: ISO date string
- architecture: enum ["dense-transformer", "moe", "ssm", "multimodal", "reasoning", "other"]
- parameters: number (in billions) or "unknown"
- context_window: number (in tokens) or "unknown"
- benchmarks: object with benchmark names as keys
- paper_url: string (arXiv or paper URL)
- announcement_url: string (blog post URL)
- tags: array of strings

Save schema to: docs/schemas/model-metadata.json
Create validation script: scripts/validate-model-schema.py
```

---

### Story 1.2: arXiv Query Automation
**Assignee:** Literature Review Agent  
**Points:** 5  
**Status:** Ready

**Description:**
Build automated queries to fetch latest AI model papers from arXiv.

**Tasks:**
- [ ] Set up arXiv API queries for AI model papers
- [ ] Filter by categories: cs.AI, cs.LG, cs.CL
- [ ] Filter by date range (last 30 days)
- [ ] Keywords: "large language model", "multimodal", "reasoning"
- [ ] Save results to data/raw/arxiv_papers.json

**Acceptance Criteria:**
- [ ] Script queries arXiv successfully
- [ ] Filters by date and category
- [ ] Saves structured JSON with paper metadata
- [ ] Minimum 50 papers per query

**Agent Context:**
```
Use the arxiv skill to query for AI model papers.

Query parameters:
- Categories: cs.AI, cs.CL, cs.LG
- Date range: last 30 days
- Keywords: "large language model" OR "multimodal" OR "reasoning" OR "foundation model"

Output format:
{
  "query_date": "2025-04-19",
  "papers": [
    {
      "arxiv_id": "...",
      "title": "...",
      "authors": [...],
      "abstract": "...",
      "published": "...",
      "categories": [...],
      "pdf_url": "..."
    }
  ]
}

Save to: data/raw/arxiv_papers_YYYY-MM-DD.json
```

---

### Story 1.3: Model Database (Dev Team)
**Assignee:** Dev Team  
**Points:** 8  
**Status:** Ready

**Description:**
Create a database to store and query AI model information.

**Handoff from AI Agent:**
- Schema: `docs/schemas/model-metadata.json`
- Sample data: `data/raw/sample-models.json`

**Tasks:**
- [ ] Set up database (SQLite/PostgreSQL)
- [ ] Create tables matching schema
- [ ] Build data ingestion script
- [ ] Create API endpoints for CRUD operations
- [ ] Add search/filter functionality

**Acceptance Criteria:**
- [ ] Database schema created
- [ ] API supports: list, get, create, update, delete
- [ ] Search by lab, architecture, date range
- [ ] Tests pass
- [ ] Documentation updated

**Dev Team Spec:**
```
Database: SQLite (for now, easy to migrate to PostgreSQL)

Tables:
- models: id, name, lab, release_date, architecture, parameters, context_window, paper_url, announcement_url, created_at, updated_at
- benchmarks: id, model_id, benchmark_name, score, metric
- tags: id, model_id, tag_name

API Endpoints:
GET /api/models - List all models (with pagination)
GET /api/models/:id - Get specific model
POST /api/models - Create new model
PUT /api/models/:id - Update model
DELETE /api/models/:id - Delete model
GET /api/models/search?q=... - Search models

Tech Stack:
- Python FastAPI
- SQLAlchemy ORM
- Pydantic models
```

---

### Story 1.4: Set up llm-wiki
**Assignee:** Literature Review Agent  
**Points:** 2  
**Status:** Ready

**Description:**
Initialize and configure llm-wiki knowledge base for the research team.

**Tasks:**
- [ ] Initialize llm-wiki in wiki/ directory
- [ ] Configure categories (models, benchmarks, labs, architectures)
- [ ] Set up auto-ingestion from agents
- [ ] Document wiki structure

**Acceptance Criteria:**
- [ ] llm-wiki initialized
- [ ] Config file created: `wiki/.llm-wiki-config.yaml`
- [ ] Category directories created
- [ ] README documented

**Agent Context:**
```
Initialize llm-wiki for AI model research.

Categories to set up:
1. models/llms - Large language models
2. models/multimodal - Multimodal models
3. models/reasoning - Reasoning models
4. benchmarks - Benchmark information
5. labs - Research lab profiles
6. architectures - Architecture patterns
7. research-findings - Key insights

Config file location: wiki/.llm-wiki-config.yaml
Include auto_ingest: true
```

---

### Story 1.5: Knowledge Categories
**Assignee:** Literature Review Agent  
**Points:** 2  
**Status:** Ready

**Description:**
Create initial content structure for wiki categories.

**Tasks:**
- [ ] Create template files for each category
- [ ] Document category structure
- [ ] Add placeholder content for major labs
- [ ] Link to relevant resources

**Acceptance Criteria:**
- [ ] All 7 categories have README.md
- [ ] Templates created for model entries
- [ ] Lab profiles created for top 6 labs
- [ ] Cross-links between categories

**Agent Context:**
```
Create wiki structure for AI model research.

For each category in wiki/, create:
1. README.md with category description
2. Template files for entries

Categories:
- models/: Organize by type (llms/, multimodal/, reasoning/)
- benchmarks/: List major benchmarks with descriptions
- labs/: Create profiles for OpenAI, Anthropic, Google, Meta, Mistral, Microsoft
- architectures/: Document architecture types
- research-findings/: Template for insights

Include navigation links between pages.
```

---

## Sprint Board

| Story | Assignee | Points | Status |
|-------|----------|--------|--------|
| 1.1 Model Metadata Schema | Literature Review Agent | 3 | Ready |
| 1.2 arXiv Query Automation | Literature Review Agent | 5 | Ready |
| 1.3 Model Database | Dev Team | 8 | Ready |
| 1.4 Set up llm-wiki | Literature Review Agent | 2 | Ready |
| 1.5 Knowledge Categories | Literature Review Agent | 2 | Ready |

**Total Points:** 20

---

## Daily Standup Template

```
## [Date] - Iteration 1 Standup

### Literature Review Agent
- Yesterday: 
- Today: 
- Blockers: 

### Data Analysis Agent
- Yesterday: 
- Today: 
- Blockers: 

### Writing Agent
- Yesterday: 
- Today: 
- Blockers: 

### Integration Agent
- Yesterday: 
- Today: 
- Blockers: 

### Dev Team
- Yesterday: 
- Today: 
- Blockers: 
```

---

## Definition of Done

### For AI Agent Stories:
- [ ] Spec compliance review passed
- [ ] Code quality review passed
- [ ] Output validated
- [ ] Wiki updated (if applicable)
- [ ] Handoff document created (if Dev Team involved)

### For Dev Team Stories:
- [ ] Code implemented and tested
- [ ] PR reviewed and merged
- [ ] Documentation updated
- [ ] Integration tests pass

---

## Risks

1. **Dev Team capacity** - Story 1.3 is large; monitor progress
2. **arXiv rate limits** - Implement caching and backoff
3. **Schema changes** - Keep flexible for iteration 2

---

## Notes

- Focus on getting infrastructure working
- Don't worry about completeness of data
- Document everything for iteration 2

**Sprint Goal:** Foundation ready for data collection in Iteration 2