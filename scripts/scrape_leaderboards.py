#!/usr/bin/env python3
"""
Scraping script for benchmark leaderboards.

This script scrapes data from:
1. Hugging Face Open LLM Leaderboard
2. Papers with Code (MMLU, HumanEval, GPQA benchmarks)

Usage:
    python scrape_leaderboards.py [--output-dir DIR]

Requirements:
    - requests
    - beautifulsoup4
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: Required packages not installed.")
    print("Install with: pip install requests beautifulsoup4")
    sys.exit(1)


class LeaderboardScraper:
    """Scraper for LLM benchmark leaderboards."""
    
    def __init__(self, output_dir: str = "data/raw/leaderboards"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        })
    
    def scrape_hf_leaderboard(self) -> dict:
        """
        Scrape Hugging Face Open LLM Leaderboard.
        
        Returns:
            dict: Leaderboard data with metadata
        """
        url = "https://open-llm-leaderboard-open-llm-leaderboard.hf.space/api/leaderboard"
        
        try:
            response = self.session.get(url, timeout=60)
            response.raise_for_status()
            data = response.json()
            
            # Sort by average score and get top 100
            sorted_data = sorted(data, key=lambda x: x.get('Average ⬆️', 0), reverse=True)
            top_100 = []
            
            for i, model in enumerate(sorted_data[:100]):
                clean_model = {
                    'rank': i + 1,
                    'model_name': model.get('fullname', ''),
                    'model_type': model.get('Type', ''),
                    'architecture': model.get('Architecture', ''),
                    'parameters_billions': model.get('#Params (B)', None),
                    'average_score': model.get('Average ⬆️', None),
                    'ifeval_score': model.get('IFEval', None),
                    'bbh_score': model.get('BBH', None),
                    'math_lvl5_score': model.get('MATH Lvl 5', None),
                    'gpqa_score': model.get('GPQA', None),
                    'musr_score': model.get('MUSR', None),
                    'mmlu_pro_score': model.get('MMLU-PRO', None),
                    'hub_license': model.get('Hub License', ''),
                    'hub_likes': model.get('Hub ❤️', 0),
                    'is_moe': model.get('MoE', False),
                    'submission_date': model.get('Submission Date', ''),
                    'precision': model.get('Precision', ''),
                    'weight_type': model.get('Weight type', ''),
                    'official_provider': model.get('Official Providers', False)
                }
                top_100.append(clean_model)
            
            return {
                'source': 'Hugging Face Open LLM Leaderboard',
                'url': 'https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard',
                'scraped_at': datetime.now().isoformat(),
                'total_models': len(data),
                'top_100_models': top_100
            }
            
        except Exception as e:
            print(f"Error scraping HF leaderboard: {e}")
            return None
    
    def scrape_paperswithcode_benchmark(self, benchmark: str) -> dict:
        """
        Scrape Papers with Code benchmark data.
        
        Args:
            benchmark: Benchmark name (mmlu, humaneval, gpqa)
            
        Returns:
            dict: Benchmark data with metadata
        """
        # Papers with Code API endpoints
        benchmark_urls = {
            'mmlu': 'https://paperswithcode.com/sota/multi-task-language-understanding-on-mmlu',
            'humaneval': 'https://paperswithcode.com/sota/code-generation-on-humaneval',
            'gpqa': 'https://paperswithcode.com/sota/question-answering-on-gpqa'
        }
        
        url = benchmark_urls.get(benchmark)
        if not url:
            print(f"Unknown benchmark: {benchmark}")
            return None
        
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract leaderboard table
            # Note: Papers with Code uses JavaScript-rendered tables
            # This is a basic implementation that may need Selenium for full scraping
            models = []
            
            # Try to find table data
            tables = soup.find_all('table')
            for table in tables:
                rows = table.find_all('tr')[1:]  # Skip header
                for i, row in enumerate(rows[:50]):  # Top 50
                    cells = row.find_all('td')
                    if len(cells) >= 3:
                        model = {
                            'rank': i + 1,
                            'model_name': cells[0].get_text(strip=True),
                            'score': cells[1].get_text(strip=True),
                            'paper_url': cells[0].find('a', href=True)['href'] if cells[0].find('a') else None
                        }
                        models.append(model)
            
            return {
                'source': f'Papers with Code - {benchmark.upper()}',
                'url': url,
                'scraped_at': datetime.now().isoformat(),
                'models': models
            }
            
        except Exception as e:
            print(f"Error scraping {benchmark}: {e}")
            return None
    
    def save_data(self, data: dict, filename: str):
        """Save scraped data to JSON file."""
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved data to {filepath}")
    
    def run(self):
        """Run all scrapers."""
        print("Starting leaderboard scraping...")
        
        # Scrape HF Open LLM Leaderboard
        print("\nScraping Hugging Face Open LLM Leaderboard...")
        hf_data = self.scrape_hf_leaderboard()
        if hf_data:
            self.save_data(hf_data, 'hf_leaderboard_top100.json')
            print(f"  - Found {hf_data['total_models']} total models")
            print(f"  - Extracted top 100 models")
        
        # Scrape Papers with Code benchmarks
        benchmarks = ['mmlu', 'humaneval', 'gpqa']
        for benchmark in benchmarks:
            print(f"\nScraping Papers with Code - {benchmark.upper()}...")
            data = self.scrape_paperswithcode_benchmark(benchmark)
            if data:
                self.save_data(data, f'paperswithcode_{benchmark}.json')
                print(f"  - Found {len(data['models'])} models")
        
        print("\nScraping complete!")


def main():
    parser = argparse.ArgumentParser(
        description='Scrape LLM benchmark leaderboards'
    )
    parser.add_argument(
        '--output-dir',
        default='data/raw/leaderboards',
        help='Output directory for scraped data'
    )
    
    args = parser.parse_args()
    
    scraper = LeaderboardScraper(output_dir=args.output_dir)
    scraper.run()


if __name__ == '__main__':
    main()
