#!/usr/bin/env python3
"""
Lab data ingestion script for the pipeline.

Ingests lab announcement data from lab_announcements.json into the database.
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import requests

# Add src to path for database imports
script_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(script_dir))

from scripts.pipeline.validate_data import DataValidator

logger = logging.getLogger(__name__)


class LabDataIngester:
    """Ingests lab announcement data into the database."""
    
    def __init__(self, api_base_url: str = "http://localhost:8000"):
        self.api_base_url = api_base_url
        self.stats = {
            "total": 0,
            "created": 0,
            "updated": 0,
            "skipped": 0,
            "failed": 0,
            "errors": []
        }
    
    def load_data(self, file_path: Path) -> Optional[Dict]:
        """Load lab announcements data from JSON file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logger.info(f"Loaded {data.get('total_models', 0)} models from {file_path}")
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
        is_valid, errors, warnings = validator.validate_lab_announcements(data)
        
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
    
    def transform_model(self, model: Dict, lab_name: str) -> Dict:
        """Transform lab announcement model to API format."""
        # Extract parameters from model name if available
        params = self._extract_parameters(model["name"])
        
        # Extract context window from key_features if mentioned
        context = self._extract_context_window(model.get("key_features", ""))
        
        # Build tags from key_features
        tags = []
        key_features = model.get("key_features", "")
        if key_features:
            # Split by comma and clean up
            for feature in key_features.split(","):
                feature = feature.strip().lower()
                if feature:
                    tags.append(feature)
        
        # Transform benchmarks
        benchmarks = {}
        for bench_name, score in model.get("benchmark_claims", {}).items():
            benchmarks[bench_name.lower()] = float(score)
        
        return {
            "name": model["name"],
            "lab": lab_name,
            "release_date": model["announcement_date"],
            "architecture": model["architecture"],
            "parameters": params if params else "unknown",
            "context_window": context if context else "unknown",
            "paper_url": "",  # Lab announcements don't have paper URLs
            "announcement_url": model["url"],
            "benchmarks": benchmarks,
            "tags": tags
        }
    
    def _extract_parameters(self, model_name: str) -> Optional[float]:
        """Try to extract parameter count from model name."""
        import re
        
        # Look for patterns like "7B", "70B", "405B"
        patterns = [
            r'(\d+(?:\.\d+)?)\s*B',  # e.g., "7B", "70B"
            r'(\d+(?:\.\d+)?)\s*billion',  # e.g., "7 billion"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, model_name, re.IGNORECASE)
            if match:
                try:
                    return float(match.group(1))
                except ValueError:
                    pass
        
        return None
    
    def _extract_context_window(self, key_features: str) -> Optional[int]:
        """Try to extract context window from key features."""
        import re
        
        # Look for patterns like "128K context", "32K context"
        match = re.search(r'(\d+)\s*[Kk]\s*context', key_features)
        if match:
            try:
                # Convert K to actual number
                return int(match.group(1)) * 1000
            except ValueError:
                pass
        
        # Look for patterns like "8K", "32K"
        match = re.search(r'(\d+)\s*[Kk]\b', key_features)
        if match:
            try:
                return int(match.group(1)) * 1000
            except ValueError:
                pass
        
        return None
    
    def check_model_exists(self, name: str) -> Optional[Dict]:
        """Check if a model already exists in the database."""
        try:
            response = requests.get(
                f"{self.api_base_url}/api/models/search",
                params={"q": name, "page_size": 10},
                timeout=10
            )
            response.raise_for_status()
            results = response.json()
            
            # Look for exact match
            for model in results.get("items", []):
                if model["name"].lower() == name.lower():
                    return model
            
            return None
        except requests.RequestException as e:
            logger.warning(f"Could not check for existing model '{name}': {e}")
            return None
    
    def create_model(self, model_data: Dict) -> Tuple[bool, Optional[Dict]]:
        """Create a new model via API."""
        try:
            response = requests.post(
                f"{self.api_base_url}/api/models",
                json=model_data,
                timeout=10
            )
            response.raise_for_status()
            return True, response.json()
        except requests.RequestException as e:
            error_msg = f"Failed to create model '{model_data['name']}': {e}"
            if hasattr(e.response, 'text'):
                error_msg += f" - {e.response.text}"
            self.stats["errors"].append(error_msg)
            return False, None
    
    def update_model(self, model_id: int, model_data: Dict) -> Tuple[bool, Optional[Dict]]:
        """Update an existing model via API."""
        try:
            response = requests.put(
                f"{self.api_base_url}/api/models/{model_id}",
                json=model_data,
                timeout=10
            )
            response.raise_for_status()
            return True, response.json()
        except requests.RequestException as e:
            error_msg = f"Failed to update model '{model_data['name']}' (ID: {model_id}): {e}"
            self.stats["errors"].append(error_msg)
            return False, None
    
    def ingest_model(self, model: Dict, lab_name: str, dry_run: bool = False):
        """Ingest a single model."""
        self.stats["total"] += 1
        
        # Transform to API format
        model_data = self.transform_model(model, lab_name)
        
        # Check if model exists
        existing = self.check_model_exists(model_data["name"])
        
        if dry_run:
            action = "UPDATE" if existing else "CREATE"
            logger.info(f"[DRY RUN] Would {action}: {model_data['name']} ({lab_name})")
            return
        
        if existing:
            # Update existing model
            logger.info(f"Updating existing model: {model_data['name']}")
            success, _ = self.update_model(existing["id"], model_data)
            if success:
                self.stats["updated"] += 1
            else:
                self.stats["failed"] += 1
        else:
            # Create new model
            logger.info(f"Creating new model: {model_data['name']}")
            success, _ = self.create_model(model_data)
            if success:
                self.stats["created"] += 1
            else:
                self.stats["failed"] += 1
    
    def ingest_data(self, data: Dict, dry_run: bool = False) -> Dict:
        """Ingest all models from the data."""
        logger.info(f"Starting ingestion of {data.get('total_models', 0)} models...")
        
        for lab_data in data.get("labs", []):
            lab_name = lab_data.get("lab", "Unknown")
            models = lab_data.get("models", [])
            
            logger.info(f"Processing lab: {lab_name} ({len(models)} models)")
            
            for model in models:
                self.ingest_model(model, lab_name, dry_run)
        
        return self.stats
    
    def print_summary(self):
        """Print ingestion summary."""
        print("\n" + "=" * 60)
        print("INGESTION SUMMARY")
        print("=" * 60)
        print(f"  Total models processed: {self.stats['total']}")
        print(f"  Created: {self.stats['created']}")
        print(f"  Updated: {self.stats['updated']}")
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
    
    parser = argparse.ArgumentParser(description="Ingest lab announcement data")
    parser.add_argument(
        "--input", "-i",
        default=str(script_dir / "data" / "raw" / "lab_announcements.json"),
        help="Path to lab_announcements.json"
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
    ingester = LabDataIngester(api_base_url=args.api_url)
    
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
    elif stats["created"] > 0 or stats["updated"] > 0:
        logger.info("✓ Ingestion completed successfully")
        sys.exit(0)
    else:
        logger.info("No changes made")
        sys.exit(0)


if __name__ == "__main__":
    main()
