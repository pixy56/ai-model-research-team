#!/usr/bin/env python3
"""
Pipeline scheduler for automated data ingestion.

Supports both cron-based scheduling and manual triggering.
"""

import json
import logging
import os
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class PipelineScheduler:
    """Schedules and runs the data pipeline."""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path(__file__).parent / "scheduler_config.json"
        self.config = self._load_config()
        self.run_history: List[Dict] = []
        self.pipeline_dir = Path(__file__).parent
    
    def _load_config(self) -> Dict:
        """Load scheduler configuration."""
        default_config = {
            "schedule": {
                "enabled": True,
                "frequency": "weekly",
                "day_of_week": 0,  # 0=Monday, 6=Sunday
                "hour": 2,
                "minute": 0
            },
            "pipeline": {
                "validate_before_ingest": True,
                "dry_run_first": False,
                "stop_on_error": True,
                "api_base_url": "http://localhost:8000"
            },
            "notifications": {
                "enabled": False,
                "on_success": True,
                "on_failure": True,
                "webhook_url": None
            },
            "data_sources": {
                "lab_announcements": "data/raw/lab_announcements.json",
                "benchmark_scores": "data/processed/benchmark_scores.json"
            },
            "last_run": None,
            "next_run": None
        }
        
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults
                    for key, value in default_config.items():
                        if key not in loaded_config:
                            loaded_config[key] = value
                        elif isinstance(value, dict):
                            for subkey, subvalue in value.items():
                                if subkey not in loaded_config[key]:
                                    loaded_config[key][subkey] = subvalue
                    return loaded_config
            except (json.JSONDecodeError, IOError) as e:
                logger.warning(f"Could not load config: {e}. Using defaults.")
        
        return default_config
    
    def _save_config(self):
        """Save scheduler configuration."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(self.config, f, indent=2)
        except IOError as e:
            logger.error(f"Could not save config: {e}")
    
    def _run_script(self, script_name: str, args: List[str] = None) -> tuple[bool, str]:
        """Run a pipeline script and return success status and output."""
        script_path = self.pipeline_dir / script_name
        
        if not script_path.exists():
            logger.error(f"Script not found: {script_path}")
            return False, f"Script not found: {script_path}"
        
        cmd = [sys.executable, str(script_path)]
        if args:
            cmd.extend(args)
        
        logger.info(f"Running: {' '.join(cmd)}")
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            output = result.stdout + result.stderr
            success = result.returncode == 0
            
            if not success:
                logger.error(f"Script failed with code {result.returncode}")
                logger.error(f"Output: {output[:500]}")
            
            return success, output
            
        except subprocess.TimeoutExpired:
            logger.error(f"Script timed out after 5 minutes")
            return False, "Timeout"
        except Exception as e:
            logger.error(f"Failed to run script: {e}")
            return False, str(e)
    
    def run_validation(self, data_type: str = "all") -> bool:
        """Run data validation step."""
        logger.info(f"Running validation for: {data_type}")
        
        all_passed = True
        
        if data_type in ("all", "lab"):
            lab_file = self.config["data_sources"]["lab_announcements"]
            success, output = self._run_script(
                "validate_data.py",
                ["--type", "lab", str(self.pipeline_dir.parent.parent / lab_file)]
            )
            if not success:
                logger.error("Lab data validation failed")
                all_passed = False
            else:
                logger.info("✓ Lab data validation passed")
        
        if data_type in ("all", "benchmark"):
            bench_file = self.config["data_sources"]["benchmark_scores"]
            success, output = self._run_script(
                "validate_data.py",
                ["--type", "benchmark", str(self.pipeline_dir.parent.parent / bench_file)]
            )
            if not success:
                logger.error("Benchmark data validation failed")
                all_passed = False
            else:
                logger.info("✓ Benchmark data validation passed")
        
        return all_passed
    
    def run_ingestion(self, dry_run: bool = False) -> bool:
        """Run data ingestion step."""
        logger.info(f"Running ingestion (dry_run={dry_run})")
        
        all_passed = True
        api_url = self.config["pipeline"]["api_base_url"]
        
        # Ingest lab data
        lab_file = self.config["data_sources"]["lab_announcements"]
        success, output = self._run_script(
            "ingest_lab_data.py",
            ["--input", str(self.pipeline_dir.parent.parent / lab_file),
             "--api-url", api_url] +
            (["--dry-run"] if dry_run else [])
        )
        
        if not success:
            logger.error("Lab data ingestion failed")
            if self.config["pipeline"]["stop_on_error"]:
                return False
            all_passed = False
        else:
            logger.info("✓ Lab data ingestion completed")
        
        # Ingest benchmark data
        bench_file = self.config["data_sources"]["benchmark_scores"]
        success, output = self._run_script(
            "ingest_benchmarks.py",
            ["--input", str(self.pipeline_dir.parent.parent / bench_file),
             "--api-url", api_url] +
            (["--dry-run"] if dry_run else [])
        )
        
        if not success:
            logger.error("Benchmark data ingestion failed")
            all_passed = False
        else:
            logger.info("✓ Benchmark data ingestion completed")
        
        return all_passed
    
    def run_pipeline(self, dry_run: bool = False, skip_validation: bool = False) -> Dict:
        """Run the complete pipeline."""
        start_time = datetime.now()
        run_record = {
            "started_at": start_time.isoformat(),
            "status": "running",
            "steps": []
        }
        
        logger.info("=" * 60)
        logger.info("STARTING PIPELINE RUN")
        logger.info("=" * 60)
        
        try:
            # Step 1: Validation
            if not skip_validation and self.config["pipeline"]["validate_before_ingest"]:
                validation_passed = self.run_validation()
                run_record["steps"].append({
                    "name": "validation",
                    "status": "passed" if validation_passed else "failed",
                    "timestamp": datetime.now().isoformat()
                })
                
                if not validation_passed:
                    run_record["status"] = "failed"
                    run_record["error"] = "Validation failed"
                    return run_record
            
            # Step 2: Ingestion
            ingestion_passed = self.run_ingestion(dry_run=dry_run)
            run_record["steps"].append({
                "name": "ingestion",
                "status": "passed" if ingestion_passed else "failed",
                "timestamp": datetime.now().isoformat()
            })
            
            if not ingestion_passed:
                run_record["status"] = "failed"
                run_record["error"] = "Ingestion failed"
            else:
                run_record["status"] = "completed"
            
        except Exception as e:
            logger.exception("Pipeline failed with exception")
            run_record["status"] = "failed"
            run_record["error"] = str(e)
        
        finally:
            end_time = datetime.now()
            run_record["completed_at"] = end_time.isoformat()
            run_record["duration_seconds"] = (end_time - start_time).total_seconds()
            
            # Update config
            self.config["last_run"] = start_time.isoformat()
            self._calculate_next_run()
            self._save_config()
            
            # Add to history
            self.run_history.append(run_record)
            
            logger.info("=" * 60)
            logger.info(f"PIPELINE COMPLETE: {run_record['status']}")
            logger.info(f"Duration: {run_record['duration_seconds']:.1f}s")
            logger.info("=" * 60)
        
        return run_record
    
    def _calculate_next_run(self):
        """Calculate the next scheduled run time."""
        schedule = self.config["schedule"]
        
        if not schedule["enabled"]:
            self.config["next_run"] = None
            return
        
        now = datetime.now()
        
        if schedule["frequency"] == "weekly":
            # Find next occurrence of the specified day
            days_ahead = schedule["day_of_week"] - now.weekday()
            if days_ahead <= 0:  # Target day already happened this week
                days_ahead += 7
            
            next_run = now + timedelta(days=days_ahead)
            next_run = next_run.replace(
                hour=schedule["hour"],
                minute=schedule["minute"],
                second=0,
                microsecond=0
            )
            
            self.config["next_run"] = next_run.isoformat()
        
        elif schedule["frequency"] == "daily":
            next_run = now + timedelta(days=1)
            next_run = next_run.replace(
                hour=schedule["hour"],
                minute=schedule["minute"],
                second=0,
                microsecond=0
            )
            self.config["next_run"] = next_run.isoformat()
        
        else:
            self.config["next_run"] = None
    
    def health_check(self) -> Dict:
        """Perform health check on the pipeline."""
        health = {
            "status": "healthy",
            "checks": {}
        }
        
        # Check API availability
        import requests
        try:
            response = requests.get(
                f"{self.config['pipeline']['api_base_url']}/health",
                timeout=5
            )
            health["checks"]["api"] = "healthy" if response.status_code == 200 else "unhealthy"
        except Exception as e:
            health["checks"]["api"] = f"unhealthy: {e}"
            health["status"] = "degraded"
        
        # Check data files exist
        for name, path in self.config["data_sources"].items():
            full_path = self.pipeline_dir.parent.parent / path
            health["checks"][f"data_{name}"] = "exists" if full_path.exists() else "missing"
            if not full_path.exists():
                health["status"] = "degraded"
        
        # Check last run status
        last_run = self.config.get("last_run")
        if last_run:
            health["checks"]["last_run"] = last_run
        
        next_run = self.config.get("next_run")
        if next_run:
            health["checks"]["next_run"] = next_run
        
        return health
    
    def print_status(self):
        """Print current scheduler status."""
        print("\n" + "=" * 60)
        print("PIPELINE SCHEDULER STATUS")
        print("=" * 60)
        
        print("\nConfiguration:")
        print(f"  Schedule enabled: {self.config['schedule']['enabled']}")
        print(f"  Frequency: {self.config['schedule']['frequency']}")
        
        if self.config["schedule"]["frequency"] == "weekly":
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", 
                    "Friday", "Saturday", "Sunday"]
            day = days[self.config["schedule"]["day_of_week"]]
            print(f"  Day: {day}")
        
        print(f"  Time: {self.config['schedule']['hour']:02d}:{self.config['schedule']['minute']:02d}")
        
        print("\nPipeline Settings:")
        print(f"  Validate before ingest: {self.config['pipeline']['validate_before_ingest']}")
        print(f"  Stop on error: {self.config['pipeline']['stop_on_error']}")
        print(f"  API URL: {self.config['pipeline']['api_base_url']}")
        
        print("\nRun History:")
        last_run = self.config.get("last_run")
        if last_run:
            print(f"  Last run: {last_run}")
        else:
            print("  Last run: Never")
        
        next_run = self.config.get("next_run")
        if next_run:
            print(f"  Next scheduled: {next_run}")
        else:
            print("  Next scheduled: Not scheduled")
        
        # Health check
        health = self.health_check()
        print("\nHealth Check:")
        print(f"  Overall status: {health['status']}")
        for check, status in health["checks"].items():
            print(f"  {check}: {status}")
        
        print("=" * 60)


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Pipeline scheduler")
    parser.add_argument(
        "action",
        choices=["run", "dry-run", "status", "health", "enable", "disable"],
        help="Action to perform"
    )
    parser.add_argument(
        "--skip-validation",
        action="store_true",
        help="Skip validation step"
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
    
    # Create scheduler
    scheduler = PipelineScheduler()
    
    if args.action == "run":
        result = scheduler.run_pipeline(
            dry_run=False,
            skip_validation=args.skip_validation
        )
        sys.exit(0 if result["status"] == "completed" else 1)
    
    elif args.action == "dry-run":
        result = scheduler.run_pipeline(
            dry_run=True,
            skip_validation=args.skip_validation
        )
        sys.exit(0 if result["status"] in ("completed", "failed") else 1)
    
    elif args.action == "status":
        scheduler.print_status()
    
    elif args.action == "health":
        health = scheduler.health_check()
        print(json.dumps(health, indent=2))
        sys.exit(0 if health["status"] == "healthy" else 1)
    
    elif args.action == "enable":
        scheduler.config["schedule"]["enabled"] = True
        scheduler._calculate_next_run()
        scheduler._save_config()
        logger.info("Scheduler enabled")
        scheduler.print_status()
    
    elif args.action == "disable":
        scheduler.config["schedule"]["enabled"] = False
        scheduler.config["next_run"] = None
        scheduler._save_config()
        logger.info("Scheduler disabled")
        scheduler.print_status()


if __name__ == "__main__":
    main()
