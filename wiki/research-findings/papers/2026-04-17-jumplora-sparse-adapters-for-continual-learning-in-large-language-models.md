---
title: "JumpLoRA: Sparse Adapters for Continual Learning in Large Language Models"
category: research-finding
subcategory: paper
author: "Alexandra Dragomir et al."
date: "2026-04-17"
tags: ["large language model", "cs.LG", "cs.AI", "cs.CL"]
status: ingested
source: arxiv
paper_id: "2604.16171"
---

# JumpLoRA: Sparse Adapters for Continual Learning in Large Language Models

## Summary

Adapter-based methods have become a cost-effective approach to continual learning (CL) for Large Language Models (LLMs), by sequentially learning a low-rank update matrix for each task. To mitigate catastrophic forgetting, state-of-the-art approaches impose constraints on new adapters with respect to the previous ones, by targeting either subspace or coordinate-wise interference. In this paper, we propose JumpLoRA, a novel framework to adaptively induce sparsity in the Low-Rank Adaptation (LoRA)...

## Paper Details

- **arXiv ID:** 2604.16171
- **Published:** 2026-04-17
- **Authors:** Alexandra Dragomir, Ioana Pintilie, Antonio Barbalau, Marius Dragoi, Florin Brad et al.
- **Categories:** cs.LG, cs.AI, cs.CL
- **Keywords Matched:** large language model

## Key Findings

1. In this paper, we propose JumpLoRA, a novel framework to adaptively induce sparsity in the Low-Rank Adaptation (LoRA) blocks through the use of JumpReLU gating
2. The method achieves dynamic parameter isolation, which helps prevent task interference
3. We demonstrate that our method is highly modular and compatible with LoRA-based CL approaches

## Context

### Background
This paper was published on 2026-04-17 and relates to language model research.

### Approach
The authors present their methodology and findings in the domain of cs.LG.

## Implications

### For Researchers
This work contributes to the growing body of knowledge in cs.LG, cs.AI.

### For Practitioners
Practitioners may find the approaches and findings applicable to real-world problems in the domain.

## Resources

- [arXiv Abstract](http://arxiv.org/abs/2604.16171v1)
- [PDF Download](https://arxiv.org/pdf/2604.16171.pdf)

## Tags

#large language model #cs.LG #cs.AI #cs.CL

---
*Ingested on 2026-04-19 by automated ingestion script*
