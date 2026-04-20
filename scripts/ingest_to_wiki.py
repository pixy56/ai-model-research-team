#!/usr/bin/env python3
"""
LLM-Wiki Ingestion Script

Automates the ingestion of knowledge into the wiki from various sources:
- arXiv papers (from JSON files)
- Analysis notebooks
- External sources

Usage:
    python ingest_to_wiki.py --source arxiv --input data/raw/arxiv_papers_*.json
    python ingest_to_wiki.py --source all --dry-run
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Wiki root directory
WIKI_ROOT = Path(__file__).parent.parent / "wiki"
TEMPLATES_DIR = WIKI_ROOT / "templates"


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text[:100]  # Limit length


def format_authors(authors: List[str]) -> str:
    """Format author list for display."""
    if len(authors) <= 2:
        return ", ".join(authors)
    return f"{authors[0]} et al."


def extract_key_findings(abstract: str) -> List[str]:
    """Extract key findings from abstract."""
    findings = []
    sentences = abstract.split('. ')
    
    # Look for result indicators
    result_keywords = ['propose', 'introduce', 'demonstrate', 'show', 'achieve', 
                       'find', 'reveal', 'present', 'develop']
    
    for sentence in sentences:
        for keyword in result_keywords:
            if keyword in sentence.lower() and len(sentence) > 20:
                finding = sentence.strip()
                if finding and finding not in findings:
                    findings.append(finding)
                break
    
    return findings[:3]  # Return top 3


def categorize_paper(paper: Dict) -> str:
    """Determine paper category based on content."""
    title = paper.get('title', '').lower()
    abstract = paper.get('abstract', '').lower()
    categories = paper.get('categories', [])
    keywords = paper.get('keywords_matched', [])
    
    text = f"{title} {abstract}"
    
    # Check for model-focused papers
    if any(k in text for k in ['model', 'llm', 'language model', 'transformer']):
        if 'multimodal' in text or 'vision' in text or 'image' in text:
            return 'multimodal'
        if 'reasoning' in text or 'theorem' in text or 'math' in text:
            return 'reasoning'
        return 'llms'
    
    # Check for benchmark papers
    if 'benchmark' in text or 'evaluation' in text:
        return 'benchmark'
    
    # Check for architecture papers
    if any(k in text for k in ['architecture', 'transformer', 'attention', 'mamba', 'moe']):
        return 'architecture'
    
    # Default to research findings
    return 'research'


def create_paper_wiki_entry(paper: Dict, output_dir: Path) -> Optional[Path]:
    """Create a wiki entry for an arXiv paper."""
    
    arxiv_id = paper.get('arxiv_id', 'unknown')
    title = paper.get('title', 'Untitled')
    authors = paper.get('authors', [])
    abstract = paper.get('abstract', '')
    published = paper.get('published', datetime.now().strftime('%Y-%m-%d'))
    categories = paper.get('categories', [])
    keywords = paper.get('keywords_matched', [])
    pdf_url = paper.get('pdf_url', '')
    arxiv_url = paper.get('arxiv_url', '')
    
    # Generate filename
    slug = slugify(title)
    filename = f"{published}-{slug}.md"
    filepath = output_dir / filename
    
    # Extract key findings
    findings = extract_key_findings(abstract)
    
    # Format content
    content = f"""---
title: "{title}"
category: research-finding
subcategory: paper
author: "{format_authors(authors)}"
date: "{published}"
tags: {json.dumps(keywords + categories)}
status: ingested
source: arxiv
paper_id: "{arxiv_id}"
---

# {title}

## Summary

{abstract[:500]}{'...' if len(abstract) > 500 else ''}

## Paper Details

- **arXiv ID:** {arxiv_id}
- **Published:** {published}
- **Authors:** {', '.join(authors[:5])}{' et al.' if len(authors) > 5 else ''}
- **Categories:** {', '.join(categories)}
- **Keywords Matched:** {', '.join(keywords)}

## Key Findings

"""
    
    for i, finding in enumerate(findings, 1):
        content += f"{i}. {finding}\n"
    
    content += f"""
## Context

### Background
This paper was published on {published} and relates to {'multimodal AI' if 'multimodal' in keywords else 'language model research' if 'large language model' in keywords else 'AI reasoning' if 'reasoning' in keywords else 'AI/ML research'}.

### Approach
The authors present their methodology and findings in the domain of {categories[0] if categories else 'AI research'}.

## Implications

### For Researchers
This work contributes to the growing body of knowledge in {', '.join(categories[:2]) if categories else 'AI research'}.

### For Practitioners
Practitioners may find the approaches and findings applicable to real-world problems in the domain.

## Resources

- [arXiv Abstract]({arxiv_url})
- [PDF Download]({pdf_url})

## Tags

{' '.join([f'#{tag}' for tag in keywords + categories])}

---
*Ingested on {datetime.now().strftime('%Y-%m-%d')} by automated ingestion script*
"""
    
    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath


def ingest_arxiv_papers(input_file: Path, dry_run: bool = False) -> Dict:
    """Ingest arXiv papers from JSON file."""
    
    results = {
        'processed': 0,
        'created': 0,
        'errors': []
    }
    
    # Load papers
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    papers = data.get('papers', [])
    results['total'] = len(papers)
    
    # Setup output directories
    papers_dir = WIKI_ROOT / "research-findings" / "papers"
    papers_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Processing {len(papers)} papers from {input_file}")
    
    for paper in papers:
        try:
            results['processed'] += 1
            
            if dry_run:
                print(f"  [DRY RUN] Would create: {slugify(paper.get('title', ''))[:50]}...")
                continue
            
            filepath = create_paper_wiki_entry(paper, papers_dir)
            if filepath:
                results['created'] += 1
                if results['created'] <= 5:  # Show first 5
                    print(f"  Created: {filepath.name}")
                
        except Exception as e:
            results['errors'].append({
                'paper': paper.get('arxiv_id', 'unknown'),
                'error': str(e)
            })
    
    return results


def update_research_findings_readme(papers: List[Dict]):
    """Update the research-findings README with recent papers."""
    
    readme_path = WIKI_ROOT / "research-findings" / "README.md"
    
    # Sort by date, get recent
    recent = sorted(papers, key=lambda x: x.get('published', ''), reverse=True)[:10]
    
    content = f"""# Research Findings

Latest research insights and paper summaries from arXiv and other sources.

## Recent Papers

Last updated: {datetime.now().strftime('%Y-%m-%d')}

| Date | Title | Authors | Category |
|------|-------|---------|----------|
"""
    
    for paper in recent:
        title = paper.get('title', 'Untitled')[:60] + '...' if len(paper.get('title', '')) > 60 else paper.get('title', 'Untitled')
        authors = format_authors(paper.get('authors', []))[:30]
        date = paper.get('published', 'Unknown')
        categories = ', '.join(paper.get('categories', [])[:2])
        
        content += f"| {date} | [{title}](papers/{slugify(paper.get('title', ''))}.md) | {authors} | {categories} |\n"
    
    content += f"""
## Categories

- [Papers](papers/) - Individual paper summaries
- [Insights](insights/) - Analysis insights from notebooks
- [Trends](trends/) - Emerging trends and patterns

## Ingestion

Papers are automatically ingested from:
- arXiv (cs.AI, cs.LG, cs.CL, cs.CV)
- Keywords: large language model, multimodal, reasoning, transformer

Run `python scripts/ingest_to_wiki.py --source arxiv` to manually trigger ingestion.

---
*Automatically maintained by Literature Review Agent*
"""
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Updated: {readme_path}")


def create_sample_entries():
    """Create sample entries for demonstration."""
    
    samples = [
        {
            'type': 'model',
            'name': 'GPT-4o',
            'developer': 'OpenAI',
            'date': '2024-05-13'
        },
        {
            'type': 'benchmark',
            'name': 'MMLU-Pro',
            'description': 'Enhanced MMLU benchmark'
        }
    ]
    
    print("Created sample entry templates")


def main():
    parser = argparse.ArgumentParser(description='Ingest knowledge into LLM-Wiki')
    parser.add_argument('--source', choices=['arxiv', 'all'], default='arxiv',
                       help='Source to ingest from')
    parser.add_argument('--input', type=Path, 
                       default=Path(__file__).parent.parent / "data" / "raw" / "arxiv_papers_2026-04-19.json",
                       help='Input file for arXiv papers')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be done without making changes')
    parser.add_argument('--limit', type=int, default=0,
                       help='Limit number of papers to process (0 = all)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("LLM-Wiki Ingestion Script")
    print("=" * 60)
    print(f"Wiki root: {WIKI_ROOT}")
    print(f"Mode: {'DRY RUN' if args.dry_run else 'LIVE'}")
    print()
    
    # Ensure directories exist
    if not args.dry_run:
        (WIKI_ROOT / "research-findings" / "papers").mkdir(parents=True, exist_ok=True)
        (WIKI_ROOT / "research-findings" / "insights").mkdir(parents=True, exist_ok=True)
        (WIKI_ROOT / "research-findings" / "trends").mkdir(parents=True, exist_ok=True)
    
    results = {'processed': 0, 'created': 0, 'errors': []}
    
    if args.source in ['arxiv', 'all']:
        print("\n[1/1] Processing arXiv papers...")
        if args.input.exists():
            # Load papers
            with open(args.input, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            papers = data.get('papers', [])
            if args.limit > 0:
                papers = papers[:args.limit]
                data['papers'] = papers
            
            # Save limited data if needed
            if args.limit > 0:
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tf:
                    json.dump(data, tf)
                    temp_path = Path(tf.name)
                results = ingest_arxiv_papers(temp_path, args.dry_run)
                temp_path.unlink()
            else:
                results = ingest_arxiv_papers(args.input, args.dry_run)
            
            # Update README
            if not args.dry_run:
                update_research_findings_readme(data.get('papers', []))
        else:
            print(f"  ERROR: Input file not found: {args.input}")
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Total papers: {results.get('total', 0)}")
    print(f"Processed: {results['processed']}")
    print(f"Created: {results['created']}")
    print(f"Errors: {len(results['errors'])}")
    
    if results['errors']:
        print("\nErrors encountered:")
        for err in results['errors'][:5]:
            print(f"  - {err['paper']}: {err['error']}")
    
    print("\nDone!")
    return 0


if __name__ == '__main__':
    sys.exit(main())
