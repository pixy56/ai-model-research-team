#!/usr/bin/env python3
"""
Benchmark scores ingestion script for the pipeline.

Ingests benchmark scores from benchmark_scores.json and links them to models.
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from collections import defaultdict

import requests

# Add src to path for database imports
script_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(script_dir))

from scripts.pipeline.validate_data import DataValidator

logger = logging.getLogger(__name__)


class BenchmarkIngester:
    """Ingests benchmark scores into the database."""
    
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url
        self.stats = {
            "total_extractions": 0,
            "linked_to_models": 0,
            "new_benchmarks_added": 0,
            "skipped": 0,
            "failed": 0,
            "errors": []
        }
        self.model_cache: Dict[str, Optional[Dict]] = {}
    
    def load_data(self, file_path: Path) -> Optional[Dict]:
        """Load benchmark scores data from JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Loaded {len(data.get('extractions', []))} extractions from {file_path}")
            return data
        except FileNotFoundError:
            logger.error(f"File not found: {file_path}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {file_path}: {e}")
            return None
    
    def validate_data(self, data: Dict) -> bool:
        """Validate data before ingestion."""
        validator = DataValidator()
        is_valid, errors, warnings = validator.validate_benchmark_scores(data)
        
        if warnings:
            logger.warning(f"Validation warnings ({len(warnings)}):")
            for warning in warnings[:5]:
                logger.warning(f"  ⚠ {warning}")
        
        if not is_valid:
            logger.error(f"Validation failed with {len(errors)} errors:")
            for error in errors[:10]:
                logger.error(f"  ✗ {error}")
            return False
        
        logger.info("✓ Data validation passed")
        return True
    
    def get_all_models(self) -> List[Dict]:
        """Fetch all models from the database."""
        models = []
        page = 1
        
        while True:
            try:
                response = requests.get(
                    f"{self.api_base_url}/api/models",
                    params={"page": page, "page_size": 100},
                    timeout=10
                )
                response.raise_for_status()
                result = response.json()
                
                models.extend(result.get("items", []))
                
                # Check if we've reached the end
                if page >= result.get("pages", 1):
                    break
                page += 1
                
            except requests.RequestException as e:
                logger.error(f"Failed to fetch models: {e}")
                break
        
        logger.info(f"Fetched {len(models)} models from database")
        return models
    
    def find_model_by_name(self, model_name: str) -> Optional[Dict]:
        """Find a model in the database by name (with caching)."""
        if model_name in self.model_cache:
            return self.model_cache[model_name]
        
        try:
            response = requests.get(
                f"{self.api_base_url}/api/models/search",
                params={"q": model_name, "page_size": 20},
                timeout=10
            )
            response.raise_for_status()
            results = response.json()
            
            # Look for exact or partial match
            for model in results.get("items", []):
                if model["name"].lower() == model_name.lower():
                    self.model_cache[model_name] = model
                    return model
                # Check for partial match (e.g., "GPT-4" matches "GPT-4 Turbo")
                if model_name.lower() in model["name"].lower():
                    self.model_cache[model_name] = model
                    return model
            
            self.model_cache[model_name] = None
            return None
            
        except requests.RequestException as e:
            logger.warning(f"Could not search for model '{model_name}': {e}")
            return None
    
    def extract_model_from_context(self, extraction: Dict) -> Optional[str]:
        """Try to extract model name from the context or paper."""
        # If model field is already present
        if extraction.get("model"):
            return extraction["model"]
        
        context = extraction.get("context", "")
        
        # Common model name patterns
        model_patterns = [
            r'\b(GPT-[\w\-]+)\b',
            r'\b(Claude[\s\w\-\.]+)\b',
            r'\b(Gemini[\s\w\-\.]+)\b',
            r'\b(Llama[\s\w\-\.]+)\b',
            r'\b(Mistral[\s\w\-\.]+)\b',
            r'\b(Mixtral[\s\w\-\.]+)\b',
            r'\b(Qwen[\s\w\-\.]+)\b',
        ]
        
        import re
        for pattern in model_patterns:
            match = re.search(pattern, context, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return None
    
    def add_benchmark_to_model(self, model_id: int, benchmark_name: str, 
                               score: float, metric: str = "score") -> bool:
        """Add a benchmark score to an existing model."""
        try:
            # First get the model to see existing benchmarks
            response = requests.get(
                f"{self.api_base_url}/api/models/{model_id}",
                timeout=10
            )
            response.raise_for_status()
            model = response.json()
            
            # Update benchmarks
            benchmarks = model.get("benchmarks", {}).copy()
            benchmarks[benchmark_name] = score
            
            # Update the model
            response = requests.put(
                f"{self.api_base_url}/api/models/{model_id}",
                json={"benchmarks": benchmarks},
                timeout=10
            )
            response.raise_for_status()
            return True
            
        except requests.RequestException as e:
            error_msg = f"Failed to add benchmark to model {model_id}: {e}"
            if hasattr(e, 'response') and e.response:
                error_msg += f" - {e.response.text}"
            self.stats["errors"].append(error_msg)
            return False
    
    def process_extraction(self, extraction: Dict, dry_run: bool = False):
        """Process a single benchmark extraction."""
        self.stats["total_extractions"] += 1
        
        # Skip if no score
        if extraction.get("score") is None:
            self.stats["skipped"] += 1
            logger.debug(f"Skipping extraction: no score available")
            return
        
        # Try to find associated model
        model_name = self.extract_model_from_context(extraction)
        
        if not model_name:
            self.stats["skipped"] += 1
            logger.debug(f"Skipping extraction: could not identify model from context")
            return
        
        # Find the model in database
        model = self.find_model_by_name(model_name)
        
        if not model:
            self.stats["skipped"] += 1
            logger.debug(f"Skipping extraction: model '{model_name}' not found in database")
            return
        
        self.stats["linked_to_models"] += 1
        
        # Prepare benchmark data
        benchmark_name = extraction["benchmark"]
        score = extraction["score"]
        metric = extraction.get("metric", "score")
        
        if dry_run:
            logger.info(f"[DRY RUN] Would add benchmark '{benchmark_name}'={score} to '{model['name']}'")
            return
        
        # Check if this benchmark already exists for the model
        existing_benchmarks = model.get("benchmarks", {})
        if benchmark_name in existing_benchmarks:
            logger.debug(f"Benchmark '{benchmark_name}' already exists for '{model['name']}'")
        
        # Add benchmark to model
        logger.info(f"Adding benchmark '{benchmark_name}'={score} to '{model['name']}'")
        success = self.add_benchmark_to_model(
            model["id"], benchmark_name, score, metric
        )
        
        if success:
            self.stats["new_benchmarks_added"] += 1
        else:
            self.stats["failed"] += 1
    
    def ingest_data(self, data: Dict, dry_run: bool = False) -> Dict:
        """Ingest all benchmark extractions from the data."""
        extractions = data.get("extractions", [])
        logger.info(f"Starting ingestion of {len(extractions)} benchmark extractions...")
        
        # Pre-fetch all models for better matching
        all_models = self.get_all_models()
        for model in all_models:
            self.model_cache[model["name"]] = model
        
        # Process each extraction
        for extraction in extractions:
            self.process_extraction(extraction, dry_run)
        
        return self.stats
    
    def print_summary(self):
        """Print ingestion summary."""
        print("\n" + "=" * 60)
        print("BENCHMARK INGESTION SUMMARY")
        print("=" * 60)
        print(f"  Total extractions processed: {self.stats['total_extractions']}")
        print(f"  Linked to models: {self.stats['linked_to_models']}")
        print(f"  New benchmarks added: {self.stats['new_benchmarks_added']}")
        print(f"  Skipped: {self.stats['skipped']}")
        print(f"  Failed: {self.stats['failed']}")
        
        if self.stats["errors"]:
            print(f"\n  Errors ({len(self.stats['errors'])}):")
            for error in self.stats["errors"][:5]:
                print(f"    - {error}")
            if len(self.stats["errors"]) > 5:
                print(f"    ... and {len(self.stats['errors']) - 5} more")
        
        print("=" * 60)


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Ingest benchmark scores")
    parser.add_argument(
        "--input", "-i",
        default=str(script_dir / "data" / "processed" / "benchmark_scores.json"),
        help="Path to benchmark_scores.json"
    )
    parser.add_argument(
        "--api-url", "-u",
        default="http://localhost:8000",
        help="Base URL of the API"
    )
    parser.add_argument(
        "--dry-run", "-d",
        action="store_true",
        help="Show what would be done without making changes"
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip data validation"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Create ingester
    ingester = BenchmarkIngester(api_base_url=args.api_url)
    
    # Load data
    data = ingester.load_data(Path(args.input))
    if not data:
        sys.exit(1)
    
    # Validate data
    if not args.skip_validation:
        if not ingester.validate_data(data):
            logger.error("Data validation failed. Use --skip-validation to proceed anyway.")
            sys.exit(1)
    
    # Ingest data
    stats = ingester.ingest_data(data, dry_run=args.dry_run)
    
    # Print summary
    ingester.print_summary()
    
    # Exit with appropriate code
    if stats["failed"] > 0:
        sys.exit(1)
    elif stats["new_benchmarks_added"] > 0:
        logger.info("✓ Benchmark ingestion completed successfully")
        sys.exit(0)
    else:
        logger.info("No new benchmarks added")
        sys.exit(0)


if __name__ == "__main__":
    main()
