# Iteration 2 Backlog: Data Collection

**Dates:** May 3 - May 16, 2025 (2 weeks)  
**Goal:** Populate model database and start benchmark collection  
**Sprint Capacity:** 5 stories

---

## Stories

### Story 1.3b: Scrape Lab Announcement Pages
**Assignee:** Literature Review Agent  
**Points:** 5  
**Status:** Ready

**Description:**
Scrape official model announcement pages from major AI labs to populate the model database.

**Tasks:**
- [ ] Scrape OpenAI blog announcements
- [ ] Scrape Anthropic announcements
- [ ] Scrape Google DeepMind announcements
- [ ] Scrape Meta AI announcements
- [ ] Scrape Mistral AI announcements
- [ ] Extract model metadata from announcements
- [ ] Save to database via API

**Labs to Scrape:**
- OpenAI (openai.com/blog)
- Anthropic (anthropic.com/news)
- Google DeepMind (deepmind.google)
- Meta AI (ai.meta.com)
- Mistral AI (mistral.ai/news)

**Acceptance Criteria:**
- [ ] 20+ models extracted from lab announcements
- [ ] Data validated against schema
- [ ] Models saved to database via API
- [ ] Wiki updated with new models

---

### Story 2.1: Identify Key Benchmarks
**Assignee:** Literature Review Agent  
**Points:** 2  
**Status:** Ready

**Description:**
Identify and document the key benchmarks used for evaluating AI models.

**Tasks:**
- [ ] Research standard benchmarks from papers
- [ ] Document benchmark descriptions
- [ ] Identify metrics for each benchmark
- [ ] Create benchmark registry

**Key Benchmarks to Document:**
- MMLU (Massive Multitask Language Understanding)
- HumanEval (Code generation)
- GPQA (Graduate-Level Google-Proof Q&A)
- MATH (Mathematics)
- SWE-bench (Software engineering)
- MMMU (Multimodal understanding)
- MMBench (Multimodal evaluation)
- ARC (Reasoning)
- HellaSwag (Commonsense)

**Acceptance Criteria:**
- [ ] 10+ benchmarks documented
- [ ] Descriptions include task type and metric
- [ ] Wiki updated at wiki/benchmarks/
- [ ] Benchmark registry created

---

### Story 2.2: Extract Benchmark Data from Papers
**Assignee:** Data Analysis Agent  
**Points:** 5  
**Status:** Ready

**Description:**
Extract benchmark scores from the 100 arXiv papers already collected.

**Tasks:**
- [ ] Parse paper abstracts for benchmark mentions
- [ ] Extract benchmark scores where available
- [ ] Map scores to models
- [ ] Create benchmark dataset
- [ ] Validate data quality

**Input:**
- data/raw/arxiv_papers_2026-04-19.json (100 papers)
- data/processed/paper_insights.json (analysis results)

**Output:**
- data/processed/benchmark_scores.json
- Notebooks with extraction methodology

**Acceptance Criteria:**
- [ ] Benchmark scores extracted from papers
- [ ] Data mapped to specific models
- [ ] Quality validation performed
- [ ] Minimum 50 benchmark entries

---

### Story 2.5: Build Data Pipeline (Dev Team)
**Assignee:** Dev Team  
**Points:** 13  
**Status:** Ready

**Description:**
Build automated data pipeline to ingest model and benchmark data into the database.

**Tasks:**
- [ ] Create ingestion service
- [ ] Build arXiv data importer
- [ ] Build lab announcement importer
- [ ] Add data validation
- [ ] Create pipeline scheduler
- [ ] Add error handling and logging

**API Integration:**
- Use existing FastAPI at http://localhost:8000
- POST /api/models for new models
- Extend API for bulk import if needed

**Acceptance Criteria:**
- [ ] Pipeline ingests arXiv data automatically
- [ ] Pipeline ingests lab announcements
- [ ] Data validation enforced
- [ ] Scheduler runs daily/weekly
- [ ] Tests pass

**Handoff Document:** See docs/handoffs/story-2.5-data-pipeline.md

---

### Story 3.1: Create Architecture Taxonomy
**Assignee:** Literature Review Agent  
**Points:** 3  
**Status:** Ready

**Description:**
Create a taxonomy for classifying AI model architectures.

**Tasks:**
- [ ] Research architecture types from papers
- [ ] Define taxonomy categories
- [ ] Create classification system
- [ ] Document in wiki

**Architecture Categories:**
- Dense Transformers (GPT, Llama)
- Mixture of Experts (MoE) - Mixtral, Switch
- State Space Models (SSM) - Mamba
- Multimodal - GPT-4V, Gemini
- Reasoning - o3, test-time compute
- Other - Novel architectures

**Acceptance Criteria:**
- [ ] Taxonomy defined with 6+ categories
- [ ] Each category documented with examples
- [ ] Classification criteria defined
- [ ] Wiki updated at wiki/architectures/

---

## Sprint Board

| Story | Assignee | Points | Status |
|-------|----------|--------|--------|
| 1.3b Scrape Lab Announcements | Literature Review Agent | 5 | Ready |
| 2.1 Identify Benchmarks | Literature Review Agent | 2 | Ready |
| 2.2 Extract Benchmark Data | Data Analysis Agent | 5 | Ready |
| 2.5 Data Pipeline | Dev Team | 13 | Ready |
| 3.1 Architecture Taxonomy | Literature Review Agent | 3 | Ready |

**Total Points:** 28

---

## Dependencies

```
Story 2.1 (Benchmarks) 
    │
    ├── Story 2.2 (Extract Data)
    │
    └── Story 2.5 (Pipeline)

Story 1.3b (Lab Scraping)
    │
    └── Story 2.5 (Pipeline)

Story 3.1 (Taxonomy) - Independent
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

1. **Rate limiting on lab websites** - Implement delays and caching
2. **Inconsistent data formats** - Build flexible parsers
3. **Dev Team capacity** - Story 2.5 is large; monitor progress

---

## Notes

- Focus on data quality over quantity
- Validate all data against schema
- Document all assumptions
- Iteration 3 will build on this data

**Sprint Goal:** Database populated with models and benchmarks