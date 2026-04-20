#!/usr/bin/env python3
"""
Benchmark Score Normalization Script

Normalizes scores from multiple sources to a consistent 0-100 scale.
Handles different evaluation setups and benchmark versions.
"""

import json
import os
from typing import Dict, List, Any, Optional
from datetime import datetime

def normalize_score(score: float, metric_name: str = "") -> float:
    """
    Normalize a score to 0-100 scale.
    
    Rules:
    - If score <= 1.0, assume it's 0-1 scale and multiply by 100
    - If score > 1.0, assume it's already 0-100 scale
    - Handle special cases like AUROC which are typically 0-1
    """
    if score is None:
        return None
    
    # AUROC is typically 0-1
    if "auroc" in metric_name.lower():
        return round(score * 100, 2) if score <= 1.0 else round(score, 2)
    
    # Standard normalization
    if score <= 1.0:
        normalized = score * 100
    else:
        normalized = score
    
    return round(normalized, 2)

def detect_benchmark_type(name: str) -> str:
    """Detect the standardized benchmark type from various naming conventions."""
    name_lower = name.lower().replace("_", "").replace("-", "")
    
    mappings = {
        "mmlu_pro": ["mmlupro", "mmlu_pro", "mmlu-pro"],
        "mmlu": ["mmlu"],
        "gpqa": ["gpqa"],
        "math_lvl5": ["mathlvl5", "math_level5", "math5"],
        "math": ["math"],
        "humaneval": ["humaneval", "human eval", "humaneval+"],
        "bbh": ["bbh", "bigbenchhard", "bigbench_hard"],
        "ifeval": ["ifeval", "ifeval"],
        "musr": ["musr"],
        "gsm8k": ["gsm8k", "gsm_8k"],
        "accuracy": ["accuracy", "acc"],
        "f1": ["f1", "f1score"],
    }
    
    for standard, aliases in mappings.items():
        if any(alias in name_lower for alias in aliases):
            return standard
    
    return name_lower

def load_json(filepath: str) -> Any:
    """Load JSON file."""
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def process_hf_leaderboard(data: List[Dict]) -> List[Dict]:
    """Process Hugging Face leaderboard data."""
    normalized = []
    
    benchmark_mappings = {
        "ifeval_score": ("ifeval", "0-shot"),
        "bbh_score": ("bbh", "3-shot"),
        "math_lvl5_score": ("math_lvl5", "0-shot"),
        "gpqa_score": ("gpqa", "0-shot"),
        "musr_score": ("musr", "0-shot"),
        "mmlu_pro_score": ("mmlu_pro", "0-shot"),
    }
    
    for model in data:
        model_name = model.get("model_name", "")
        base_entry = {
            "model_name": model_name,
            "source": "hf_leaderboard",
            "architecture": model.get("architecture", ""),
            "parameters_billions": model.get("parameters_billions", 0),
            "submission_date": model.get("submission_date", ""),
        }
        
        for score_key, (bench_type, setup) in benchmark_mappings.items():
            score = model.get(score_key)
            if score is not None:
                entry = base_entry.copy()
                entry.update({
                    "benchmark": bench_type,
                    "original_score": score,
                    "normalized_score": normalize_score(score, bench_type),
                    "evaluation_setup": setup,
                    "score_range": "0-100",
                    "confidence": "high",
                })
                normalized.append(entry)
    
    return normalized

def process_paperswithcode_mmlu(data: List[Dict]) -> List[Dict]:
    """Process Papers with Code MMLU data."""
    normalized = []
    
    for model in data:
        model_name = model.get("model_name", "")
        base_entry = {
            "model_name": model_name,
            "source": "paperswithcode_mmlu",
            "architecture": model.get("architecture", ""),
            "parameters_billions": model.get("parameters_billions", 0),
            "submission_date": model.get("submission_date", ""),
        }
        
        # Process mmlu_pro_score
        score = model.get("mmlu_pro_score")
        if score is not None:
            entry = base_entry.copy()
            entry.update({
                "benchmark": "mmlu_pro",
                "original_score": score,
                "normalized_score": normalize_score(score, "mmlu_pro"),
                "evaluation_setup": "unknown",
                "score_range": "0-100",
                "confidence": "medium",
                "note": "From Papers with Code leaderboard"
            })
            normalized.append(entry)
        
        # Process raw score if available
        raw_score = model.get("mmlu_pro_raw")
        if raw_score is not None:
            entry = base_entry.copy()
            entry.update({
                "benchmark": "mmlu_pro",
                "original_score": raw_score,
                "normalized_score": normalize_score(raw_score, "mmlu_pro"),
                "evaluation_setup": "unknown",
                "score_range": "0-1-converted",
                "confidence": "medium",
                "score_type": "raw",
                "note": "Raw score from Papers with Code"
            })
            normalized.append(entry)
    
    return normalized

def process_paperswithcode_gpqa(data: List[Dict]) -> List[Dict]:
    """Process Papers with Code GPQA data."""
    normalized = []
    
    for model in data:
        model_name = model.get("model_name", "")
        base_entry = {
            "model_name": model_name,
            "source": "paperswithcode_gpqa",
            "architecture": model.get("architecture", ""),
            "parameters_billions": model.get("parameters_billions", 0),
        }
        
        score = model.get("gpqa_score")
        if score is not None:
            entry = base_entry.copy()
            entry.update({
                "benchmark": "gpqa",
                "original_score": score,
                "normalized_score": normalize_score(score, "gpqa"),
                "evaluation_setup": "unknown",
                "score_range": "0-100",
                "confidence": "medium",
            })
            normalized.append(entry)
    
    return normalized

def process_paperswithcode_math(data: List[Dict]) -> List[Dict]:
    """Process Papers with Code MATH data."""
    normalized = []
    
    for model in data:
        model_name = model.get("model_name", "")
        base_entry = {
            "model_name": model_name,
            "source": "paperswithcode_math",
            "architecture": model.get("architecture", ""),
            "parameters_billions": model.get("parameters_billions", 0),
        }
        
        score = model.get("math_lvl5_score")
        if score is not None:
            entry = base_entry.copy()
            entry.update({
                "benchmark": "math_lvl5",
                "original_score": score,
                "normalized_score": normalize_score(score, "math_lvl5"),
                "evaluation_setup": "unknown",
                "score_range": "0-100",
                "confidence": "medium",
            })
            normalized.append(entry)
    
    return normalized

def process_paper_extractions(data: Dict) -> List[Dict]:
    """Process paper extraction benchmark scores."""
    normalized = []
    
    extractions = data.get("extractions", [])
    
    for extraction in extractions:
        paper_id = extraction.get("paper_id", "")
        benchmark = extraction.get("benchmark", "")
        score = extraction.get("score")
        metric = extraction.get("metric", "")
        confidence = extraction.get("confidence", "low")
        model = extraction.get("model", "")
        
        if score is None:
            continue
        
        bench_type = detect_benchmark_type(benchmark)
        
        entry = {
            "model_name": model if model else f"paper_{paper_id}",
            "source": "paper_extraction",
            "paper_id": paper_id,
            "benchmark": bench_type,
            "original_benchmark_name": benchmark,
            "original_score": score,
            "normalized_score": normalize_score(score, bench_type),
            "evaluation_setup": "unknown",
            "metric_type": metric,
            "confidence": confidence,
            "context": extraction.get("context", "")[:100] + "..." if len(extraction.get("context", "")) > 100 else extraction.get("context", ""),
        }
        
        normalized.append(entry)
    
    return normalized

def generate_statistics(normalized_scores: List[Dict]) -> Dict:
    """Generate statistics about the normalized data."""
    stats = {
        "total_scores": len(normalized_scores),
        "total_unique_models": len(set(s.get("model_name", "") for s in normalized_scores)),
        "benchmarks_covered": {},
        "sources": {},
        "confidence_distribution": {},
    }
    
    for score in normalized_scores:
        bench = score.get("benchmark", "unknown")
        source = score.get("source", "unknown")
        confidence = score.get("confidence", "unknown")
        
        stats["benchmarks_covered"][bench] = stats["benchmarks_covered"].get(bench, 0) + 1
        stats["sources"][source] = stats["sources"].get(source, 0) + 1
        stats["confidence_distribution"][confidence] = stats["confidence_distribution"].get(confidence, 0) + 1
    
    return stats

def main():
    """Main processing function."""
    base_path = os.path.expanduser("~/ai-model-research-team")
    
    all_normalized = []
    
    # Process HF Leaderboard
    hf_data = load_json(f"{base_path}/data/raw/leaderboards/hf_leaderboard_top100.json")
    if hf_data:
        all_normalized.extend(process_hf_leaderboard(hf_data))
        print(f"Processed {len(hf_data)} HF leaderboard entries")
    
    # Process Papers with Code MMLU
    pwc_mmlu = load_json(f"{base_path}/data/raw/leaderboards/paperswithcode_mmlu.json")
    if pwc_mmlu:
        all_normalized.extend(process_paperswithcode_mmlu(pwc_mmlu))
        print(f"Processed {len(pwc_mmlu)} Papers with Code MMLU entries")
    
    # Process Papers with Code GPQA
    pwc_gpqa = load_json(f"{base_path}/data/raw/leaderboards/paperswithcode_gpqa.json")
    if pwc_gpqa:
        all_normalized.extend(process_paperswithcode_gpqa(pwc_gpqa))
        print(f"Processed {len(pwc_gpqa)} Papers with Code GPQA entries")
    
    # Process Papers with Code MATH
    pwc_math = load_json(f"{base_path}/data/raw/leaderboards/paperswithcode_math.json")
    if pwc_math:
        all_normalized.extend(process_paperswithcode_math(pwc_math))
        print(f"Processed {len(pwc_math)} Papers with Code MATH entries")
    
    # Process Paper Extractions
    paper_data = load_json(f"{base_path}/data/processed/benchmark_scores.json")
    if paper_data:
        all_normalized.extend(process_paper_extractions(paper_data))
        print(f"Processed paper extraction entries")
    
    # Load existing normalized_scores.json to preserve structure
    output_path = f"{base_path}/data/processed/normalized_scores.json"
    existing_data = load_json(output_path) or {}
    
    # Generate statistics
    stats = generate_statistics(all_normalized)
    
    # Update metadata
    existing_data["normalization_metadata"].update({
        "total_models": stats["total_unique_models"],
        "total_scores": stats["total_scores"],
        "processing_date": datetime.now().isoformat(),
    })
    
    # Add statistics
    existing_data["statistics"] = stats
    
    # Add normalized scores
    existing_data["normalized_scores"] = all_normalized
    
    # Write output
    with open(output_path, 'w') as f:
        json.dump(existing_data, f, indent=2)
    
    print(f"\nNormalization complete!")
    print(f"Total scores normalized: {stats['total_scores']}")
    print(f"Unique models: {stats['total_unique_models']}")
    print(f"Benchmarks covered: {list(stats['benchmarks_covered'].keys())}")
    print(f"Output saved to: {output_path}")

if __name__ == "__main__":
    main()
