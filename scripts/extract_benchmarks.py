#!/usr/bin/env python3
"""
Enhanced Benchmark Extraction Script for arXiv Papers

Extracts benchmark scores from paper abstracts and titles using comprehensive regex patterns.
Supports multiple benchmark types and confidence scoring.
"""

import json
import re
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from collections import Counter

# Enhanced benchmark patterns to search for
BENCHMARK_PATTERNS = {
    # Academic benchmarks with score extraction
    "MMLU": [
        r"MMLU(?:-Pro|-Redux)?[:\s]+(\d+\.?\d*)\s*%?",
        r"MMLU.*?score[s]?[:\s]+(\d+\.?\d*)\s*%?",
        r"(\d+\.?\d*)%?\s+on\s+MMLU",
        r"MMLU.*?achieves.*?([\d\.]+)\s*%?",
        r"MMLU.*?accuracy[:\s]+(\d+\.?\d*)\s*%?",
        r"MMLU.*?([\d\.]+)%\s+accuracy",
        r"MMLU.*?([\d\.]+)\s*percent",
    ],
    "MMLU-Pro": [
        r"MMLU-Pro[:\s]+(\d+\.?\d*)\s*%?",
        r"MMLU[-\s]Pro.*?score[s]?[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "HumanEval": [
        r"HumanEval[:\s]+(\d+\.?\d*)\s*%?",
        r"HumanEval.*?pass@1[:\s]+(\d+\.?\d*)\s*%?",
        r"HumanEval.*?score[s]?[:\s]+(\d+\.?\d*)\s*%?",
        r"(\d+\.?\d*)%?\s+on\s+HumanEval",
        r"HumanEval.*?([\d\.]+)%\s+accuracy",
        r"HumanEval.*?([\d\.]+)\s*percent",
    ],
    "MATH": [
        r"MATH[:\s]+(\d+\.?\d*)\s*%?",
        r"MATH.*?score[s]?[:\s]+(\d+\.?\d*)\s*%?",
        r"(\d+\.?\d*)%?\s+on\s+MATH\b",
        r"MATH.*?achieves.*?([\d\.]+)\s*%?",
        r"MATH.*?([\d\.]+)%\s+accuracy",
        r"MATH.*?([\d\.]+)\s*percent",
    ],
    "GSM8K": [
        r"GSM8K[:\s]+(\d+\.?\d*)\s*%?",
        r"GSM8K.*?score[s]?[:\s]+(\d+\.?\d*)\s*%?",
        r"(\d+\.?\d*)%?\s+on\s+GSM8K",
        r"GSM8K.*?([\d\.]+)%\s+accuracy",
        r"GSM8K.*?([\d\.]+)\s*percent",
    ],
    "GPQA": [
        r"GPQA[:\s]+(\d+\.?\d*)\s*%?",
        r"GPQA.*?score[s]?[:\s]+(\d+\.?\d*)\s*%?",
        r"(\d+\.?\d*)%?\s+on\s+GPQA",
        r"GPQA.*?([\d\.]+)%\s+accuracy",
    ],
    "BBH": [
        r"BBH[:\s]+(\d+\.?\d*)\s*%?",
        r"Big-Bench Hard[:\s]+(\d+\.?\d*)\s*%?",
        r"(\d+\.?\d*)%?\s+on\s+BBH",
    ],
    "ARC": [
        r"ARC(?:-C|-E|-Challenge|-Easy)?[:\s]+(\d+\.?\d*)\s*%?",
        r"ARC.*?score[s]?[:\s]+(\d+\.?\d*)\s*%?",
        r"(\d+\.?\d*)%?\s+on\s+ARC\b",
    ],
    "ARC-Challenge": [
        r"ARC-Challenge[:\s]+(\d+\.?\d*)\s*%?",
        r"ARC-C[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "ARC-Easy": [
        r"ARC-Easy[:\s]+(\d+\.?\d*)\s*%?",
        r"ARC-E[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "HellaSwag": [
        r"HellaSwag[:\s]+(\d+\.?\d*)\s*%?",
        r"HellaSwag.*?score[s]?[:\s]+(\d+\.?\d*)\s*%?",
        r"(\d+\.?\d*)%?\s+on\s+HellaSwag",
    ],
    "TruthfulQA": [
        r"TruthfulQA[:\s]+(\d+\.?\d*)\s*%?",
        r"TruthfulQA.*?score[s]?[:\s]+(\d+\.?\d*)\s*%?",
        r"(\d+\.?\d*)%?\s+on\s+TruthfulQA",
    ],
    "GQA": [
        r"GQA[:\s]+(\d+\.?\d*)\s*%?",
        r"GQA.*?score[s]?[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "VQA": [
        r"VQA(?:-v2)?[:\s]+(\d+\.?\d*)\s*%?",
        r"VQA.*?score[s]?[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "WinoGrande": [
        r"WinoGrande[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "COPA": [
        r"COPA[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "OpenBookQA": [
        r"OpenBookQA[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "CommonsenseQA": [
        r"CommonsenseQA[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "PIQA": [
        r"PIQA[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "SIQA": [
        r"SIQA[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "RACE": [
        r"RACE[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "DROP": [
        r"DROP[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "SQuAD": [
        r"SQuAD(?:\s*\d\.?\d?)?:\s+(\d+\.?\d*)\s*%?",
    ],
    "NaturalQuestions": [
        r"Natural Questions[:\s]+(\d+\.?\d*)\s*%?",
        r"NQ[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "TriviaQA": [
        r"TriviaQA[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "BoolQ": [
        r"BoolQ[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "MultiRC": [
        r"MultiRC[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "ReCoRD": [
        r"ReCoRD[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "RTE": [
        r"RTE[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "CB": [
        r"CB[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "WSC": [
        r"WSC[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "ANLI": [
        r"ANLI[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "SNLI": [
        r"SNLI[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "MNLI": [
        r"MNLI[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "QNLI": [
        r"QNLI[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "SST-2": [
        r"SST-2[:\s]+(\d+\.?\d*)\s*%?",
        r"SST2[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "MRPC": [
        r"MRPC[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "STS-B": [
        r"STS-B[:\s]+(\d+\.?\d*)\s*%?",
        r"STSB[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "QQP": [
        r"QQP[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "WNLI": [
        r"WNLI[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "SuperGLUE": [
        r"SuperGLUE[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "GLUE": [
        r"GLUE[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "XSum": [
        r"XSum[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "CNN/DailyMail": [
        r"CNN/DailyMail[:\s]+(\d+\.?\d*)\s*%?",
        r"CNN-DailyMail[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "BigBench": [
        r"BigBench[:\s]+(\d+\.?\d*)\s*%?",
        r"BIG-bench[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "C-Eval": [
        r"C-Eval[:\s]+(\d+\.?\d*)\s*%?",
        r"CEval[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "CMMLU": [
        r"CMMLU[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "GAIA": [
        r"GAIA[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "SWE-bench": [
        r"SWE-bench[:\s]+(\d+\.?\d*)\s*%?",
        r"SWEbench[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "LiveCodeBench": [
        r"LiveCodeBench[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "Codeforces": [
        r"Codeforces[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "AIME": [
        r"AIME(?:\s*\d*)?[:\s]+(\d+\.?\d*)\s*%?",
        r"AIME.*?score[s]?[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "AMC": [
        r"AMC(?:\s*\d+)?[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "Kaggle": [
        r"Kaggle[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "AtCoder": [
        r"AtCoder[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "HackerRank": [
        r"HackerRank[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "LeetCode": [
        r"LeetCode[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "CodeChef": [
        r"CodeChef[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "TopCoder": [
        r"TopCoder[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "IOI": [
        r"IOI[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "IMO": [
        r"IMO[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "Putnam": [
        r"Putnam[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "AP": [
        r"AP(?:\s*[A-Z]+)?[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "SAT": [
        r"SAT[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "LSAT": [
        r"LSAT[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "GRE": [
        r"GRE[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "GMAT": [
        r"GMAT[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "MCAT": [
        r"MCAT[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "USMLE": [
        r"USMLE[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "BarExam": [
        r"Bar Exam[:\s]+(\d+\.?\d*)\s*%?",
        r"BarExam[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "PubMedQA": [
        r"PubMedQA[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "BioASQ": [
        r"BioASQ[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "MedQA": [
        r"MedQA[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "MedMCQA": [
        r"MedMCQA[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "F1": [
        r"F1[-\s]score.*?([\d\.]+)\s*%?",
        r"F1[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "Accuracy": [
        r"accuracy.*?([\d\.]+)%",
        r"([\d\.]+)%\s+accuracy",
    ],
    "Precision": [
        r"precision.*?([\d\.]+)%",
    ],
    "Recall": [
        r"recall.*?([\d\.]+)%",
    ],
    "AUROC": [
        r"AUROC[:\s]+(\d+\.?\d*)\s*%?",
        r"AUC[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "BLEU": [
        r"BLEU[:\s]+(\d+\.?\d*)\s*%?",
        r"BLEU[-\s]?(\d+)[:\s]+(\d+\.?\d*)",
    ],
    "ROUGE": [
        r"ROUGE[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "pass@1": [
        r"pass@1[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "pass@5": [
        r"pass@5[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "pass@10": [
        r"pass@10[:\s]+(\d+\.?\d*)\s*%?",
    ],
    "pass@k": [
        r"pass@k[:\s]+(\d+\.?\d*)\s*%?",
    ],
}

# Model name patterns
MODEL_PATTERNS = [
    r"\b(GPT-4o(?:\s*Mini)?)\b",
    r"\b(GPT-4(?:\s*\d+)?)\b",
    r"\b(GPT-3\.5(?:-turbo)?)\b",
    r"\b(Claude\s*3(?:\.\d+)?(?:\s*(?:Opus|Sonnet|Haiku))?)\b",
    r"\b(Gemini(?:\s*\d+\.?\d*(?:\s*Pro)?)?)\b",
    r"\b(Llama[-\s]*3(?:\.\d+)?(?:-\d+B)?)\b",
    r"\b(Llama[-\s]*2(?:-\d+B)?)\b",
    r"\b(DeepSeek(?:[-\s]*\w+)?)\b",
    r"\b(Grok[-\s]*\d*)\b",
    r"\b(Qwen(?:[-\s]*\d+(?:\.\d+)?)?(?:[-\s]*\w+)?)\b",
    r"\b(Mistral(?:[-\s]*\w+)?)\b",
    r"\b(Mixtral(?:[-\s]*\w+)?)\b",
    r"\b(Gemma(?:[-\s]*\d+)?)\b",
    r"\b(PaLM(?:[-\s]*\d+)?)\b",
    r"\b(Phi[-\s]*\d+)\b",
    r"\b(Aya(?:[-\s]*\w+)?)\b",
    r"\b(Olmo(?:[-\s]*\d+B)?)\b",
    r"\b(Pythia(?:[-\s]*\d+B)?)\b",
    r"\b(GPT-OSS[-\s]*\d+B?)\b",
    r"\b(O[1-9](?:\s*Mini|Pro)?)\b",
]

# Benchmark names for generic mentions
BENCHMARK_NAMES = [
    "MMLU", "MMLU-Pro", "MMLU-Redux", "HumanEval", "MATH", "GSM8K", "GPQA", 
    "BBH", "Big-Bench Hard", "ARC", "ARC-Challenge", "ARC-Easy", "HellaSwag",
    "TruthfulQA", "GQA", "VQA", "VQA-v2", "SQuAD", "NaturalQuestions", "NQ",
    "TriviaQA", "WinoGrande", "COPA", "OpenBookQA", "CommonsenseQA", "PIQA",
    "SIQA", "RACE", "DROP", "BoolQ", "MultiRC", "ReCoRD", "RTE", "CB", "WSC",
    "ANLI", "SNLI", "MNLI", "QNLI", "SST-2", "SST2", "MRPC", "STS-B", "STSB",
    "QQP", "WNLI", "SuperGLUE", "GLUE", "XSum", "CNN/DailyMail", "BigBench",
    "C-Eval", "CEval", "CMMLU", "GAIA", "SWE-bench", "SWEbench", "LiveCodeBench",
    "Codeforces", "AIME", "AMC", "Kaggle", "AtCoder", "HackerRank", "LeetCode",
    "CodeChef", "TopCoder", "IOI", "IMO", "Putnam", "SAT", "LSAT", "GRE", "GMAT",
    "MCAT", "USMLE", "BarExam", "PubMedQA", "BioASQ", "MedQA", "MedMCQA",
    "CrossMath", "SocialGrid", "Mind's Eye", "ReactBench", "UniEditBench",
    "MEDLEY-BENCH", "BAGEL", "PLUM", "KA-LogicQuery", "XAI Question Bank",
]


def extract_model_names(text: str) -> List[str]:
    """Extract model names from text."""
    models = []
    for pattern in MODEL_PATTERNS:
        matches = re.findall(pattern, text, re.IGNORECASE)
        models.extend(matches)
    return list(set(models))


def extract_benchmark_scores(text: str, paper_id: str) -> List[Dict[str, Any]]:
    """Extract benchmark scores from text."""
    extractions = []
    models = extract_model_names(text)
    
    for benchmark_name, patterns in BENCHMARK_PATTERNS.items():
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    # Get the last captured group that contains a number
                    groups = [g for g in match.groups() if g is not None]
                    if not groups:
                        continue
                    score = float(groups[-1])
                    # Validate reasonable score range
                    if 0 <= score <= 100:
                        extraction = {
                            "paper_id": paper_id,
                            "benchmark": benchmark_name,
                            "score": score,
                            "metric": "accuracy",
                            "confidence": "high",
                            "context": text[max(0, match.start() - 50):min(len(text), match.end() + 50)].strip(),
                        }
                        # Add model if found
                        if models:
                            extraction["model"] = models[0]
                        extractions.append(extraction)
                except (ValueError, IndexError):
                    continue
    
    return extractions


def extract_generic_mentions(text: str, paper_id: str, existing_benchmarks: set) -> List[Dict[str, Any]]:
    """Extract generic benchmark mentions without specific scores."""
    extractions = []
    
    for benchmark_name in BENCHMARK_NAMES:
        if benchmark_name in existing_benchmarks:
            continue
        # Look for benchmark name as a word
        pattern = r"\b" + re.escape(benchmark_name) + r"\b"
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            extraction = {
                "paper_id": paper_id,
                "benchmark": benchmark_name,
                "metric": "mentioned",
                "confidence": "low",
                "context": text[max(0, match.start() - 30):min(len(text), match.end() + 30)].strip(),
            }
            extractions.append(extraction)
    
    return extractions


def extract_performance_metrics(text: str, paper_id: str) -> List[Dict[str, Any]]:
    """Extract performance metrics like accuracy, F1, etc."""
    extractions = []
    
    # Generic patterns for performance metrics
    metric_patterns = [
        (r"(\d+\.?\d*)%\s+(?:accuracy|accurate)", "accuracy"),
        (r"(?:accuracy|accurate).*?(\d+\.?\d*)%", "accuracy"),
        (r"F1[-\s]score.*?([\d\.]+)", "F1"),
        (r"F1[:\s]+([\d\.]+)", "F1"),
        (r"precision.*?([\d\.]+)%", "precision"),
        (r"recall.*?([\d\.]+)%", "recall"),
        (r"AUROC.*?([\d\.]+)", "AUROC"),
        (r"AUC.*?([\d\.]+)", "AUC"),
        (r"BLEU.*?([\d\.]+)", "BLEU"),
        (r"ROUGE.*?([\d\.]+)", "ROUGE"),
    ]
    
    for pattern, metric_name in metric_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            try:
                score = float(match.group(1))
                if 0 <= score <= 100:
                    extraction = {
                        "paper_id": paper_id,
                        "benchmark": metric_name,
                        "score": score,
                        "metric": metric_name,
                        "confidence": "medium",
                        "context": text[max(0, match.start() - 40):min(len(text), match.end() + 40)].strip(),
                    }
                    extractions.append(extraction)
            except (ValueError, IndexError):
                continue
    
    return extractions


def process_papers(papers_data: Dict) -> Tuple[List[Dict], Dict]:
    """Process all papers and extract benchmark scores."""
    all_extractions = []
    papers_with_benchmarks = set()
    benchmark_counts = Counter()
    
    papers = papers_data.get("papers", [])
    
    for paper in papers:
        paper_id = paper.get("arxiv_id", "unknown")
        title = paper.get("title", "")
        abstract = paper.get("abstract", "")
        
        # Combine title and abstract for extraction
        full_text = f"{title} {abstract}"
        
        # Track which benchmarks already have scores
        existing_benchmarks = set()
        
        # Extract scored benchmarks
        scored = extract_benchmark_scores(full_text, paper_id)
        for s in scored:
            existing_benchmarks.add(s["benchmark"])
        all_extractions.extend(scored)
        
        # Extract generic mentions
        generic = extract_generic_mentions(full_text, paper_id, existing_benchmarks)
        all_extractions.extend(generic)
        
        # Extract performance metrics
        metrics = extract_performance_metrics(full_text, paper_id)
        all_extractions.extend(metrics)
        
        # Track papers with benchmarks
        if scored or generic or metrics:
            papers_with_benchmarks.add(paper_id)
        
        # Count benchmarks
        for ext in scored + generic + metrics:
            benchmark_counts[ext["benchmark"]] += 1
    
    # Calculate statistics
    stats = {
        "total_extractions": len(all_extractions),
        "papers_with_benchmarks": len(papers_with_benchmarks),
        "total_papers": len(papers),
        "papers_with_benchmarks_pct": round(len(papers_with_benchmarks) / len(papers) * 100, 2) if papers else 0,
        "most_common_benchmark": benchmark_counts.most_common(1)[0][0] if benchmark_counts else None,
        "most_common_count": benchmark_counts.most_common(1)[0][1] if benchmark_counts else 0,
        "benchmark_distribution": dict(benchmark_counts.most_common(20)),
        "high_confidence_extractions": len([e for e in all_extractions if e.get("confidence") == "high"]),
        "medium_confidence_extractions": len([e for e in all_extractions if e.get("confidence") == "medium"]),
        "low_confidence_extractions": len([e for e in all_extractions if e.get("confidence") == "low"]),
    }
    
    return all_extractions, stats


def main():
    """Main extraction function."""
    # Load papers data
    input_path = Path("data/raw/arxiv_papers_2026-04-19.json")
    output_path = Path("data/processed/benchmark_scores.json")
    
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return
    
    print(f"Loading papers from {input_path}...")
    with open(input_path, "r", encoding="utf-8") as f:
        papers_data = json.load(f)
    
    print(f"Processing {papers_data.get('total_papers', 0)} papers...")
    extractions, stats = process_papers(papers_data)
    
    # Prepare output
    output = {
        "extraction_date": "2026-04-20",
        "source_file": str(input_path),
        "total_papers": papers_data.get("total_papers", 0),
        "extractions": extractions,
        "statistics": stats,
    }
    
    # Save results
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    
    print(f"\nExtraction complete!")
    print(f"Total extractions: {stats['total_extractions']}")
    print(f"Papers with benchmarks: {stats['papers_with_benchmarks']} ({stats['papers_with_benchmarks_pct']}%)")
    print(f"High confidence: {stats['high_confidence_extractions']}")
    print(f"Medium confidence: {stats['medium_confidence_extractions']}")
    print(f"Low confidence: {stats['low_confidence_extractions']}")
    print(f"Most common benchmark: {stats['most_common_benchmark']} ({stats['most_common_count']} mentions)")
    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    main()
