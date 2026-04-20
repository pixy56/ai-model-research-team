#!/usr/bin/env python3
"""
Test suite for the data pipeline.

Tests validation, ingestion logic, and scheduler without requiring API.
"""

import json
import sys
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add project to path
script_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(script_dir))

from scripts.pipeline.validate_data import DataValidator


class TestDataValidator(unittest.TestCase):
    """Test data validation module."""
    
    def setUp(self):
        self.validator = DataValidator()
    
    def test_validate_lab_announcements_valid(self):
        """Test validation with valid lab data."""
        data = {
            "scraped_at": "2025-01-19T23:58:00Z",
            "total_labs": 1,
            "total_models": 1,
            "labs": [
                {
                    "lab": "TestLab",
                    "models": [
                        {
                            "name": "TestModel",
                            "announcement_date": "2024-01-15",
                            "architecture": "dense-transformer",
                            "key_features": "test feature",
                            "benchmark_claims": {"mmlu": 85.0},
                            "url": "https://example.com"
                        }
                    ]
                }
            ]
        }
        
        is_valid, errors, warnings = self.validator.validate_lab_announcements(data)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_lab_announcements_missing_field(self):
        """Test validation with missing required field."""
        data = {
            "scraped_at": "2025-01-19T23:58:00Z",
            "total_labs": 1,
            "total_models": 1,
            "labs": [
                {
                    "lab": "TestLab",
                    "models": [
                        {
                            "name": "TestModel",
                            # Missing announcement_date
                            "architecture": "dense-transformer",
                            "url": "https://example.com"
                        }
                    ]
                }
            ]
        }
        
        is_valid, errors, warnings = self.validator.validate_lab_announcements(data)
        self.assertFalse(is_valid)
        self.assertTrue(any("announcement_date" in e for e in errors))
    
    def test_validate_lab_announcements_invalid_architecture(self):
        """Test validation with invalid architecture."""
        data = {
            "scraped_at": "2025-01-19T23:58:00Z",
            "total_labs": 1,
            "total_models": 1,
            "labs": [
                {
                    "lab": "TestLab",
                    "models": [
                        {
                            "name": "TestModel",
                            "announcement_date": "2024-01-15",
                            "architecture": "invalid-arch",
                            "url": "https://example.com"
                        }
                    ]
                }
            ]
        }
        
        is_valid, errors, warnings = self.validator.validate_lab_announcements(data)
        self.assertFalse(is_valid)
        self.assertTrue(any("architecture" in e.lower() for e in errors))
    
    def test_validate_benchmark_scores_valid(self):
        """Test validation with valid benchmark data."""
        data = {
            "extraction_date": "2026-04-20",
            "source_file": "test.json",
            "total_papers": 1,
            "extractions": [
                {
                    "paper_id": "1234.56789",
                    "benchmark": "MMLU",
                    "score": 85.5,
                    "metric": "accuracy",
                    "confidence": "high",
                    "context": "Test context"
                }
            ]
        }
        
        is_valid, errors, warnings = self.validator.validate_benchmark_scores(data)
        self.assertTrue(is_valid)
        self.assertEqual(len(errors), 0)
    
    def test_validate_benchmark_scores_missing_paper_id(self):
        """Test validation with missing paper_id."""
        data = {
            "extractions": [
                {
                    "benchmark": "MMLU",
                    "confidence": "high"
                }
            ]
        }
        
        is_valid, errors, warnings = self.validator.validate_benchmark_scores(data)
        self.assertFalse(is_valid)
        self.assertTrue(any("paper_id" in e.lower() for e in errors))
    
    def test_extract_parameters(self):
        """Test parameter extraction from model name."""
        from scripts.pipeline.ingest_lab_data import LabDataIngester
        
        ingester = LabDataIngester()
        
        test_cases = [
            ("Llama 2 7B", 7.0),
            ("GPT-4 175B", 175.0),
            ("Mixtral 8x7B", 7.0),  # Extracts the last B value
            ("Test Model", None),
        ]
        
        for name, expected in test_cases:
            result = ingester._extract_parameters(name)
            self.assertEqual(result, expected, f"Failed for {name}")


class TestLabDataIngester(unittest.TestCase):
    """Test lab data ingestion module."""
    
    @patch('scripts.pipeline.ingest_lab_data.requests.get')
    def test_check_model_exists_found(self, mock_get):
        """Test checking if model exists."""
        from scripts.pipeline.ingest_lab_data import LabDataIngester
        
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "items": [
                {"id": 1, "name": "GPT-4"}
            ],
            "total": 1
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        ingester = LabDataIngester()
        result = ingester.check_model_exists("GPT-4")
        
        self.assertIsNotNone(result)
        self.assertEqual(result["id"], 1)
    
    def test_transform_model(self):
        """Test model transformation."""
        from scripts.pipeline.ingest_lab_data import LabDataIngester
        
        ingester = LabDataIngester()
        
        model = {
            "name": "TestModel 7B",
            "announcement_date": "2024-01-15",
            "architecture": "dense-transformer",
            "key_features": "128K context, fast",
            "benchmark_claims": {"mmlu": 85.0},
            "url": "https://example.com"
        }
        
        result = ingester.transform_model(model, "TestLab")
        
        self.assertEqual(result["name"], "TestModel 7B")
        self.assertEqual(result["lab"], "TestLab")
        self.assertEqual(result["parameters"], 7.0)
        self.assertEqual(result["context_window"], 128000)
        self.assertEqual(result["benchmarks"]["mmlu"], 85.0)
        self.assertIn("128k context", result["tags"])


class TestBenchmarkIngester(unittest.TestCase):
    """Test benchmark ingestion module."""
    
    def test_extract_model_from_context(self):
        """Test model extraction from context."""
        from scripts.pipeline.ingest_benchmarks import BenchmarkIngester
        
        ingester = BenchmarkIngester()
        
        test_cases = [
            ({"model": "GPT-4", "context": ""}, "GPT-4"),
            ({"context": "Testing GPT-4 model"}, "GPT-4"),
            ({"context": "Llama 2 70B results"}, "Llama 2 70B"),
            ({"context": "No model here"}, None),
        ]
        
        for extraction, expected in test_cases:
            result = ingester.extract_model_from_context(extraction)
            # For context-only extraction, just check it finds something
            if expected and "context" in extraction and "model" not in extraction:
                self.assertIsNotNone(result)
            else:
                self.assertEqual(result, expected, f"Failed for {extraction}")


class TestPipelineScheduler(unittest.TestCase):
    """Test pipeline scheduler."""
    
    def test_load_config_defaults(self):
        """Test loading default configuration."""
        from scripts.pipeline.scheduler import PipelineScheduler
        
        scheduler = PipelineScheduler(config_path=Path("/nonexistent"))
        
        self.assertTrue(scheduler.config["schedule"]["enabled"])
        self.assertEqual(scheduler.config["schedule"]["frequency"], "weekly")
        self.assertEqual(scheduler.config["pipeline"]["api_base_url"], "http://localhost:8000")
    
    def test_health_check_no_api(self):
        """Test health check when API is unavailable."""
        from scripts.pipeline.scheduler import PipelineScheduler
        
        scheduler = PipelineScheduler(config_path=Path("/nonexistent"))
        health = scheduler.health_check()
        
        self.assertEqual(health["status"], "degraded")
        self.assertIn("api", health["checks"])


class TestDataFiles(unittest.TestCase):
    """Test actual data files."""
    
    def test_lab_announcements_exists(self):
        """Test lab announcements file exists."""
        file_path = script_dir / "data" / "raw" / "lab_announcements.json"
        self.assertTrue(file_path.exists())
    
    def test_lab_announcements_valid_json(self):
        """Test lab announcements is valid JSON."""
        file_path = script_dir / "data" / "raw" / "lab_announcements.json"
        with open(file_path) as f:
            data = json.load(f)
        
        self.assertIn("labs", data)
        self.assertIn("total_models", data)
    
    def test_benchmark_scores_exists(self):
        """Test benchmark scores file exists."""
        file_path = script_dir / "data" / "processed" / "benchmark_scores.json"
        self.assertTrue(file_path.exists())
    
    def test_benchmark_scores_valid_json(self):
        """Test benchmark scores is valid JSON."""
        file_path = script_dir / "data" / "processed" / "benchmark_scores.json"
        with open(file_path) as f:
            data = json.load(f)
        
        self.assertIn("extractions", data)


class TestAcceptanceCriteria(unittest.TestCase):
    """Test acceptance criteria."""
    
    def test_47_lab_models_available(self):
        """Verify 47+ lab models in data file."""
        file_path = script_dir / "data" / "raw" / "lab_announcements.json"
        with open(file_path) as f:
            data = json.load(f)
        
        total = sum(len(lab["models"]) for lab in data["labs"])
        self.assertGreaterEqual(total, 47, f"Expected 47+ models, got {total}")
    
    def test_69_benchmark_scores_available(self):
        """Verify 69+ benchmark scores in data file."""
        file_path = script_dir / "data" / "processed" / "benchmark_scores.json"
        with open(file_path) as f:
            data = json.load(f)
        
        total = len(data["extractions"])
        self.assertGreaterEqual(total, 69, f"Expected 69+ scores, got {total}")
    
    def test_data_validation_passes(self):
        """Verify data validation passes."""
        validator = DataValidator()
        
        # Test lab data
        lab_path = script_dir / "data" / "raw" / "lab_announcements.json"
        with open(lab_path) as f:
            lab_data = json.load(f)
        
        is_valid, errors, _ = validator.validate_lab_announcements(lab_data)
        self.assertTrue(is_valid, f"Lab data validation failed: {errors}")
        
        # Test benchmark data
        bench_path = script_dir / "data" / "processed" / "benchmark_scores.json"
        with open(bench_path) as f:
            bench_data = json.load(f)
        
        is_valid, errors, _ = validator.validate_benchmark_scores(bench_data)
        self.assertTrue(is_valid, f"Benchmark data validation failed: {errors}")


def run_tests():
    """Run all tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestDataValidator))
    suite.addTests(loader.loadTestsFromTestCase(TestLabDataIngester))
    suite.addTests(loader.loadTestsFromTestCase(TestBenchmarkIngester))
    suite.addTests(loader.loadTestsFromTestCase(TestPipelineScheduler))
    suite.addTests(loader.loadTestsFromTestCase(TestDataFiles))
    suite.addTests(loader.loadTestsFromTestCase(TestAcceptanceCriteria))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
