---
title: "Information Router for Mitigating Modality Dominance in Vision-Language Models"
category: research-finding
subcategory: paper
author: "Seulgi Kim et al."
date: "2026-04-17"
tags: ["large language model", "reasoning", "cs.CV", "cs.LG"]
status: ingested
source: arxiv
paper_id: "2604.16264"
---

# Information Router for Mitigating Modality Dominance in Vision-Language Models

## Summary

Vision Language models (VLMs) have demonstrated strong performance across a wide range of benchmarks, yet they often suffer from modality dominance, where predictions rely disproportionately on a single modality. Prior approaches primarily address this issue by steering model's attention allocation, implicitly assuming that all modalities provide sufficient information. However, attention only determines where the model focuses, and cannot enrich information that is missing or ambiguous. In the ...

## Paper Details

- **arXiv ID:** 2604.16264
- **Published:** 2026-04-17
- **Authors:** Seulgi Kim, Mohit Prabhushankar, Ghassan AlRegib
- **Categories:** cs.CV, cs.LG
- **Keywords Matched:** large language model, reasoning

## Key Findings

1. Vision Language models (VLMs) have demonstrated strong performance across a wide range of benchmarks, yet they often suffer from modality dominance, where predictions rely disproportionately on a single modality
2. In this paper, we propose \textsc{MoIR}: \textit{Multi-modal Information Router}, an information-level fusion method that explicitly reduces information disparity prior to fusion
3. \textsc{MoIR} identifies less informative tokens and routes complementary information from a stronger modality, constructing information-dense token representations before they are processed by a large language model

## Context

### Background
This paper was published on 2026-04-17 and relates to language model research.

### Approach
The authors present their methodology and findings in the domain of cs.CV.

## Implications

### For Researchers
This work contributes to the growing body of knowledge in cs.CV, cs.LG.

### For Practitioners
Practitioners may find the approaches and findings applicable to real-world problems in the domain.

## Resources

- [arXiv Abstract](http://arxiv.org/abs/2604.16264v1)
- [PDF Download](https://arxiv.org/pdf/2604.16264.pdf)

## Tags

#large language model #reasoning #cs.CV #cs.LG

---
*Ingested on 2026-04-19 by automated ingestion script*
