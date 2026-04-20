---
title: MMBench (Comprehensive Multimodal Evaluation)
category: benchmark
author: AI Model Research Team
date: 2026-04-20
tags: [multimodal, vision-language, comprehensive-evaluation, circular-testing]
status: active
---

# MMBench

## Overview

**Benchmark Name:** MMBench  
**Full Name:** MMBench - A Comprehensive Evaluation Benchmark for Multimodal Large Language Models  
**Category:** Multimodal Benchmark  
**First Introduced:** 2023  
**Maintained By:** OpenCompass Team, Shanghai AI Laboratory

## Description

MMBench is a comprehensive multimodal evaluation benchmark with a unique circular evaluation strategy. It tests vision-language models across 20+ capability dimensions using carefully designed multiple-choice questions.

Key features:
- **Circular evaluation** tests consistency
- **Comprehensive coverage** 20+ capability dimensions
- **Robust testing** minimizes position bias

## Purpose

MMBench was created to:
1. **Comprehensively evaluate** multimodal capabilities
2. **Test specific skills** across multiple dimensions
3. **Reduce evaluation bias** through circular testing
4. **Provide detailed analysis** of model strengths/weaknesses

## Dataset Details

### Size
- **Total Questions:** ~3,000
- **Training:** None (evaluation-only)
- **Validation:** Included in test
- **Test:** ~3,000 questions

### Format
- Multiple-choice questions (4 options)
- Circular evaluation: same question with shuffled options
- Questions across 20+ capability dimensions

### Circular Evaluation
The circular strategy:
1. Present same question multiple times
2. Shuffle answer choices each time
3. Model must be consistent across permutations
4. Reduces position bias and guessing

## Evaluation Metrics

| Metric | Description |
|--------|-------------|
| Accuracy | Overall percentage correct |
| Circular Accuracy | Consistent across option permutations |
| Per-dimension Score | Score for each capability |

## Score Ranges

| Level | Score Range | Description |
|-------|-------------|-------------|
| Poor | <50% | Limited multimodal ability |
| Basic | 50-65% | Developing capabilities |
| Good | 65-75% | Competent multimodal model |
| Strong | 75-85% | Advanced capabilities |
| State-of-the-art | 85%+ | Leading performance |

## Current Leaderboard (2025)

| Rank | Model | Score | Date |
|------|-------|-------|------|
| 1 | Gemini 2.0 Pro | 89.2% | 2025-02 |
| 2 | GPT-4o | 83.4% | 2024-05 |
| 3 | Claude 3.7 Sonnet | 81.5% | 2025-02 |
| 4 | Gemini 1.5 Pro | 78.5% | 2024-02 |
| 5 | InternVL2-Llama3-76B | 82.3% | 2024-07 |

## Capability Dimensions

| Category | Capabilities |
|----------|--------------|
| Perception | Object recognition, OCR, attribute recognition |
| Cognition | Commonsense reasoning, numerical calculation, logic reasoning |
| Coherent | Image-to-text generation consistency |
| Hallucination | Resistance to generating false information |

## Limitations

1. **Multiple-choice only** limited answer formats
2. **Synthetic circular** may not reflect real usage
3. **English-centric** limited multilingual support
4. **Static dataset** potential contamination
5. **Specific dimensions** may miss emergent capabilities

## Related Benchmarks

- [MMMU](mmmu.md) - College-level multimodal
- [SEED-Bench](https://arxiv.org/abs/2307.16125) - Comprehensive multimodal
- [MM-Vet](https://arxiv.org/abs/2308.02490) - Multimodal evaluation
- [Q-Bench](https://arxiv.org/abs/2309.14181) - Low-level vision

## Resources

- **Official Site:** https://opencompass.org.cn/mmbench
- **Paper:** https://arxiv.org/abs/2307.06281
- **Code:** https://github.com/open-compass/mmbench
- **Dataset:** Via OpenCompass platform
- **Leaderboard:** https://opencompass.org.cn/mmbench

## References

1. Liu, Y., et al. (2023). "MMBench: Is Your Multi-modal Model an All-around Player?" arXiv:2307.06281.
2. OpenCompass Documentation

---
*Last updated: 2026-04-20 by AI Model Research Team*
