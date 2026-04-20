#!/usr/bin/env python3
"""
Classify all 179 models by architecture type using the established taxonomy.

Taxonomy:
1. Dense Transformer - Full attention, all parameters active
2. MoE - Mixture of Experts, sparse activation
3. SSM - State Space Models, linear complexity
4. Multimodal - Cross-modal (vision + text)
5. Reasoning - Test-time compute, chain-of-thought
6. Diffusion - Iterative denoising for generation
"""

import json
import re
from collections import defaultdict
from datetime import datetime

# Architecture classification rules based on model name patterns
ARCHITECTURE_RULES = {
    "reasoning": {
        "patterns": [
            r"\bo1\b", r"\bo3\b", r"o1-mini", r"o1-preview",
            r"deepseek-r1", r"deepseek-r1-zero", r"claude.*3\.7",
            r"kimi.*k1\.5", r"qwq-", r"gemini.*thinking",
            r"marco-o1", r"reflection-llama", r"r1-", r"-r1-",
            r"cirrus", r"nevoira",  # Community reasoning variants
        ],
        "keywords": ["reasoning", "thinking", "r1", "reflection", "thought", "cirrus"],
        "confidence": "high"
    },
    "moe": {
        "patterns": [
            r"mixtral", r"mixtral.*8x", r"qwen.*moe", r"grok",
            r"deepseek-v3", r"dbrx", r"jamba", r"switch",
            r"8x7b", r"8x22b", r"\bmoe\b",
        ],
        "keywords": ["moe", "mixture", "expert", "8x", "16x", "64x", "256x"],
        "confidence": "high"
    },
    "multimodal": {
        "patterns": [
            r"gpt-4o$", r"gpt-4v", r"claude.*vision", r"llava",
            r"pixtral", r"llama.*vision", r"qwen.*vl", r"internvl",
            r"dall-e", r"sora", r"imagen", r"veo",
            r"qwen2-vl", r"qwen.*audio",
            r"visstar", r"vl-", r"vision-",
            r"qwen2vl",  # HF class
        ],
        "keywords": ["vision", "vl", "multimodal", "image", "video", "audio", "4o", "4v", "vis"],
        "confidence": "high"
    },
    "diffusion": {
        "patterns": [
            r"stable-diffusion", r"sdxl", r"sd3", r"dall-e",
            r"imagen", r"sora", r"veo", r"flux", r"midjourney",
            r"video.*diffusion", r"image.*diffusion",
        ],
        "keywords": ["diffusion", "generative", "image", "video"],
        "confidence": "high"
    },
    "ssm": {
        "patterns": [
            r"\bmamba\b", r"\bjamba\b", r"\brwkv\b",
            r"falcon.*mamba", r"griffin", r"cheetah",
            r"zamba", r"retnet",
        ],
        "keywords": ["mamba", "ssm", "state", "space", "rwkv", "linear"],
        "confidence": "high"
    }
}

# HuggingFace class to architecture mapping
HF_CLASS_MAPPING = {
    "LlamaForCausalLM": "dense-transformer",
    "Qwen2ForCausalLM": "dense-transformer",
    "Qwen2_5ForCausalLM": "dense-transformer",
    "MistralForCausalLM": "dense-transformer",
    "MixtralForCausalLM": "moe",
    "Gemma2ForCausalLM": "dense-transformer",
    "GemmaForCausalLM": "dense-transformer",
    "Phi3ForCausalLM": "dense-transformer",
    "PhiForCausalLM": "dense-transformer",
    "CohereForCausalLM": "dense-transformer",
    "FalconForCausalLM": "dense-transformer",
    "GPT2LMHeadModel": "dense-transformer",
    "GPTNeoForCausalLM": "dense-transformer",
    "GPTJForCausalLM": "dense-transformer",
    "OPTForCausalLM": "dense-transformer",
    "BloomForCausalLM": "dense-transformer",
    "MambaForCausalLM": "ssm",
    "Qwen2VLForConditionalGeneration": "multimodal",
    "Unknown": "unknown",
}


def normalize_model_name(name):
    """Normalize model name for matching."""
    # Remove org prefix
    name = re.sub(r'^[\w-]+/', '', name)
    # Remove common suffixes
    name = re.sub(r'-(Instruct|Chat|Base|Pretrained|DPO|SFT|v\d+\.\d+)$', '', name, flags=re.I)
    return name.lower().strip()


def classify_by_name(model_name):
    """Classify model based on its name using pattern matching."""
    name_lower = model_name.lower()
    
    # Check architecture rules in priority order
    for arch_type, rules in ARCHITECTURE_RULES.items():
        # Check patterns first (more specific)
        for pattern in rules["patterns"]:
            if re.search(pattern, name_lower, re.I):
                return arch_type, rules["confidence"], f"Pattern match: {pattern}"
        
        # Check keywords
        for keyword in rules["keywords"]:
            if keyword.lower() in name_lower:
                return arch_type, "medium", f"Keyword match: {keyword}"
    
    return None, None, None


def classify_by_hf_class(hf_class):
    """Classify based on HuggingFace architecture class."""
    if hf_class in HF_CLASS_MAPPING:
        arch = HF_CLASS_MAPPING[hf_class]
        if arch != "unknown":
            return arch, "high", f"HF class: {hf_class}"
    return None, None, None


def classify_model(model_name, hf_class=None):
    """
    Classify a single model with confidence scoring.
    
    Priority:
    1. Name-based patterns (reasoning, multimodal, etc.)
    2. HF class mapping
    3. Default to dense-transformer
    """
    evidence = []
    
    # Priority 1: Name-based classification (catches reasoning, multimodal, MoE, etc.)
    arch, conf, reason = classify_by_name(model_name)
    if arch:
        evidence.append(reason)
        return {
            "architecture_type": arch,
            "confidence": conf,
            "confidence_score": 0.90 if conf == "high" else 0.75,
            "evidence": evidence,
            "classification_method": "name_pattern"
        }
    
    # Priority 2: HuggingFace class mapping
    if hf_class and hf_class != "Unknown":
        arch, conf, reason = classify_by_hf_class(hf_class)
        if arch:
            evidence.append(reason)
            return {
                "architecture_type": arch,
                "confidence": conf,
                "confidence_score": 0.90 if conf == "high" else 0.75,
                "evidence": evidence,
                "classification_method": "hf_class"
            }
    
    # Priority 3: For Unknown HF class, check for specific patterns
    name_lower = model_name.lower()
    
    # Check for Gemini
    if "gemini" in name_lower:
        return {
            "architecture_type": "multimodal",
            "confidence": "high",
            "confidence_score": 0.90,
            "evidence": ["Model name contains 'Gemini' - known multimodal model"],
            "classification_method": "name_pattern"
        }
    
    # Check for GPT variants
    if "gpt" in name_lower:
        return {
            "architecture_type": "dense-transformer",
            "confidence": "medium",
            "confidence_score": 0.70,
            "evidence": ["Model name contains 'GPT' - likely dense transformer"],
            "classification_method": "name_pattern"
        }
    
    # Check for paper references (research models)
    if "paper_" in name_lower:
        return {
            "architecture_type": "dense-transformer",
            "confidence": "low",
            "confidence_score": 0.60,
            "evidence": ["Research paper model - defaulting to dense transformer"],
            "classification_method": "default",
            "note": "Research paper model, may need manual verification"
        }
    
    # Default: Dense transformer (most common)
    return {
        "architecture_type": "dense-transformer",
        "confidence": "low",
        "confidence_score": 0.50,
        "evidence": ["Default classification - no specific indicators found"],
        "classification_method": "default",
        "note": "May need manual verification"
    }


def extract_unique_models(normalized_scores):
    """Extract unique models from normalized scores."""
    models = {}
    for entry in normalized_scores.get("normalized_scores", []):
        model_name = entry.get("model_name")
        if model_name not in models:
            models[model_name] = {
                "name": model_name,
                "hf_class": entry.get("architecture"),
                "parameters_billions": entry.get("parameters_billions"),
                "source": entry.get("source"),
                "submission_date": entry.get("submission_date"),
                "benchmarks": []
            }
        models[model_name]["benchmarks"].append(entry.get("benchmark"))
    return models


def classify_all_models(normalized_scores_path, output_path):
    """Main classification function."""
    
    # Load normalized scores
    with open(normalized_scores_path, 'r') as f:
        data = json.load(f)
    
    # Extract unique models
    models = extract_unique_models(data)
    print(f"Found {len(models)} unique models to classify")
    
    # Classify each model
    classifications = {
        "metadata": {
            "version": "1.0.0",
            "created_date": datetime.now().isoformat(),
            "total_models": len(models),
            "taxonomy_version": "1.0",
            "taxonomy": [
                "dense-transformer",
                "moe",
                "ssm",
                "multimodal",
                "reasoning",
                "diffusion"
            ],
            "classification_methods": [
                "name_pattern",
                "hf_class",
                "default"
            ]
        },
        "classifications": {},
        "statistics": {},
        "edge_cases": [],
        "methodology": {
            "description": "Classification based on model names and HuggingFace architecture classes",
            "confidence_scoring": {
                "high": "0.90-0.95 - Explicit naming or authoritative source",
                "medium": "0.70-0.85 - Strong pattern/keyword match",
                "low": "0.50-0.70 - Default or inferred classification"
            },
            "edge_case_handling": "Hybrid architectures classified by primary distinguishing feature"
        }
    }
    
    # Track statistics
    arch_counts = defaultdict(int)
    confidence_counts = defaultdict(int)
    
    for model_name, model_info in models.items():
        classification = classify_model(
            model_name,
            model_info.get("hf_class")
        )
        
        # Add model metadata
        classification["model_name"] = model_name
        classification["parameters_billions"] = model_info.get("parameters_billions")
        classification["hf_class"] = model_info.get("hf_class")
        
        # Check for edge cases (hybrid architectures)
        name_lower = model_name.lower()
        
        # Multimodal models based on dense transformers
        if classification["architecture_type"] == "multimodal":
            if any(x in name_lower for x in ["llama", "qwen", "gemma", "mistral"]):
                classification["edge_case"] = "hybrid"
                classification["edge_case_note"] = "Dense transformer base with multimodal capabilities"
                classifications["edge_cases"].append({
                    "model": model_name,
                    "type": "hybrid",
                    "note": "Dense transformer base with multimodal capabilities"
                })
        
        # Reasoning models with dense base
        if classification["architecture_type"] == "reasoning":
            if any(x in name_lower for x in ["llama", "qwen", "gemma"]):
                classification["edge_case"] = "hybrid"
                classification["edge_case_note"] = "Dense transformer with reasoning training"
                classifications["edge_cases"].append({
                    "model": model_name,
                    "type": "hybrid",
                    "note": "Dense transformer with reasoning training"
                })
        
        classifications["classifications"][model_name] = classification
        arch_counts[classification["architecture_type"]] += 1
        confidence_counts[classification["confidence"]] += 1
    
    # Calculate statistics
    classifications["statistics"] = {
        "total_models": len(models),
        "by_architecture": dict(arch_counts),
        "by_confidence": dict(confidence_counts),
        "coverage": {
            "high_confidence": confidence_counts["high"],
            "medium_confidence": confidence_counts["medium"],
            "low_confidence": confidence_counts["low"],
            "high_confidence_percentage": round(confidence_counts["high"] / len(models) * 100, 2)
        }
    }
    
    # Save classifications
    with open(output_path, 'w') as f:
        json.dump(classifications, f, indent=2)
    
    print(f"\nClassification complete!")
    print(f"Total models: {len(models)}")
    print(f"\nBy Architecture:")
    for arch, count in sorted(arch_counts.items(), key=lambda x: -x[1]):
        pct = count / len(models) * 100
        print(f"  {arch}: {count} ({pct:.1f}%)")
    print(f"\nBy Confidence:")
    for conf, count in sorted(confidence_counts.items(), key=lambda x: -x[1]):
        pct = count / len(models) * 100
        print(f"  {conf}: {count} ({pct:.1f}%)")
    print(f"\nHigh confidence coverage: {classifications['statistics']['coverage']['high_confidence_percentage']:.1f}%")
    print(f"\nEdge cases: {len(classifications['edge_cases'])}")
    print(f"\nOutput saved to: {output_path}")
    
    return classifications


if __name__ == "__main__":
    import sys
    
    normalized_scores_path = "data/processed/normalized_scores.json"
    output_path = "data/processed/architecture_classifications.json"
    
    if len(sys.argv) > 1:
        normalized_scores_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_path = sys.argv[2]
    
    classify_all_models(normalized_scores_path, output_path)
