---
title: MMLU (Massive Multitask Language Understanding)
category: benchmark
author: AI Model Research Team
date: 2026-04-20
tags: [language-understanding, knowledge, multitask, stem, humanities]
status: active
---

# MMLU (Massive Multitask Language Understanding)

## Overview

**Benchmark Name:** MMLU  
**Full Name:** Massive Multitask Language Understanding  
**Category:** Core Benchmark - Knowledge & Reasoning  
**First Introduced:** 2020  
**Maintained By:** UC Berkeley, OpenAI, and collaborators

## Description

MMLU is a comprehensive benchmark designed to evaluate the breadth and depth of knowledge in language models across 57 diverse subjects. It tests models on their ability to understand and reason about topics ranging from elementary mathematics to professional law and medicine.

The benchmark consists of multiple-choice questions covering:
- **STEM subjects:** Mathematics, physics, chemistry, biology, computer science, engineering
- **Humanities:** History, philosophy, literature, art
- **Social Sciences:** Psychology, sociology, economics, political science
- **Professional subjects:** Law, medicine, finance, accounting

## Purpose

MMLU was created to address the limitations of narrow benchmarks by testing models on:
1. **Breadth of knowledge** across many domains
2. **Depth of understanding** from elementary to professional levels
3. **Zero-shot and few-shot learning** capabilities
4. **Factuality and reasoning** in diverse contexts

## Dataset Details

### Size
- **Total Questions:** ~15,908
- **Training:** Not publicly released (held-out test set)
- **Validation:** ~285 questions per subject
- **Test:** ~140 questions per subject

### Format
- Multiple-choice questions (4 options: A, B, C, D)
- Questions sourced from textbooks, exams, and professional tests
- Covers 57 subjects across difficulty levels

### Task Types
- Zero-shot question answering
- Few-shot question answering
- Chain-of-thought reasoning

## Evaluation Metrics

| Metric | Description |
|--------|-------------|
| Accuracy | Percentage of questions answered correctly |
| Per-subject Accuracy | Accuracy broken down by individual subject |
| Macro-average | Average accuracy across all subjects |

## Score Ranges

| Level | Score Range | Description |
|-------|-------------|-------------|
| Random | ~25% | Random guessing baseline |
| Basic | 40-60% | Elementary understanding |
| Competent | 60-80% | High school to undergraduate level |
| Expert | 80-90% | Graduate to professional level |
| State-of-the-art | 90%+ | Near or above human expert performance |

## Current Leaderboard (2025)

| Rank | Model | Score | Date |
|------|-------|-------|------|
| 1 | o3-mini (high) | 92.4% | 2025-01 |
| 2 | GPT-4.5 | 90.2% | 2025-02 |
| 3 | Claude 3.7 Sonnet | 90.8% | 2025-02 |
| 4 | Gemini 2.0 Pro | 89.8% | 2025-02 |
| 5 | Llama 3.1 405B | 85.2% | 2024-07 |

## Historical Progress

| Year | Top Score | Model |
|------|-----------|-------|
| 2020 | 43.9% | GPT-3 |
| 2022 | 67.5% | Chinchilla |
| 2023 | 86.4% | GPT-4 |
| 2024 | 89.8% | Gemini 2.0 Pro |
| 2025 | 92.4% | o3-mini |

## Limitations

1. **Multiple-choice format** may not capture open-ended reasoning
2. **Static dataset** susceptible to contamination from training data
3. **English-centric** limited multilingual coverage
4. **Knowledge cutoff** questions may become outdated
5. **Memorization vs. reasoning** difficult to distinguish

## Related Benchmarks

- [MMLU-Pro](https://arxiv.org/abs/2406.01574) - Enhanced version with more difficult questions
- [MMLU-Redux](https://github.com/simpler-conversation/MMLU-Redux) - Human-verified subset
- [MMMLU](https://huggingface.co/datasets/openai/MMMLU) - Multilingual extension

## Resources

- **Official Site:** https://paperswithcode.com/sota/multi-task-language-understanding-on-mmlu
- **Paper:** https://arxiv.org/abs/2009.03300
- **Code:** https://github.com/hendrycks/test
- **Dataset:** https://huggingface.co/datasets/cais/mmlu
- **Leaderboard:** https://huggingface.co/spaces/open-llm-leaderboard

## Categories Tested

| Category | Subjects |
|----------|----------|
| STEM (18) | abstract_algebra, astronomy, college_biology, college_chemistry, college_computer_science, college_mathematics, college_physics, computer_security, conceptual_physics, electrical_engineering, elementary_mathematics, high_school_biology, high_school_chemistry, high_school_computer_science, high_school_mathematics, high_school_physics, high_school_statistics, machine_learning |
| Humanities (11) | formal_logic, high_school_european_history, high_school_us_history, high_school_world_history, international_law, jurisprudence, logical_fallacies, moral_disputes, moral_scenarios, philosophy, world_religions |
| Social Sciences (12) | econometrics, high_school_geography, high_school_government_and_politics, high_school_macroeconomics, high_school_microeconomics, human_sexuality, professional_psychology, public_relations, security_studies, sociology, us_foreign_policy, virology |
| Professional (16) | anatomy, business_ethics, clinical_knowledge, college_medicine, global_facts, marketing, medical_genetics, miscellaneous, nutrition, professional_accounting, professional_law, professional_medicine, virology (overlap) |

## References

1. Hendrycks, D., et al. (2021). "Measuring Massive Multitask Language Understanding." ICLR 2021.
2. Papers with Code MMLU Leaderboard
3. Open LLM Leaderboard Results

---
*Last updated: 2026-04-20 by AI Model Research Team*
