#!/usr/bin/env python3
"""
Validation script for AI Model Metadata Schema.

Usage:
    python validate-model-schema.py <json_file>
    python validate-model-schema.py --test  # Run built-in tests
"""

import json
import sys
import os
from pathlib import Path

try:
    import jsonschema
    from jsonschema import validate, ValidationError
except ImportError:
    print("Error: jsonschema library required. Install with: pip install jsonschema")
    sys.exit(1)


# Get paths relative to script location
SCRIPT_DIR = Path(__file__).parent.parent
SCHEMA_PATH = SCRIPT_DIR / "docs" / "schemas" / "model-metadata.json"


def load_schema():
    """Load the JSON schema from file."""
    if not SCHEMA_PATH.exists():
        print(f"Error: Schema file not found at {SCHEMA_PATH}")
        sys.exit(1)
    
    with open(SCHEMA_PATH, 'r') as f:
        return json.load(f)


def validate_model_data(data: dict, schema: dict) -> tuple[bool, list]:
    """
    Validate model data against the schema.
    
    Returns:
        Tuple of (is_valid, error_messages)
    """
    errors = []
    
    try:
        validate(instance=data, schema=schema)
        return True, []
    except ValidationError as e:
        errors.append(f"Validation error: {e.message}")
        if e.path:
            errors.append(f"  Path: {'.'.join(str(p) for p in e.path)}")
        return False, errors


def validate_file(file_path: str, schema: dict) -> bool:
    """Validate a JSON file against the schema."""
    path = Path(file_path)
    
    if not path.exists():
        print(f"Error: File not found: {file_path}")
        return False
    
    try:
        with open(path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {file_path}: {e}")
        return False
    
    is_valid, errors = validate_model_data(data, schema)
    
    if is_valid:
        print(f"✓ {file_path} - Valid")
        return True
    else:
        print(f"✗ {file_path} - Invalid")
        for error in errors:
            print(f"  {error}")
        return False


def run_tests():
    """Run built-in tests with sample data."""
    schema = load_schema()
    
    print("Running validation tests...\n")
    
    # Test 1: Valid sample data
    sample_path = SCRIPT_DIR / "data" / "sample-model.json"
    print(f"Test 1: Validating sample data ({sample_path})")
    result1 = validate_file(str(sample_path), schema)
    
    # Test 2: Valid minimal data
    print("\nTest 2: Validating minimal valid data")
    minimal_data = {
        "name": "Test Model",
        "lab": "Test Lab",
        "release_date": "2024-01-01",
        "architecture": "dense-transformer",
        "parameters": 7,
        "context_window": 4096,
        "benchmarks": {},
        "paper_url": "https://arxiv.org/abs/2401.00001",
        "announcement_url": "https://example.com/announcement"
    }
    is_valid, errors = validate_model_data(minimal_data, schema)
    if is_valid:
        print("✓ Minimal valid data - Valid")
        result2 = True
    else:
        print("✗ Minimal valid data - Invalid")
        for error in errors:
            print(f"  {error}")
        result2 = False
    
    # Test 3: Invalid data (missing required field)
    print("\nTest 3: Validating data with missing required field")
    invalid_data = {
        "name": "Test Model",
        "lab": "Test Lab"
        # missing release_date, architecture, etc.
    }
    is_valid, errors = validate_model_data(invalid_data, schema)
    if not is_valid:
        print("✓ Correctly rejected invalid data (missing required fields)")
        result3 = True
    else:
        print("✗ Should have rejected invalid data")
        result3 = False
    
    # Test 4: Invalid architecture enum
    print("\nTest 4: Validating data with invalid architecture value")
    invalid_arch_data = {
        "name": "Test Model",
        "lab": "Test Lab",
        "release_date": "2024-01-01",
        "architecture": "invalid-arch",
        "parameters": 7,
        "context_window": 4096,
        "benchmarks": {},
        "paper_url": "https://arxiv.org/abs/2401.00001",
        "announcement_url": "https://example.com/announcement"
    }
    is_valid, errors = validate_model_data(invalid_arch_data, schema)
    if not is_valid:
        print("✓ Correctly rejected invalid architecture value")
        result4 = True
    else:
        print("✗ Should have rejected invalid architecture")
        result4 = False
    
    # Test 5: Valid MoE model
    print("\nTest 5: Validating MoE model data")
    moe_data = {
        "name": "Mixtral 8x7B",
        "lab": "Mistral AI",
        "release_date": "2023-12-11",
        "architecture": "moe",
        "parameters": 47,
        "context_window": 32768,
        "benchmarks": {
            "mmlu": 70.6,
            "humaneval": 54.2
        },
        "paper_url": "https://arxiv.org/abs/2401.04088",
        "announcement_url": "https://mistral.ai/news/mixtral-of-experts/",
        "tags": ["open-weight", "multilingual"]
    }
    is_valid, errors = validate_model_data(moe_data, schema)
    if is_valid:
        print("✓ MoE model data - Valid")
        result5 = True
    else:
        print("✗ MoE model data - Invalid")
        for error in errors:
            print(f"  {error}")
        result5 = False
    
    # Summary
    print("\n" + "=" * 50)
    passed = sum([result1, result2, result3, result4, result5])
    total = 5
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("All tests passed! ✓")
        return 0
    else:
        print("Some tests failed. ✗")
        return 1


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate-model-schema.py <json_file>")
        print("       python validate-model-schema.py --test")
        sys.exit(1)
    
    if sys.argv[1] == "--test":
        sys.exit(run_tests())
    
    schema = load_schema()
    file_path = sys.argv[1]
    
    if validate_file(file_path, schema):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
