# Benchmark Coverage Report

**Date**: 2026-04-20  
**Source**: 100 arXiv Papers (2026-03-20 to 2026-04-19)  
**Categories**: cs.AI, cs.LG, cs.CL

## Executive Summary

This report documents the extraction of benchmark scores from 100 recent arXiv papers focusing on large language models, multimodal models, and reasoning systems.

| Metric | Value |
|--------|-------|
| Total Papers Analyzed | 100 |
| Papers with Benchmark Mentions | 26 (26.0%) |
| Total Extractions | 69 |
| High Confidence Extractions | 16 (23.2%) |
| Medium Confidence Extractions | 14 (20.3%) |
| Low Confidence Extractions | 39 (56.5%) |

## Benchmark Coverage

### Most Referenced Benchmarks

| Benchmark | Mentions | Type |
|-----------|----------|------|
| Accuracy | 20 | Generic Metric |
| BAGEL | 5 | Domain-Specific |
| UniEditBench | 5 | Multimodal |
| F1 | 4 | Generic Metric |
| SocialGrid | 4 | Multi-Agent |
| MATH | 3 | Mathematical Reasoning |
| CrossMath | 3 | Multimodal Reasoning |
| KA-LogicQuery | 3 | Code Reasoning |
| MEDLEY-BENCH | 3 | Metacognition |
| PLUM | 2 | Linguistic |
| ReCoRD | 2 | NLP |
| Mind's Eye | 2 | Visual Reasoning |
| AP (Academic) | 2 | Academic Exam |
| ReactBench | 2 | Scientific |

### Standard Academic Benchmarks

The following standard benchmarks were mentioned:

- **MMLU** (1 mention): Massive Multitask Language Understanding
- **GSM8K** (1 mention): Grade School Math
- **HumanEval** (0 mentions): Code generation
- **MATH** (3 mentions): Mathematical reasoning
- **GPQA** (0 mentions): Graduate-level questions
- **BBH** (0 mentions): Big-Bench Hard
- **ARC** (0 mentions): AI2 Reasoning Challenge
- **HellaSwag** (0 mentions): Commonsense reasoning
- **TruthfulQA** (0 mentions): Truthfulness

## Score Distribution

### Extracted Scores by Confidence Level

**High Confidence (Explicit benchmark:score patterns)**
- Score range: 10% - 94.65%
- Mean: ~56%
- Examples:
  - GPT-OSS-20B: 84% accuracy on AIME25
  - GPT-OSS-120B: 60% accuracy on task completion
  - Gemini-3-Pro: 60% accuracy on visual tasks
  - Qwen3-VL: 47% accuracy on visual tasks

**Medium Confidence (Performance metrics)**
- Metrics: accuracy, F1, AUROC, precision
- AUROC scores: 0.97 (high)
- F1 scores: 68% - 94.64%

**Low Confidence (Benchmark name mentions)**
- 39 mentions of benchmark names without specific scores
- Indicates benchmark awareness in the community

## Model Coverage

Models identified with benchmark scores:

| Model | Benchmark | Score |
|-------|-----------|-------|
| GPT-OSS-20B | AIME25 | 84% |
| GPT-OSS-120B | SocialGrid | 60% |
| Gemini-3-Pro | Visual Task | 60% |
| Qwen3-VL | Visual Task | 47% |
| Llama-3.2-3B | MMLU/GSM8K | mentioned |

## New Benchmarks Introduced

Several papers introduced new benchmarks:

1. **BAGEL**: Animal knowledge expertise evaluation
2. **CrossMath**: Multimodal reasoning benchmark
3. **Mind's Eye**: Visual abstraction and reasoning
4. **SocialGrid**: Multi-agent planning and social reasoning
5. **MEDLEY-BENCH**: Metacognition evaluation
6. **ReactBench**: Chemical reaction diagram understanding
7. **UniEditBench**: Image and video editing evaluation
8. **KA-LogicQuery**: Code localization reasoning
9. **PLUM**: Politeness in multilingual contexts

## Limitations

1. **Abstract-Only Analysis**: Extraction limited to paper abstracts; full papers may contain more scores
2. **Score Format Variability**: Many papers mention benchmarks without specific scores
3. **Model Name Ambiguity**: Some model references are unclear or refer to variants
4. **Domain-Specific Focus**: Many papers introduce domain-specific rather than general benchmarks

## Quality Validation

### Validation Checks Performed

1. **Score Range Validation**: All scores validated to be within 0-100%
2. **Duplicate Detection**: Identified and handled duplicate extractions
3. **Context Validation**: Verified benchmark mentions appear in relevant context
4. **Confidence Scoring**: Assigned based on pattern specificity:
   - High: Explicit `Benchmark: XX.X%` patterns
   - Medium: Performance metrics with context
   - Low: Benchmark name mentions only

### Confidence Distribution

- **High**: Explicit score patterns (16 extractions)
- **Medium**: Performance metrics (14 extractions)
- **Low**: Generic mentions (39 extractions)

## Recommendations

1. **PDF Mining**: Extend extraction to full paper PDFs for comprehensive coverage
2. **Table Extraction**: Develop table parsing for benchmark comparison tables
3. **Model Normalization**: Standardize model name variations
4. **Temporal Analysis**: Track benchmark score evolution over time
5. **Cross-Reference**: Validate against official benchmark leaderboards

## Files Generated

- `data/processed/benchmark_scores.json`: Structured extraction results
- `notebooks/benchmark_extraction.ipynb`: Extraction methodology
- `scripts/extract_benchmarks.py`: Reusable extraction script
- `docs/research/benchmark_coverage_report.md`: This report

## Conclusion

The extraction successfully identified 69 benchmark mentions across 26 papers (26% coverage). While standard academic benchmarks like MMLU and GSM8K were mentioned, the majority of papers focused on introducing new domain-specific benchmarks rather than reporting scores on existing ones. This reflects the active development of specialized evaluation frameworks in the LLM research community.

The high proportion of low-confidence extractions (56.5%) indicates that many papers reference benchmarks without providing specific numerical scores, suggesting either preliminary work or focus on methodology over quantitative evaluation.
