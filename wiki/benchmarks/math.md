---
title: MATH (Mathematics Competition Benchmark)
category: benchmark
author: AI Model Research Team
date: 2026-04-20
tags: [mathematics, competition-math, reasoning, problem-solving]
status: active
---

# MATH Dataset

## Overview

**Benchmark Name:** MATH  
**Full Name:** MATH Dataset (Mathematics Aptitude Test of Heuristics)  
**Category:** Reasoning Benchmark - Mathematics  
**First Introduced:** 2021  
**Maintained By:** UC Berkeley, OpenAI

## Description

The MATH dataset is a challenging benchmark of competition mathematics problems. It tests language models' ability to solve complex mathematical problems requiring multi-step reasoning, symbolic manipulation, and mathematical intuition.

Problems are sourced from:
- AMC 10/12 (American Mathematics Competitions)
- AIME (American Invitational Mathematics Examination)
- Various mathematics competitions

## Purpose

MATH was created to:
1. **Test mathematical reasoning** beyond simple arithmetic
2. **Evaluate multi-step problem-solving** capabilities
3. **Measure progress** in mathematical AI systems
4. **Provide a challenging** benchmark for advanced reasoning

## Dataset Details

### Size
- **Total Problems:** 12,500
- **Training:** 7,500 problems
- **Validation:** 500 problems
- **Test:** 5,000 problems

### Format
- Competition-style mathematics problems
- Free-form numerical or symbolic answers
- LaTeX formatting for mathematical expressions
- Step-by-step solutions included in training set

### Difficulty Levels
| Level | Description | Example Competitions |
|-------|-------------|---------------------|
| Level 1 | Easier problems | AMC 10 early questions |
| Level 2-3 | Medium difficulty | AMC 12, mid AMC 10 |
| Level 4-5 | Hard problems | AIME, late AMC 12 |

## Evaluation Metrics

| Metric | Description |
|--------|-------------|
| Accuracy | Percentage of problems with correct final answer |
| Step Accuracy | Correctness of intermediate reasoning steps |
| Majorities@k | Accuracy using majority voting over k samples |

## Score Ranges

| Level | Score Range | Description |
|-------|-------------|-------------|
| Poor | <20% | Limited mathematical ability |
| Basic | 20-40% | Elementary competition level |
| Good | 40-60% | Strong AMC 10 performance |
| Advanced | 60-80% | AIME qualification level |
| Expert | 80%+ | Top competition performance |

## Current Leaderboard (2025)

| Rank | Model | Score | Date |
|------|-------|-------|------|
| 1 | o3-mini (high) | 97.3% | 2025-01 |
| 2 | DeepSeek-R1 | 97.3% | 2025-01 |
| 3 | GPT-4.5 | 83.4% | 2025-02 |
| 4 | Claude 3.7 Sonnet | 82.5% | 2025-02 |
| 5 | Gemini 2.0 Pro | 78.5% | 2025-02 |

## Historical Progress

| Year | Score | Model | Approach |
|------|-------|-------|----------|
| 2021 | 6.9% | GPT-3 | Direct generation |
| 2022 | 23.5% | Minerva | Fine-tuned on math |
| 2023 | 52.9% | GPT-4 | Chain-of-thought |
| 2024 | 78.2% | o1-preview | Test-time compute |
| 2025 | 97.3% | o3-mini | Advanced reasoning |

## Categories Tested

| Category | Topics | % of Dataset |
|----------|--------|--------------|
| Algebra | Equations, inequalities, polynomials | ~25% |
| Geometry | Euclidean, coordinate, solid geometry | ~20% |
| Number Theory | Primes, divisibility, modular arithmetic | ~15% |
| Counting & Probability | Combinatorics, probability | ~20% |
| Pre-calculus | Trigonometry, complex numbers | ~15% |
| Intermediate Algebra | Advanced algebraic techniques | ~5% |

## Limitations

1. **Competition focus** may not reflect practical math needs
2. **Symbolic answers** limited natural language reasoning
3. **English only** no multilingual support
4. **Training set available** potential for memorization
5. **No visual components** pure text-based problems

## Related Benchmarks

- [GSM8K](gsm8k.md) - Grade school math word problems
- [MathVista](https://mathvista.github.io/) - Multimodal math problems
- [TheoremQA](https://arxiv.org/abs/2305.12524) - Theorem-based questions
- [LiveBench](https://www.livebench.ai/) - Includes math reasoning

## Resources

- **Official Site:** https://huggingface.co/datasets/hendrycks/competition_math
- **Paper:** https://arxiv.org/abs/2103.03874
- **Code:** https://github.com/hendrycks/math
- **Dataset:** https://huggingface.co/datasets/hendrycks/competition_math
- **Leaderboard:** Papers with Code MATH section

## References

1. Hendrycks, D., et al. (2021). "Measuring Mathematical Problem Solving With the MATH Dataset." NeurIPS 2021.
2. Lightman, H., et al. (2023). "Let's Verify Step by Step." OpenAI.

---
*Last updated: 2026-04-20 by AI Model Research Team*
