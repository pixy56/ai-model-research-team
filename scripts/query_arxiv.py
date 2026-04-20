#!/usr/bin/env python3
"""
arXiv Query Automation for AI Model Research Team

Fetches latest AI model papers from arXiv API with filters for:
- Categories: cs.AI, cs.LG, cs.CL
- Date range: last 30 days
- Keywords: "large language model", "multimodal", "reasoning"

Usage:
    python3 query_arxiv.py [--output PATH] [--days DAYS] [--max-results N]

Output:
    JSON file with paper metadata matching the expected schema
"""

import argparse
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
import sys


# arXiv API endpoint
ARXIV_API_URL = "http://export.arxiv.org/api/query"

# Default categories to search
DEFAULT_CATEGORIES = ["cs.AI", "cs.LG", "cs.CL"]

# Default keywords to search for
DEFAULT_KEYWORDS = ["large language model", "multimodal", "reasoning"]

# XML namespaces
NAMESPACES = {
    'atom': 'http://www.w3.org/2005/Atom',
    'arxiv': 'http://arxiv.org/schemas/atom'
}


def build_query(categories, keywords, date_from, date_to):
    """
    Build arXiv search query string.
    
    Args:
        categories: List of arXiv categories (e.g., ['cs.AI', 'cs.LG'])
        keywords: List of keywords to search for
        date_from: Start date (YYYY-MM-DD)
        date_to: End date (YYYY-MM-DD)
    
    Returns:
        Query string for arXiv API
    """
    # Build category filter
    cat_query = " OR ".join([f"cat:{cat}" for cat in categories])
    
    # Build keyword filter (search in title and abstract)
    keyword_query = " OR ".join([f'"{kw}"' for kw in keywords])
    
    # Build date range filter (submitted date)
    # arXiv uses YYYYMMDD format for submittedDate
    date_from_compact = date_from.replace("-", "")
    date_to_compact = date_to.replace("-", "")
    date_query = f"submittedDate:[{date_from_compact}0000 TO {date_to_compact}2359]"
    
    # Combine all filters
    query = f"({cat_query}) AND ({keyword_query}) AND {date_query}"
    
    return query


def fetch_arxiv_papers(query, max_results=100, start=0):
    """
    Fetch papers from arXiv API.
    
    Args:
        query: Search query string
        max_results: Maximum number of results to fetch
        start: Start index for pagination
    
    Returns:
        List of paper dictionaries
    """
    params = {
        'search_query': query,
        'start': start,
        'max_results': max_results,
        'sortBy': 'submittedDate',
        'sortOrder': 'descending'
    }
    
    url = f"{ARXIV_API_URL}?{urllib.parse.urlencode(params)}"
    
    headers = {
        'User-Agent': 'ai-model-research-bot/1.0 (research-team@example.com)'
    }
    
    request = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            data = response.read()
            return parse_arxiv_response(data)
    except urllib.error.HTTPError as e:
        print(f"HTTP Error {e.code}: {e.reason}", file=sys.stderr)
        raise
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}", file=sys.stderr)
        raise


def parse_arxiv_response(xml_data):
    """
    Parse arXiv API XML response.
    
    Args:
        xml_data: Raw XML response bytes
    
    Returns:
        List of paper dictionaries
    """
    root = ET.fromstring(xml_data)
    papers = []
    
    for entry in root.findall('atom:entry', NAMESPACES):
        paper = parse_entry(entry)
        if paper:
            papers.append(paper)
    
    return papers


def parse_entry(entry):
    """
    Parse a single arXiv entry into a dictionary.
    
    Args:
        entry: XML Element for an entry
    
    Returns:
        Dictionary with paper metadata
    """
    # Extract arXiv ID
    id_elem = entry.find('atom:id', NAMESPACES)
    if id_elem is None:
        return None
    
    arxiv_url = id_elem.text
    # Extract ID from URL (e.g., http://arxiv.org/abs/2504.01234v1 -> 2504.01234)
    arxiv_id = arxiv_url.split('/')[-1].split('v')[0]
    
    # Extract title
    title_elem = entry.find('atom:title', NAMESPACES)
    title = title_elem.text.strip() if title_elem is not None else ""
    
    # Extract abstract
    summary_elem = entry.find('atom:summary', NAMESPACES)
    abstract = summary_elem.text.strip() if summary_elem is not None else ""
    
    # Extract authors
    authors = []
    for author_elem in entry.findall('atom:author', NAMESPACES):
        name_elem = author_elem.find('atom:name', NAMESPACES)
        if name_elem is not None:
            authors.append(name_elem.text)
    
    # Extract published date
    published_elem = entry.find('atom:published', NAMESPACES)
    published = published_elem.text[:10] if published_elem is not None else ""
    
    # Extract categories
    categories = []
    for cat_elem in entry.findall('atom:category', NAMESPACES):
        term = cat_elem.get('term')
        if term:
            categories.append(term)
    
    # Extract primary category
    primary_elem = entry.find('arxiv:primary_category', NAMESPACES)
    primary_category = primary_elem.get('term') if primary_elem is not None else None
    
    # Build PDF URL
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
    
    # Determine which keywords matched
    keywords_matched = detect_keywords(title + " " + abstract)
    
    return {
        "arxiv_id": arxiv_id,
        "title": title,
        "authors": authors,
        "abstract": abstract,
        "published": published,
        "categories": categories,
        "primary_category": primary_category,
        "pdf_url": pdf_url,
        "keywords_matched": keywords_matched,
        "arxiv_url": arxiv_url
    }


def detect_keywords(text):
    """
    Detect which keywords are present in the text.
    
    Args:
        text: Text to search in
    
    Returns:
        List of matched keywords
    """
    text_lower = text.lower()
    matched = []
    
    for keyword in DEFAULT_KEYWORDS:
        if keyword.lower() in text_lower:
            matched.append(keyword)
    
    return matched


def fetch_all_papers(query, min_papers=50, batch_size=100):
    """
    Fetch papers until we have at least min_papers.
    
    Args:
        query: Search query string
        min_papers: Minimum number of papers to fetch
        batch_size: Number of papers to fetch per request
    
    Returns:
        List of all paper dictionaries
    """
    all_papers = []
    start = 0
    max_iterations = 10  # Safety limit
    
    for iteration in range(max_iterations):
        print(f"Fetching papers {start+1} to {start+batch_size}...")
        
        papers = fetch_arxiv_papers(query, max_results=batch_size, start=start)
        
        if not papers:
            print("No more papers found.")
            break
        
        all_papers.extend(papers)
        start += len(papers)
        
        print(f"  Retrieved {len(papers)} papers (total: {len(all_papers)})")
        
        if len(all_papers) >= min_papers:
            print(f"Reached minimum target of {min_papers} papers.")
            break
        
        if len(papers) < batch_size:
            print("Reached end of results.")
            break
    
    return all_papers


def build_output(papers, query_params):
    """
    Build the final output JSON structure.
    
    Args:
        papers: List of paper dictionaries
        query_params: Dictionary with query parameters
    
    Returns:
        Dictionary matching the expected output format
    """
    today = datetime.now().strftime("%Y-%m-%d")
    
    return {
        "query_date": today,
        "total_papers": len(papers),
        "query_params": query_params,
        "papers": papers
    }


def validate_output(data, min_papers=50):
    """
    Validate the output data meets requirements.
    
    Args:
        data: Output dictionary
        min_papers: Minimum number of papers required
    
    Returns:
        (is_valid, error_message)
    """
    if not isinstance(data, dict):
        return False, "Output must be a dictionary"
    
    required_keys = ["query_date", "total_papers", "query_params", "papers"]
    for key in required_keys:
        if key not in data:
            return False, f"Missing required key: {key}"
    
    if not isinstance(data["papers"], list):
        return False, "papers must be a list"
    
    if data["total_papers"] < min_papers:
        return False, f"Expected at least {min_papers} papers, got {data['total_papers']}"
    
    # Validate each paper has required fields
    paper_required = ["arxiv_id", "title", "authors", "abstract", "published", "categories", "pdf_url"]
    for i, paper in enumerate(data["papers"]):
        for key in paper_required:
            if key not in paper:
                return False, f"Paper {i} missing required field: {key}"
    
    return True, "Validation passed"


def main():
    parser = argparse.ArgumentParser(
        description="Query arXiv for AI model research papers"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output file path (default: data/raw/arxiv_papers_YYYY-MM-DD.json)"
    )
    parser.add_argument(
        "--days", "-d",
        type=int,
        default=30,
        help="Number of days to look back (default: 30)"
    )
    parser.add_argument(
        "--max-results", "-m",
        type=int,
        default=100,
        help="Maximum results per query (default: 100)"
    )
    parser.add_argument(
        "--min-papers",
        type=int,
        default=50,
        help="Minimum papers to fetch (default: 50)"
    )
    parser.add_argument(
        "--categories",
        nargs="+",
        default=DEFAULT_CATEGORIES,
        help=f"arXiv categories to search (default: {' '.join(DEFAULT_CATEGORIES)})"
    )
    parser.add_argument(
        "--keywords",
        nargs="+",
        default=DEFAULT_KEYWORDS,
        help=f"Keywords to search for (default: {' '.join(DEFAULT_KEYWORDS)})"
    )
    
    args = parser.parse_args()
    
    # Calculate date range
    today = datetime.now()
    date_to = today.strftime("%Y-%m-%d")
    date_from = (today - timedelta(days=args.days)).strftime("%Y-%m-%d")
    
    # Determine output path
    if args.output:
        output_path = Path(args.output)
    else:
        output_path = Path(f"data/raw/arxiv_papers_{date_to}.json")
    
    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Querying arXiv for papers...")
    print(f"  Categories: {', '.join(args.categories)}")
    print(f"  Keywords: {', '.join(args.keywords)}")
    print(f"  Date range: {date_from} to {date_to}")
    print(f"  Min papers: {args.min_papers}")
    print()
    
    # Build query
    query = build_query(args.categories, args.keywords, date_from, date_to)
    print(f"Query: {query}")
    print()
    
    # Fetch papers
    try:
        papers = fetch_all_papers(query, min_papers=args.min_papers, batch_size=args.max_results)
    except Exception as e:
        print(f"Error fetching papers: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Build output
    query_params = {
        "categories": args.categories,
        "date_from": date_from,
        "date_to": date_to,
        "keywords": args.keywords
    }
    
    output_data = build_output(papers, query_params)
    
    # Validate output
    is_valid, message = validate_output(output_data, min_papers=args.min_papers)
    if not is_valid:
        print(f"Validation failed: {message}", file=sys.stderr)
        sys.exit(1)
    
    print(f"\nValidation passed: {message}")
    
    # Write output
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: {output_path}")
    print(f"Total papers: {len(papers)}")
    print(f"Query completed successfully!")


if __name__ == "__main__":
    main()
