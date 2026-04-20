---
title: HellaSwag (Commonsense Reasoning)
category: benchmark
author: AI Model Research Team
date: 2026-04-20
tags: [commonsense-reasoning, sentence-completion, adversarial, natural-language]
status: active
---

# HellaSwag

## Overview

**Benchmark Name:** HellaSwag  
**Full Name:** Harder Endings, Longer Contexts, and Lower-level Activities - SWAG  
**Category:** Reasoning Benchmark - Commonsense  
**First Introduced:** 2019  
**Maintained By:** University of Washington, Allen Institute for AI

## Description

HellaSwag is a challenging commonsense reasoning benchmark that tests models' ability to complete sentences describing everyday activities. It uses adversarial filtering to create difficult negative examples that are plausible but incorrect.

The task: given an activity description, choose the most likely continuation from four options.

## Purpose

HellaSwag was created to:
1. **Test commonsense reasoning** about everyday activities
2. **Evaluate contextual understanding** of situations
3. **Challenge models** with adversarial examples
4. **Assess physical commonsense** and social reasoning

## Dataset Details

### Size
- **Total Examples:** 39,905
- **Training:** 39,905 (ActivityNet Captions)
- **Validation:** 9,905
- **Test:** 10,003 (held-out)

### Format
- Activity description (1-2 sentences)
- Four possible endings
- One correct, three adversarially filtered incorrect

### Adversarial Filtering
The dataset creation process:
1. Generate candidate endings using language models
2. Filter to keep only endings that confuse baseline models
3. Results in challenging negative examples

## Evaluation Metrics

| Metric | Description |
|--------|-------------|
| Accuracy | Percentage of correct completions |
| Perplexity | Language model perplexity on endings |

## Score Ranges

| Level | Score Range | Description |
|-------|-------------|-------------|
| Random | ~25% | Random guessing |
| Basic | 40-60% | Some contextual understanding |
| Good | 60-75% | Strong commonsense reasoning |
| Excellent | 75-90% | Near-human performance |
| State-of-the-art | 90%+ | Superhuman performance |

## Current Leaderboard (2025)

| Rank | Model | Score | Date |
|------|-------|-------|------|
| 1 | o3-mini | 95.5% | 2025-01 |
| 2 | GPT-4.5 | 94.2% | 2025-02 |
| 3 | Claude 3.7 Sonnet | 93.8% | 2025-02 |
| 4 | Gemini 2.0 Pro | 93.5% | 2025-02 |
| 5 | Llama 3.1 405B | 91.2% | 2024-07 |

## Historical Progress

| Year | Score | Model |
|------|-------|-------|
| 2019 | 39.0% | BERT-Large |
| 2020 | 85.3% | RoBERTa |
| 2022 | 93.9% | PaLM |
| 2023 | 95.3% | GPT-4 |
| 2025 | 95.5% | o3-mini |

## Comparison with Human Performance

| Group | Score |
|-------|-------|
| Average Humans | ~95% |
| Domain Experts | ~95% |
| Best AI Models | ~95.5% |

Note: HellaSwag is considered "saturated" as models now match or exceed human performance.

## Categories Tested

| Category | Examples |
|----------|----------|
| Physical Activities | Sports, exercise, manual tasks |
| Household Chores | Cleaning, cooking, organizing |
| Social Interactions | Conversations, group activities |
| Creative Activities | Art, music, crafts |
| Outdoor Activities | Gardening, hiking, recreation |

## Limitations

1. **Saturated benchmark** models exceed human performance
2. **ActivityNet bias** based on video captions
3. **English only** limited language coverage
4. **Static dataset** potential memorization
5. **Format limitations** only sentence completion

## Related Benchmarks

- [SWAG](https://rowanzellers.com/swag/) - Original SWAG dataset
- [CommonsenseQA](https://www.tau-nlp.org/commonsenseqa) - Commonsense QA
- [PIQA](https://yonatanbisk.com/piqa/) - Physical commonsense
- [Social IQA](https://masatran.github.io/social-iqa/) - Social commonsense
- [WinoGrande](https://winogrande.allenai.org/) - Commonsense coreference

## Resources

- **Official Site:** https://rowanzellers.com/hellaswag/
- **Paper:** https://arxiv.org/abs/1905.07830
- **Code:** https://github.com/rowanz/hellaswag
- **Dataset:** https://huggingface.co/datasets/Rowan/hellaswag
- **Leaderboard:** https://rowanzellers.com/hellaswag/

## References

1. Zellers, R., et al. (2019). "HellaSwag: Can a Machine Really Finish Your Sentence?" ACL 2019.
2. SWAG Dataset Paper

---
*Last updated: 2026-04-20 by AI Model Research Team*
