# AI Benchmarks

Comprehensive reference for evaluating and comparing AI model performance across tasks and domains.

---

## Quick Navigation

| Category | Description | Benchmarks |
|----------|-------------|------------|
| [Core Benchmarks](#core-benchmarks) | Language understanding & reasoning | MMLU, HumanEval, GPQA, MATH, SWE-bench |
| [Multimodal Benchmarks](#multimodal-benchmarks) | Vision, video, audio tasks | MMMU, MMBench, ChartQA |
| [Reasoning Benchmarks](#reasoning-benchmarks) | Advanced reasoning | ARC, HellaSwag, GSM8K |
| [Code Benchmarks](#code-benchmarks) | Programming tasks | HumanEval, MBPP, SWE-bench |
| [Safety Benchmarks](#safety-benchmarks) | Alignment & safety | TruthfulQA, BBQ, HELM |
| [Leaderboards](#leaderboards) | Live rankings | LMSYS, Open LLM Leaderboard |

---

## Core Benchmarks

### MMLU (Massive Multitask Language Understanding)
- **Description:** 57 tasks covering STEM, humanities, social sciences, and professional subjects
- **Metric:** Accuracy (%)
- **Difficulty:** High school to professional level
- **Source:** [Papers with Code](https://paperswithcode.com/sota/multi-task-language-understanding-on-mmlu)
- **Top Scores (2025):**
  - o3-mini: 92.4%
  - GPT-4.5: 90.2%
  - Gemini 2.0 Pro: 89.8%

### HumanEval
- **Description:** Code generation benchmark with 164 programming problems
- **Metric:** Pass@k (Pass@1, Pass@10, Pass@100)
- **Language:** Python
- **Source:** [OpenAI](https://github.com/openai/human-eval)
- **Top Scores (2025):**
  - Claude 3.7 Sonnet: 92.0% (Pass@1)
  - GPT-4.5: 90.5% (Pass@1)
  - o3-mini: 92.4% (Pass@1)

### GPQA (Graduate-Level Google-Proof Q&A)
- **Description:** Graduate-level science questions requiring deep expertise
- **Variants:** GPQA Extended, GPQA Diamond
- **Metric:** Accuracy (%)
- **Source:** [NYU](https://github.com/idavidrein/gpqa)
- **Top Scores (2025):**
  - o3-mini (high): 86.0% (Diamond)
  - Claude 3.7 Sonnet: 74.0% (Diamond)
  - Gemini 2.0 Pro: 74.2% (Diamond)

### MATH
- **Description:** Competition mathematics problems from AMC, AIME, Olympiads
- **Metric:** Accuracy (%)
- **Difficulty:** High school competition to undergraduate
- **Source:** [Hugging Face](https://huggingface.co/datasets/hendrycks/competition_math)
- **Top Scores (2025):**
  - o3-mini (high): 97.3%
  - DeepSeek-R1: 97.3%
  - GPT-4.5: 83.4%

### SWE-bench
- **Description:** Real-world software engineering tasks from GitHub issues
- **Variants:** SWE-bench Lite, SWE-bench Verified
- **Metric:** Resolution rate (%)
- **Source:** [Princeton](https://www.swebench.com/)
- **Top Scores (2025):**
  - Claude 3.7 Sonnet: 62.3% (Verified)
  - o3-mini: 61.0% (Verified)
  - GPT-4.5: 58.5% (Verified)

---

## Multimodal Benchmarks

### MMMU (Massive Multi-discipline Multimodal Understanding)
- **Description:** College-level multimodal problems across disciplines
- **Metric:** Accuracy (%)
- **Tasks:** Image + text questions
- **Top Scores (2025):**
  - Gemini 2.0 Pro: 82.4%
  - GPT-4o: 69.1%
  - Claude 3.7 Sonnet: 68.3%

### MMBench
- **Description:** Comprehensive multimodal evaluation with circular evaluation
- **Metric:** Accuracy (%)
- **Categories:** 20+ capability dimensions
- **Top Scores (2025):**
  - Gemini 2.0 Pro: 89.2%
  - GPT-4o: 83.4%
  - Claude 3.7 Sonnet: 81.5%

### ChartQA
- **Description:** Chart understanding and reasoning
- **Metric:** Accuracy (%)
- **Source:** [Microsoft](https://github.com/vis-nlp/ChartQA)

### DocVQA
- **Description:** Document visual question answering
- **Metric:** ANLS (Average Normalized Levenshtein Similarity)
- **Source:** [DocVQA](https://rrc.cvc.uab.es/?ch=17)

### TextVQA
- **Description:** Text-based visual question answering
- **Metric:** Accuracy (%)
- **Source:** [TextVQA](https://textvqa.org/)

---

## Reasoning Benchmarks

### ARC (AI2 Reasoning Challenge)
- **Description:** Grade-school science questions
- **Variants:** ARC-Easy, ARC-Challenge
- **Metric:** Accuracy (%)
- **Source:** [AI2](https://allenai.org/data/arc)

### HellaSwag
- **Description:** Commonsense reasoning through sentence completion
- **Metric:** Accuracy (%)
- **Source:** [HellaSwag](https://rowanzellers.com/hellaswag/)

### GSM8K
- **Description:** Grade school math word problems
- **Metric:** Accuracy (%)
- **Source:** [OpenAI](https://github.com/openai/grade-school-math)
- **Top Scores:** Most models now >95%

### BBH (Big-Bench Hard)
- **Description:** Challenging subset of BIG-bench tasks
- **Metric:** Accuracy (%)
- **Source:** [Google](https://github.com/google/BIG-bench)

---

## Code Benchmarks

### MBPP (Mostly Basic Python Problems)
- **Description:** Python coding problems
- **Metric:** Pass@k
- **Source:** [Google](https://github.com/google-research/google-research/tree/master/mbpp)

### DS-1000
- **Description:** Data science code generation
- **Metric:** Accuracy (%)
- **Source:** [DS-1000](https://ds1000-code-gen.github.io/)

### LiveCodeBench
- **Description:** Live coding competition problems
- **Metric:** Pass@k
- **Source:** [LiveCodeBench](https://livecodebench.github.io/)

### Aider
- **Description:** AI pair programming benchmark
- **Metric:** Success rate (%)
- **Source:** [Aider](https://aider.chat/docs/leaderboard.html)

---

## Safety Benchmarks

### TruthfulQA
- **Description:** Truthfulness in question answering
- **Metric:** Accuracy (%)
- **Source:** [TruthfulQA](https://github.com/sylinrl/TruthfulQA)

### BBQ (Bias Benchmark for QA)
- **Description:** Social bias evaluation
- **Source:** [BBQ](https://github.com/nyu-mll/BBQ)

### HELM (Holistic Evaluation of Language Models)
- **Description:** Multi-metric evaluation framework
- **Source:** [HELM](https://crfm.stanford.edu/helm/)

### MT-Bench
- **Description:** Multi-turn conversation capability
- **Source:** [LMSYS](https://lmsys.org/blog/2023-06-22-mt-bench/)

---

## Leaderboards

### Live Leaderboards

| Platform | URL | Features |
|----------|-----|----------|
| LMSYS Chatbot Arena | [chat.lmsys.org](https://chat.lmsys.org) | Human preference rankings |
| Open LLM Leaderboard | [huggingface.co/spaces/open-llm-leaderboard](https://huggingface.co/spaces/open-llm-leaderboard) | Open model comparison |
| LiveBench | [livebench.ai](https://www.livebench.ai/) | Contamination-resistant |
| SEAL | [scale.com/leaderboard](https://scale.com/leaderboard) | Private evaluations |

### Evaluation Platforms
- **EleutherAI LM Evaluation Harness:** Standardized evaluation framework
- **BIG-bench:** Collaborative benchmark suite
- **BIG-bench Lite:** Lightweight version

---

## Benchmark Selection Guide

### For General Capability
1. MMLU - Broad knowledge assessment
2. HumanEval - Coding ability
3. MATH - Mathematical reasoning
4. GPQA - Expert-level reasoning

### For Multimodal Models
1. MMMU - Comprehensive multimodal
2. MMBench - Detailed capability breakdown
3. ChartQA - Visual data understanding

### For Reasoning Models
1. MATH - Competition math
2. GPQA - Graduate-level science
3. SWE-bench - Real-world coding
4. ARC-Challenge - Scientific reasoning

### For Production Models
1. TruthfulQA - Factual accuracy
2. MT-Bench - Conversation quality
3. LMSYS Arena - Real user preferences

---

## Related Categories

- [Models](../models/) - Models tracked on these benchmarks
- [Research Findings](../research-findings/) - Benchmark analysis papers
- [Labs](../labs/) - Lab-specific benchmark results

---

## Template

To add a new benchmark entry, use the [benchmark template](../templates/benchmark-template.md).

---

## Benchmark Comparison Table

| Benchmark | Category | Metric | Dataset Size | Difficulty | Top Score (2025) | Leader |
|-----------|----------|--------|--------------|------------|------------------|--------|
| [MMLU](mmlu.md) | Core | Accuracy | 15,908 | High School-Professional | 92.4% | o3-mini |
| [HumanEval](humaneval.md) | Code | Pass@1 | 164 | Varied | 92.4% | o3-mini |
| [GPQA](gpqa.md) | Reasoning | Accuracy | 1,670 | Graduate | 86.0% | o3-mini |
| [MATH](math.md) | Reasoning | Accuracy | 12,500 | Competition | 97.3% | o3-mini |
| [SWE-bench](swe-bench.md) | Code | Resolution | 2,294 | Professional | 62.3% | Claude 3.7 Sonnet |
| [MMMU](mmmu.md) | Multimodal | Accuracy | 11,500 | College | 82.4% | Gemini 2.0 Pro |
| [MMBench](mmbench.md) | Multimodal | Accuracy | 3,000 | Varied | 89.2% | Gemini 2.0 Pro |
| [ARC](arc.md) | Reasoning | Accuracy | 7,787 | Grade School | 97.5% | o3-mini |
| [HellaSwag](hellaswag.md) | Reasoning | Accuracy | 39,905 | Varied | 95.5% | o3-mini |
| [BBH](bbh.md) | Reasoning | Accuracy | 6,500 | Challenging | 92.5% | o3-mini |
| [GSM8K](gsm8k.md) | Reasoning | Accuracy | 8,500 | Grade School | 99.2% | o3-mini |

## Detailed Benchmark Registry

### Core Benchmarks
| Benchmark | Full Name | Description | Categories Tested |
|-----------|-----------|-------------|-------------------|
| [MMLU](mmlu.md) | Massive Multitask Language Understanding | 57 tasks covering STEM, humanities, social sciences | STEM, Humanities, Social Sciences, Professional |

### Code Benchmarks
| Benchmark | Full Name | Description | Categories Tested |
|-----------|-----------|-------------|-------------------|
| [HumanEval](humaneval.md) | Human Evaluation of Code Generation | 164 Python programming problems | Algorithms, String Processing, Data Structures |
| [SWE-bench](swe-bench.md) | Software Engineering Benchmark | Real-world GitHub issue resolution | Bug Fixing, Feature Implementation, Testing |

### Reasoning Benchmarks
| Benchmark | Full Name | Description | Categories Tested |
|-----------|-----------|-------------|-------------------|
| [GPQA](gpqa.md) | Graduate-Level Google-Proof Q&A | Graduate science questions (Bio, Chem, Physics) | Biology, Chemistry, Physics |
| [MATH](math.md) | Mathematics Competition | Competition math from AMC, AIME | Algebra, Geometry, Number Theory, Probability |
| [ARC](arc.md) | AI2 Reasoning Challenge | Grade school science questions | Biology, Physics, Chemistry, Earth Science |
| [HellaSwag](hellaswag.md) | Commonsense Completion | Sentence completion with adversarial examples | Physical Activities, Social Interactions |
| [BBH](bbh.md) | Big-Bench Hard | 23 challenging reasoning tasks | Logic, Algorithms, Commonsense |
| [GSM8K](gsm8k.md) | Grade School Math | 8,500 math word problems | Arithmetic, Word Problems, Multi-step |

### Multimodal Benchmarks
| Benchmark | Full Name | Description | Categories Tested |
|-----------|-----------|-------------|-------------------|
| [MMMU](mmmu.md) | Massive Multi-discipline Multimodal | College-level multimodal problems | Art, Business, Medicine, Science, Math |
| [MMBench](mmbench.md) | Comprehensive Multimodal Eval | 20+ capability dimensions with circular testing | Perception, Cognition, Hallucination |

## Score Interpretation Guide

### Accuracy-Based Benchmarks
| Score Range | Interpretation |
|-------------|----------------|
| 25% | Random baseline |
| 25-40% | Below basic |
| 40-60% | Basic understanding |
| 60-80% | Competent performance |
| 80-90% | Expert-level |
| 90%+ | State-of-the-art |

### Pass@k Benchmarks (HumanEval)
| Score Range | Interpretation |
|-------------|----------------|
| <30% | Limited coding ability |
| 30-50% | Basic coding skills |
| 50-70% | Competent programmer |
| 70-85% | Advanced coding |
| 85%+ | Expert-level |

### Resolution Rate (SWE-bench)
| Score Range | Interpretation |
|-------------|----------------|
| <5% | Minimal capability |
| 5-15% | Basic issue resolution |
| 15-30% | Competent engineering |
| 30-50% | Advanced engineering |
| 50%+ | Expert-level |

## Machine-Readable Registry

A machine-readable JSON registry of all benchmarks is available at:
- **Location:** `../../scripts/benchmark_registry.json`
- **Format:** JSON with full benchmark metadata
- **Schema:** Includes IDs, metrics, score ranges, sources, and categories

## Statistics

| Category | Count | Last Updated |
|----------|-------|--------------|
| Core Benchmarks | 1 | 2026-04-20 |
| Code Benchmarks | 2 | 2026-04-20 |
| Reasoning Benchmarks | 6 | 2026-04-20 |
| Multimodal Benchmarks | 2 | 2026-04-20 |
| **Total Documented** | **11** | **2026-04-20** |

---

*Last updated: 2026-04-20 by AI Model Research Team*