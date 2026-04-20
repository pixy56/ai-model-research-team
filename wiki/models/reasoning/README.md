# Reasoning Models

Documentation of AI models specialized in advanced reasoning, chain-of-thought, and problem-solving capabilities.

---

## Quick Navigation

| Section | Description |
|---------|-------------|
| [Overview](#overview) | Reasoning model landscape |
| [Types of Reasoning](#types-of-reasoning) | Different reasoning approaches |
| [Leading Models](#leading-models) | Top reasoning models |
| [By Lab](#by-lab) | Models organized by lab |
| [Benchmarks](#benchmark-performance) | Reasoning evaluation |
| [Techniques](#reasoning-techniques) | Methods and approaches |

---

## Overview

Reasoning models are designed to perform multi-step logical inference, mathematical problem-solving, and complex decision-making. They employ various techniques to improve reasoning capabilities beyond standard pattern matching.

### Key Characteristics
- **Chain-of-Thought:** Step-by-step reasoning
- **Self-Correction:** Ability to verify and fix errors
- **Tool Use:** Integration with calculators, code execution
- **Long Context:** Support for extended reasoning chains

### Current Trends (2025-2026)
- Test-time compute scaling (o1-style reasoning)
- Process reward models (PRM)
- Tree-of-thought exploration
- Formal verification integration

---

## Types of Reasoning

### Mathematical Reasoning
- Competition mathematics (AIME, IMO)
- Symbolic manipulation
- Proof generation

### Logical Reasoning
- Deductive inference
- Abductive reasoning
- Commonsense reasoning

### Code Reasoning
- Algorithm design
- Code debugging
- Software engineering tasks

### Scientific Reasoning
- Hypothesis generation
- Experimental design
- Literature synthesis

---

## Leading Models

### Frontier Reasoning Models

| Model | Lab | Type | Key Strength | Date |
|-------|-----|------|--------------|------|
| o3-mini | OpenAI | Test-time compute | STEM reasoning | 2025-01 |
| Claude 3.7 Sonnet (Extended) | Anthropic | Long CoT | Analysis, coding | 2025-02 |
| Gemini 2.0 Flash Thinking | Google | Test-time compute | Multimodal reasoning | 2024-12 |
| DeepSeek-R1 | DeepSeek | RL-based | Math, code | 2025-01 |
| QwQ-32B | Alibaba | Test-time compute | Reasoning, STEM | 2025-03 |

### Specialized Reasoning Models

| Model | Lab | Domain | Notable Feature |
|-------|-----|--------|-----------------|
| AlphaProof | Google | Mathematics | Formal proof generation |
| AlphaGeometry 2 | Google | Geometry | IMO-level geometry |
| OpenAI o1 | OpenAI | General | Chain-of-thought |
| Kimi k1.5 | Moonshot | General | Long context reasoning |

---

## By Lab

### [OpenAI](../../labs/openai.md)
- **o3-mini** - High-efficiency reasoning model
- **o1** - Original test-time compute model
- **o1-pro** - Extended reasoning capabilities
- **GPT-4.5** - General reasoning with CoT

### [Anthropic](../../labs/anthropic.md)
- **Claude 3.7 Sonnet (Extended)** - Long-form reasoning
- **Claude 3.5 Sonnet** - Strong coding and analysis

### [Google DeepMind](../../labs/google.md)
- **Gemini 2.0 Flash Thinking** - Multimodal reasoning
- **AlphaProof** - Formal mathematical reasoning
- **AlphaGeometry 2** - Geometric theorem proving

### [Meta AI](../../labs/meta.md)
- **Llama 3.1 405B** - Strong base model reasoning
- **Llama 4** (preview) - Improved reasoning

### [DeepSeek](../../labs/deepseek.md)
- **DeepSeek-R1** - Open reasoning model via RL
- **DeepSeek-V3** - Strong base capabilities

### [Alibaba](../../labs/alibaba.md)
- **QwQ-32B** - Test-time compute reasoning
- **Qwen2.5-72B** - General reasoning

---

## Benchmark Performance

### MATH (Competition Mathematics)
| Model | Score | Date |
|-------|-------|------|
| o3-mini (high) | 97.3% | 2025-01 |
| DeepSeek-R1 | 97.3% | 2025-01 |
| Gemini 2.0 Flash Thinking | 90.8% | 2024-12 |
| Claude 3.7 Sonnet | 80.2% | 2025-02 |
| GPT-4.5 | 83.4% | 2025-02 |

### GPQA Diamond (Graduate-Level Science)
| Model | Score | Date |
|-------|-------|------|
| o3-mini (high) | 86.0% | 2025-01 |
| DeepSeek-R1 | 71.5% | 2025-01 |
| Claude 3.7 Sonnet | 74.0% | 2025-02 |
| Gemini 2.0 Pro | 74.2% | 2025-02 |

### AIME 2024 (Math Competition)
| Model | Score | Date |
|-------|-------|------|
| o3-mini (high) | 87.3% | 2025-01 |
| DeepSeek-R1 | 79.8% | 2025-01 |
| QwQ-32B | 79.5% | 2025-03 |
| Claude 3.7 Sonnet | 72.0% | 2025-02 |

### SWE-bench Verified (Software Engineering)
| Model | Resolution Rate | Date |
|-------|-----------------|------|
| Claude 3.7 Sonnet | 62.3% | 2025-02 |
| o3-mini | 61.0% | 2025-01 |
| DeepSeek-R1 | 49.2% | 2025-01 |
| GPT-4.5 | 58.5% | 2025-02 |

---

## Reasoning Techniques

### Chain-of-Thought (CoT)
- **Standard CoT:** Step-by-step text reasoning
- **Zero-shot CoT:** "Let's think step by step"
- **Self-Consistency:** Multiple reasoning paths, majority voting

### Tree-of-Thought (ToT)
- Explore multiple reasoning branches
- Evaluate and prune paths
- Best for complex problems

### Test-Time Compute
- **o1-style:** Spend more compute at inference
- **Process Reward Models:** Reward intermediate steps
- **Monte Carlo Tree Search:** Structured exploration

### Tool-Augmented Reasoning
- **Code Execution:** Python for calculations
- **Calculator:** Precise arithmetic
- **Search:** External knowledge retrieval
- **Verification:** Self-checking outputs

### Formal Methods
- **Theorem Proving:** Lean, Coq integration
- **Symbolic Verification:** Logical proof checking
- **Constraint Solving:** SAT/SMT solvers

---

## Tracked Models

*Individual model pages will be created here*

### Test-Time Compute Models
- [ ] o3-mini
- [ ] o1 / o1-pro
- [ ] Gemini 2.0 Flash Thinking
- [ ] DeepSeek-R1
- [ ] QwQ-32B

### General Models with Strong Reasoning
- [ ] Claude 3.7 Sonnet
- [ ] GPT-4.5
- [ ] Gemini 2.0 Pro
- [ ] Llama 3.1 405B

### Specialized Reasoning
- [ ] AlphaProof
- [ ] AlphaGeometry 2

---

## Research Insights

### Key Papers
- [Learning to Reason with LLMs](../../research-findings/papers/) - OpenAI o1 methodology
- [Process Reward Models](../../research-findings/papers/) - Rewarding reasoning steps
- [Scaling Test-Time Compute](../../research-findings/papers/) - Inference-time scaling laws

See [Research Findings](../../research-findings/) for more.

---

## Related Categories

- [LLMs](../llms/) - Base language models
- [Multimodal Models](../multimodal/) - Vision-language reasoning
- [Benchmarks](../../benchmarks/) - Reasoning benchmarks
- [Architectures](../../architectures/) - Reasoning architectures

---

## Template

To add a new reasoning model entry, use the [model template](../../templates/model-template.md).

---

*Last updated: 2026-04-19 by AI Model Research Team*