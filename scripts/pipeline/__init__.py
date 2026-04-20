"""
Data Pipeline module for automated ingestion.

This module provides tools for:
- Data validation before ingestion
- Lab announcement data ingestion
- Benchmark scores ingestion
- Automated scheduling
"""

__version__ = "1.0.0"
__all__ = [
    "DataValidator",
    "LabDataIngester",
    "BenchmarkIngester",
    "PipelineScheduler",
]
