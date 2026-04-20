# AI Model Research Wiki - Index

**Version:** 1.0  
**Last Updated:** 2026-04-19  
**Maintained by:** AI Model Research Team

---

## Quick Navigation

| Category | Description | Entries |
|----------|-------------|---------|
| [Models](models/) | Individual model information and specifications | [LLMs](models/llms/) · [Multimodal](models/multimodal/) · [Reasoning](models/reasoning/) |
| [Benchmarks](benchmarks/) | Benchmark information, scores, and leaderboards | [Core](benchmarks/#core-benchmarks) · [Multimodal](benchmarks/#multimodal-benchmarks) |
| [Labs](labs/) | Research lab profiles and releases | [OpenAI](labs/openai.md) · [Anthropic](labs/anthropic.md) · [Google](labs/google.md) |
| [Architectures](architectures/) | Architecture patterns and innovations | [Transformers](architectures/) · [MoE](architectures/) · [SSM](architectures/) |
| [Research Findings](research-findings/) | Key research insights and discoveries | [Papers](research-findings/papers/) · [Insights](research-findings/insights/) |

---

## Recent Updates

### 2026-04-19
- Initial wiki setup with automated ingestion
- Added 100 arXiv papers from April 2026
- Created category templates

---

## Wiki Structure

```
wiki/
├── README.md                 # This file
├── .llm-wiki-config.yaml     # Wiki configuration
├── index.md                  # Main navigation (this file)
│
├── models/                   # Model information
│   ├── README.md
│   ├── llms/                 # Large Language Models
│   ├── multimodal/           # Multimodal models
│   └── reasoning/            # Reasoning-focused models
│
├── benchmarks/               # Benchmark data
│   ├── README.md
│   └── *.md                  # Individual benchmarks
│
├── labs/                     # Research lab profiles
│   ├── README.md
│   └── *.md                  # Lab profiles
│
├── architectures/            # Architecture documentation
│   └── README.md
│
├── research-findings/        # Research insights
│   ├── README.md
│   ├── papers/               # Paper summaries
│   └── insights/             # Analysis insights
│
└── templates/                # Entry templates
    ├── model-template.md
    ├── benchmark-template.md
    ├── lab-template.md
    ├── architecture-template.md
    └── research-template.md
```

---

## Usage

### Adding New Content

1. **Manual Entry**: Copy the appropriate template from `templates/` and fill in the details
2. **Auto-Ingestion**: Run `scripts/ingest_to_wiki.py` to automatically import from configured sources

### Searching

Use the category indices or search by tags. All entries include metadata for filtering.

### Contributing

- Literature Review Agent: Updates research findings
- Data Analysis Agent: Updates benchmarks and model stats
- Writing Agent: Maintains lab profiles and architecture docs

---

## Data Sources

- **arXiv**: Automated daily ingestion of cs.AI, cs.LG, cs.CL papers
- **Lab Blogs**: Monitored for new model announcements
- **Analysis Notebooks**: Insights from team analysis

---

## Statistics

| Category | Count | Last Updated |
|----------|-------|--------------|
| Models | TBD | 2026-04-19 |
| Benchmarks | TBD | 2026-04-19 |
| Labs | TBD | 2026-04-19 |
| Research Papers | 100 | 2026-04-19 |

---

*This wiki is automatically maintained by the AI Model Research Team agents.*
