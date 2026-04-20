# Large Language Models (LLMs)

Documentation of major large language models, their capabilities, and performance characteristics.

---

## Quick Navigation

| Section | Description |
|---------|-------------|
| [Overview](#overview) | LLM landscape summary |
| [By Lab](#by-lab) | Models organized by research lab |
| [By Architecture](#by-architecture) | Models by architectural approach |
| [By Size](#by-model-size) | Models organized by parameter count |
| [Benchmarks](#benchmark-performance) | Performance on key benchmarks |
| [All Models](#tracked-models) | Complete list of tracked models |

---

## Overview

Large Language Models (LLMs) are transformer-based models trained on vast text corpora to understand and generate human language. This category tracks general-purpose text models with >1B parameters.

### Key Characteristics
- **Primary Input:** Text tokens
- **Primary Output:** Text generation
- **Training:** Self-supervised on web text, books, code
- **Capabilities:** Text completion, summarization, translation, reasoning

### Current Trends (2025-2026)
- Increasing context windows (128K+ tokens)
- Mixture of Experts (MoE) architectures for efficiency
- Improved reasoning through test-time compute
- Better instruction following and alignment

---

## By Lab

### [OpenAI](../../labs/openai.md)
| Model | Release | Parameters | Context | Status |
|-------|---------|------------|---------|--------|
| GPT-4o | May 2024 | Unknown | 128K | Active |
| GPT-4.5 | Feb 2025 | Unknown | 128K | Active |
| o3-mini | Jan 2025 | Unknown | 200K | Active |

### [Anthropic](../../labs/anthropic.md)
| Model | Release | Parameters | Context | Status |
|-------|---------|------------|---------|--------|
| Claude 3.5 Sonnet | Jun 2024 | Unknown | 200K | Active |
| Claude 3.5 Opus | - | Unknown | 200K | Active |
| Claude 3.7 Sonnet | Feb 2025 | Unknown | 200K | Active |

### [Google DeepMind](../../labs/google.md)
| Model | Release | Parameters | Context | Status |
|-------|---------|------------|---------|--------|
| Gemini 1.5 Pro | Feb 2024 | Unknown | 1M-2M | Active |
| Gemini 2.0 Flash | Dec 2024 | Unknown | 1M | Active |
| Gemini 2.0 Pro | Feb 2025 | Unknown | 2M | Active |

### [Meta AI](../../labs/meta.md)
| Model | Release | Parameters | Context | Status |
|-------|---------|------------|---------|--------|
| Llama 3.1 405B | Jul 2024 | 405B | 128K | Active |
| Llama 3.3 70B | Dec 2024 | 70B | 128K | Active |
| Llama 4 | Apr 2025 | Unknown | 256K | Preview |

### [Mistral AI](../../labs/mistral.md)
| Model | Release | Parameters | Context | Status |
|-------|---------|------------|---------|--------|
| Mistral Large 2 | Jul 2024 | 123B | 128K | Active |
| Mistral Small 3 | Jan 2025 | 24B | 128K | Active |
| Codestral | May 2024 | 22B | 32K | Active |

### [Microsoft Research](../../labs/microsoft.md)
| Model | Release | Parameters | Context | Status |
|-------|---------|------------|---------|--------|
| Phi-4 | Dec 2024 | 14B | 16K | Active |
| MAUI-1 | 2025 | Unknown | 128K | Research |

---

## By Architecture

### Dense Transformers
- GPT-4 series
- Claude series
- Llama 2/3 series
- Phi series

### Mixture of Experts (MoE)
- Mixtral 8x7B / 8x22B
- Qwen2-57B-A14B
- DeepSeek-V3

### State Space Models (SSM)
- Mamba-based models (emerging in 2025)

---

## By Model Size

### Small (< 10B parameters)
- Phi-4 (14B)
- Mistral Small 3 (24B)

### Medium (10B - 100B parameters)
- Llama 3.3 70B
- Mistral Large 2 (123B)
- Qwen2.5-72B

### Large (> 100B parameters)
- Llama 3.1 405B
- GPT-4 series
- Gemini 2.0 Pro

---

## Benchmark Performance

### MMLU (Higher is better)
| Model | Score | Date |
|-------|-------|------|
| GPT-4.5 | 90.2% | 2025-02 |
| Gemini 2.0 Pro | 89.8% | 2025-02 |
| Claude 3.7 Sonnet | 88.5% | 2025-02 |
| Llama 3.1 405B | 85.2% | 2024-07 |

### HumanEval (Code Generation)
| Model | Pass@1 | Date |
|-------|--------|------|
| Claude 3.7 Sonnet | 92.0% | 2025-02 |
| GPT-4.5 | 90.5% | 2025-02 |
| Gemini 2.0 Pro | 89.2% | 2025-02 |

### MATH (Mathematical Reasoning)
| Model | Score | Date |
|-------|-------|------|
| GPT-4.5 | 83.4% | 2025-02 |
| Gemini 2.0 Pro | 81.9% | 2025-02 |
| Claude 3.7 Sonnet | 80.2% | 2025-02 |

See [full benchmarks](../../benchmarks/README.md) for more details.

---

## Tracked Models

*Individual model pages will be created here*

### OpenAI
- [ ] GPT-4o
- [ ] GPT-4.5
- [ ] o3-mini

### Anthropic
- [ ] Claude 3.5 Sonnet
- [ ] Claude 3.5 Opus
- [ ] Claude 3.7 Sonnet

### Google
- [ ] Gemini 1.5 Pro
- [ ] Gemini 2.0 Flash
- [ ] Gemini 2.0 Pro

### Meta
- [ ] Llama 3.1 405B
- [ ] Llama 3.3 70B
- [ ] Llama 4 (when released)

### Mistral
- [ ] Mistral Large 2
- [ ] Mistral Small 3
- [ ] Codestral

### Microsoft
- [ ] Phi-4

---

## Related Categories

- [Multimodal Models](../multimodal/) - Vision-language models
- [Reasoning Models](../reasoning/) - Specialized reasoning models
- [Benchmarks](../../benchmarks/) - Evaluation metrics
- [Architectures](../../architectures/) - Technical architecture details
- [Research Findings](../../research-findings/) - Latest research insights

---

## Template

To add a new LLM entry, use the [model template](../../templates/model-template.md).

---

*Last updated: 2026-04-19 by AI Model Research Team*