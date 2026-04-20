#!/usr/bin/env python3
"""
Test script for arXiv query automation.

Tests:
1. Query building
2. Small fetch (5 papers) to verify API connectivity
3. Output format validation
4. Keyword detection
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from query_arxiv import (
    build_query,
    fetch_arxiv_papers,
    parse_arxiv_response,
    build_output,
    validate_output,
    detect_keywords,
    DEFAULT_CATEGORIES,
    DEFAULT_KEYWORDS
)


def test_build_query():
    """Test query building functionality."""
    print("=" * 60)
    print("TEST 1: Build Query")
    print("=" * 60)
    
    categories = ["cs.AI", "cs.LG"]
    keywords = ["large language model", "multimodal"]
    date_from = "2025-04-01"
    date_to = "2025-04-19"
    
    query = build_query(categories, keywords, date_from, date_to)
    
    print(f"Categories: {categories}")
    print(f"Keywords: {keywords}")
    print(f"Date range: {date_from} to {date_to}")
    print(f"\nGenerated query:")
    print(f"  {query}")
    
    # Verify query contains expected components
    assert "cat:cs.AI" in query, "Missing cs.AI category"
    assert "cat:cs.LG" in query, "Missing cs.LG category"
    assert '"large language model"' in query, "Missing keyword"
    assert "submittedDate:[202504010000 TO 202504192359]" in query, "Date range incorrect"
    
    print("\n✓ Query building test PASSED")
    return True


def test_fetch_small():
    """Test fetching a small number of papers."""
    print("\n" + "=" * 60)
    print("TEST 2: Fetch Small Batch (5 papers)")
    print("=" * 60)
    
    # Use a simple query for testing
    categories = ["cs.AI", "cs.LG", "cs.CL"]
    keywords = ["large language model"]
    
    # Use last 60 days to ensure we get results
    today = datetime.now()
    date_to = today.strftime("%Y-%m-%d")
    date_from = (today - timedelta(days=60)).strftime("%Y-%m-%d")
    
    query = build_query(categories, keywords, date_from, date_to)
    
    print(f"Query: {query}")
    print("Fetching...")
    
    try:
        papers = fetch_arxiv_papers(query, max_results=5)
        print(f"\nRetrieved {len(papers)} papers")
        
        if papers:
            print("\nFirst paper sample:")
            paper = papers[0]
            print(f"  arXiv ID: {paper['arxiv_id']}")
            print(f"  Title: {paper['title'][:80]}...")
            print(f"  Authors: {', '.join(paper['authors'][:3])}{'...' if len(paper['authors']) > 3 else ''}")
            print(f"  Published: {paper['published']}")
            print(f"  Categories: {', '.join(paper['categories'][:3])}")
            print(f"  Keywords matched: {paper['keywords_matched']}")
        
        print(f"\n✓ Fetch test PASSED (retrieved {len(papers)} papers)")
        return papers
        
    except Exception as e:
        print(f"\n✗ Fetch test FAILED: {e}")
        return None


def test_output_format(papers):
    """Test output format validation."""
    print("\n" + "=" * 60)
    print("TEST 3: Output Format Validation")
    print("=" * 60)
    
    if not papers:
        print("⚠ Skipping - no papers to validate")
        return False
    
    query_params = {
        "categories": DEFAULT_CATEGORIES,
        "date_from": "2025-04-01",
        "date_to": "2025-04-19",
        "keywords": DEFAULT_KEYWORDS
    }
    
    output_data = build_output(papers, query_params)
    
    # Check required keys
    required_keys = ["query_date", "total_papers", "query_params", "papers"]
    for key in required_keys:
        assert key in output_data, f"Missing required key: {key}"
        print(f"  ✓ Has '{key}'")
    
    # Check query_params
    qp = output_data["query_params"]
    qp_required = ["categories", "date_from", "date_to", "keywords"]
    for key in qp_required:
        assert key in qp, f"Missing query_params key: {key}"
        print(f"  ✓ query_params has '{key}'")
    
    # Check paper structure
    paper_required = ["arxiv_id", "title", "authors", "abstract", "published", "categories", "pdf_url", "keywords_matched"]
    for key in paper_required:
        assert key in papers[0], f"Paper missing field: {key}"
        print(f"  ✓ Paper has '{key}'")
    
    print(f"\n✓ Output format test PASSED")
    return True


def test_keyword_detection():
    """Test keyword detection functionality."""
    print("\n" + "=" * 60)
    print("TEST 4: Keyword Detection")
    print("=" * 60)
    
    test_cases = [
        ("This is about large language models and multimodal reasoning", ["large language model", "multimodal", "reasoning"]),
        ("We present a new reasoning approach", ["reasoning"]),
        ("A multimodal transformer architecture", ["multimodal"]),
        ("Standard neural network", []),
    ]
    
    for text, expected in test_cases:
        detected = detect_keywords(text)
        print(f"  Text: '{text[:50]}...'")
        print(f"    Expected: {expected}")
        print(f"    Detected: {detected}")
        assert detected == expected, f"Keyword detection mismatch"
        print("    ✓ Match!")
    
    print("\n✓ Keyword detection test PASSED")
    return True


def test_full_validation():
    """Test full validation with minimum paper count."""
    print("\n" + "=" * 60)
    print("TEST 5: Full Validation (min 50 papers)")
    print("=" * 60)
    
    # Create mock data with 50 papers
    papers = []
    for i in range(50):
        papers.append({
            "arxiv_id": f"2504.{i:05d}",
            "title": f"Test Paper {i}",
            "authors": ["Author One", "Author Two"],
            "abstract": "This is a test abstract about large language models.",
            "published": "2025-04-15",
            "categories": ["cs.AI", "cs.LG"],
            "pdf_url": f"https://arxiv.org/pdf/2504.{i:05d}.pdf",
            "keywords_matched": ["large language model"]
        })
    
    query_params = {
        "categories": DEFAULT_CATEGORIES,
        "date_from": "2025-04-01",
        "date_to": "2025-04-19",
        "keywords": DEFAULT_KEYWORDS
    }
    
    output_data = build_output(papers, query_params)
    
    is_valid, message = validate_output(output_data, min_papers=50)
    
    if is_valid:
        print(f"  ✓ Validation passed: {message}")
        print(f"  ✓ Total papers: {output_data['total_papers']}")
    else:
        print(f"  ✗ Validation failed: {message}")
        return False
    
    # Test with insufficient papers
    output_data["papers"] = output_data["papers"][:30]
    output_data["total_papers"] = 30
    
    is_valid, message = validate_output(output_data, min_papers=50)
    
    if not is_valid:
        print(f"  ✓ Correctly detected insufficient papers: {message}")
    else:
        print(f"  ✗ Should have failed with insufficient papers")
        return False
    
    print(f"\n✓ Full validation test PASSED")
    return True


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("arXiv Query Automation - Test Suite")
    print("=" * 60)
    
    results = []
    
    # Test 1: Query building
    results.append(("Build Query", test_build_query()))
    
    # Test 2: Fetch small batch
    papers = test_fetch_small()
    results.append(("Fetch Small Batch", papers is not None))
    
    # Test 3: Output format
    results.append(("Output Format", test_output_format(papers)))
    
    # Test 4: Keyword detection
    results.append(("Keyword Detection", test_keyword_detection()))
    
    # Test 5: Full validation
    results.append(("Full Validation", test_full_validation()))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, r in results if r)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"  {name:.<40} {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
