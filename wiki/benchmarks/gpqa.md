---
title: GPQA (Graduate-Level Google-Proof Q&A)
category: benchmark
author: AI Model Research Team
date: 2026-04-20
tags: [graduate-level, expert-reasoning, science, difficult-qa]
status: active
---

# GPQA (Graduate-Level Google-Proof Q&A)

## Overview

**Benchmark Name:** GPQA  
**Full Name:** Graduate-Level Google-Proof Q&A  
**Category:** Reasoning Benchmark - Expert Level  
**First Introduced:** 2023  
**Maintained By:** NYU, Meta AI, and collaborators

## Description

GPQA is a challenging benchmark consisting of graduate-level multiple-choice questions in biology, physics, and chemistry. The questions are designed to be "Google-proof" - meaning they cannot be easily answered by simple web searches or memorization.

The benchmark has three variants:
- **GPQA Diamond:** 448 questions, highest quality
- **GPQA Extended:** 1,670 questions, includes more borderline cases
- **GPQA Main:** 546 questions, original dataset

## Purpose

GPQA was created to:
1. **Test expert-level reasoning** beyond standard benchmarks
2. **Evaluate deep understanding** of scientific concepts
3. **Measure capabilities** at the frontier of AI reasoning
4. **Provide a difficult benchmark** that distinguishes top models

## Dataset Details

### Size
- **GPQA Diamond:** 448 questions
- **GPQA Extended:** 1,670 questions
- **GPQA Main:** 546 questions

### Format
- Multiple-choice questions (4-5 options)
- Questions written by domain experts (PhD level)
- Expert validation to ensure quality

### Task Types
- Scientific reasoning
- Multi-step problem solving
- Domain-specific knowledge application

## Evaluation Metrics

| Metric | Description |
|--------|-------------|
| Accuracy | Percentage of questions answered correctly |
| Expert Comparison | Performance relative to PhD-level experts |

## Score Ranges

| Level | Score Range | Description |
|-------|-------------|-------------|
| Random | ~25% | Random guessing |
| Novice | 30-40% | Basic understanding |
| Competent | 40-60% | Good domain knowledge |
| Expert | 60-80% | PhD-level performance |
| Superhuman | 80%+ | Beyond typical expert performance |

## Current Leaderboard - GPQA Diamond (2025)

| Rank | Model | Score | Date |
|------|-------|-------|------|
| 1 | o3-mini (high) | 86.0% | 2025-01 |
| 2 | Claude 3.7 Sonnet | 74.0% | 2025-02 |
| 3 | Gemini 2.0 Pro | 74.2% | 2025-02 |
| 4 | GPT-4.5 | 71.4% | 2025-02 |
| 5 | Llama 3.1 405B | 50.0% | 2024-07 |

## Historical Progress

| Year | Diamond Score | Model |
|------|---------------|-------|
| 2023 | 39.8% | GPT-4 |
| 2024 | 53.6% | Claude 3 Opus |
| 2024 | 65.2% | o1-preview |
| 2025 | 74.0% | Claude 3.7 Sonnet |
| 2025 | 86.0% | o3-mini |

## Comparison with Human Experts

| Group | GPQA Diamond Score |
|-------|---------------------|
| Non-expert Humans | ~34% |
| Expert Humans (Same Domain) | ~65% |
| Expert Humans (Different Domain) | ~41% |
| Best AI Models (2025) | ~86% |

## Limitations

1. **Limited domains** only biology, chemistry, physics
2. **Multiple-choice format** may not capture full reasoning
3. **Small dataset** especially Diamond subset
4. **English only** no multilingual coverage
5. **Expert bias** questions may reflect specific expertise areas

## Related Benchmarks

- [MMLU](mmlu.md) - Broader knowledge assessment
- [MATH](math.md) - Competition mathematics
- [ARC-AGI](arc.md) - Abstract reasoning
- [TheoremQA](https://arxiv.org/abs/2305.12524) - Theorem proving questions

## Resources

- **Official Site:** https://github.com/idavidrein/gpqa
- **Paper:** https://arxiv.org/abs/2311.12022
- **Code:** https://github.com/idavidrein/gpqa
- **Dataset:** https://huggingface.co/datasets/Idavidrein/gpqa
- **Leaderboard:** Papers with Code GPQA section

## Categories Tested

| Domain | Topics |
|--------|--------|
| Biology | Molecular biology, genetics, biochemistry, cell biology |
| Chemistry | Organic, inorganic, physical chemistry |
| Physics | Quantum mechanics, thermodynamics, electromagnetism |

## References

1. Rein, D., et al. (2023). "GPQA: A Graduate-Level Google-Proof Q&A Benchmark." arXiv:2311.12022.
2. Papers with Code GPQA Leaderboard

---
*Last updated: 2026-04-20 by AI Model Research Team*
