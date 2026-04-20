---
title: AI Model Architecture Taxonomy
category: wiki
author: AI Model Research Team
date: 2026-04-20
tags: [taxonomy, architecture, classification, overview]
---

# AI Model Architecture Taxonomy

A comprehensive classification of modern AI model architectures based on analysis of 47 models from major labs and 100+ research papers.

---

## Quick Navigation

| Architecture | Type | Key Feature | Notable Models | Status |
|--------------|------|-------------|----------------|--------|
| [Dense Transformer](#dense-transformers) | Foundation | Full attention | GPT-4, Claude, Llama | Mature |
| [Mixture of Experts](#mixture-of-experts-moe) | Efficiency | Sparse activation | Mixtral, DeepSeek-V3 | Emerging |
| [State Space Models](#state-space-models-ssm) | Long Context | Linear attention | Mamba, Jamba | Emerging |
| [Multimodal](#multimodal-architectures) | Fusion | Cross-modal | GPT-4o, Gemini, Llama Vision | Maturing |
| [Reasoning](#reasoning-architectures) | Inference | Test-time compute | o3, DeepSeek-R1 | Emerging |
| [Diffusion](#diffusion-models) | Generation | Iterative denoising | Sora, DALL-E, Stable Diffusion | Mature |

---

## Architecture Overview

### Dense Transformers

The foundational architecture for modern LLMs. Uses full multi-head self-attention with all parameters active during forward passes.

**Key Characteristics:**
- **Complexity:** O(n²) attention
- **Parameters:** 100% active
- **Context:** 4K-2M tokens
- **Best For:** General purpose, proven reliability

**Notable Models:** Llama 3.1 405B, Claude 3.7, GPT-4, Gemini 1.5 Pro

→ [Read Full Documentation](dense-transformer.md)

---

### Mixture of Experts (MoE)

Sparse architectures that activate only a subset of parameters per token, enabling massive models with efficient inference.

**Key Characteristics:**
- **Activation:** 10-20% of parameters
- **Routing:** Learned token-to-expert assignment
- **Efficiency:** Higher capacity without proportional compute
- **Best For:** High throughput, cost efficiency

**Notable Models:** DeepSeek-V3 (671B), Mixtral 8x22B, DBRX

→ [Read Full Documentation](moe.md)

---

### State Space Models (SSM)

Linear complexity alternatives to transformers with O(n) scaling, enabling very long sequence processing.

**Key Characteristics:**
- **Complexity:** O(n) sequence length
- **Memory:** Constant w.r.t sequence
- **State:** Compressed history representation
- **Best For:** Very long contexts (>100K tokens)

**Notable Models:** Mamba, Jamba, Falcon Mamba, RWKV

→ [Read Full Documentation](ssm.md)

---

### Multimodal Architectures

Unified frameworks for processing vision, language, audio, and other modalities together.

**Key Characteristics:**
- **Modalities:** Vision + Language (+ Audio)
- **Fusion:** Cross-modal attention
- **Approaches:** Flamingo, LLaVA, Native
- **Best For:** Vision-language tasks, cross-modal reasoning

**Notable Models:** GPT-4o, Gemini 2.0, Claude 3.5, Llama 3.2 Vision

→ [Read Full Documentation](multimodal.md)

---

### Reasoning Architectures

Test-time compute architectures that allocate additional inference computation for complex reasoning tasks.

**Key Characteristics:**
- **Compute:** Scaled at inference time
- **Method:** Chain-of-thought, search, verification
- **Training:** RL-based or supervised
- **Best For:** Math, coding, scientific reasoning

**Notable Models:** o3, o1, DeepSeek-R1, Claude 3.7 Sonnet (hybrid)

→ [Read Full Documentation](reasoning.md)

---

### Diffusion Models

Iterative generative architectures that denoise data to produce high-quality images, video, and audio.

**Key Characteristics:**
- **Generation:** Iterative denoising
- **Quality:** State-of-the-art visuals
- **Speed:** Slower than autoregressive
- **Best For:** Image/video generation, editing

**Notable Models:** Sora, DALL-E 3, Stable Diffusion 3, Imagen 3, Veo 2

→ [Read Full Documentation](diffusion.md)

---

## Architecture Comparison Matrix

| Aspect | Dense | MoE | SSM | Multimodal | Reasoning | Diffusion |
|--------|-------|-----|-----|------------|-----------|-----------|
| **Complexity** | O(n²) | O(n²) | O(n) | O(n²) | O(n²) | O(n·T) |
| **Memory** | O(n) | O(n) | O(1) | O(n) | O(n) | O(n) |
| **Training Stability** | High | Medium | Medium | High | Low | High |
| **Inference Speed** | Medium | Fast | Fast | Medium | Slow | Slow |
| **Context Length** | 128K-2M | 128K-2M | 1M+ | 128K | 128K | N/A |
| **Ecosystem** | Mature | Growing | Early | Maturing | Early | Mature |

---

## Classification Criteria

### How to Classify a Model

| Architecture | Required Criteria |
|--------------|-------------------|
| **Dense Transformer** | Full parameter activation, O(n²) attention, no routing |
| **MoE** | <50% active params, expert layers, learned routing |
| **SSM** | State-based, O(n) complexity, no attention |
| **Multimodal** | Multiple encoders, cross-modal fusion, vision component |
| **Reasoning** | Extended inference, CoT generation, RL training |
| **Diffusion** | Iterative denoising, noise prediction, U-Net/DiT backbone |

### Hybrid Architectures

Many modern models combine multiple architectures:
- **Jamba:** SSM + Transformer + MoE
- **Claude 3.7:** Dense + Reasoning modes
- **GPT-4o:** Dense + Multimodal

Use the primary distinguishing feature for classification.

---

## Model Distribution by Architecture

Based on analysis of 47 models from OpenAI, Anthropic, Google, Meta, and Mistral:

| Architecture | Count | Percentage |
|--------------|-------|------------|
| Dense Transformer | 28 | 59.6% |
| Multimodal | 7 | 14.9% |
| Reasoning | 5 | 10.6% |
| MoE | 2 | 4.3% |
| Diffusion | 3 | 6.4% |
| Other | 2 | 4.3% |

---

## Selection Guide

### By Use Case

| Use Case | Recommended Architecture | Notes |
|----------|-------------------------|-------|
| General purpose LLM | Dense Transformer | Proven, widely supported |
| High-throughput serving | MoE | Better cost/capability ratio |
| Very long documents | SSM | >100K token support |
| Vision-language tasks | Multimodal | Unified understanding |
| Math/coding reasoning | Reasoning | Quality over speed |
| Image/video generation | Diffusion | SOTA quality |
| Edge deployment | Small Dense / Quantized | Latency critical |

### By Constraint

| Constraint | Recommended Architecture |
|------------|-------------------------|
| Limited memory | SSM or Small Dense |
| Limited compute | MoE or Small Dense |
| Need long context | SSM or Long Context Dense |
| Need multimodal | Multimodal |
| Need reasoning | Reasoning |
| Need generation | Diffusion |

---

## Key Papers

### Foundational
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762) (2017) - Transformer
- [Denoising Diffusion Probabilistic Models](https://arxiv.org/abs/2006.11239) (2020) - Diffusion

### Recent Innovations
- [Mamba](https://arxiv.org/abs/2312.00752) (2023) - SSM
- [Mixtral](https://arxiv.org/abs/2401.04088) (2023) - Open MoE
- [o1 System Card](https://openai.com/index/openai-o1-system-card/) (2024) - Test-time compute
- [DeepSeek-R1](https://arxiv.org/abs/2501.12948) (2025) - RL-based reasoning

---

## Related Resources

### Tools
- [Architecture Classifier](../../scripts/architecture_classifier.py) - Automatic classification script

### Other Wiki Sections
- [Models](../models/) - Models using these architectures
- [Benchmarks](../benchmarks/) - Performance comparisons
- [Research Findings](../research-findings/) - Architecture papers
- [Labs](../labs/) - Lab-specific innovations

---

## Updates and Maintenance

| Date | Change | Author |
|------|--------|--------|
| 2026-04-20 | Initial taxonomy creation | AI Model Research Team |
| 2026-04-20 | Added 6 architecture types | AI Model Research Team |
| 2026-04-20 | Created classifier script | AI Model Research Team |

---

## Contributing

To add a new architecture:

1. Use the [architecture template](../templates/architecture-template.md)
2. Update this README with navigation links
3. Update the comparison matrix
4. Add to the classifier script
5. Submit for review

---

*Last updated: 2026-04-20 by AI Model Research Team*
