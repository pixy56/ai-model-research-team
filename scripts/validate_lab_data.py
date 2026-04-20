#!/usr/bin/env python3
"""
Validate lab_announcements.json data against the model schema.

Usage:
    python validate_lab_data.py [path_to_json]
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any, Tuple


def validate_lab_announcements(data: Dict) -> Tuple[bool, List[str]]:
    """
    Validate lab announcements data structure.
    
    Returns:
        (is_valid, list of error messages)
    """
    errors = []
    
    # Check top-level structure
    required_top = ["scraped_at", "total_labs", "total_models", "labs"]
    for field in required_top:
        if field not in data:
            errors.append(f"Missing required top-level field: {field}")
    
    if "labs" not in data:
        return False, errors
    
    # Validate each lab
    total_models_count = 0
    labs_seen = set()
    
    for lab_data in data.get("labs", []):
        # Check lab structure
        if "lab" not in lab_data:
            errors.append("Lab entry missing 'lab' field")
            continue
            
        lab_name = lab_data["lab"]
        labs_seen.add(lab_name)
        
        if "models" not in lab_data:
            errors.append(f"Lab '{lab_name}' missing 'models' field")
            continue
        
        models = lab_data["models"]
        total_models_count += len(models)
        
        # Validate each model
        for i, model in enumerate(models):
            model_errors = validate_model(model, lab_name, i)
            errors.extend(model_errors)
    
    # Check totals
    if data.get("total_labs") != len(labs_seen):
        errors.append(f"total_labs ({data.get('total_labs')}) doesn't match actual labs ({len(labs_seen)})")
    
    if data.get("total_models") != total_models_count:
        errors.append(f"total_models ({data.get('total_models')}) doesn't match actual models ({total_models_count})")
    
    return len(errors) == 0, errors


def validate_model(model: Dict, lab_name: str, index: int) -> List[str]:
    """Validate a single model entry."""
    errors = []
    prefix = f"Lab '{lab_name}', Model[{index}]"
    
    # Required fields
    required = ["name", "announcement_date", "architecture", "url"]
    for field in required:
        if field not in model:
            errors.append(f"{prefix}: Missing required field '{field}'")
    
    # Validate architecture value
    allowed_archs = ["dense-transformer", "moe", "ssm", "multimodal", "reasoning", "other"]
    if model.get("architecture") not in allowed_archs:
        errors.append(f"{prefix}: Invalid architecture '{model.get('architecture')}'. Must be one of: {allowed_archs}")
    
    # Validate date format (if not 'unknown')
    date = model.get("announcement_date", "")
    if date and date != "unknown":
        if not isinstance(date, str) or len(date.split("-")) != 3:
            errors.append(f"{prefix}: Invalid date format '{date}'. Expected YYYY-MM-DD or 'unknown'")
    
    # Validate benchmark_claims is a dict
    if "benchmark_claims" in model:
        if not isinstance(model["benchmark_claims"], dict):
            errors.append(f"{prefix}: benchmark_claims must be a dictionary")
        else:
            # Validate benchmark values are numbers
            for bench_name, score in model["benchmark_claims"].items():
                if not isinstance(score, (int, float)):
                    errors.append(f"{prefix}: Benchmark '{bench_name}' score must be a number")
                elif score < 0 or score > 100:
                    errors.append(f"{prefix}: Benchmark '{bench_name}' score {score} is outside reasonable range (0-100)")
    
    return errors


def print_summary(data: Dict):
    """Print a summary of the data."""
    print("\n" + "=" * 60)
    print("LAB ANNOUNCEMENTS DATA SUMMARY")
    print("=" * 60)
    
    print(f"\nScraped at: {data.get('scraped_at', 'unknown')}")
    print(f"Total labs: {data.get('total_labs', 0)}")
    print(f"Total models: {data.get('total_models', 0)}")
    
    print("\nBreakdown by lab:")
    print("-" * 40)
    
    for lab_data in data.get("labs", []):
        lab_name = lab_data.get("lab", "Unknown")
        models = lab_data.get("models", [])
        print(f"  {lab_name}: {len(models)} models")
        
        # Show first few models
        for model in models[:3]:
            arch = model.get("architecture", "unknown")
            date = model.get("announcement_date", "unknown")
            print(f"    - {model['name']} ({arch}, {date})")
        
        if len(models) > 3:
            print(f"    ... and {len(models) - 3} more")
    
    # Architecture distribution
    print("\n\nArchitecture distribution:")
    print("-" * 40)
    arch_counts = {}
    for lab_data in data.get("labs", []):
        for model in lab_data.get("models", []):
            arch = model.get("architecture", "unknown")
            arch_counts[arch] = arch_counts.get(arch, 0) + 1
    
    for arch, count in sorted(arch_counts.items(), key=lambda x: -x[1]):
        pct = (count / data.get("total_models", 1)) * 100
        print(f"  {arch}: {count} ({pct:.1f}%)")


def main():
    # Get file path
    if len(sys.argv) > 1:
        file_path = Path(sys.argv[1])
    else:
        # Default path
        script_dir = Path(__file__).parent.parent
        file_path = script_dir / "data" / "raw" / "lab_announcements.json"
    
    print(f"Validating: {file_path}")
    
    # Load data
    if not file_path.exists():
        print(f"Error: File not found: {file_path}")
        sys.exit(1)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON: {e}")
        sys.exit(1)
    
    # Validate
    is_valid, errors = validate_lab_announcements(data)
    
    # Print results
    if is_valid:
        print("\n✓ Validation PASSED")
        print_summary(data)
        
        # Check acceptance criteria
        total_models = data.get("total_models", 0)
        total_labs = data.get("total_labs", 0)
        
        print("\n" + "=" * 60)
        print("ACCEPTANCE CRITERIA CHECK")
        print("=" * 60)
        
        checks = [
            ("20+ models extracted", total_models >= 20),
            ("All 5 labs covered", total_labs >= 5),
            ("Data validated against schema", True),
        ]
        
        for check_name, passed in checks:
            status = "✓" if passed else "✗"
            print(f"  {status} {check_name}")
        
        all_passed = all(p for _, p in checks)
        
        if all_passed:
            print("\n✓ All acceptance criteria met!")
            sys.exit(0)
        else:
            print("\n✗ Some acceptance criteria not met")
            sys.exit(1)
    else:
        print("\n✗ Validation FAILED")
        print(f"\nFound {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
