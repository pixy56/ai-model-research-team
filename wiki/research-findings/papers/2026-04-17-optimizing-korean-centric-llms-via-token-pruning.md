---
title: "Optimizing Korean-Centric LLMs via Token Pruning"
category: research-finding
subcategory: paper
author: "Hoyeol Kim, Hyeonwoo Kim"
date: "2026-04-17"
tags: ["large language model", "cs.CL"]
status: ingested
source: arxiv
paper_id: "2604.16235"
---

# Optimizing Korean-Centric LLMs via Token Pruning

## Summary

This paper presents a systematic benchmark of state-of-the-art multilingual large language models (LLMs) adapted via token pruning - a compression technique that eliminates tokens and embedding parameters corresponding to languages irrelevant to the target application. Focusing on Korean-centric natural language processing (NLP) tasks, we evaluate architectures including Qwen3, Gemma-3, Llama-3, and Aya across three vocabulary configurations: Original, English-Korean (EnKo), and English-Korean-C...

## Paper Details

- **arXiv ID:** 2604.16235
- **Published:** 2026-04-17
- **Authors:** Hoyeol Kim, Hyeonwoo Kim
- **Categories:** cs.CL
- **Keywords Matched:** large language model

## Key Findings

1. This paper presents a systematic benchmark of state-of-the-art multilingual large language models (LLMs) adapted via token pruning - a compression technique that eliminates tokens and embedding parameters corresponding to languages irrelevant to the target application
2. Our findings indicate that token pruning significantly improves generation stability by eliminating language confusion, and in the case of machine translation, frequently enhances performance on Korean-specific tasks
3. While instruction-following capabilities display architecture-dependent variance linked to latent cross-lingual representations, the significant reduction in vocabulary size validates token pruning as a highly effective optimization strategy for memory-constrained, domain-specific deployments, despite modest gains in inference latency.

## Context

### Background
This paper was published on 2026-04-17 and relates to language model research.

### Approach
The authors present their methodology and findings in the domain of cs.CL.

## Implications

### For Researchers
This work contributes to the growing body of knowledge in cs.CL.

### For Practitioners
Practitioners may find the approaches and findings applicable to real-world problems in the domain.

## Resources

- [arXiv Abstract](http://arxiv.org/abs/2604.16235v1)
- [PDF Download](https://arxiv.org/pdf/2604.16235.pdf)

## Tags

#large language model #cs.CL

---
*Ingested on 2026-04-19 by automated ingestion script*
