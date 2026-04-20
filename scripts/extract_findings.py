#!/usr/bin/env python3
"""
Enhanced Key Findings Extraction Script
Extracts findings, claims, methods, and limitations from analyzed papers with improved patterns.
"""

import json
import re
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict

def load_json(filepath: str) -> Dict:
    with open(filepath, 'r') as f:
        return json.load(f)

def extract_numerical_results(text: str, title: str) -> List[Dict]:
    """Extract numerical results from text."""
    results = []
    
    # Pattern: achieves/scores/reaches X% on benchmark
    patterns = [
        r'(?:achieves?|reaches?|obtains?|scores?)\s+(?:up\s+to\s+)?(~?\d+\.?\d*)%?\s*(?:accuracy|score|performance)?(?:\s+on\s+)?([A-Z][a-zA-Z0-9-]*)',
        r'(?:accuracy|score|performance)\s+(?:of\s+)?(?:up\s+to\s+)?(~?\d+\.?\d*)%?',
        r'(\d+\.?\d*)%?\s+(?:improvement|increase|decrease|reduction|gain)',
        r'(\d+\.?\d*)%?\s+(?:accuracy|F1|precision|recall|AUROC)',
        r'(?:accuracy|F1)\s+(?:of|up\s+to)\s+(\d+\.?\d*)',
        r'(\d+\.?\d*)\s+balanced\s+accuracy',
        r'(\d+\.?\d*)\s+macro\s+F1',
        r'AUROC\s+(?:above|of|up\s+to)\s+(\d+\.?\d*)',
    ]
    
    for pattern in patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            result_text = match.group(0)
            value = None
            for group in match.groups():
                if group and re.match(r'^\d+\.?\d*$', group):
                    value = group
                    break
            
            results.append({
                'type': 'result',
                'text': result_text,
                'value': value
            })
    
    return results

def extract_claims(text: str) -> List[Dict]:
    """Extract claims from text."""
    claims = []
    
    # Pattern: We show/demonstrate/prove/find that...
    claim_patterns = [
        r'[Ww]e\s+(?:show|demonstrate|prove|find|identify)\s+that\s+([^\.]+)',
        r'[Oo]ur\s+(?:results?|findings?|analysis?)\s+(?:show|demonstrate|prove|find|indicate)\s+(?:that\s+)?([^\.]+)',
        r'[Tt]hese\s+(?:results?|findings?)\s+(?:suggest|indicate|demonstrate|show)\s+(?:that\s+)?([^\.]+)',
        r'[Ww]e\s+identify\s+(?:that\s+)?([^\.]+)',
        r'[Oo]ur\s+findings?\s+reveal\s+(?:that\s+)?([^\.]+)',
        r'[Rr]esults?\s+(?:show|demonstrate|indicate)\s+(?:that\s+)?([^\.]+)',
        r'[Ff]indings?\s+(?:suggest|indicate|show)\s+(?:that\s+)?([^\.]+)',
        r'[Ww]e\s+(?:also\s+)?find\s+that\s+([^\.]+)',
        r'[Tt]his\s+(?:paper|work|study)\s+(?:shows|demonstrates|reveals)\s+(?:that\s+)?([^\.]+)',
    ]
    
    for pattern in claim_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            claim_text = match.group(1).strip()
            if len(claim_text) > 20 and len(claim_text) < 300:
                claims.append({
                    'type': 'claim',
                    'text': claim_text,
                    'full_context': match.group(0)[:400]
                })
    
    return claims

def extract_methods(text: str, title: str) -> List[Dict]:
    """Extract novel methods from text."""
    methods = []
    
    # Pattern: We propose/introduce...
    method_patterns = [
        r'[Ww]e\s+propose\s+(?:a\s+)?(?:novel\s+)?(?:framework|method|approach|mechanism|technique|model|architecture)\s+(?:called\s+)?([^\.]+)',
        r'[Ww]e\s+introduce\s+(?:a\s+)?([^\.]+(?:benchmark|framework|method|approach|dataset|technique))',
        r'[Tt]his\s+paper\s+presents?\s+(?:a\s+)?(novel\s+)?(?:method|approach|framework|technique)\s+(?:for\s+)?([^\.]+)',
        r'[Ww]e\s+present\s+(?:a\s+)?(novel\s+)?([^\.]+(?:framework|method|approach|technique))',
    ]
    
    for pattern in method_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            method_text = match.group(0)
            methods.append({
                'type': 'method',
                'text': method_text[:300],
                'is_novel': 'novel' in method_text.lower() or 'new' in method_text.lower()
            })
    
    # Extract named methods (CAPS or CamelCase)
    named_method_patterns = [
        r'[Ww]e\s+propose\s+([A-Z][a-zA-Z0-9-]+(?::\s*[^\.]+)?)',
        r'[Ww]e\s+introduce\s+([A-Z][a-zA-Z0-9-]+)',
        r'[Ww]e\s+present\s+([A-Z][a-zA-Z0-9-]+)',
    ]
    
    for pattern in named_method_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            name = match.group(1).split(':')[0].strip()
            if len(name) > 2 and not name.lower() in ['the', 'this', 'that', 'with', 'from']:
                methods.append({
                    'type': 'named_method',
                    'name': name,
                    'text': match.group(0)[:200],
                    'is_novel': True
                })
    
    return methods

def extract_limitations(text: str) -> List[Dict]:
    """Extract limitations from text."""
    limitations = []
    
    # Pattern: limitations, challenges, issues
    limitation_patterns = [
        r'(?:limitation|challenge|issue|problem|drawback|shortcoming|weakness|barrier|bottleneck)\s+(?:is|of|in|for|to)\s+([^\.]+)',
        r'(?:does\s+not\s+work|fails?\s+to|struggles?\s+to|unable\s+to)\s+([^\.]+)',
        r'(?:significant\s+)?(?:gap|bottleneck|barrier)\s+(?:in|for|to)\s+([^\.]+)',
        r'[Oo]ur\s+approach\s+(?:does\s+not|cannot|fails?\s+to)\s+([^\.]+)',
        r'(?:remains?|is)\s+(?:unclear|unknown|challenging|difficult|uncertain)\s+([^\.]+)',
        r'(?:remains?|is)\s+(?:a\s+)?(?:significant\s+)?(?:challenge|problem|issue)\s+([^\.]+)',
        r'[Hh]owever,?\s+([^\.]+(?:limitation|challenge|issue|problem|unclear|unknown))',
    ]
    
    for pattern in limitation_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            limitations.append({
                'type': 'limitation',
                'text': match.group(0)[:300]
            })
    
    return limitations

def extract_models(text: str) -> List[str]:
    """Extract model names mentioned in text."""
    models = []
    
    # Common model patterns
    model_patterns = [
        r'\b(GPT-[0-9.]+(?:-[A-Za-z]+)?(?:-[0-9]+[BM])?)\b',
        r'\b(Llama-?[0-9.]*(?:-[0-9]+[BM])?)\b',
        r'\b(Claude(?:\s*[0-9.]*\s*[A-Za-z]+)?)\b',
        r'\b(Gemini(?:-[0-9.]+)?(?:\s*[A-Za-z]+)?)\b',
        r'\b(Qwen[0-9.-]*(?:-[A-Za-z]+)?)\b',
        r'\b(DeepSeek(?:-[A-Za-z]+)?)\b',
        r'\b(BERT(?:-[A-Za-z]+)?)\b',
        r'\b(T5(?:-[A-Za-z]+)?)\b',
        r'\b(Mistral(?:-[A-Za-z]+)?)\b',
        r'\b(Gemma-?[0-9.]*)\b',
        r'\b(Pythia(?:-[0-9.]+[BM])?)\b',
        r'\b(OLMo(?:-[0-9.]+[BM])?)\b',
        r'\b(Phi-[0-9]+)\b',
        r'\b(LLaMA-?[0-9]*)\b',
        r'\b(Mixtral(?:-[A-Za-z]+)?)\b',
    ]
    
    for pattern in model_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            models.append(match.group(1))
    
    return list(set(models))

def extract_benchmarks(text: str) -> List[str]:
    """Extract benchmark names mentioned in text."""
    benchmarks = []
    
    # Common benchmark patterns
    benchmark_patterns = [
        r'\b(MMLU)\b',
        r'\b(GSM8?K)\b',
        r'\b(ARC)\b',
        r'\b(HellaSwag)\b',
        r'\b(TruthfulQA)\b',
        r'\b(HumanEval)\b',
        r'\b(MATH)\b',
        r'\b(GPQA)\b',
        r'\b(MMMU)\b',
        r'\b(VQA)\b',
        r'\b(CrossMath)\b',
        r'\b(Mind\'s\s+Eye)\b',
        r'\b(BAGEL)\b',
        r'\b(PLUM)\b',
        r'\b(SocialGrid)\b',
        r'\b(ReactBench)\b',
        r'\b(UniEditBench)\b',
        r'\b(MEDLEY-BENCH)\b',
        r'\b(LiveCodeBench)\b',
        r'\b(XAI\s+Question\s+Bank)\b',
        r'\b(GPTSniffer)\b',
        r'\b(Whodunit)\b',
        r'\b(KA-LogicQuery)\b',
        r'\b(DROP)\b',
        r'\b(ReCoRD)\b',
        r'\b(AIME25?)\b',
        r'\b(GTA-[A-Za-z]+)\b',
        r'\b(STOP)\b',
        r'\b(GRIFT)\b',
        r'\b(CHOP)\b',
        r'\b(ChemGraph-XANES)\b',
        r'\b(HILBERT)\b',
        r'\b(AtManRL)\b',
        r'\b(JumpLoRA)\b',
        r'\b(MoIR)\b',
        r'\b(DeepInsightTheorem)\b',
        r'\b(RISE)\b',
    ]
    
    for pattern in benchmark_patterns:
        matches = re.finditer(pattern, text, re.IGNORECASE)
        for match in matches:
            benchmarks.append(match.group(1))
    
    return list(set(benchmarks))

def process_papers(papers_data: Dict) -> Dict:
    """Process all papers and extract findings."""
    papers = papers_data.get('papers', [])
    
    findings_db = {
        'metadata': {
            'extraction_date': datetime.now().isoformat(),
            'source_file': 'data/processed/paper_insights.json',
            'total_papers': len(papers),
            'papers_processed': 0,
            'methodology': {
                'description': 'Automated extraction of key findings from paper abstracts using regex patterns',
                'finding_types': ['result', 'claim', 'method', 'limitation'],
                'extraction_sources': ['title', 'abstract'],
                'patterns_used': {
                    'results': 'Numerical achievements, scores, improvements (e.g., "achieves X%", "accuracy of Y")',
                    'claims': 'Research findings stated with confidence (e.g., "we show that", "our results demonstrate")',
                    'methods': 'Novel approaches, frameworks, techniques (e.g., "we propose X", "we introduce Y")',
                    'limitations': 'Constraints, challenges, gaps (e.g., "remains unclear", "challenge is")'
                }
            }
        },
        'findings': [],
        'statistics': {
            'by_type': defaultdict(int),
            'by_category': defaultdict(int),
            'by_model': defaultdict(int),
            'by_benchmark': defaultdict(int)
        }
    }
    
    finding_id = 0
    
    for paper in papers:
        paper_id = paper.get('arxiv_id', '')
        title = paper.get('title', '')
        abstract = paper.get('abstract', '')
        categories = paper.get('categories', [])
        primary_category = paper.get('primary_category', '')
        
        # Combine title and abstract for analysis
        full_text = f"{title}. {abstract}"
        
        # Extract models and benchmarks mentioned
        models = extract_models(full_text)
        benchmarks = extract_benchmarks(full_text)
        
        # Extract different types of findings
        numerical_results = extract_numerical_results(full_text, title)
        claims = extract_claims(full_text)
        methods = extract_methods(full_text, title)
        limitations = extract_limitations(full_text)
        
        # Create findings
        for result in numerical_results:
            finding_id += 1
            finding = {
                'id': f"finding_{finding_id:04d}",
                'type': 'result',
                'category': 'numerical_result',
                'paper_id': paper_id,
                'paper_title': title,
                'paper_categories': categories,
                'primary_category': primary_category,
                'text': result.get('text', ''),
                'value': result.get('value'),
                'confidence': 'medium',
                'models_mentioned': models,
                'benchmarks_mentioned': benchmarks,
                'extraction_source': 'abstract'
            }
            findings_db['findings'].append(finding)
            findings_db['statistics']['by_type']['result'] += 1
        
        for claim in claims:
            finding_id += 1
            finding = {
                'id': f"finding_{finding_id:04d}",
                'type': 'claim',
                'category': 'research_claim',
                'paper_id': paper_id,
                'paper_title': title,
                'paper_categories': categories,
                'primary_category': primary_category,
                'text': claim.get('text', ''),
                'context': claim.get('full_context', ''),
                'models_mentioned': models,
                'benchmarks_mentioned': benchmarks,
                'confidence': 'medium',
                'extraction_source': 'abstract'
            }
            findings_db['findings'].append(finding)
            findings_db['statistics']['by_type']['claim'] += 1
        
        for method in methods:
            finding_id += 1
            finding = {
                'id': f"finding_{finding_id:04d}",
                'type': 'method',
                'category': 'novel_method' if method.get('is_novel') else 'method',
                'paper_id': paper_id,
                'paper_title': title,
                'paper_categories': categories,
                'primary_category': primary_category,
                'text': method.get('text', ''),
                'method_name': method.get('name'),
                'is_novel': method.get('is_novel', False),
                'models_mentioned': models,
                'benchmarks_mentioned': benchmarks,
                'confidence': 'high' if method.get('is_novel') else 'medium',
                'extraction_source': 'abstract'
            }
            findings_db['findings'].append(finding)
            findings_db['statistics']['by_type']['method'] += 1
        
        for limitation in limitations:
            finding_id += 1
            finding = {
                'id': f"finding_{finding_id:04d}",
                'type': 'limitation',
                'category': 'limitation',
                'paper_id': paper_id,
                'paper_title': title,
                'paper_categories': categories,
                'primary_category': primary_category,
                'text': limitation.get('text', ''),
                'models_mentioned': models,
                'benchmarks_mentioned': benchmarks,
                'confidence': 'medium',
                'extraction_source': 'abstract'
            }
            findings_db['findings'].append(finding)
            findings_db['statistics']['by_type']['limitation'] += 1
        
        findings_db['metadata']['papers_processed'] += 1
        findings_db['statistics']['by_category'][primary_category] += 1
        
        for model in models:
            findings_db['statistics']['by_model'][model] += 1
        for bench in benchmarks:
            findings_db['statistics']['by_benchmark'][bench] += 1
    
    # Convert defaultdicts to regular dicts for JSON serialization
    findings_db['statistics']['by_type'] = dict(findings_db['statistics']['by_type'])
    findings_db['statistics']['by_category'] = dict(findings_db['statistics']['by_category'])
    findings_db['statistics']['by_model'] = dict(findings_db['statistics']['by_model'])
    findings_db['statistics']['by_benchmark'] = dict(findings_db['statistics']['by_benchmark'])
    findings_db['statistics']['total_findings'] = len(findings_db['findings'])
    findings_db['statistics']['papers_with_findings'] = findings_db['metadata']['papers_processed']
    
    return findings_db

def main():
    # Load data
    papers_data = load_json('data/processed/paper_insights.json')
    
    # Process papers
    findings_db = process_papers(papers_data)
    
    # Save findings database
    with open('data/processed/paper_findings.json', 'w') as f:
        json.dump(findings_db, f, indent=2)
    
    # Print summary
    print("=" * 60)
    print("KEY FINDINGS EXTRACTION COMPLETE")
    print("=" * 60)
    print(f"\nTotal papers processed: {findings_db['metadata']['papers_processed']}")
    print(f"Total findings extracted: {findings_db['statistics']['total_findings']}")
    print(f"\nFindings by type:")
    for ftype, count in sorted(findings_db['statistics']['by_type'].items(), key=lambda x: -x[1]):
        print(f"  - {ftype}: {count}")
    print(f"\nTop models mentioned:")
    for model, count in sorted(findings_db['statistics']['by_model'].items(), key=lambda x: -x[1])[:15]:
        print(f"  - {model}: {count}")
    print(f"\nTop benchmarks mentioned:")
    for bench, count in sorted(findings_db['statistics']['by_benchmark'].items(), key=lambda x: -x[1])[:15]:
        print(f"  - {bench}: {count}")
    print(f"\nOutput saved to: data/processed/paper_findings.json")

if __name__ == '__main__':
    main()