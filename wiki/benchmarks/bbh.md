---
title: BBH (Big-Bench Hard)
category: benchmark
author: AI Model Research Team
date: 2026-04-20
tags: [reasoning, challenging-tasks, diverse, chain-of-thought]
status: active
---

# BBH (Big-Bench Hard)

## Overview

**Benchmark Name:** BBH  
**Full Name:** Big-Bench Hard  
**Category:** Reasoning Benchmark - Challenging Tasks  
**First Introduced:** 2022  
**Maintained By:** Google Research (BIG-bench collaboration)

## Description

BBH (Big-Bench Hard) is a subset of 23 challenging tasks from the larger BIG-bench benchmark. These are tasks where prior language models performed below average human performance, selected to test the limits of model capabilities.

The tasks require:
- Multi-step reasoning
- Domain knowledge
- Algorithmic thinking
- Commonsense reasoning

## Purpose

BBH was created to:
1. **Focus on challenging tasks** that distinguish model capabilities
2. **Test reasoning limits** beyond standard benchmarks
3. **Evaluate chain-of-thought** prompting effectiveness
4. **Provide diverse evaluation** across task types

## Dataset Details

### Size
- **Total Tasks:** 23
- **Examples per task:** Varies (typically 100-1,000)
- **Total Examples:** ~6,500

### Format
- Diverse task formats (QA, classification, generation)
- Free-form or multiple-choice answers
- Requires various reasoning strategies

### Task Categories
| Category | Tasks |
|----------|-------|
| Logical Reasoning | Navigate, Web of Lies, Logical Deduction |
| Algorithmic | Word Sorting, Multistep Arithmetic, Python Programming |
| Linguistic | Linguistics Mappings, Disambiguation QA |
| Commonsense | Snarks, Causes, Implicatures |
| Domain-Specific | Formal Fallacies, Tracking Shuffled Objects |

## Evaluation Metrics

| Metric | Description |
|--------|-------------|
| Accuracy | Exact match accuracy |
| Task Average | Average across all 23 tasks |
| Per-task Score | Individual task performance |

## Score Ranges

| Level | Score Range | Description |
|-------|-------------|-------------|
| Poor | <40% | Below human baseline |
| Basic | 40-60% | Near human baseline |
| Good | 60-75% | Above human baseline |
| Advanced | 75-85% | Strong reasoning |
| Expert | 85%+ | Excellent performance |

## Current Leaderboard (2025)

| Rank | Model | Score | Date |
|------|-------|-------|------|
| 1 | o3-mini | 92.5% | 2025-01 |
| 2 | Claude 3.7 Sonnet | 89.2% | 2025-02 |
| 3 | GPT-4.5 | 88.5% | 2025-02 |
| 4 | Gemini 2.0 Pro | 87.8% | 2025-02 |
| 5 | Llama 3.1 405B | 82.0% | 2024-07 |

## Historical Progress

| Year | Score | Model | Notes |
|------|-------|-------|-------|
| 2022 | 52.0% | PaLM | Without CoT |
| 2022 | 66.0% | PaLM | With CoT |
| 2023 | 83.1% | GPT-4 | With CoT |
| 2024 | 86.0% | Claude 3.5 | With CoT |
| 2025 | 92.5% | o3-mini | Advanced reasoning |

## Comparison with Human Performance

| Group | Score |
|-------|-------|
| Average Human Rater | ~67% |
| Best Human Performance | ~90%+ |
| GPT-4 (CoT) | ~83% |
| o3-mini | ~92.5% |

## Selected Tasks

| Task | Description | Skills Tested |
|------|-------------|---------------|
| Navigate | Follow directions on a grid | Spatial reasoning |
| Web of Lies | Track truth-tellers and liars | Logical deduction |
| Word Sorting | Sort words alphabetically | Algorithmic reasoning |
| Multi-step Arithmetic | Complex calculations | Mathematical reasoning |
| Tracking Shuffled Objects | Follow object movements | Working memory |
| Logical Deduction | Solve logic puzzles | Deductive reasoning |
| Formal Fallacies | Identify logical errors | Critical thinking |

## Limitations

1. **Diverse formats** difficult to standardize
2. **Small sample sizes** for some tasks
3. **Static dataset** potential contamination
4. **English-centric** limited multilingual support
5. **Task selection bias** may not cover all capabilities

## Related Benchmarks

- [BIG-bench](https://github.com/google/BIG-bench) - Full benchmark suite
- [BIG-bench Lite](https://github.com/google/BIG-bench/tree/main/bigbench/benchmark_tasks/lite) - Lightweight version
- [MMLU](mmlu.md) - Broad knowledge assessment
- [ARC](arc.md) - Commonsense reasoning

## Resources

- **Official Site:** https://github.com/google/BIG-bench/tree/main/bigbench/benchmark_tasks
- **Paper:** https://arxiv.org/abs/2210.09261
- **Code:** https://github.com/google/BIG-bench
- **Dataset:** Included in BIG-bench repository
- **Leaderboard:** Papers with Code BBH section

## References

1. Suzgun, Y., et al. (2022). "Challenging BIG-Bench Tasks and Whether Chain-of-Thought Can Solve Them." arXiv:2210.09261.
2. BIG-bench Collaboration. (2022). "Beyond the Imitation Game: Quantifying and Extrapolating the Capabilities of Language Models." arXiv:2206.04615.

---
*Last updated: 2026-04-20 by AI Model Research Team*
