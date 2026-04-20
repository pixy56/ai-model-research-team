# AI Model Research Wiki

This is the knowledge base for the AI Model Research Team.

## Structure

```
wiki/
├── README.md                 # This file
├── .llm-wiki-config.yaml     # Wiki configuration
├── index.md                  # Main navigation
│
├── models/                   # Model information
│   ├── README.md
│   ├── llms/                 # Large Language Models
│   ├── multimodal/           # Multimodal models
│   └── reasoning/            # Reasoning-focused models
│
├── benchmarks/               # Benchmark data
│   └── README.md
│
├── labs/                     # Research lab profiles
│   └── README.md
│
├── architectures/            # Architecture documentation
│   └── README.md
│
├── research-findings/        # Research insights
│   ├── README.md
│   ├── papers/               # Paper summaries
│   ├── insights/             # Analysis insights
│   └── trends/               # Emerging trends
│
└── templates/                # Entry templates
    ├── model-template.md
    ├── benchmark-template.md
    ├── lab-template.md
    ├── architecture-template.md
    └── research-template.md
```

## Quick Links

- [Main Index](index.md) - Complete wiki navigation
- [Latest Models](models/) - Tracked AI models
- [Top Benchmarks](benchmarks/) - Evaluation benchmarks
- [Research Labs](labs/) - Lab profiles and releases
- [Architecture Trends](architectures/) - Architecture innovations
- [Research Findings](research-findings/) - Paper summaries and insights

## Usage

This wiki is maintained by the Literature Review Agent and Writing Agent.

Knowledge is ingested from:
- **arXiv papers** - Automated daily ingestion (cs.AI, cs.LG, cs.CL)
- **Lab announcements** - Blog and news monitoring
- **Benchmark leaderboards** - Automated tracking
- **Analysis notebooks** - Team research insights

### Adding Content

**Manual Entry:**
1. Copy the appropriate template from `templates/`
2. Fill in the required information
3. Save to the correct category directory

**Auto-Ingestion:**
```bash
# Ingest arXiv papers
python scripts/ingest_to_wiki.py --source arxiv --input data/raw/arxiv_papers_*.json

# Dry run (preview changes)
python scripts/ingest_to_wiki.py --source arxiv --dry-run
```

## Configuration

Wiki settings are in `.llm-wiki-config.yaml`:
- Categories and structure
- Ingestion sources
- Query settings
- Template configuration

## Statistics

| Category | Count | Last Updated |
|----------|-------|--------------|
| Models | TBD | 2026-04-19 |
| Benchmarks | 10+ | 2026-04-19 |
| Labs | 9 | 2026-04-19 |
| Research Papers | 20+ | 2026-04-19 |

## Contributing

- **Literature Review Agent**: Updates research findings, paper summaries
- **Data Analysis Agent**: Maintains benchmarks and model statistics
- **Writing Agent**: Lab profiles, architecture documentation

---

*This wiki is automatically maintained by the AI Model Research Team.*
