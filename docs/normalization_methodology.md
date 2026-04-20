# Benchmark Score Normalization Methodology

## Overview

This document describes the normalization methodology used to create comparable benchmark scores across different evaluation setups and versions.

## Data Sources

The normalization system processes data from the following sources:

1. **Hugging Face Leaderboard** (`hf_leaderboard_top100.json`)
   - 100 top models with 6 benchmarks
   - Standardized evaluation setup

2. **Papers with Code**
   - `paperswithcode_mmlu.json`: 50 models with MMLU-Pro scores
   - `paperswithcode_gpqa.json`: 50 models with GPQA scores
   - `paperswithcode_math.json`: 50 models with MATH Level 5 scores

3. **Paper Extractions** (`benchmark_scores.json`)
   - 69 benchmark mentions from 100 arXiv papers
   - Various metrics and confidence levels

## Normalization Rules

### Score Range Normalization

All scores are normalized to a 0-100 scale:

| Input Range | Conversion Rule | Example |
|-------------|-----------------|---------|
| 0-1 | `score * 100` | 0.87 → 87.0 |
| 0-100 | `score` (no change) | 62.5 → 62.5 |
| > 100 | `score` (assumed correct) | 150.0 → 150.0 |

### Benchmark-Specific Rules

#### MMLU / MMLU-Pro
- **Category**: Knowledge
- **Input ranges**: 0-1, 0-100
- **Evaluation setups**:
  - 0-shot (weight: 1.0) - baseline
  - 5-shot (weight: 0.95) - slight advantage from examples
  - 10-shot (weight: 0.9) - larger advantage from examples
  - CoT (weight: 1.0) - chain-of-thought reasoning

#### GPQA (Graduate-Level Google-Proof Q&A)
- **Category**: Reasoning
- **Input ranges**: 0-1, 0-100
- **Evaluation setups**:
  - 0-shot (weight: 1.0)
  - CoT (weight: 1.0)

#### MATH / MATH Level 5
- **Category**: Mathematical Reasoning
- **Input ranges**: 0-1, 0-100
- **Evaluation setups**:
  - 0-shot (weight: 1.0)
  - 4-shot (weight: 0.95)
  - CoT (weight: 1.0)

#### HumanEval
- **Category**: Code Generation
- **Input ranges**: 0-1, 0-100
- **Evaluation setups**:
  - 0-shot (weight: 1.0)

#### BBH (Big Bench Hard)
- **Category**: Reasoning
- **Input ranges**: 0-1, 0-100
- **Evaluation setups**:
  - 3-shot (weight: 1.0) - standard with CoT
  - 0-shot (weight: 0.95)

#### IFEval (Instruction Following)
- **Category**: Instruction Following
- **Input ranges**: 0-100
- **Evaluation setups**:
  - 0-shot (weight: 1.0)

#### MUSR (Multi-Step Reasoning)
- **Category**: Reasoning
- **Input ranges**: 0-100
- **Evaluation setups**:
  - 0-shot (weight: 1.0)

#### GSM8K
- **Category**: Grade School Math
- **Input ranges**: 0-1, 0-100
- **Evaluation setups**:
  - 0-shot (weight: 1.0)
  - 5-shot (weight: 0.95)
  - 8-shot (weight: 0.9)
  - CoT (weight: 1.0)

## Benchmark Version Handling

### Version Mapping

| Legacy Name | Standard Name | Status |
|-------------|---------------|--------|
| mmlu | mmlu | Active, superseded by mmlu_pro |
| mmlu_pro | mmlu_pro | Current standard |
| math_lvl5 | math_lvl5 | MATH subset (Level 5 difficulty) |
| humaneval+ | humaneval+ | Enhanced version |

## Evaluation Setup Weights

Weights are applied to adjust for the advantage provided by different shot counts:

| Setup | Weight | Rationale |
|-------|--------|-----------|
| 0-shot | 1.0 | Baseline - no prior examples |
| 3-shot | 1.0 | Standard for BBH with CoT |
| 4-shot | 0.95 | Slight advantage for MATH |
| 5-shot | 0.95 | Slight advantage from examples |
| 8-shot | 0.90 | Larger advantage from examples |
| 10-shot | 0.90 | Larger advantage from examples |
| CoT | 1.0 | Reasoning approach, not memorization |

## Confidence Levels

Each normalized score includes a confidence level:

| Level | Description | Source |
|-------|-------------|--------|
| High | Direct benchmark score | Leaderboards |
| Medium | Extracted from papers with clear context | Paper extractions |
| Low | Mentioned but not clearly scored | Paper mentions |

## Output Format

### Normalized Score Entry

```json
{
  "model_name": "model/name",
  "source": "hf_leaderboard",
  "architecture": "Qwen2ForCausalLM",
  "parameters_billions": 77.965,
  "submission_date": "2024-11-28",
  "benchmark": "mmlu_pro",
  "original_score": 70.03,
  "normalized_score": 70.03,
  "evaluation_setup": "0-shot",
  "score_range": "0-100",
  "confidence": "high"
}
```

## Statistics

### Current Dataset (as of 2026-04-20)

- **Total normalized scores**: 830
- **Unique models**: 179
- **Benchmarks covered**: 12
  - ifeval, bbh, math_lvl5, gpqa, musr, mmlu_pro
  - auroc, f1, accuracy, ap, math, precision
- **Sources**: 5 (HF Leaderboard, Papers with Code x3, Paper Extractions)

### Confidence Distribution

- High: 616 scores (74.2%)
- Medium: 214 scores (25.8%)

## Usage

### Python Script

```bash
# Run normalization
python scripts/normalize_benchmarks.py

# Output location
data/processed/normalized_scores.json
```

### Accessing Normalized Data

```python
import json

with open('data/processed/normalized_scores.json', 'r') as f:
    data = json.load(f)

# Access scores
scores = data['normalized_scores']

# Filter by benchmark
mmlu_scores = [s for s in scores if s['benchmark'] == 'mmlu_pro']

# Filter by confidence
high_confidence = [s for s in scores if s['confidence'] == 'high']
```

## Limitations

1. **Evaluation Setup Unknown**: Many scores from Papers with Code lack explicit evaluation setup information
2. **Version Confusion**: Some legacy benchmark names may not be correctly mapped
3. **Contextual Scores**: Paper extraction scores may lack model attribution
4. **Weight Subjectivity**: Evaluation setup weights are based on heuristic assumptions

## Future Improvements

1. Add more sophisticated evaluation setup detection from paper text
2. Implement statistical calibration across different setups
3. Add benchmark-specific normalization curves (not just linear scaling)
4. Include temporal normalization (accounting for benchmark saturation over time)
5. Add cross-benchmark correlation analysis

## References

- Hugging Face Open LLM Leaderboard: https://huggingface.co/spaces/open-llm-leaderboard
- Papers with Code: https://paperswithcode.com/
- MMLU Paper: https://arxiv.org/abs/2009.03300
- MMLU-Pro Paper: https://arxiv.org/abs/2406.01574
- GPQA Paper: https://arxiv.org/abs/2311.12022
- MATH Paper: https://arxiv.org/abs/2103.03874
