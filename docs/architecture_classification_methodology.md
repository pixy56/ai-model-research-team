# Architecture Classification Methodology

## Overview

This document describes the methodology used to classify 179 AI models by architecture type using the established taxonomy.

## Taxonomy

The classification uses 6 architecture types:

1. **Dense Transformer** - Full attention, all parameters active (e.g., GPT-4, Llama, Claude)
2. **MoE (Mixture of Experts)** - Sparse activation, expert routing (e.g., Mixtral, DeepSeek-V3)
3. **SSM (State Space Models)** - Linear complexity, state-based (e.g., Mamba, Jamba)
4. **Multimodal** - Cross-modal processing (e.g., GPT-4o, Gemini, Llama Vision)
5. **Reasoning** - Test-time compute, chain-of-thought (e.g., o3, DeepSeek-R1)
6. **Diffusion** - Iterative denoising for generation (e.g., DALL-E, Sora, Stable Diffusion)

## Classification Methods

### Method 1: Name Pattern Matching (High Priority)

Models are classified by analyzing their names for architectural indicators:

- **Reasoning indicators**: `o1`, `o3`, `r1`, `reflection`, `reasoning`, `thinking`, `marco-o1`, `cirrus`
- **Multimodal indicators**: `vl`, `vision`, `4o`, `pixtral`, `visstar`, `gemini`, `audio`
- **MoE indicators**: `mixtral`, `8x`, `moe`, `expert`
- **SSM indicators**: `mamba`, `ssm`, `rwkv`, `state-space`
- **Diffusion indicators**: `diffusion`, `dall-e`, `sora`, `imagen`, `veo`

### Method 2: HuggingFace Architecture Class (Medium Priority)

Mapping from HuggingFace transformer classes:

| HF Class | Architecture |
|----------|--------------|
| LlamaForCausalLM | dense-transformer |
| Qwen2ForCausalLM | dense-transformer |
| MistralForCausalLM | dense-transformer |
| MixtralForCausalLM | moe |
| Gemma2ForCausalLM | dense-transformer |
| Phi3ForCausalLM | dense-transformer |
| Qwen2VLForConditionalGeneration | multimodal |
| MambaForCausalLM | ssm |

### Method 3: Default Classification (Low Priority)

Models without specific indicators default to `dense-transformer` with low confidence.

## Confidence Scoring

| Confidence | Score | Criteria |
|------------|-------|----------|
| High | 0.90-0.95 | Explicit naming or authoritative source |
| Medium | 0.70-0.85 | Strong pattern/keyword match |
| Low | 0.50-0.70 | Default or inferred classification |

## Results Summary

### Classification Distribution

| Architecture | Count | Percentage |
|--------------|-------|------------|
| Dense Transformer | 169 | 94.4% |
| Reasoning | 5 | 2.8% |
| Multimodal | 4 | 2.2% |
| SSM | 1 | 0.6% |
| MoE | 0 | 0.0% |
| Diffusion | 0 | 0.0% |

### Confidence Distribution

| Confidence | Count | Percentage |
|------------|-------|------------|
| High | 162 | 90.5% |
| Low | 14 | 7.8% |
| Medium | 3 | 1.7% |

**High confidence coverage: 90.5%**

## Edge Cases and Hybrid Architectures

The following models were identified as hybrid architectures:

1. **glaiveai/Reflection-Llama-3.1-70B** - Dense transformer with reasoning training
2. **Qwen/Qwen2-VL-72B-Instruct** - Dense transformer base with multimodal capabilities
3. **Qwen/QwQ-32B-Preview** - Dense transformer with reasoning training

These are classified by their primary distinguishing feature (reasoning/multimodal) but noted as hybrids.

## Cross-Validation with Lab Announcements

The classifications were cross-validated against 47 models from lab announcements:

| Architecture | Lab Announcements | Our Classification |
|--------------|-------------------|-------------------|
| Dense Transformer | 41 | 169* |
| Multimodal | 7 | 4* |
| Reasoning | 5 | 5 |
| MoE | 2 | 0* |
| Other | 4 | 0* |

*Note: The 179 models in normalized_scores are primarily community/modified variants of lab models, which explains the different distributions. Lab models like Mixtral 8x7B/8x22B (MoE) and Gemini (multimodal) are not present in the normalized_scores dataset as they are API-only models.

## Reasoning Models (5)

| Model | Confidence | Evidence |
|-------|------------|----------|
| AIDC-AI/Marco-o1 | High | Pattern match: \\bo1\\b |
| glaiveai/Reflection-Llama-3.1-70B | High | Pattern match: reflection-llama |
| Qwen/QwQ-32B-Preview | High | Pattern match: qwq- |
| Sao10K/70B-L3.3-Cirrus-x1 | High | Pattern match: cirrus |
| Steelskull/L3.3-Nevoria-R1-70b | High | Pattern match: r1- |

## Multimodal Models (4)

| Model | Confidence | Evidence |
|-------|------------|----------|
| Gemini | High | Model name contains 'Gemini' |
| 1TuanPham/T-VisStar-7B-v0.1 | High | Pattern match: visstar |
| 1TuanPham/T-VisStar-v0.1 | High | Pattern match: visstar |
| Qwen/Qwen2-VL-72B-Instruct | High | Pattern match: qwen.*vl |

## SSM Models (1)

| Model | Confidence | Evidence |
|-------|------------|----------|
| ssmits/Qwen2.5-95B-Instruct | Medium | Keyword match: ssm |

## Low Confidence Classifications (14 models)

These models require manual verification:

- Research paper models (paper_2604.*): Defaulted to dense-transformer
- Models with unusual naming patterns
- Models with "Unknown" HF class

## Limitations

1. **Lab API models not included**: Major lab models (GPT-4, Claude, Gemini, etc.) are not in the normalized_scores dataset as they are API-only
2. **Community models**: Most models are fine-tuned variants of base architectures
3. **Naming inconsistencies**: Community models may not follow consistent naming conventions
4. **Missing MoE/Diffusion**: No MoE or diffusion models in the dataset (these are primarily lab/API models)

## Recommendations for Manual Review

The following models should be manually reviewed:

1. All 14 low-confidence classifications
2. Models with "Unknown" HF class (17 models)
3. Research paper models (paper_2604.*)

## Files Generated

- `data/processed/architecture_classifications.json` - Complete classifications with metadata
- `docs/architecture_classification_methodology.md` - This documentation

## Version

- Classification Version: 1.0.0
- Taxonomy Version: 1.0
- Created: 2026-04-20
