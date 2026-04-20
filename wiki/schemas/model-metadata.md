# Model Metadata Schema

This document describes the JSON schema for AI model metadata used by the research team.

## Overview

The Model Metadata Schema provides a standardized format for documenting AI models, ensuring consistent data across the research team. This schema supports tracking of LLMs, multimodal models, and reasoning models.

## Schema Location

- **Schema File**: `docs/schemas/model-metadata.json`
- **Validation Script**: `scripts/validate-model-schema.py`
- **Sample Data**: `data/sample-model.json`

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Model name (e.g., "GPT-4", "Claude 3") |
| `lab` | string | Research lab or organization (e.g., "OpenAI", "Anthropic") |
| `release_date` | string (ISO date) | Release date in YYYY-MM-DD format |
| `architecture` | enum | Model architecture type |
| `parameters` | number or "unknown" | Number of parameters in billions |
| `context_window` | number or "unknown" | Context window size in tokens |
| `benchmarks` | object | Benchmark scores with names as keys |
| `paper_url` | string (URI) | Link to research paper (arXiv or other) |
| `announcement_url` | string (URI) | Link to announcement blog post |

## Architecture Types

The following architecture types are supported:

| Value | Description |
|-------|-------------|
| `dense-transformer` | Dense Transformer architecture |
| `moe` | Mixture of Experts |
| `ssm` | State Space Model (e.g., Mamba) |
| `multimodal` | Multimodal architecture |
| `reasoning` | Reasoning-focused architecture |
| `other` | Other architectures |

## Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `tags` | array of strings | Tags for categorization (e.g., ["multimodal", "reasoning"]) |

## Example

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
    "humaneval": 67.0,
    "mgsm": 61.3,
    "drop": 80.9
  },
  "paper_url": "https://arxiv.org/abs/2303.08774",
  "announcement_url": "https://openai.com/blog/gpt-4",
  "tags": ["multimodal", "reasoning", "instruction-tuned"]
}
```

## Validation

### Using the Validation Script

Validate a single file:
```bash
python scripts/validate-model-schema.py path/to/model.json
```

Run built-in tests:
```bash
python scripts/validate-model-schema.py --test
```

### Programmatic Usage

```python
import json
from jsonschema import validate, ValidationError

# Load schema
with open('docs/schemas/model-metadata.json', 'r') as f:
    schema = json.load(f)

# Validate data
try:
    validate(instance=model_data, schema=schema)
    print("Valid!")
except ValidationError as e:
    print(f"Invalid: {e.message}")
```

## Benchmarks

The `benchmarks` object supports any benchmark name as a key. Common benchmarks include:

- `mmlu` - Massive Multitask Language Understanding
- `humaneval` - HumanEval (code generation)
- `mgsm` - Multilingual Grade School Math
- `drop` - Discrete Reasoning Over Paragraphs
- `gsm8k` - Grade School Math 8K
- `hellaswag` - HellaSwag (commonsense reasoning)
- `arc` - AI2 Reasoning Challenge

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2024-01-19 | Initial schema creation |

## See Also

- [Research Findings](../research-findings/)
- [Model Database](../models/)
- [Benchmarks](../benchmarks/)
