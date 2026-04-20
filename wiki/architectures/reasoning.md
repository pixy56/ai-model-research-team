---
title: Reasoning Architecture
category: architecture
subcategory: inference
author: AI Model Research Team
date: 2026-04-20
tags: [reasoning, test-time-compute, chain-of-thought, o1, r1, inference-scaling]
status: emerging
---

# Reasoning Architecture

## Overview

**Architecture Name:** Reasoning Architecture (Test-Time Compute)  
**Type:** Inference-Optimized Architecture  
**First Introduced:** 2024 (OpenAI o1)  
**Pioneered By:** OpenAI, DeepSeek

## Description

Reasoning architectures represent a paradigm shift from training-time scaling to test-time compute scaling. Instead of solely relying on larger models trained with more data, these architectures allocate additional computation during inference to "think longer" about problems. They use techniques like chain-of-thought generation, reward model verification, and search over reasoning paths to improve performance on complex tasks like mathematics, coding, and scientific reasoning.

## How It Works

### Core Mechanism

1. **Extended Thinking:** Generate long chain-of-thought reasoning
2. **Process Reward:** Score intermediate reasoning steps
3. **Search/Verification:** Explore multiple reasoning paths
4. **Self-Consistency:** Verify and refine answers
5. **Token Budget:** Allocate compute based on problem difficulty

### Architecture Patterns

#### Pattern 1: o1-Style (Inference-Time Scaling)
```
Input Problem
     ↓
Think (Chain-of-Thought Generation)
     ↓
┌─────────────────────────────────────┐
│  Process Reward Model (PRM)          │
│  - Scores each reasoning step        │
│  - Guides search direction           │
└─────────────────────────────────────┘
     ↓
Search / Beam Search / MCTS
     ↓
Verify Answer
     ↓
Output Final Answer
```

#### Pattern 2: DeepSeek-R1 (RL-Based)
```
Base LLM (Pre-trained)
     ↓
Cold Start (Small SFT for stability)
     ↓
Reinforcement Learning (GRPO)
     ↓
┌─────────────────────────────────────┐
│  Reward Functions:                   │
│  - Accuracy rewards (verifiable)     │
│  - Format rewards (CoT structure)      │
│  - Language consistency              │
└─────────────────────────────────────┘
     ↓
Rejection Sampling Fine-tuning
     ↓
Final RL (Human preferences)
```

#### Pattern 3: Hybrid (Claude 3.7 Sonnet)
```
Input
     ↓
┌─────────────────────────────────────┐
│  Mode Selection                      │
│  - Standard: Fast response           │
│  - Extended: Deep reasoning          │
└─────────────────────────────────────┘
     ↓
[Standard Path]    [Extended Path]
     ↓                    ↓
Quick Answer      Chain-of-Thought
                         ↓
                   Reasoning Engine
                         ↓
                   Verified Answer
```

### Key Equations

**Process Reward Model:**
```
PRM(s_t | s_{<t}) = P(correct_step | current_state)
where s_t is reasoning step t
```

**Test-Time Compute Scaling:**
```
Performance ∝ (Model_Capability × Compute_Budget)
where Compute_Budget = N_samples × L_reasoning
```

**GRPO (Group Relative Policy Optimization):**
```
∇J = E[clip(ratio · A_t, 1-ε, 1+ε)]
where A_t = (R_i - mean(R)) / std(R) for group rewards
```

## Variants

| Variant | Key Feature | Models Using It |
|---------|-------------|-----------------|
| Inference Scaling | More tokens at test time | o1, o3 |
| RL-Based | Pure RL from base model | DeepSeek-R1 |
| Hybrid | Switchable reasoning modes | Claude 3.7 Sonnet |
| MCTS | Tree search over reasoning | Research |
| Self-Play | Generate and critique | AlphaProof |
| Tool-Augmented | External tool use | o3 with tools |

## Innovations (2024-2025)

- **Process Reward Models:** Step-by-step verification
- **Inference Scaling Laws:** Performance vs compute curves
- **Test-Time Training:** Update weights during inference
- **Chain-of-Thought Distillation:** Transfer to smaller models
- **Multi-Modal Reasoning:** Visual reasoning with CoT
- **Tool-Integrated Reasoning:** Calculator, code interpreter

## Advantages

- **Better Accuracy:** Significant gains on reasoning benchmarks
- **Verifiable Outputs:** Step-by-step reasoning auditable
- **Compute Flexibility:** Trade time for quality
- **Self-Improvement:** Can critique own reasoning
- **Emergent Strategies:** Discovers novel solution approaches
- **Interpretability:** Chain-of-thought explains decisions

## Disadvantages

- **Latency:** Much slower than standard inference
- **Cost:** Higher per-query compute costs
- **Training Complexity:** Requires RL and reward modeling
- **Narrow Applicability:** Best for verifiable domains (math, code)
- **Overthinking:** May reason excessively on simple problems
- **Training Instability:** RL training challenging

## Notable Models Using This Architecture

| Model | Approach | Training | Lab | Key Feature |
|-------|----------|----------|-----|-------------|
| o3 | Inference Scaling | RL + Search | OpenAI | Highest reasoning scores |
| o1 | Inference Scaling | RL | OpenAI | First reasoning model |
| DeepSeek-R1 | RL-Based | GRPO | DeepSeek | Open reasoning model |
| DeepSeek-R1-Zero | Pure RL | No SFT | DeepSeek | Emergent CoT |
| Claude 3.7 Sonnet | Hybrid | Constitutional | Anthropic | Toggle reasoning |
| Gemini 2.0 Flash Thinking | Inference Scaling | RL | Google | Fast reasoning |
| QwQ-32B | Inference Scaling | RL | Alibaba | Open model |
| Kimi k1.5 | Long-CoT | RL | Moonshot | Extended thinking |

## When to Use

### Use Reasoning Models When:
- Complex mathematics required
- Multi-step coding problems
- Scientific reasoning tasks
- Logic puzzles and competitions
- Answer verification possible
- Quality more important than latency

### Avoid When:
- Low latency critical
- Simple factual queries
- Creative writing tasks
- Budget constraints tight
- Verifiable answers unavailable
- Standard LLM suffices

## Performance Characteristics

| Metric | Typical Range | Notes |
|--------|---------------|-------|
| Reasoning Tokens | 1K-100K | Much longer than standard |
| Latency | 10-100× standard | Minutes for hard problems |
| Math Benchmarks | 90-95% | AIME, AMC scores |
| Code Benchmarks | 80-90% | Competitive programming |
| Cost | 10-50× higher | Per-query compute |

## Classification Criteria

A model is classified as Reasoning if it meets these criteria:

1. **Extended Inference:** Allocates additional compute at test time
2. **Chain-of-Thought:** Generates explicit reasoning steps
3. **Verification:** Self-checks or validates intermediate steps
4. **RL Training:** Uses reinforcement learning in training

## Related Architectures

- [Dense Transformer](dense-transformer.md) - Base architecture
- [Mixture of Experts](moe.md) - Often combined with reasoning
- [Multimodal](multimodal.md) - Can include reasoning

## Resources

- o1 System Card: [OpenAI 2024](https://openai.com/index/openai-o1-system-card/)
- DeepSeek-R1: [DeepSeek 2025](https://arxiv.org/abs/2501.12948)
- Inference Scaling: [Snell et al. 2024](https://arxiv.org/abs/2408.03314)
- Process Reward Models: [Lightman et al. 2023](https://arxiv.org/abs/2305.20050)

## References

1. OpenAI. (2024). Learning to Reason with LLMs.
2. Guo, D., et al. (2025). DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning.
3. Lightman, H., et al. (2023). Let's Verify Step by Step.

---

*Last updated: 2026-04-20 by AI Model Research Team*
