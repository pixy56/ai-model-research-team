# Key Findings Extraction Methodology

## Overview

This document describes the methodology used to extract key findings from analyzed papers in the AI Model Research Team project.

## Extraction Process

### Source Data
- **Input File**: `data/processed/paper_insights.json`
- **Total Papers**: 100 papers
- **Date Range**: 2026-03-20 to 2026-04-19
- **Categories**: cs.AI, cs.LG, cs.CL, cs.CV, and others

### Extraction Approach

The extraction process uses automated pattern matching on paper abstracts to identify four types of findings:

#### 1. Results (Numerical Findings)
**Patterns Used:**
- "achieves/reaches/scores X% on benchmark"
- "accuracy/score of Y%"
- "X% improvement/increase/decrease"
- "F1/accuracy/AUROC of Z"

**Example:** "GPT-OSS-20B achieves 84% accuracy on AIME25"

#### 2. Claims (Research Findings)
**Patterns Used:**
- "We show/demonstrate/prove/find that..."
- "Our results/findings demonstrate that..."
- "These results suggest/indicate that..."
- "Our findings reveal that..."

**Example:** "Our results demonstrate that teaching models to identify core techniques substantially improves mathematical reasoning"

#### 3. Methods (Novel Approaches)
**Patterns Used:**
- "We propose/introduce/present [MethodName]"
- "We propose a novel framework/method/approach"
- "This paper presents a method for..."

**Example:** "We propose HILBERT, a cross-attentive multimodal framework"

#### 4. Limitations (Constraints and Challenges)
**Patterns Used:**
- "limitation/challenge/issue/problem is..."
- "does not work/fails to..."
- "remains unclear/unknown/challenging"
- "significant gap/bottleneck/barrier"

**Example:** "remains unclear due to lack of benchmarks reflecting real-world scenarios"

### Entity Extraction

#### Models Extracted
- GPT-4, GPT-3.5, GPT-OSS series
- Llama-2, Llama-3, Llama-3.2 variants
- Claude 3, Claude 3.7 Sonnet, Claude 3 Opus
- Gemini, Gemini-1.5 Pro, Gemini-3-Pro
- Qwen2.5, Qwen3, Qwen3-VL
- DeepSeek-Chat
- BERT, T5, Mistral, Gemma, Pythia, OLMo

#### Benchmarks Extracted
- MMLU, GSM8K, MATH, GPQA
- HumanEval, ARC, HellaSwag
- CrossMath, Mind's Eye, BAGEL
- PLUM, SocialGrid, ReactBench
- XAI Question Bank, MEDLEY-BENCH
- And more specialized benchmarks

## Output Structure

Each finding is structured as:
```json
{
  "id": "finding_XXXX",
  "type": "result|claim|method|limitation",
  "category": "sub-category",
  "paper_id": "arxiv_id",
  "paper_title": "Paper Title",
  "paper_categories": ["cs.AI", "cs.CL"],
  "primary_category": "cs.CL",
  "text": "Extracted finding text",
  "context": "Full sentence context (for claims)",
  "method_name": "Named method if applicable",
  "is_novel": true|false,
  "value": "Numerical value if result",
  "models_mentioned": ["Model1", "Model2"],
  "benchmarks_mentioned": ["Benchmark1"],
  "confidence": "high|medium|low",
  "extraction_source": "abstract"
}
```

## Statistics

### Total Findings Extracted: 196

**By Type:**
- Methods: 82 (41.8%)
- Claims: 71 (36.2%)
- Limitations: 28 (14.3%)
- Results: 15 (7.7%)

**By Category:**
- cs.CL (Computation and Language): ~40 papers
- cs.LG (Machine Learning): ~21 papers
- cs.AI (Artificial Intelligence): ~15 papers
- cs.CV (Computer Vision): ~10 papers
- Others: ~14 papers

**Top Models Mentioned:**
- Gemini: 5
- Qwen3: 4
- Llama series: Multiple variants
- GPT series: Multiple variants

**Top Benchmarks Mentioned:**
- MATH, MMLU, GSM8K
- CrossMath, BAGEL, PLUM
- XAI Question Bank, Mind's Eye

## Validation

- **Papers Processed**: 100 (exceeds 50+ requirement)
- **Findings Categorized**: result, claim, method, limitation
- **Source Attribution**: Each finding linked to paper_id and paper_title
- **Model/Benchmark Linking**: Extracted via pattern matching
- **Structured Output**: JSON format with consistent schema

## Limitations of Extraction Method

1. **Abstract-Only Analysis**: Findings are extracted from abstracts only, not full papers
2. **Pattern Dependency**: Relies on regex patterns that may miss unconventional phrasings
3. **Confidence Levels**: All findings marked as "medium" confidence unless explicitly novel
4. **Numerical Precision**: Some numerical results may be extracted as text rather than structured values
5. **Context Sensitivity**: May extract partial sentences or miss nuanced findings

## Future Improvements

1. Integrate full-text PDF analysis for more comprehensive extraction
2. Use LLM-based extraction for better context understanding
3. Add citation network analysis to identify influential findings
4. Implement temporal trend analysis
5. Cross-reference with benchmark_scores.json for validation