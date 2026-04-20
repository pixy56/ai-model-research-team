---
title: SWE-bench (Software Engineering Benchmark)
category: benchmark
author: AI Model Research Team
date: 2026-04-20
tags: [software-engineering, code-repair, github-issues, real-world]
status: active
---

# SWE-bench

## Overview

**Benchmark Name:** SWE-bench  
**Full Name:** Software Engineering Benchmark  
**Category:** Code Benchmark - Real-world Engineering  
**First Introduced:** 2023  
**Maintained By:** Princeton NLP Group

## Description

SWE-bench is a benchmark for evaluating large language models on real-world software engineering tasks. It tests models' ability to resolve GitHub issues from popular open-source Python repositories.

The benchmark presents models with:
- A GitHub issue description
- The relevant codebase
- The task: generate a patch that resolves the issue

## Purpose

SWE-bench was created to:
1. **Evaluate real-world coding** beyond toy problems
2. **Test end-to-end software engineering** capabilities
3. **Measure practical AI assistance** for developers
4. **Provide realistic evaluation** of code generation systems

## Dataset Details

### Size
- **Total Issues:** 2,294 (original) / 500+ Lite
- **Training:** Not applicable (test-only benchmark)
- **Validation:** Dev split available
- **Test:** Held-out repository issues

### Variants
| Variant | Description | Size |
|---------|-------------|------|
| SWE-bench Full | Complete benchmark | 2,294 issues |
| SWE-bench Lite | Curated easier subset | 300 issues |
| SWE-bench Verified | Human-verified subset | 500 issues |
| SWE-bench Multimodal | With screenshots | 100+ issues |

### Task Types
- Bug fixing
- Feature implementation
- Test case resolution
- Code refactoring

## Evaluation Metrics

| Metric | Description |
|--------|-------------|
| Resolution Rate | % of issues successfully resolved |
| Patch Application | % of patches that apply cleanly |
| Test Pass Rate | % of patches passing test suite |
| Partial Credit | Progress toward resolution |

## Score Ranges

| Level | Resolution Rate | Description |
|-------|-----------------|-------------|
| Poor | <5% | Minimal capability |
| Basic | 5-15% | Can fix simple issues |
| Competent | 15-30% | Moderate engineering ability |
| Advanced | 30-50% | Strong practical coding |
| Expert | 50%+ | Professional-level assistance |

## Current Leaderboard (2025)

| Rank | Model | SWE-bench Verified | Full | Date |
|------|-------|-------------------|------|------|
| 1 | Claude 3.7 Sonnet | 62.3% | 24.4% | 2025-02 |
| 2 | o3-mini | 61.0% | 23.0% | 2025-01 |
| 3 | GPT-4.5 | 58.5% | 22.1% | 2025-02 |
| 4 | o1 | 48.0% | 20.0% | 2024-09 |
| 5 | Claude 3.5 Sonnet | 46.0% | 18.0% | 2024-06 |

## Historical Progress

| Year | Verified Score | Model |
|------|----------------|-------|
| 2023 | 1.96% | GPT-4 (zero-shot) |
| 2024 | 12.0% | Claude 3 Opus |
| 2024 | 46.0% | Claude 3.5 Sonnet |
| 2025 | 62.3% | Claude 3.7 Sonnet |

## Repository Distribution

| Repository | Language | Issues |
|------------|----------|--------|
| scikit-learn | Python | 124 |
| django | Python | 186 |
| sympy | Python | 203 |
| pytest-dev/pytest | Python | 156 |
| sphinx-doc/sphinx | Python | 134 |
| pandas-dev/pandas | Python | 289 |
| matplotlib | Python | 98 |
| numpy | Python | 87 |

## Limitations

1. **Python only** limited language support
2. **Open source focus** not enterprise/private code
3. **Test oracle** requires existing tests
4. **Issue quality** variable difficulty and clarity
5. **Computational cost** expensive to evaluate

## Related Benchmarks

- [HumanEval](humaneval.md) - Function-level code generation
- [MBPP](https://github.com/google-research/google-research/tree/master/mbpp) - Basic Python problems
- [Aider](https://aider.chat/docs/leaderboard.html) - AI pair programming
- [CodeContests](https://github.com/deepmind/code_contests) - Competitive programming

## Resources

- **Official Site:** https://www.swebench.com/
- **Paper:** https://arxiv.org/abs/2310.06770
- **Code:** https://github.com/princeton-nlp/SWE-bench
- **Dataset:** Included in repository
- **Leaderboard:** https://www.swebench.com/

## Categories Tested

| Category | Skills Required |
|----------|-----------------|
| Bug Fixing | Debugging, root cause analysis |
| Feature Implementation | Understanding requirements, design |
| Code Navigation | Large codebase understanding |
| Testing | Writing and running tests |
| Version Control | Git operations, patch generation |

## References

1. Jimenez, C., et al. (2023). "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?" ICLR 2024.
2. SWE-bench Official Website
3. Princeton NLP Group Research

---
*Last updated: 2026-04-20 by AI Model Research Team*
