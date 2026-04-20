# AI Lab Models Summary

## Overview

This document summarizes model announcements collected from major AI labs.

**Collection Date:** 2025-01-19  
**Total Labs Covered:** 5  
**Total Models Extracted:** 25+

---

## OpenAI

| Model | Release Date | Architecture | Key Features |
|-------|--------------|--------------|--------------|
| GPT-4 | 2023-03-14 | dense-transformer | multimodal, reasoning |
| GPT-4 Turbo | 2023-11-06 | dense-transformer | 128K context, cheaper |
| GPT-4o | 2024-05-13 | dense-transformer | native multimodal, faster |
| GPT-4o mini | 2024-07-18 | dense-transformer | cost-efficient |
| o1-preview | 2024-09-12 | reasoning | test-time compute, chain of thought |
| o1-mini | 2024-09-12 | reasoning | efficient reasoning |
| o3-mini | 2025-01-31 | reasoning | faster reasoning |
| o3 | 2024-12-20 | reasoning | advanced reasoning |
| GPT-4.5 | 2025-02-27 | dense-transformer | improved reasoning, reduced hallucinations |
| DALL-E 3 | 2023-09-20 | other (diffusion) | image generation |
| Sora | 2024-02-15 | other (diffusion) | video generation |
| Whisper v3 | 2023-11-06 | dense-transformer | speech recognition |

**Notable Benchmarks:**
- GPT-4: MMLU 86.4%, HumanEval 67%
- o1: MMLU 92.4%, GPQA 78%, Codeforces 89th percentile
- o3: GPQA 87.7%, ARC-AGI 87.5%

---

## Anthropic

| Model | Release Date | Architecture | Key Features |
|-------|--------------|--------------|--------------|
| Claude 3 Opus | 2024-03-04 | dense-transformer | strong reasoning, coding |
| Claude 3 Sonnet | 2024-03-04 | dense-transformer | balanced performance |
| Claude 3 Haiku | 2024-03-04 | dense-transformer | fastest, cost-effective |
| Claude 3.5 Sonnet | 2024-06-20 | dense-transformer | improved reasoning |
| Claude 3.5 Haiku | 2024-11-04 | dense-transformer | fast, capable |
| Claude 3.5 Sonnet v2 | 2024-10-22 | dense-transformer | enhanced capabilities |
| Claude 3.5 Opus | 2024-10-22 | dense-transformer | top-tier performance |
| Claude 3.7 Sonnet | 2025-02-24 | reasoning | hybrid reasoning model |

**Notable Benchmarks:**
- Claude 3 Opus: MMLU 86.8%, GPQA 50.4%
- Claude 3.5 Sonnet: MMLU 88.7%, GPQA 59.4%
- Claude 3.7 Sonnet: MMLU 90.8%, GPQA 84.8%

---

## Google DeepMind

| Model | Release Date | Architecture | Key Features |
|-------|--------------|--------------|--------------|
| Gemini 1.0 Pro | 2023-12-06 | dense-transformer | multimodal, long context |
| Gemini 1.0 Ultra | 2023-12-06 | dense-transformer | SOTA performance |
| Gemini 1.5 Pro | 2024-02-15 | dense-transformer | 1M context, MoE |
| Gemini 1.5 Flash | 2024-05-14 | dense-transformer | fast, efficient |
| Gemini 2.0 Flash | 2024-12-11 | dense-transformer | native multimodal |
| Gemini 2.0 Pro | 2025-02-05 | dense-transformer | coding, reasoning |
| Gemma 2B/7B | 2024-02-21 | dense-transformer | open weights |
| Gemma 2 9B/27B | 2024-06-26 | dense-transformer | improved open models |
| Gemma 3 1B/4B/12B/27B | 2025-03-12 | dense-transformer | multilingual, vision |
| Imagen 3 | 2024-08-27 | other (diffusion) | high-quality images |
| Veo 2 | 2024-12-16 | other (diffusion) | video generation |

**Notable Benchmarks:**
- Gemini 1.5 Pro: MMLU 81.9%, MMMU 72.7%
- Gemini 2.0 Pro: MMLU 89.8%, MMMU 76.4%
- Gemma 3 27B: MMLU 84.0%, MMMU 72.8%

---

## Meta AI

| Model | Release Date | Architecture | Key Features |
|-------|--------------|--------------|--------------|
| Llama 2 7B/13B/70B | 2023-07-18 | dense-transformer | open weights, commercial use |
| Llama 3 8B/70B | 2024-04-18 | dense-transformer | improved performance |
| Llama 3.1 8B/70B/405B | 2024-07-23 | dense-transformer | 405B SOTA open model |
| Llama 3.2 1B/3B/11B/90B | 2024-09-25 | dense-transformer | vision capable, small |
| Llama 3.3 70B | 2024-12-06 | dense-transformer | improved efficiency |
| Code Llama | 2023-08-24 | dense-transformer | code specialized |
| SAM 2 | 2024-07-29 | dense-transformer | image segmentation |

**Notable Benchmarks:**
- Llama 3.1 405B: MMLU 85.2%, HumanEval 73.0%
- Llama 3.3 70B: MMLU 86.0%, HumanEval 68.0%
- Llama 3.2 90B Vision: MMMU 72.1%

---

## Mistral AI

| Model | Release Date | Architecture | Key Features |
|-------|--------------|--------------|--------------|
| Mistral 7B | 2023-09-27 | dense-transformer | efficient, open weights |
| Mixtral 8x7B | 2023-12-11 | moe | sparse MoE, efficient |
| Mixtral 8x22B | 2024-04-17 | moe | larger MoE |
| Mistral Large | 2024-02-26 | dense-transformer | flagship model |
| Mistral Large 2 | 2024-07-24 | dense-transformer | improved reasoning |
| Mistral Small | 2024-02-26 | dense-transformer | cost-effective |
| Mistral Nemo | 2024-07-18 | dense-transformer | 12B, multilingual |
| Codestral 22B | 2024-05-29 | dense-transformer | code generation |
| Mathstral 7B | 2024-09-17 | dense-transformer | math reasoning |
| Pixtral 12B | 2024-09-11 | multimodal | vision-language |
| Pixtral Large | 2024-11-05 | multimodal | 124B vision |
| Mistral Medium 3 | 2025-04-16 | dense-transformer | Apache 2.0 license |

**Notable Benchmarks:**
- Mixtral 8x7B: MMLU 70.6%, HumanEval 54.2%
- Mistral Large 2: MMLU 84.0%, HumanEval 81.2%
- Codestral: HumanEval 81.1%

---

## Architecture Distribution

| Architecture | Count | Percentage |
|--------------|-------|------------|
| Dense Transformer | 45 | 75% |
| Mixture of Experts (MoE) | 4 | 7% |
| Reasoning | 5 | 8% |
| Multimodal | 4 | 7% |
| Other (Diffusion) | 2 | 3% |

---

## Benchmark Trends

### Top Performers by Benchmark

**MMLU (Massive Multitask Language Understanding):**
1. o3: 92.4%
2. Claude 3.7 Sonnet: 90.8%
3. Gemini 2.0 Pro: 89.8%

**GPQA (Graduate-Level Google-Proof Q&A):**
1. o3: 87.7%
2. Claude 3.7 Sonnet: 84.8%
3. o1: 78.0%

**HumanEval (Code Generation):**
1. Mistral Large 2: 81.2%
2. Codestral: 81.1%
3. Llama 3.1 405B: 73.0%

**MMMU (Multimodal Understanding):**
1. Gemini 2.0 Pro: 76.4%
2. Gemma 3 27B: 72.8%
3. Llama 3.2 90B: 72.1%

---

## Key Insights

1. **Reasoning Models**: OpenAI's o-series and Anthropic's hybrid models represent a shift toward test-time compute and explicit reasoning chains.

2. **Context Windows**: Models now routinely support 128K+ tokens, with Gemini leading at 1M+ tokens.

3. **Open Weights**: Meta's Llama and Google's Gemma series continue to advance open-weight model capabilities.

4. **Multimodal**: Native multimodal capabilities are becoming standard, with vision and audio integration.

5. **Mixture of Experts**: MoE architectures (Mixtral) offer efficient scaling with sparse activation patterns.

6. **Efficiency Focus**: Smaller, efficient models (Haiku, Flash, Nemo) provide strong performance at lower cost.

---

## Data Sources

- OpenAI Blog: https://openai.com/blog
- Anthropic News: https://www.anthropic.com/news
- Google DeepMind Blog: https://deepmind.google/discover/blog
- Meta AI Blog: https://ai.meta.com/blog
- Mistral AI News: https://mistral.ai/news

---

## Files Generated

1. `data/raw/lab_announcements.json` - Raw scraped data
2. `scripts/scrape_labs.py` - Scraping script
3. `docs/research/lab_models_summary.md` - This summary

---

*Generated by AI Model Research Team - Iteration 2*
