---
title: Dense Transformer Architecture
category: architecture
subcategory: foundation
author: AI Model Research Team
date: 2026-04-20
tags: [transformer, attention, dense, gpt, llama, claude]
status: stable
---

# Dense Transformer Architecture

## Overview

**Architecture Name:** Dense Transformer  
**Type:** Foundation Architecture  
**First Introduced:** 2017 ("Attention Is All You Need")  
**Pioneered By:** Google Brain (Vaswani et al.)

## Description

The Dense Transformer is the foundational neural architecture for modern large language models. It uses the transformer block with multi-head self-attention where all parameters are active during forward passes. Unlike sparse architectures, every layer and attention head processes every token, providing consistent computational patterns and predictable behavior.

## How It Works

### Core Mechanism

1. **Tokenization:** Input text is converted to token embeddings
2. **Positional Encoding:** Position information is added (sinusoidal, learned, or RoPE)
3. **Transformer Blocks:** Stack of N identical layers, each containing:
   - Multi-Head Self-Attention: O(n²) complexity
   - Feed-Forward Network: Applied to each position independently
   - Layer Normalization: Pre-norm or post-norm
   - Residual Connections: Around attention and FFN

4. **Output Head:** Projects to vocabulary for next-token prediction

### Architecture Diagram

```
Input Tokens
     ↓
Embedding + Position
     ↓
┌─────────────────────────────────┐
│  Layer Norm                      │
│     ↓                            │
│  Multi-Head Attention            │
│     ↓                            │
│  Residual Addition               │
│     ↓                            │
│  Layer Norm                      │
│     ↓                            │
│  Feed-Forward Network            │
│     ↓                            │
│  Residual Addition               │
└─────────────────────────────────┘
     ↓ (×N layers)
Linear + Softmax
     ↓
Output Tokens
```

### Key Equations

**Self-Attention:**
```
Attention(Q, K, V) = softmax(QK^T / √d_k) V
```

**Multi-Head Attention:**
```
MultiHead(Q, K, V) = Concat(head_1, ..., head_h) W^O
where head_i = Attention(QW_i^Q, KW_i^K, VW_i^V)
```

## Variants

| Variant | Key Difference | Models Using It |
|---------|---------------|-----------------|
| Decoder-Only | Causal masking, left-to-right | GPT-4, Llama, Claude |
| Encoder-Only | Bidirectional attention | BERT, RoBERTa |
| Encoder-Decoder | Cross-attention mechanism | T5, BART |
| Prefix-LM | Partial causal masking | GLM, U-PaLM |

## Innovations (2024-2025)

- **RoPE (Rotary Position Embeddings):** Relative position encoding (Llama, Mistral)
- **ALiBi:** Attention with Linear Biases for better extrapolation
- **Multi-Query Attention:** Shared KV heads for efficient inference
- **Grouped-Query Attention:** Balance between MHA and MQA
- **Sliding Window Attention:** Local attention for long contexts
- **Long Context Extensions:** 128K-2M token windows via fine-tuning

## Advantages

- **Predictable Performance:** Consistent behavior across sequence lengths
- **Proven Scaling Laws:** Well-understood relationship between size and capability
- **Hardware Optimization:** Highly optimized kernels (FlashAttention, etc.)
- **Training Stability:** Extensive research on stable training recipes
- **Ecosystem Maturity:** Widest tooling and deployment support
- **Fine-tuning Flexibility:** Easy to adapt for specific tasks

## Disadvantages

- **Quadratic Complexity:** O(n²) attention limits sequence length
- **Memory Intensive:** KV cache grows with sequence length
- **Compute Inefficiency:** All parameters active regardless of input
- **Context Window Limits:** Practical limits around 100K-200K tokens
- **Inference Cost:** Linear growth in compute with sequence length

## Notable Models Using This Architecture

| Model | Parameters | Context | Lab | Key Feature |
|-------|------------|---------|-----|-------------|
| Llama 3.1 405B | 405B | 128K | Meta | Largest open dense model |
| Claude 3.7 Sonnet | Unknown | 200K | Anthropic | Constitutional AI |
| GPT-4 | Unknown | 128K | OpenAI | RLHF optimized |
| GPT-4.5 | Unknown | 128K | OpenAI | Improved reasoning |
| Gemini 1.5 Pro | Unknown | 2M | Google | Longest context |
| Llama 3 70B | 70B | 8K | Meta | Strong open model |
| Mistral Large 2 | 123B | 128K | Mistral | Efficient architecture |
| Gemma 2 27B | 27B | 8K | Google | Open weights |

## When to Use

### Use Dense Transformers When:
- Maximum compatibility and ecosystem support needed
- Predictable, consistent behavior is critical
- Fine-tuning for specific domains
- Sequence length under 100K tokens
- Hardware optimized deployment required
- Research reproducibility matters

### Avoid When:
- Processing very long sequences (>200K tokens)
- Maximum inference throughput is critical
- Severe compute budget constraints
- Edge deployment with limited memory

## Performance Characteristics

| Metric | Typical Range | Notes |
|--------|---------------|-------|
| Training Compute | ~1e24 FLOPs for 100B+ models | Chinchilla-optimal |
| Inference Latency | Linear with sequence length | ~1-10ms/token |
| Memory (Inference) | 2× model size for KV cache | Varies by optimization |
| Context Window | 4K-2M tokens | Extended via methods |
| Throughput | 10-1000 tokens/sec | Hardware dependent |

## Classification Criteria

A model is classified as Dense Transformer if it meets these criteria:

1. **Full Parameter Activation:** All parameters participate in every forward pass
2. **Attention-Based:** Uses multi-head self-attention as primary mechanism
3. **No Expert Routing:** No conditional computation or routing layers
4. **Standard Transformer Stack:** Layer normalization → attention → FFN pattern

## Related Architectures

- [Mixture of Experts](moe.md) - Sparse alternative
- [State Space Models](ssm.md) - Linear complexity alternative
- [Multimodal](multimodal.md) - Often built on dense transformers

## Resources

- Original Paper: [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- Llama Architecture: [Llama 2 Paper](https://arxiv.org/abs/2307.09288)
- FlashAttention: [Dao et al. 2022](https://arxiv.org/abs/2205.14135)
- RoPE: [Su et al. 2021](https://arxiv.org/abs/2104.09864)

## References

1. Vaswani, A., et al. (2017). Attention Is All You Need. NeurIPS.
2. Brown, T., et al. (2020). Language Models are Few-Shot Learners. NeurIPS.
3. Touvron, H., et al. (2023). Llama 2: Open Foundation and Fine-Tuned Chat Models.

---

*Last updated: 2026-04-20 by AI Model Research Team*
