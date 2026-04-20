---
title: GSM8K (Grade School Math)
category: benchmark
author: AI Model Research Team
date: 2026-04-20
tags: [mathematics, grade-school, word-problems, chain-of-thought]
status: active
---

# GSM8K

## Overview

**Benchmark Name:** GSM8K  
**Full Name:** Grade School Math 8K  
**Category:** Reasoning Benchmark - Mathematics  
**First Introduced:** 2021  
**Maintained By:** OpenAI

## Description

GSM8K is a dataset of 8,500 grade school math word problems. Each problem requires 2-8 steps to solve using basic arithmetic operations. The problems are linguistically diverse and test models' ability to understand word problems and perform multi-step reasoning.

## Purpose

GSM8K was created to:
1. **Test mathematical reasoning** at accessible difficulty
2. **Evaluate multi-step problem solving**
3. **Assess chain-of-thought** reasoning effectiveness
4. **Provide high-quality** training and evaluation data

## Dataset Details

### Size
- **Total Problems:** 8,500
- **Training:** 7,473 problems
- **Validation:** None (use test for validation)
- **Test:** 1,319 problems

### Format
- Natural language word problems
- Integer answers (typically 0-999)
- Solutions include step-by-step reasoning

### Problem Characteristics
- 2-8 steps to solve
- Basic arithmetic operations only (+, -, *, /)
- Diverse problem types and contexts
- Natural language variations

## Evaluation Metrics

| Metric | Description |
|--------|-------------|
| Accuracy | Percentage of correct final answers |
| Solution Rate | Problems with correct step-by-step solution |
| Per-step Accuracy | Correctness of intermediate steps |

## Score Ranges

| Level | Score Range | Description |
|-------|-------------|-------------|
| Poor | <40% | Limited math word problem ability |
| Basic | 40-70% | Some problem-solving capability |
| Good | 70-85% | Competent at grade school math |
| Excellent | 85-95% | Strong performance |
| Near-perfect | 95%+ | Mastery of benchmark |

## Current Leaderboard (2025)

| Rank | Model | Score | Date |
|------|-------|-------|------|
| 1 | o3-mini | 99.2% | 2025-01 |
| 2 | Claude 3.7 Sonnet | 98.5% | 2025-02 |
| 3 | GPT-4.5 | 98.2% | 2025-02 |
| 4 | Gemini 2.0 Pro | 97.8% | 2025-02 |
| 5 | Llama 3.1 405B | 95.0% | 2024-07 |

## Historical Progress

| Year | Score | Model | Approach |
|------|-------|-------|----------|
| 2021 | 6.0% | GPT-3 | Direct generation |
| 2022 | 55.0% | Minerva | Fine-tuned on math |
| 2022 | 74.0% | PaLM | Chain-of-thought |
| 2023 | 92.0% | GPT-4 | Advanced CoT |
| 2024 | 97.0% | Claude 3.5 | Improved reasoning |
| 2025 | 99.2% | o3-mini | Test-time compute |

## Problem Types

| Category | Examples | % of Dataset |
|----------|----------|--------------|
| Arithmetic | Addition, subtraction, multiplication, division | ~30% |
| Word Problems | Money, time, distance, rate | ~40% |
| Multi-step | Problems requiring multiple operations | ~25% |
| Logic Puzzles | Age problems, ratio problems | ~5% |

## Example Problem

**Problem:**
> Janet's ducks lay 16 eggs per day. She eats three for breakfast every morning and bakes muffins for her friends every day with four. She sells the remainder at the farmers' market daily for $2 per fresh duck egg. How much in dollars does she make every day at the farmers' market?

**Solution:**
1. Total eggs laid: 16
2. Eggs eaten for breakfast: 3
3. Eggs used for muffins: 4
4. Remaining eggs: 16 - 3 - 4 = 9
5. Money made: 9 * $2 = $18

**Answer:** 18

## Limitations

1. **Grade school level** not advanced mathematics
2. **English only** limited language diversity
3. **Integer answers only** no fractions/decimals
3. **Static dataset** potential contamination
4. **Saturated** top models achieve near-perfect scores
5. **Limited problem types** basic arithmetic focus

## Related Benchmarks

- [MATH](math.md) - Competition mathematics
- [SVAMP](https://arxiv.org/abs/2103.07191) - Simple math word problems
- [MultiArith](https://aclanthology.org/D17-1088/) - Multi-step arithmetic
- [ASDiv](https://aclanthology.org/2020.acl-main.92/) - Diverse math word problems
- [MAWPS](https://aclanthology.org/D15-1132/) - Math word problem repository

## Resources

- **Official Site:** https://github.com/openai/grade-school-math
- **Paper:** https://arxiv.org/abs/2110.14168
- **Code:** https://github.com/openai/grade-school-math
- **Dataset:** https://huggingface.co/datasets/openai/gsm8k
- **Leaderboard:** Papers with Code GSM8K section

## References

1. Cobbe, K., et al. (2021). "Training Verifiers to Solve Math Word Problems." arXiv:2110.14168.
2. OpenAI GSM8K Repository

---
*Last updated: 2026-04-20 by AI Model Research Team*
