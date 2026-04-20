#!/usr/bin/env python3
"""
Data validation module for the ingestion pipeline.

Validates lab announcements and benchmark data before ingestion.
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import logging

logger = logging.getLogger(__name__)


class DataValidator:
    """Validates data before ingestion into the database."""
    
    # Allowed architectures from the schema
    ALLOWED_ARCHITECTURES = [
        "dense-transformer", "moe", "ssm", "multimodal", "reasoning", "other"
    ]
    
    # Date format regex (YYYY-MM-DD)
    DATE_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2}$')
    
    def __init__(self):
        self.errors: List[str] = []
        self.warnings: List[str] = []
    
    def validate_lab_announcements(self, data: Dict) -> Tuple[bool, List[str], List[str]]:
        """
        Validate lab announcements data structure.
        
        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        # Check top-level structure
        required_top = ["scraped_at", "total_labs", "total_models", "labs"]
        for field in required_top:
            if field not in data:
                self.errors.append(f"Missing required top-level field: {field}")
        
        if "labs" not in data:
            return False, self.errors, self.warnings
        
        # Validate each lab
        total_models_count = 0
        labs_seen = set()
        
        for lab_data in data.get("labs", []):
            self._validate_lab_entry(lab_data, labs_seen)
            if "models" in lab_data:
                total_models_count += len(lab_data["models"])
        
        # Check totals match (treat as warning, not error)
        if data.get("total_labs") != len(labs_seen):
            self.warnings.append(
                f"total_labs ({data.get('total_labs')}) doesn't match actual labs ({len(labs_seen)})"
            )
        
        if data.get("total_models") != total_models_count:
            self.warnings.append(
                f"total_models ({data.get('total_models')}) doesn't match actual models ({total_models_count})"
            )
        
        # Check scraped_at format
        scraped_at = data.get("scraped_at", "")
        if scraped_at:
            try:
                datetime.fromisoformat(scraped_at.replace('Z', '+00:00'))
            except ValueError:
                self.warnings.append(f"Invalid scraped_at timestamp format: {scraped_at}")
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _validate_lab_entry(self, lab_data: Dict, labs_seen: set):
        """Validate a single lab entry."""
        if "lab" not in lab_data:
            self.errors.append("Lab entry missing 'lab' field")
            return
        
        lab_name = lab_data["lab"]
        labs_seen.add(lab_name)
        
        if "models" not in lab_data:
            self.errors.append(f"Lab '{lab_name}' missing 'models' field")
            return
        
        # Validate each model
        for i, model in enumerate(lab_data["models"]):
            self._validate_model(model, lab_name, i)
    
    def _validate_model(self, model: Dict, lab_name: str, index: int):
        """Validate a single model entry."""
        prefix = f"Lab '{lab_name}', Model[{index}]"
        
        # Required fields
        required = ["name", "announcement_date", "architecture", "url"]
        for field in required:
            if field not in model:
                self.errors.append(f"{prefix}: Missing required field '{field}'")
        
        # Validate name
        name = model.get("name", "")
        if not name or not isinstance(name, str):
            self.errors.append(f"{prefix}: Invalid or missing model name")
        
        # Validate architecture
        arch = model.get("architecture")
        if arch and arch not in self.ALLOWED_ARCHITECTURES:
            self.errors.append(
                f"{prefix}: Invalid architecture '{arch}'. Must be one of: {self.ALLOWED_ARCHITECTURES}"
            )
        
        # Validate date format
        date = model.get("announcement_date", "")
        if date and date != "unknown":
            if not self.DATE_PATTERN.match(date):
                self.warnings.append(
                    f"{prefix}: Non-standard date format '{date}'. Expected YYYY-MM-DD"
                )
            else:
                # Validate date is reasonable
                try:
                    parsed_date = datetime.strptime(date, "%Y-%m-%d")
                    if parsed_date.year < 2010 or parsed_date.year > 2030:
                        self.warnings.append(
                            f"{prefix}: Date {date} seems unusual (expected 2010-2030)"
                        )
                except ValueError:
                    self.warnings.append(f"{prefix}: Invalid date: {date}")
        
        # Validate URL
        url = model.get("url", "")
        if url and not url.startswith(("http://", "https://")):
            self.warnings.append(f"{prefix}: URL doesn't start with http/https: {url}")
        
        # Validate benchmark_claims
        if "benchmark_claims" in model:
            claims = model["benchmark_claims"]
            if not isinstance(claims, dict):
                self.errors.append(f"{prefix}: benchmark_claims must be a dictionary")
            else:
                for bench_name, score in claims.items():
                    if not isinstance(score, (int, float)):
                        self.errors.append(
                            f"{prefix}: Benchmark '{bench_name}' score must be a number"
                        )
                    elif score < 0 or score > 100:
                        self.warnings.append(
                            f"{prefix}: Benchmark '{bench_name}' score {score} is outside typical range (0-100)"
                        )
        
        # Validate key_features
        if "key_features" in model:
            features = model["key_features"]
            if not isinstance(features, str):
                self.warnings.append(f"{prefix}: key_features should be a string")
    
    def validate_benchmark_scores(self, data: Dict) -> Tuple[bool, List[str], List[str]]:
        """
        Validate benchmark scores data structure.
        
        Returns:
            Tuple of (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        # Check top-level structure
        if "extractions" not in data:
            self.errors.append("Missing 'extractions' field")
            return False, self.errors, self.warnings
        
        extractions = data.get("extractions", [])
        if not isinstance(extractions, list):
            self.errors.append("'extractions' must be a list")
            return False, self.errors, self.warnings
        
        # Validate each extraction
        for i, extraction in enumerate(extractions):
            self._validate_extraction(extraction, i)
        
        return len(self.errors) == 0, self.errors, self.warnings
    
    def _validate_extraction(self, extraction: Dict, index: int):
        """Validate a single benchmark extraction entry."""
        prefix = f"Extraction[{index}]"
        
        # Required fields
        required = ["paper_id", "benchmark"]
        for field in required:
            if field not in extraction:
                self.errors.append(f"{prefix}: Missing required field '{field}'")
        
        # Validate metric
        metric = extraction.get("metric", "")
        if not metric:
            self.warnings.append(f"{prefix}: Missing metric field")
        
        # Validate score if present
        score = extraction.get("score")
        if score is not None:
            if not isinstance(score, (int, float)):
                self.errors.append(f"{prefix}: Score must be a number")
            elif score < 0 or score > 1000:  # Allow higher scores for some metrics
                self.warnings.append(f"{prefix}: Score {score} seems unusual")
        
        # Validate confidence
        confidence = extraction.get("confidence", "")
        allowed_confidence = ["high", "medium", "low", "mentioned"]
        if confidence and confidence not in allowed_confidence:
            self.warnings.append(
                f"{prefix}: Unusual confidence value '{confidence}'. Expected one of: {allowed_confidence}"
            )
        
        # Validate model field if present
        model = extraction.get("model")
        if model and not isinstance(model, str):
            self.warnings.append(f"{prefix}: Model field should be a string")
    
    def get_summary(self, data: Dict, data_type: str = "lab") -> Dict[str, Any]:
        """Get a summary of the validated data."""
        summary = {
            "data_type": data_type,
            "total_errors": len(self.errors),
            "total_warnings": len(self.warnings),
        }
        
        if data_type == "lab":
            summary["total_labs"] = data.get("total_labs", 0)
            summary["total_models"] = data.get("total_models", 0)
            
            # Count by architecture
            arch_counts = {}
            for lab in data.get("labs", []):
                for model in lab.get("models", []):
                    arch = model.get("architecture", "unknown")
                    arch_counts[arch] = arch_counts.get(arch, 0) + 1
            summary["architecture_distribution"] = arch_counts
            
        elif data_type == "benchmark":
            summary["total_extractions"] = len(data.get("extractions", []))
            
            # Count by confidence level
            confidence_counts = {}
            for ext in data.get("extractions", []):
                conf = ext.get("confidence", "unknown")
                confidence_counts[conf] = confidence_counts.get(conf, 0) + 1
            summary["confidence_distribution"] = confidence_counts
        
        return summary


def main():
    """CLI entry point for validation."""
    import sys
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate data before ingestion")
    parser.add_argument("file", help="Path to JSON file to validate")
    parser.add_argument("--type", choices=["lab", "benchmark"], 
                       help="Type of data (auto-detected if not specified)")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(levelname)s: %(message)s'
    )
    
    # Load data
    file_path = Path(args.file)
    if not file_path.exists():
        logger.error(f"File not found: {file_path}")
        sys.exit(1)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}")
        sys.exit(1)
    
    # Auto-detect type if not specified
    data_type = args.type
    if not data_type:
        if "labs" in data:
            data_type = "lab"
        elif "extractions" in data:
            data_type = "benchmark"
        else:
            logger.error("Cannot auto-detect data type. Use --type to specify.")
            sys.exit(1)
    
    # Validate
    validator = DataValidator()
    
    if data_type == "lab":
        is_valid, errors, warnings = validator.validate_lab_announcements(data)
    else:
        is_valid, errors, warnings = validator.validate_benchmark_scores(data)
    
    # Print results
    summary = validator.get_summary(data, data_type)
    
    print("\n" + "=" * 60)
    print(f"VALIDATION RESULTS - {data_type.upper()} DATA")
    print("=" * 60)
    
    print(f"\nSummary:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for error in errors[:20]:  # Show first 20
            print(f"  ✗ {error}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more")
    
    if warnings:
        print(f"\nWarnings ({len(warnings)}):")
        for warning in warnings[:10]:  # Show first 10
            print(f"  ⚠ {warning}")
        if len(warnings) > 10:
            print(f"  ... and {len(warnings) - 10} more")
    
    print("\n" + "=" * 60)
    if is_valid:
        print("✓ Validation PASSED")
        sys.exit(0)
    else:
        print("✗ Validation FAILED")
        sys.exit(1)


if __name__ == "__main__":
    main()
