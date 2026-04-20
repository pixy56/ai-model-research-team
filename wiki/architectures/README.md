# AI Model Architectures

Documentation of architectural innovations and patterns in modern AI models.

---

## Quick Navigation

| Architecture | Type | Key Feature | Notable Models |
|--------------|------|-------------|----------------|
| [Dense Transformers](#dense-transformers) | Foundation | Full attention | GPT-4, Claude, Llama |
| [Mixture of Experts](#mixture-of-experts-moe) | Efficiency | Sparse activation | Mixtral, Qwen-MoE |
| [State Space Models](#state-space-models-ssm) | Long Context | Linear attention | Mamba, Jamba |
| [Multimodal Architectures](#multimodal-architectures) | Fusion | Cross-modal | Gemini, GPT-4o |
| [Reasoning Architectures](#reasoning-architectures) | Inference | Test-time compute | o1, DeepSeek-R1 |

---

## Dense Transformers

### Overview
The standard transformer architecture with full self-attention across all tokens.

### Key Characteristics
- **Attention:** O(n²) complexity
- **Activation:** All parameters active
- **Scaling:** Proven scaling laws

### Innovations (2024-2025)
- **Long Context:** 128K-2M token windows (Gemini, Llama 3)
- **RoPE:** Rotary Position Embeddings (Llama, Mistral)
- **ALiBi:** Attention with Linear Biases
- **Multi-Query Attention:** Efficient KV cache

### Notable Implementations
| Model | Parameters | Context | Key Feature |
|-------|------------|---------|-------------|
| Llama 3.1 405B | 405B | 128K | Dense flagship |
| Claude 3.7 | Unknown | 200K | Constitutional AI |
| GPT-4 | Unknown | 128K | RLHF optimized |

---

## Mixture of Experts (MoE)

### Overview
Sparse architectures activating only a subset of parameters per token.

### Key Characteristics
- **Sparse Activation:** ~10-20% of parameters active
- **Routing:** Learned token-to-expert assignment
- **Efficiency:** Higher capacity without proportional compute

### Architecture Patterns
```
Input → Router → Top-K Experts → Combine → Output
           ↓
      Expert 1, Expert 2, ..., Expert N
```

### Notable Implementations
| Model | Total Params | Active Params | Experts | Lab |
|-------|--------------|---------------|---------|-----|
| Mixtral 8x22B | 176B | 44B | 8 | Mistral |
| Mixtral 8x7B | 56B | 14B | 8 | Mistral |
| Qwen2-57B-A14B | 57B | 14B | 64 | Alibaba |
| DeepSeek-V3 | 671B | 37B | 256 | DeepSeek |

### Load Balancing
- **Loss Terms:** Auxiliary load balancing losses
- **Capacity Factor:** Limit tokens per expert
- **Expert Choice:** Alternative routing strategies

---

## State Space Models (SSM)

### Overview
Linear attention alternatives with O(n) complexity, enabling very long sequences.

### Key Characteristics
- **Complexity:** O(n) sequence length
- **Memory:** Constant memory w.r.t sequence
- **Selectivity:** Input-dependent state transitions

### Mamba Architecture
```
x → Linear → Selective SSM → Linear → Output
     ↑            ↑
   Parameters   State (h)
```

### Variants
| Variant | Key Feature | Models |
|---------|-------------|--------|
| Mamba-1 | Selective SSM | Research |
| Mamba-2 | Structured attention | Research |
| Jamba | SSM + Transformer | AI21 Labs |
| Griffin | Gated linear RNN | Google |

### Trade-offs
| Aspect | Transformer | SSM |
|--------|-------------|-----|
| Long sequences | Poor | Excellent |
| Training stability | Good | Moderate |
| Hardware utilization | Optimized | Emerging |
| Recall ability | Strong | Developing |

---

## Multimodal Architectures

### Vision-Language Models

#### Architecture Patterns
1. **Flamingo-style:** Perceiver resampler + frozen LLM
2. **LLaVA-style:** Projection layer + fine-tuned LLM
3. **Native Multimodal:** Unified architecture (Gemini, GPT-4o)

#### Components
| Component | Function | Examples |
|-----------|----------|----------|
| Vision Encoder | Image features | CLIP, SigLIP, DINOv2 |
| Connector | Bridge vision-text | Q-Former, MLP projector |
| LLM Backbone | Language generation | Llama, Qwen, Mistral |

### Native Multimodal
- **Unified Token Space:** Single vocabulary for all modalities
- **Early Fusion:** Process all modalities together from start
- **Examples:** Gemini 2.0, GPT-4o

---

## Reasoning Architectures

### Test-Time Compute

#### o1-style Architecture
```
Input → Think (Chain-of-Thought) → Verify → Output
         ↑          ↓
      Generate   Reward Model
```

#### Components
1. **Base LLM:** Strong foundation model
2. **Process Reward Model (PRM):** Score reasoning steps
3. **Search:** MCTS, beam search over reasoning paths
4. **Verification:** Self-consistency, tool use

### DeepSeek-R1 Architecture
- **RL-based:** Pure reinforcement learning from base model
- **GRPO:** Group Relative Policy Optimization
- **Cold Start:** SFT before RL for stability

### Reasoning Techniques Comparison
| Technique | Compute | Performance | Models |
|-----------|---------|-------------|--------|
| Chain-of-Thought | Low | Moderate | All |
| Self-Consistency | Medium | Good | All |
| Tree-of-Thought | High | Better | GPT-4, Claude |
| Test-Time Scaling | Very High | Best | o3, R1 |

---

## Emerging Architectures

### Test-Time Training (TTT)
- Update model weights during inference
- Research phase

### Mixture of Depth (MoD)
- Dynamically skip layers
- Efficiency optimization

### Diffusion Language Models
- Discrete diffusion for text generation
- Alternative to autoregressive

### RWKV
- RNN with transformer-like parallelization
- Linear complexity

---

## Architecture Selection Guide

| Use Case | Recommended Architecture | Notes |
|----------|-------------------------|-------|
| General purpose | Dense Transformer | Proven, widely supported |
| Long documents | SSM / Long Context Transformer | >100K tokens |
| High throughput | MoE | Better throughput/cost |
| Edge deployment | Small Dense / Quantized MoE | Latency critical |
| Reasoning tasks | Test-Time Compute | Quality over speed |
| Multimodal | Native Multimodal | Unified processing |

---

## Key Papers

See [Research Findings](../research-findings/) for detailed paper summaries:

- **Attention Is All You Need** (2017) - Original Transformer
- **Mamba** (2023) - SSM architecture
- **Mixtral** (2023) - Open MoE
- **o1 System Card** (2024) - Test-time compute
- **DeepSeek-R1** (2025) - RL-based reasoning

---

## Related Categories

- [Models](../models/) - Models using these architectures
- [Research Findings](../research-findings/) - Architecture papers
- [Labs](../labs/) - Lab-specific architectural innovations

---

## Template

To document a new architecture, use the [architecture template](../templates/architecture-template.md).

---

*Last updated: 2026-04-19 by AI Model Research Team*