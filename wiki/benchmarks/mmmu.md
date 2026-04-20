---
title: MMMU (Massive Multi-discipline Multimodal Understanding)
category: benchmark
author: AI Model Research Team
date: 2026-04-20
tags: [multimodal, vision-language, college-level, comprehensive]
status: active
---

# MMMU

## Overview

**Benchmark Name:** MMMU  
**Full Name:** Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark  
**Category:** Multimodal Benchmark  
**First Introduced:** 2023  
**Maintained By:** Carnegie Mellon University, Microsoft Research

## Description

MMMU is a comprehensive multimodal benchmark designed to evaluate large multimodal models on college-level knowledge and reasoning tasks. It requires understanding and reasoning across multiple modalities including images, diagrams, charts, and text.

The benchmark emphasizes:
- **Expert-level knowledge** across disciplines
- **Multimodal reasoning** combining vision and language
- **College-level difficulty** requiring deep understanding

## Purpose

MMMU was created to:
1. **Test college-level multimodal understanding**
2. **Evaluate cross-modal reasoning** capabilities
3. **Assess expert knowledge** with visual components
4. **Provide challenging** evaluation for multimodal models

## Dataset Details

### Size
- **Total Questions:** 11.5K
- **Training:** Not publicly released
- **Validation:** ~1,150
- **Test:** ~10,350

### Format
- Multiple-choice questions (usually 4 options)
- Questions require analyzing images, charts, diagrams
- College-level difficulty across disciplines

### Task Types
- Image understanding with reasoning
- Chart and graph interpretation
- Diagram analysis
- Multimodal question answering

## Evaluation Metrics

| Metric | Description |
|--------|-------------|
| Accuracy | Percentage of questions answered correctly |
| Per-subject Accuracy | Breakdown by discipline |

## Score Ranges

| Level | Score Range | Description |
|-------|-------------|-------------|
| Random | ~25% | Random guessing |
| Basic | 35-50% | Basic multimodal understanding |
| Competent | 50-65% | Good college-level reasoning |
| Advanced | 65-75% | Strong multimodal capabilities |
| Expert | 75%+ | Near-expert performance |

## Current Leaderboard (2025)

| Rank | Model | Score | Date |
|------|-------|-------|------|
| 1 | Gemini 2.0 Pro | 82.4% | 2025-02 |
| 2 | GPT-4o | 69.1% | 2024-05 |
| 3 | Claude 3.7 Sonnet | 68.3% | 2025-02 |
| 4 | Gemini 1.5 Pro | 72.7% | 2024-02 |
| 5 | Llama 3.2 90B Vision | 72.1% | 2024-09 |

## Historical Progress

| Year | Score | Model |
|------|-------|-------|
| 2023 | 34.0% | GPT-4V |
| 2024 | 56.8% | Gemini 1.0 Ultra |
| 2024 | 72.7% | Gemini 1.5 Pro |
| 2025 | 82.4% | Gemini 2.0 Pro |

## Disciplines Tested

| Discipline | Topics | % of Dataset |
|------------|--------|--------------|
| Art | Art history, theory, design | ~10% |
| Business | Finance, accounting, marketing | ~10% |
| Health & Medicine | Anatomy, diagnosis, treatment | ~15% |
| Science & Technology | Physics, chemistry, engineering | ~25% |
| Humanities & Social Science | Psychology, sociology, history | ~20% |
| Math | Calculus, statistics, algebra | ~20% |

## Limitations

1. **College-centric** may not reflect general knowledge
2. **Multiple-choice format** limited answer types
3. **English only** limited language diversity
4. **Image quality** varies across sources
5. **Domain expertise** requires specialized knowledge

## Related Benchmarks

- [MMBench](mmbench.md) - Comprehensive multimodal evaluation
- [ChartQA](https://github.com/vis-nlp/ChartQA) - Chart understanding
- [TextVQA](https://textvqa.org/) - Text in images
- [DocVQA](https://rrc.cvc.uab.es/?ch=17) - Document understanding

## Resources

- **Official Site:** https://mmmu-benchmark.github.io/
- **Paper:** https://arxiv.org/abs/2311.16502
- **Code:** https://github.com/MMMU-Benchmark/MMMU
- **Dataset:** https://huggingface.co/datasets/MMMU/MMMU
- **Leaderboard:** https://mmmu-benchmark.github.io/

## References

1. Yue, X., et al. (2023). "MMMU: A Massive Multi-discipline Multimodal Understanding and Reasoning Benchmark for Expert AGI." arXiv:2311.16502.

---
*Last updated: 2026-04-20 by AI Model Research Team*
