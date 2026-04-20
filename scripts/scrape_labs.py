#!/usr/bin/env python3
"""
Scrape lab announcement pages from major AI labs.
Extracts model announcements with metadata including:
- model name, release date, architecture hints, benchmark claims

Target labs:
- OpenAI (openai.com/blog)
- Anthropic (anthropic.com/news)
- Google DeepMind (deepmind.google)
- Meta AI (ai.meta.com)
- Mistral AI (mistral.ai/news)

Usage:
    python scrape_labs.py [--output PATH] [--delay SECONDS]

Output format:
    {
      "lab": "OpenAI",
      "models": [
        {
          "name": "GPT-4",
          "announcement_date": "2023-03-14",
          "architecture": "dense-transformer",
          "key_features": "multimodal, reasoning",
          "benchmark_claims": {"mmlu": 86.4},
          "url": "https://openai.com/blog/gpt-4"
        }
      ]
    }
"""

import argparse
import json
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# Constants
DEFAULT_DELAY = 2  # seconds between requests to respect rate limits
USER_AGENT = "AI-Model-Research-Team/1.0 (Research Project)"

# Lab configurations
LABS = {
    "OpenAI": {
        "base_url": "https://openai.com",
        "blog_path": "/blog",
        "article_selector": "article, .blog-post, [data-testid='post-card']",
        "title_selector": "h1, h2, h3, .post-title",
        "date_selector": "time, .date, [datetime]",
        "content_selector": ".prose, .post-content, article",
    },
    "Anthropic": {
        "base_url": "https://www.anthropic.com",
        "blog_path": "/news",
        "article_selector": "article, .news-item, .blog-post-card",
        "title_selector": "h1, h2, h3, .title",
        "date_selector": "time, .date, .published-date",
        "content_selector": ".content, .article-body, article",
    },
    "Google DeepMind": {
        "base_url": "https://deepmind.google",
        "blog_path": "/discover/blog",
        "article_selector": "article, .blog-card, .news-item",
        "title_selector": "h1, h2, h3, .heading",
        "date_selector": "time, .date",
        "content_selector": ".content, article",
    },
    "Meta AI": {
        "base_url": "https://ai.meta.com",
        "blog_path": "/blog",
        "article_selector": "article, .blog-post, .news-card",
        "title_selector": "h1, h2, h3, .title",
        "date_selector": "time, .date",
        "content_selector": ".content, article",
    },
    "Mistral AI": {
        "base_url": "https://mistral.ai",
        "blog_path": "/news",
        "article_selector": "article, .news-item, .blog-post",
        "title_selector": "h1, h2, h3, .post-title",
        "date_selector": "time, .date",
        "content_selector": ".content, .post-content, article",
    },
}

# Model name patterns
MODEL_PATTERNS = {
    "OpenAI": [
        r"GPT-4[\w\-]*",
        r"GPT-3[\w\-]*",
        r"o1[\w\-]*",
        r"o3[\w\-]*",
        r"DALL-E[\w\-]*",
        r"Sora[\w\-]*",
        r"Whisper[\w\-]*",
        r"Codex[\w\-]*",
        r"ChatGPT[\w\-]*",
    ],
    "Anthropic": [
        r"Claude[\w\-]*",
        r"Claude\s+\d+[\w\-]*",
    ],
    "Google DeepMind": [
        r"Gemini[\w\-]*",
        r"Gemini\s+\d+[\w\-]*",
        r"Imagen[\w\-]*",
        r"Veo[\w\-]*",
        r"Lyria[\w\-]*",
        r"Alpha[\w\-]*",
        r"Gemma[\w\-]*",
        r"PaLM[\w\-]*",
    ],
    "Meta AI": [
        r"Llama[\w\-]*",
        r"Llama\s+\d+[\w\-]*",
        r"Code[\s-]*Llama[\w\-]*",
        r"OPT[\w\-]*",
        r"Galactica[\w\-]*",
        r"SAM[\w\-]*",
        r"Audio[\s-]*Seal[\w\-]*",
    ],
    "Mistral AI": [
        r"Mixtral[\w\-]*",
        r"Mistral[\w\-]*",
        r"Mistral\s+\d+[\w\-]*",
        r"Codestral[\w\-]*",
        r"Mathstral[\w\-]*",
    ],
}

# Architecture keywords
ARCHITECTURE_KEYWORDS = {
    "dense-transformer": ["transformer", "dense", "decoder-only", "autoregressive"],
    "moe": ["mixture of experts", "moe", "sparse", "expert"],
    "ssm": ["state space", "mamba", "structured state", "ssm"],
    "multimodal": ["multimodal", "vision", "image", "audio", "video"],
    "reasoning": ["reasoning", "chain of thought", "test-time compute", "inference-time"],
    "other": ["diffusion", "flow matching", "state-based", "hybrid"],
}

# Benchmark patterns
BENCHMARK_PATTERNS = {
    "mmlu": r"MMLU[:\s]+(\d+\.?\d*)",
    "hellaswag": r"HellaSwag[:\s]+(\d+\.?\d*)",
    "humaneval": r"HumanEval[:\s]+(\d+\.?\d*)",
    "gpqa": r"GPQA[:\s]+(\d+\.?\d*)",
    "math": r"MATH[:\s]+(\d+\.?\d*)",
    "gsm8k": r"GSM8?K[:\s]+(\d+\.?\d*)",
    "arc": r"ARC(?:-C)?[:\s]+(\d+\.?\d*)",
    "drop": r"DROP[:\s]+(\d+\.?\d*)",
    "winogrande": r"WinoGrande[:\s]+(\d+\.?\d*)",
    "swe-bench": r"SWE-bench[:\s]+(\d+\.?\d*)",
    "mmmu": r"MMMU[:\s]+(\d+\.?\d*)",
    "mmbench": r"MMBench[:\s]+(\d+\.?\d*)",
}


class LabScraper:
    """Scraper for AI lab announcement pages."""

    def __init__(self, delay: float = DEFAULT_DELAY):
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
        })

    def _fetch(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch and parse a webpage with rate limiting."""
        try:
            print(f"  Fetching: {url}")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            time.sleep(self.delay)
            return BeautifulSoup(response.content, "html.parser")
        except requests.RequestException as e:
            print(f"  Error fetching {url}: {e}")
            return None

    def _extract_date(self, soup: BeautifulSoup, selectors: Dict) -> Optional[str]:
        """Extract date from page."""
        # Try time element first
        time_elem = soup.find("time")
        if time_elem:
            date_str = time_elem.get("datetime") or time_elem.get_text(strip=True)
            return self._parse_date(date_str)

        # Try other selectors
        for selector in selectors.get("date_selector", ",").split(","):
            elem = soup.select_one(selector.strip())
            if elem:
                return self._parse_date(elem.get_text(strip=True))
        return None

    def _parse_date(self, date_str: str) -> Optional[str]:
        """Parse various date formats to ISO 8601."""
        if not date_str:
            return None

        # Clean up the string
        date_str = date_str.strip()

        # Try various formats
        formats = [
            "%Y-%m-%d",
            "%B %d, %Y",
            "%b %d, %Y",
            "%d %B %Y",
            "%d %b %Y",
            "%m/%d/%Y",
            "%d/%m/%Y",
        ]

        for fmt in formats:
            try:
                parsed = datetime.strptime(date_str, fmt)
                return parsed.strftime("%Y-%m-%d")
            except ValueError:
                continue

        # Try to extract year-month-day pattern
        match = re.search(r'(\d{4})[-/](\d{1,2})[-/](\d{1,2})', date_str)
        if match:
            year, month, day = match.groups()
            return f"{year}-{int(month):02d}-{int(day):02d}"

        return None

    def _extract_model_name(self, title: str, content: str, lab: str) -> Optional[str]:
        """Extract model name from title and content."""
        patterns = MODEL_PATTERNS.get(lab, [])
        text = f"{title} {content}"

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(0).strip()

        return None

    def _extract_architecture(self, content: str) -> Optional[str]:
        """Extract architecture hints from content."""
        content_lower = content.lower()

        for arch, keywords in ARCHITECTURE_KEYWORDS.items():
            for keyword in keywords:
                if keyword in content_lower:
                    return arch

        return "other"

    def _extract_key_features(self, content: str) -> str:
        """Extract key features from content."""
        features = []
        content_lower = content.lower()

        feature_keywords = {
            "multimodal": ["multimodal", "vision", "image understanding", "audio"],
            "reasoning": ["reasoning", "chain of thought", "step-by-step"],
            "coding": ["code", "coding", "programming"],
            "multilingual": ["multilingual", "language", "translation"],
            "long-context": ["long context", "context window", "128k", "1m"],
            "open-weight": ["open", "open source", "open-weight"],
        }

        for feature, keywords in feature_keywords.items():
            if any(kw in content_lower for kw in keywords):
                features.append(feature)

        return ", ".join(features) if features else ""

    def _extract_benchmarks(self, content: str) -> Dict[str, float]:
        """Extract benchmark scores from content."""
        benchmarks = {}

        for benchmark, pattern in BENCHMARK_PATTERNS.items():
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                try:
                    # Take the first match, convert to float
                    score = float(matches[0])
                    # Validate reasonable range (0-100)
                    if 0 <= score <= 100:
                        benchmarks[benchmark] = score
                except ValueError:
                    continue

        return benchmarks

    def scrape_openai(self) -> Dict[str, Any]:
        """Scrape OpenAI blog announcements."""
        print("\n=== Scraping OpenAI ===")
        config = LABS["OpenAI"]
        url = f"{config['base_url']}{config['blog_path']}"

        models = []

        # Fetch blog listing page
        soup = self._fetch(url)
        if not soup:
            return {"lab": "OpenAI", "models": []}

        # Find article links
        articles = soup.find_all("a", href=re.compile(r"/blog/"))
        article_urls = set()
        for article in articles[:15]:  # Limit to recent articles
            href = article.get("href")
            if href:
                full_url = urljoin(config["base_url"], href)
                article_urls.add(full_url)

        print(f"  Found {len(article_urls)} articles")

        for article_url in list(article_urls)[:10]:  # Process first 10
            article_soup = self._fetch(article_url)
            if not article_soup:
                continue

            # Extract title
            title_elem = article_soup.find("h1") or article_soup.find("title")
            title = title_elem.get_text(strip=True) if title_elem else ""

            # Extract content
            content_elem = article_soup.find("article") or article_soup.find("main") or article_soup.find("body")
            content = content_elem.get_text(separator=" ", strip=True) if content_elem else ""

            # Extract date
            date = self._extract_date(article_soup, config)

            # Extract model name
            model_name = self._extract_model_name(title, content, "OpenAI")

            if model_name:
                model_data = {
                    "name": model_name,
                    "announcement_date": date or "unknown",
                    "architecture": self._extract_architecture(content),
                    "key_features": self._extract_key_features(content),
                    "benchmark_claims": self._extract_benchmarks(content),
                    "url": article_url,
                }
                models.append(model_data)
                print(f"    Found: {model_name}")

        return {"lab": "OpenAI", "models": models}

    def scrape_anthropic(self) -> Dict[str, Any]:
        """Scrape Anthropic news announcements."""
        print("\n=== Scraping Anthropic ===")
        config = LABS["Anthropic"]
        url = f"{config['base_url']}{config['blog_path']}"

        models = []

        soup = self._fetch(url)
        if not soup:
            return {"lab": "Anthropic", "models": []}

        # Find article links
        articles = soup.find_all("a", href=re.compile(r"/news/"))
        article_urls = set()
        for article in articles[:15]:
            href = article.get("href")
            if href:
                full_url = urljoin(config["base_url"], href)
                article_urls.add(full_url)

        print(f"  Found {len(article_urls)} articles")

        for article_url in list(article_urls)[:10]:
            article_soup = self._fetch(article_url)
            if not article_soup:
                continue

            title_elem = article_soup.find("h1") or article_soup.find("title")
            title = title_elem.get_text(strip=True) if title_elem else ""

            content_elem = article_soup.find("article") or article_soup.find("main") or article_soup.find("body")
            content = content_elem.get_text(separator=" ", strip=True) if content_elem else ""

            date = self._extract_date(article_soup, config)
            model_name = self._extract_model_name(title, content, "Anthropic")

            if model_name:
                model_data = {
                    "name": model_name,
                    "announcement_date": date or "unknown",
                    "architecture": self._extract_architecture(content),
                    "key_features": self._extract_key_features(content),
                    "benchmark_claims": self._extract_benchmarks(content),
                    "url": article_url,
                }
                models.append(model_data)
                print(f"    Found: {model_name}")

        return {"lab": "Anthropic", "models": models}

    def scrape_deepmind(self) -> Dict[str, Any]:
        """Scrape Google DeepMind blog announcements."""
        print("\n=== Scraping Google DeepMind ===")
        config = LABS["Google DeepMind"]
        url = f"{config['base_url']}{config['blog_path']}"

        models = []

        soup = self._fetch(url)
        if not soup:
            return {"lab": "Google DeepMind", "models": []}

        # Find article links
        articles = soup.find_all("a", href=re.compile(r"/discover/blog/"))
        article_urls = set()
        for article in articles[:15]:
            href = article.get("href")
            if href:
                full_url = urljoin(config["base_url"], href)
                article_urls.add(full_url)

        print(f"  Found {len(article_urls)} articles")

        for article_url in list(article_urls)[:10]:
            article_soup = self._fetch(article_url)
            if not article_soup:
                continue

            title_elem = article_soup.find("h1") or article_soup.find("title")
            title = title_elem.get_text(strip=True) if title_elem else ""

            content_elem = article_soup.find("article") or article_soup.find("main") or article_soup.find("body")
            content = content_elem.get_text(separator=" ", strip=True) if content_elem else ""

            date = self._extract_date(article_soup, config)
            model_name = self._extract_model_name(title, content, "Google DeepMind")

            if model_name:
                model_data = {
                    "name": model_name,
                    "announcement_date": date or "unknown",
                    "architecture": self._extract_architecture(content),
                    "key_features": self._extract_key_features(content),
                    "benchmark_claims": self._extract_benchmarks(content),
                    "url": article_url,
                }
                models.append(model_data)
                print(f"    Found: {model_name}")

        return {"lab": "Google DeepMind", "models": models}

    def scrape_meta(self) -> Dict[str, Any]:
        """Scrape Meta AI blog announcements."""
        print("\n=== Scraping Meta AI ===")
        config = LABS["Meta AI"]
        url = f"{config['base_url']}{config['blog_path']}"

        models = []

        soup = self._fetch(url)
        if not soup:
            return {"lab": "Meta AI", "models": []}

        # Find article links
        articles = soup.find_all("a", href=re.compile(r"/blog/"))
        article_urls = set()
        for article in articles[:15]:
            href = article.get("href")
            if href:
                full_url = urljoin(config["base_url"], href)
                article_urls.add(full_url)

        print(f"  Found {len(article_urls)} articles")

        for article_url in list(article_urls)[:10]:
            article_soup = self._fetch(article_url)
            if not article_soup:
                continue

            title_elem = article_soup.find("h1") or article_soup.find("title")
            title = title_elem.get_text(strip=True) if title_elem else ""

            content_elem = article_soup.find("article") or article_soup.find("main") or article_soup.find("body")
            content = content_elem.get_text(separator=" ", strip=True) if content_elem else ""

            date = self._extract_date(article_soup, config)
            model_name = self._extract_model_name(title, content, "Meta AI")

            if model_name:
                model_data = {
                    "name": model_name,
                    "announcement_date": date or "unknown",
                    "architecture": self._extract_architecture(content),
                    "key_features": self._extract_key_features(content),
                    "benchmark_claims": self._extract_benchmarks(content),
                    "url": article_url,
                }
                models.append(model_data)
                print(f"    Found: {model_name}")

        return {"lab": "Meta AI", "models": models}

    def scrape_mistral(self) -> Dict[str, Any]:
        """Scrape Mistral AI news announcements."""
        print("\n=== Scraping Mistral AI ===")
        config = LABS["Mistral AI"]
        url = f"{config['base_url']}{config['blog_path']}"

        models = []

        soup = self._fetch(url)
        if not soup:
            return {"lab": "Mistral AI", "models": []}

        # Find article links
        articles = soup.find_all("a", href=re.compile(r"/news/"))
        article_urls = set()
        for article in articles[:15]:
            href = article.get("href")
            if href:
                full_url = urljoin(config["base_url"], href)
                article_urls.add(full_url)

        print(f"  Found {len(article_urls)} articles")

        for article_url in list(article_urls)[:10]:
            article_soup = self._fetch(article_url)
            if not article_soup:
                continue

            title_elem = article_soup.find("h1") or article_soup.find("title")
            title = title_elem.get_text(strip=True) if title_elem else ""

            content_elem = article_soup.find("article") or article_soup.find("main") or article_soup.find("body")
            content = content_elem.get_text(separator=" ", strip=True) if content_elem else ""

            date = self._extract_date(article_soup, config)
            model_name = self._extract_model_name(title, content, "Mistral AI")

            if model_name:
                model_data = {
                    "name": model_name,
                    "announcement_date": date or "unknown",
                    "architecture": self._extract_architecture(content),
                    "key_features": self._extract_key_features(content),
                    "benchmark_claims": self._extract_benchmarks(content),
                    "url": article_url,
                }
                models.append(model_data)
                print(f"    Found: {model_name}")

        return {"lab": "Mistral AI", "models": models}

    def scrape_all(self) -> List[Dict[str, Any]]:
        """Scrape all labs and return combined results."""
        results = []

        results.append(self.scrape_openai())
        results.append(self.scrape_anthropic())
        results.append(self.scrape_deepmind())
        results.append(self.scrape_meta())
        results.append(self.scrape_mistral())

        return results


def validate_against_schema(data: Dict, schema_path: Optional[Path] = None) -> bool:
    """Validate scraped data against the model schema."""
    # Basic validation - check required fields
    required_fields = ["lab", "models"]
    for field in required_fields:
        if field not in data:
            print(f"  Validation error: Missing required field '{field}'")
            return False

    # Validate each model
    for model in data.get("models", []):
        model_required = ["name", "announcement_date", "architecture", "url"]
        for field in model_required:
            if field not in model:
                print(f"  Validation error: Model missing required field '{field}'")
                return False

        # Validate architecture value
        allowed_archs = ["dense-transformer", "moe", "ssm", "multimodal", "reasoning", "other"]
        if model.get("architecture") not in allowed_archs:
            print(f"  Validation warning: Unknown architecture '{model.get('architecture')}'")

    return True


def main():
    parser = argparse.ArgumentParser(description="Scrape AI lab announcement pages")
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default="data/raw/lab_announcements.json",
        help="Output file path (default: data/raw/lab_announcements.json)",
    )
    parser.add_argument(
        "--delay",
        "-d",
        type=float,
        default=DEFAULT_DELAY,
        help=f"Delay between requests in seconds (default: {DEFAULT_DELAY})",
    )
    parser.add_argument(
        "--validate",
        "-v",
        action="store_true",
        help="Validate output against schema",
    )
    args = parser.parse_args()

    # Create output directory if needed
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("AI Lab Announcement Scraper")
    print("=" * 60)
    print(f"Delay between requests: {args.delay}s")
    print(f"Output file: {output_path}")
    print("=" * 60)

    # Run scraper
    scraper = LabScraper(delay=args.delay)
    results = scraper.scrape_all()

    # Calculate totals
    total_models = sum(len(lab["models"]) for lab in results)

    # Save results
    output_data = {
        "scraped_at": datetime.now().isoformat(),
        "total_labs": len(results),
        "total_models": total_models,
        "labs": results,
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 60)
    print("SCRAPING COMPLETE")
    print("=" * 60)
    print(f"Total labs scraped: {len(results)}")
    print(f"Total models extracted: {total_models}")

    for lab in results:
        print(f"  - {lab['lab']}: {len(lab['models'])} models")

    print(f"\nOutput saved to: {output_path}")

    # Validation
    if args.validate:
        print("\nValidating data...")
        all_valid = True
        for lab in results:
            if not validate_against_schema(lab):
                all_valid = False
        if all_valid:
            print("✓ All data validated successfully")
        else:
            print("✗ Some validation errors found")

    return 0 if total_models >= 20 else 1


if __name__ == "__main__":
    exit(main())
