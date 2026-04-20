---
title: ARC (AI2 Reasoning Challenge)
category: benchmark
author: AI Model Research Team
date: 2026-04-20
tags: [commonsense-reasoning, science-qa, grade-school, multiple-choice]
status: active
---

# ARC (AI2 Reasoning Challenge)

## Overview

**Benchmark Name:** ARC  
**Full Name:** AI2 Reasoning Challenge  
**Category:** Reasoning Benchmark - Commonsense  
**First Introduced:** 2018  
**Maintained By:** Allen Institute for AI (AI2)

## Description

ARC is a dataset of natural science questions designed to test models' ability to answer questions that require scientific reasoning and commonsense knowledge. It consists of questions from grade school science exams.

The benchmark has two subsets:
- **ARC-Easy:** Questions answered correctly by both retrieval and co-occurrence baselines
- **ARC-Challenge:** Questions requiring more complex reasoning

## Purpose

ARC was created to:
1. **Test scientific reasoning** at grade school level
2. **Evaluate commonsense understanding** of physical world
3. **Differentiate retrieval** from reasoning capabilities
4. **Provide accessible** yet challenging benchmark

## Dataset Details

### Size
- **Total Questions:** 7,787
- **ARC-Easy:** 5,198 questions
- **ARC-Challenge:** 2,590 questions

### Format
- Multiple-choice questions (4 options)
- Grade school science exam questions
- Requires commonsense and scientific reasoning

### Task Types
- Scientific fact recall
- Physical reasoning
- Commonsense inference
- Cause and effect understanding

## Evaluation Metrics

| Metric | Description |
|--------|-------------|
| Accuracy | Percentage of questions answered correctly |
| ARC-Easy Score | Performance on easy subset |
| ARC-Challenge Score | Performance on challenge subset |

## Score Ranges

### ARC-Easy
| Level | Score Range |
|-------|-------------|
| Basic | 60-75% |
| Good | 75-85% |
| Excellent | 85-95% |
| Near-perfect | 95%+ |

### ARC-Challenge
| Level | Score Range |
|-------|-------------|
| Poor | <40% |
| Basic | 40-60% |
| Good | 60-75% |
| Excellent | 75-90% |
| State-of-the-art | 90%+ |

## Current Leaderboard (2025)

### ARC-Challenge
| Rank | Model | Score | Date |
|------|-------|-------|------|
| 1 | o3-mini | 97.5% | 2025-01 |
| 2 | GPT-4.5 | 95.2% | 2025-02 |
| 3 | Claude 3.7 Sonnet | 94.8% | 2025-02 |
| 4 | Gemini 2.0 Pro | 93.5% | 2025-02 |
| 5 | Llama 3.1 405B | 89.0% | 2024-07 |

### ARC-Easy
| Rank | Model | Score | Date |
|------|-------|-------|------|
| 1 | o3-mini | 99.2% | 2025-01 |
| 2 | GPT-4.5 | 98.5% | 2025-02 |
| 3 | Claude 3.7 Sonnet | 98.2% | 2025-02 |

## Historical Progress

### ARC-Challenge
| Year | Score | Model |
|------|-------|-------|
| 2018 | 30.3% | Best baseline |
| 2020 | 68.8% | UnifiedQA |
| 2022 | 85.4% | PaLM |
| 2023 | 96.3% | GPT-4 |
| 2025 | 97.5% | o3-mini |

## Categories Tested

| Category | Topics |
|----------|--------|
| Biology | Living organisms, ecosystems, human body |
| Physics | Forces, energy, motion, matter |
| Chemistry | Elements, compounds, reactions |
| Earth Science | Geology, weather, astronomy |
| General Science | Scientific method, tools, processes |

## Limitations

1. **Grade school level** not advanced science
2. **English only** limited language coverage
3. **Static dataset** potential memorization
4. **Multiple-choice** limited answer formats
5. **Retrieval vs reasoning** some questions test recall

## Related Benchmarks

- [OpenBookQA](https://allenai.org/data/open-book-qa) - Open book science QA
- [ScienceQA](https://scienceqa.github.io/) - Multimodal science QA
- [CommonsenseQA](https://www.tau-nlp.org/commonsenseqa) - Commonsense reasoning
- [HellaSwag](hellaswag.md) - Commonsense completion

## Resources

- **Official Site:** https://allenai.org/data/arc
- **Paper:** https://arxiv.org/abs/1803.05457
- **Code:** https://github.com/allenai/arc-solvers
- **Dataset:** https://huggingface.co/datasets/ai2_arc
- **Leaderboard:** Papers with Code ARC section

## References

1. Clark, P., et al. (2018). "Think you have Solved Question Answering? Try ARC, the AI2 Reasoning Challenge." arXiv:1803.05457.

---
*Last updated: 2026-04-20 by AI Model Research Team*
