#!/usr/bin/env python3
"""
Architecture Classifier for AI Models

Automatically classifies AI models into architecture categories based on
model metadata, configuration, and characteristics.

Usage:
    python architecture_classifier.py --model-name "GPT-4"
    python architecture_classifier.py --file models.json
    python architecture_classifier.py --lab-data /path/to/lab_announcements.json

Architecture Classes:
    - dense-transformer: Full attention, all parameters active
    - moe: Mixture of Experts, sparse activation
    - ssm: State Space Models, linear complexity
    - multimodal: Cross-modal processing (vision + text)
    - reasoning: Test-time compute, chain-of-thought
    - diffusion: Iterative denoising for generation
    - other: Novel or unclassified architectures

Author: AI Model Research Team
Date: 2026-04-20
"""

import json
import re
import sys
import argparse
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass


@dataclass
class ArchitectureCriteria:
    """Criteria for classifying an architecture."""
    name: str
    required_keywords: List[str]
    forbidden_keywords: List[str]
    confidence_threshold: float = 0.5


# Architecture classification criteria
ARCHITECTURE_CRITERIA = {
    "dense-transformer": ArchitectureCriteria(
        name="Dense Transformer",
        required_keywords=[
            "transformer", "attention", "gpt", "llama", "claude", "gemini",
            "dense", "decoder-only", "encoder-decoder", "mha", "rope"
        ],
        forbidden_keywords=["moe", "expert", "sparse", "mamba", "ssm", "diffusion"],
        confidence_threshold=0.6
    ),
    "moe": ArchitectureCriteria(
        name="Mixture of Experts",
        required_keywords=[
            "moe", "mixture of experts", "expert", "routing", "sparse",
            "mixtral", "switch transformer", "top-k", "expert choice"
        ],
        forbidden_keywords=["diffusion", "ssm"],
        confidence_threshold=0.7
    ),
    "ssm": ArchitectureCriteria(
        name="State Space Model",
        required_keywords=[
            "ssm", "state space", "mamba", "rwkv", "linear attention",
            "selective state", "structured state", "griffin", "jamba ssm"
        ],
        forbidden_keywords=["diffusion", "moe"],
        confidence_threshold=0.7
    ),
    "multimodal": ArchitectureCriteria(
        name="Multimodal",
        required_keywords=[
            "multimodal", "vision", "image", "clip", "llava", "flamingo",
            "gpt-4v", "gemini vision", "vision-language", "vlm", "pixtral"
        ],
        forbidden_keywords=["diffusion"],
        confidence_threshold=0.6
    ),
    "reasoning": ArchitectureCriteria(
        name="Reasoning",
        required_keywords=[
            "reasoning", "chain-of-thought", "cot", "test-time compute",
            "o1", "o3", "deepseek-r1", "prm", "process reward", "grpo",
            "extended thinking", "inference scaling"
        ],
        forbidden_keywords=["diffusion"],
        confidence_threshold=0.7
    ),
    "diffusion": ArchitectureCriteria(
        name="Diffusion",
        required_keywords=[
            "diffusion", "denoising", "ddpm", "latent diffusion", "dalle",
            "stable diffusion", "imagen", "sora", "flow matching", "dit",
            "video generation", "image generation"
        ],
        forbidden_keywords=[],
        confidence_threshold=0.8
    ),
    "other": ArchitectureCriteria(
        name="Other",
        required_keywords=[],
        forbidden_keywords=[],
        confidence_threshold=0.0
    )
}


# Known model architecture mappings
KNOWN_MODEL_ARCHITECTURES = {
    # OpenAI
    "gpt-4": "dense-transformer",
    "gpt-4-turbo": "dense-transformer",
    "gpt-4o": "multimodal",
    "gpt-4o-mini": "dense-transformer",
    "o1-preview": "reasoning",
    "o1-mini": "reasoning",
    "o3": "reasoning",
    "o3-mini": "reasoning",
    "gpt-4.5": "dense-transformer",
    "dall-e": "diffusion",
    "dall-e-2": "diffusion",
    "dall-e-3": "diffusion",
    "sora": "diffusion",
    "whisper": "dense-transformer",
    
    # Anthropic
    "claude": "dense-transformer",
    "claude-2": "dense-transformer",
    "claude-3": "dense-transformer",
    "claude-3-opus": "dense-transformer",
    "claude-3-sonnet": "dense-transformer",
    "claude-3-haiku": "dense-transformer",
    "claude-3.5-sonnet": "dense-transformer",
    "claude-3.5-haiku": "dense-transformer",
    "claude-3.7-sonnet": "reasoning",
    
    # Google
    "gemini": "dense-transformer",
    "gemini-1.0": "dense-transformer",
    "gemini-1.5": "dense-transformer",
    "gemini-2.0": "multimodal",
    "gemma": "dense-transformer",
    "gemma-2": "dense-transformer",
    "gemma-3": "multimodal",
    "imagen": "diffusion",
    "imagen-3": "diffusion",
    "veo": "diffusion",
    "veo-2": "diffusion",
    
    # Meta
    "llama": "dense-transformer",
    "llama-2": "dense-transformer",
    "llama-3": "dense-transformer",
    "llama-3.1": "dense-transformer",
    "llama-3.2": "dense-transformer",
    "llama-3.2-vision": "multimodal",
    "llama-3.3": "dense-transformer",
    "code-llama": "dense-transformer",
    "sam": "dense-transformer",
    "sam-2": "dense-transformer",
    
    # Mistral
    "mistral": "dense-transformer",
    "mistral-7b": "dense-transformer",
    "mixtral": "moe",
    "mixtral-8x7b": "moe",
    "mixtral-8x22b": "moe",
    "mistral-large": "dense-transformer",
    "mistral-large-2": "dense-transformer",
    "mistral-small": "dense-transformer",
    "codestral": "dense-transformer",
    "mathstral": "dense-transformer",
    "pixtral": "multimodal",
    "mistral-nemo": "dense-transformer",
    "mistral-medium": "dense-transformer",
    
    # Other
    "mamba": "ssm",
    "falcon-mamba": "ssm",
    "jamba": "ssm",
    "rwkv": "ssm",
    "stable-diffusion": "diffusion",
    "sdxl": "diffusion",
    "sd-3": "diffusion",
    "flux": "diffusion",
    "deepseek-r1": "reasoning",
    "deepseek-v3": "moe",
    "qwen": "dense-transformer",
    "qwen2-vl": "multimodal",
    "internvl": "multimodal",
    "llava": "multimodal",
}


def normalize_model_name(name):
    """Normalize model name for lookup."""
    # Convert to lowercase
    normalized = name.lower()
    # Remove version numbers with dots (e.g., "3.5" -> "35")
    normalized = re.sub(r'(\d)\.(\d)', r'\1\2', normalized)
    # Remove common separators
    normalized = re.sub(r'[-_\s]+', '-', normalized)
    # Remove trailing -v, -version, etc.
    normalized = re.sub(r'(-v)?-\d+$', '', normalized)
    return normalized


def calculate_confidence(text, criteria):
    """Calculate confidence score for architecture classification."""
    text_lower = text.lower()
    
    # Count required keyword matches
    required_matches = sum(1 for kw in criteria.required_keywords if kw in text_lower)
    required_score = required_matches / max(len(criteria.required_keywords), 1)
    
    # Count forbidden keyword matches (penalty)
    forbidden_matches = sum(1 for kw in criteria.forbidden_keywords if kw in text_lower)
    forbidden_penalty = forbidden_matches / max(len(criteria.forbidden_keywords), 1) if criteria.forbidden_keywords else 0
    
    # Calculate confidence
    confidence = required_score * (1 - forbidden_penalty * 0.5)
    
    return max(0.0, min(1.0, confidence))


def classify_by_keywords(model_data):
    """Classify model based on keywords in its data."""
    # Combine all text fields for analysis
    text_fields = []
    
    for key in ["name", "architecture", "key_features", "description", "type", "category"]:
        if key in model_data and model_data[key]:
            text_fields.append(str(model_data[key]))
    
    # Add benchmark keys as hints
    if "benchmark_claims" in model_data:
        text_fields.append(str(model_data["benchmark_claims"]))
    
    combined_text = " ".join(text_fields)
    
    # Calculate confidence for each architecture
    scores = {}
    for arch_key, criteria in ARCHITECTURE_CRITERIA.items():
        if arch_key != "other":
            scores[arch_key] = calculate_confidence(combined_text, criteria)
    
    # Get highest scoring architecture
    if scores:
        best_arch = max(scores, key=scores.get)
        best_score = scores[best_arch]
        
        # Check if it meets threshold
        if best_score >= ARCHITECTURE_CRITERIA[best_arch].confidence_threshold:
            return best_arch, best_score
    
    return "other", 0.0


def classify_model(model_data):
    """
    Classify a single model into an architecture category.
    
    Returns a dict with classification results.
    """
    model_name = model_data.get("name", "")
    normalized_name = normalize_model_name(model_name)
    
    result = {
        "model_name": model_name,
        "normalized_name": normalized_name,
        "architecture": "other",
        "confidence": 0.0,
        "method": "unknown",
        "details": {}
    }
    
    # Method 1: Check known models
    for known_name, arch in KNOWN_MODEL_ARCHITECTURES.items():
        if known_name in normalized_name or normalized_name.startswith(known_name):
            result["architecture"] = arch
            result["confidence"] = 1.0
            result["method"] = "known_model_lookup"
            result["details"]["matched_name"] = known_name
            return result
    
    # Method 2: Check explicit architecture field
    if "architecture" in model_data:
        arch_value = model_data["architecture"].lower()
        if arch_value in ARCHITECTURE_CRITERIA:
            result["architecture"] = arch_value
            result["confidence"] = 0.95
            result["method"] = "explicit_field"
            return result
    
    # Method 3: Keyword-based classification
    arch, confidence = classify_by_keywords(model_data)
    result["architecture"] = arch
    result["confidence"] = confidence
    result["method"] = "keyword_classification"
    
    return result


def classify_from_lab_data(file_path):
    """Classify all models from lab announcements JSON."""
    results = []
    
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    for lab_data in data.get("labs", []):
        lab_name = lab_data.get("lab", "Unknown")
        
        for model in lab_data.get("models", []):
            classification = classify_model(model)
            classification["lab"] = lab_name
            classification["announcement_date"] = model.get("announcement_date", "")
            classification["url"] = model.get("url", "")
            results.append(classification)
    
    return results


def generate_summary(results):
    """Generate summary statistics from classification results."""
    total = len(results)
    
    # Count by architecture
    arch_counts = {}
    for r in results:
        arch = r["architecture"]
        arch_counts[arch] = arch_counts.get(arch, 0) + 1
    
    # Count by lab
    lab_counts = {}
    for r in results:
        lab = r["lab"]
        lab_counts[lab] = lab_counts.get(lab, 0) + 1
    
    # Calculate average confidence
    avg_confidence = sum(r["confidence"] for r in results) / total if total > 0 else 0
    
    # High confidence classifications
    high_conf = sum(1 for r in results if r["confidence"] >= 0.8)
    
    return {
        "total_models": total,
        "architecture_distribution": arch_counts,
        "lab_distribution": lab_counts,
        "average_confidence": round(avg_confidence, 3),
        "high_confidence_rate": round(high_conf / total, 3) if total > 0 else 0
    }


def print_classification(result, verbose=False):
    """Print classification result."""
    print(f"\n{'='*60}")
    print(f"Model: {result['model_name']}")
    print(f"Lab: {result.get('lab', 'N/A')}")
    print(f"Architecture: {ARCHITECTURE_CRITERIA[result['architecture']].name}")
    print(f"Confidence: {result['confidence']:.2%}")
    print(f"Method: {result['method']}")
    
    if verbose and result.get("details"):
        print(f"Details: {result['details']}")


def print_summary(summary):
    """Print summary statistics."""
    print(f"\n{'='*60}")
    print("CLASSIFICATION SUMMARY")
    print(f"{'='*60}")
    print(f"Total Models: {summary['total_models']}")
    print(f"Average Confidence: {summary['average_confidence']:.2%}")
    print(f"High Confidence Rate: {summary['high_confidence_rate']:.2%}")
    
    print("\nArchitecture Distribution:")
    for arch, count in sorted(summary['architecture_distribution'].items(), key=lambda x: -x[1]):
        pct = count / summary['total_models'] * 100
        name = ARCHITECTURE_CRITERIA[arch].name if arch in ARCHITECTURE_CRITERIA else arch
        print(f"  {name}: {count} ({pct:.1f}%)")
    
    print("\nLab Distribution:")
    for lab, count in sorted(summary['lab_distribution'].items(), key=lambda x: -x[1]):
        pct = count / summary['total_models'] * 100
        print(f"  {lab}: {count} ({pct:.1f}%)")


def main():
    parser = argparse.ArgumentParser(
        description="Classify AI models by architecture",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    %(prog)s --model-name "GPT-4"
    %(prog)s --lab-data ../../data/raw/lab_announcements.json
    %(prog)s --lab-data ../../data/raw/lab_announcements.json --output results.json
        """
    )
    
    parser.add_argument("--model-name", type=str, help="Classify a single model by name")
    parser.add_argument("--file", type=str, help="JSON file with model data")
    parser.add_argument("--lab-data", type=str, help="Lab announcements JSON file")
    parser.add_argument("--output", type=str, help="Output file for results (JSON)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--summary-only", action="store_true", help="Only show summary")
    
    args = parser.parse_args()
    
    results = []
    
    if args.model_name:
        # Classify single model
        model_data = {"name": args.model_name}
        result = classify_model(model_data)
        results.append(result)
        print_classification(result, args.verbose)
        
    elif args.lab_data:
        # Classify from lab data
        results = classify_from_lab_data(args.lab_data)
        
        if not args.summary_only:
            for r in results:
                print_classification(r, args.verbose)
        
        summary = generate_summary(results)
        print_summary(summary)
        
    elif args.file:
        # Classify from generic file
        with open(args.file, 'r') as f:
            data = json.load(f)
        
        if isinstance(data, list):
            for model_data in data:
                result = classify_model(model_data)
                results.append(result)
                if not args.summary_only:
                    print_classification(result, args.verbose)
        else:
            result = classify_model(data)
            results.append(result)
            print_classification(result, args.verbose)
        
        summary = generate_summary(results)
        print_summary(summary)
    
    else:
        # Default: classify from lab_announcements.json if exists
        default_path = Path(__file__).parent.parent / "data" / "raw" / "lab_announcements.json"
        if default_path.exists():
            print(f"Using default lab data: {default_path}")
            results = classify_from_lab_data(str(default_path))
            
            if not args.summary_only:
                for r in results:
                    print_classification(r, args.verbose)
            
            summary = generate_summary(results)
            print_summary(summary)
        else:
            parser.print_help()
            sys.exit(1)
    
    # Save results if output specified
    if args.output and results:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")


if __name__ == "__main__":
    main()
