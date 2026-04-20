# Agent Configuration Directory

This directory contains configurations for each AI agent in the research team.

## Agents

### Literature Review Agent
- **Location:** `literature-review/`
- **Skills:** arxiv, blogwatcher, llm-wiki
- **Responsibilities:**
  - Query arXiv for latest AI model papers
  - Monitor AI research blogs
  - Build knowledge base entries

### Data Analysis Agent
- **Location:** `data-analysis/`
- **Skills:** jupyter-live-kernel, file
- **Responsibilities:**
  - Analyze model performance metrics
  - Create comparison visualizations
  - Statistical analysis

### Writing Agent
- **Location:** `writing/`
- **Skills:** research-paper-writing, llm-wiki
- **Responsibilities:**
  - Draft research summaries
  - Create model comparison reports
  - Documentation

### Integration Agent
- **Location:** `integration/`
- **Skills:** github-pr-workflow, github-issues
- **Responsibilities:**
  - Coordinate between agents
  - Review and merge PRs
  - Maintain project board

## Configuration Format

Each agent directory contains:
- `config.yaml` - Agent settings
- `prompts/` - Role-specific prompts
- `workflows/` - Task workflows