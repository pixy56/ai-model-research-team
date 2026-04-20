#!/usr/bin/env python3
"""
ArXiv Papers Analysis Script
Analyzes 100 arXiv papers for research trends and findings.
"""

import json
import re
from collections import Counter
from datetime import datetime
import os

# Load the data
with open('data/raw/arxiv_papers_2026-04-19.json', 'r') as f:
    data = json.load(f)

papers = data['papers']
print(f"Total papers loaded: {len(papers)}")

# Initialize counters and data structures
categories = Counter()
primary_categories = Counter()
keywords_matched = Counter()
authors = Counter()
institutions = []

# Architecture patterns to search for
architectures = {
    'transformer': r'transformer[s]?',
    'moe': r'mixture[s]? of expert[s]?|\bmoe\b',
    'llama': r'llama',
    'gpt': r'gpt[- ]?\d*',
    'bert': r'bert',
    'diffusion': r'diffusion',
    'gan': r'\bgan[s]?\b|generative adversarial',
    'vae': r'vae|variational autoencoder',
    'rnn': r'rnn|recurrent neural',
    'cnn': r'cnn|convolutional neural',
    'mamba': r'mamba',
    'retnet': r'retnet',
    'rwkv': r'rwkv',
    'state space': r'state space model[s]?',
    'lstm': r'lstm',
    'gru': r'gru'
}

# Benchmark patterns
benchmarks = {
    'mmlu': r'mmlu',
    'humaneval': r'humaneval',
    'gsm8k': r'gsm8k',
    'math': r'\bmath[- ]?\d*\b',
    'hellaswag': r'hellaswag',
    'arc': r'\barc[- ]?\w*\b',
    'boolq': r'boolq',
    'piqa': r'piqa',
    'siqa': r'siqa',
    'winogrande': r'winogrande',
    'openbookqa': r'openbookqa',
    'natural questions': r'natural questions',
    'triviaqa': r'triviaqa',
    'squad': r'squad',
    'glue': r'glue',
    'superglue': r'superglue',
    'bbh': r'bbh|big bench',
    'alpaca': r'alpaca',
    'vicuna': r'vicuna',
    'mt-bench': r'mt[- ]?bench',
    'arena': r'arena',
    'swag': r'\bswag\b',
    'copa': r'\bcopa\b',
    'rte': r'\brte\b',
    'wnli': r'wnli',
    'mnli': r'mnli',
    'qnli': r'qnli',
    'snli': r'snli',
    'sst': r'sst',
    'cola': r'cola',
    'mrpc': r'mrpc',
    'qqp': r'qqp',
    'stsb': r'stsb',
    'cifar': r'cifar',
    'imagenet': r'imagenet',
    'coco': r'coco',
    'flickr': r'flickr',
    'textvqa': r'textvqa',
    'okvqa': r'okvqa',
    'gqa': r'\bgqa\b',
    'vizwiz': r'vizwiz',
    'refcoco': r'refcoco',
    'visual genome': r'visual genome',
    'vqa': r'\bvqa\b',
    'science qa': r'science[- ]?qa',
    'theorem proving': r'theorem[- ]?prov',
    'minerva': r'minerva',
    'mathqa': r'mathqa',
    'aime': r'\baime\b',
    'amc': r'\bamc\b',
    'sat': r'\bsat\b',
    'gre': r'\bgre\b',
    'lsat': r'\blsat\b',
    'bar': r'\bbar\b',
    'medqa': r'medqa',
    'pubmed': r'pubmed',
    'legal': r'legal[- ]?bench',
    'mbpp': r'mbpp',
    'ds1000': r'ds1000',
    'swde': r'swde',
    'wtq': r'wtq',
    'wikisql': r'wikisql',
    'spider': r'\bspider\b',
    'bird': r'\bbird\b',
    'biodex': r'biodex',
    'mmlu-pro': r'mmlu[- ]?pro',
    'mmlu-redux': r'mmlu[- ]?redux'
}

# Research themes/keywords
themes = {
    'fine-tuning': r'fine[- ]?tun',
    'instruction tuning': r'instruction[- ]?tun',
    'rlhf': r'rlhf|reinforcement learning from human feedback',
    'alignment': r'align(ment)?',
    'chain of thought': r'chain[- ]?of[- ]?thought|cot',
    'prompting': r'prompt(ing)?',
    'in-context learning': r'in[- ]?context[- ]?learn',
    'few-shot': r'few[- ]?shot',
    'zero-shot': r'zero[- ]?shot',
    ' Retrieval-Augmented Generation': r'rag|retrieval[- ]?augmented',
    'hallucination': r'hallucinat',
    'safety': r'safety|safe',
    'bias': r'bias',
    'interpretability': r'interpretab|explainab|xai',
    'efficiency': r'efficien|speed|latency|throughput',
    'compression': r'compress|prun|quantiz',
    'distillation': r'distill',
    'agent': r'\bagent[s]?\b',
    'tool use': r'tool[- ]?use|tool[- ]?learn',
    'planning': r'planning',
    'memory': r'memory|long[- ]?context',
    'attention': r'attention',
    'self-supervised': r'self[- ]?supervised',
    'contrastive': r'contrastive',
    'multimodal': r'multimodal|vision[- ]?language|vlm',
    'vision': r'vision|image|visual',
    'code generation': r'code[- ]?generat|program synthesis',
    'math reasoning': r'math|mathematical|arithmetic',
    'theorem proving': r'theorem[- ]?prov',
    'knowledge graph': r'knowledge[- ]?graph',
    'graph neural': r'graph[- ]?neural|gnn',
    'reinforcement learning': r'reinforcement[- ]?learn',
    'pre-training': r'pre[- ]?train',
    'post-training': r'post[- ]?train',
    'synthetic data': r'synthetic[- ]?data',
    'data augmentation': r'data[- ]?augment',
    'curriculum learning': r'curriculum',
    'meta-learning': r'meta[- ]?learn',
    'transfer learning': r'transfer[- ]?learn',
    'domain adaptation': r'domain[- ]?adapt',
    'continual learning': r'continual[- ]?learn|lifelong',
    'federated': r'federated',
    'on-device': r'on[- ]?device|edge|mobile',
    'medical': r'medical|clinical|health|biomedical',
    'legal': r'legal|law',
    'finance': r'financ|economic|trading',
    'science': r'scientific|science',
    'education': r'education|educational',
    'reasoning': r'reason',
    'evaluation': r'evaluat|benchmark',
    'dataset': r'dataset|corpus',
    'survey': r'survey|review',
    'taxonomy': r'taxonom',
    'framework': r'framework',
    'method': r'method|approach'
}

# Institution patterns
institution_patterns = [
    r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\s+(?:University|College|Institute|School))',
    r'(Google\s*(?:DeepMind|Research)?)',
    r'(OpenAI)',
    r'(Meta\s*(?:AI|Research)?)',
    r'(Microsoft\s*(?:Research)?)',
    r'(Amazon\s*(?:Web Services|Research)?)',
    r'(Apple)',
    r'(NVIDIA)',
    r'(Intel\s*(?:Labs)?)',
    r'(IBM\s*(?:Research)?)',
    r'(Anthropic)',
    r'(Cohere)',
    r'(AI21\s*Labs?)',
    r'(Stability\s*AI)',
    r'(Hugging\s*Face)',
    r'(Allen\s*Institute)',
    r'(Salesforce\s*Research)',
    r'(Bloomberg)',
    r'(ByteDance)',
    r'(Alibaba)',
    r'(Baidu)',
    r'(Tencent)',
    r'(Huawei)',
    r'(Samsung)',
    r'(Sony)',
    r'(Toyota)',
    r'(MIT)',
    r'(Stanford)',
    r'(Berkeley)',
    r'(CMU)',
    r'(Harvard)',
    r'(Princeton)',
    r'(Yale)',
    r'(Columbia)',
    r'(Oxford)',
    r'(Cambridge)',
    r'(ETH\s*Zurich)',
    r'(INRIA)',
    r'(MPI)',
    r'(FAIR)',
    r'(DeepMind)'
]

# Process papers
arch_counts = {k: 0 for k in architectures}
benchmark_counts = {k: 0 for k in benchmarks}
theme_counts = {k: 0 for k in themes}
institution_counts = Counter()

# Extract text from all papers for analysis
all_titles = []
all_abstracts = []
all_text = []

for paper in papers:
    title = paper.get('title', '')
    abstract = paper.get('abstract', '')
    text = title + ' ' + abstract
    
    all_titles.append(title)
    all_abstracts.append(abstract)
    all_text.append(text.lower())
    
    # Count categories
    for cat in paper.get('categories', []):
        categories[cat] += 1
    primary_categories[paper.get('primary_category', 'unknown')] += 1
    
    # Count keywords matched
    for kw in paper.get('keywords_matched', []):
        keywords_matched[kw] += 1
    
    # Count authors
    for author in paper.get('authors', []):
        authors[author] += 1
    
    # Search for architectures
    text_lower = text.lower()
    for arch_name, pattern in architectures.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            arch_counts[arch_name] += 1
    
    # Search for benchmarks
    for bench_name, pattern in benchmarks.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            benchmark_counts[bench_name] += 1
    
    # Search for themes
    for theme_name, pattern in themes.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            theme_counts[theme_name] += 1

# Get top results
top_architectures = [(k, v) for k, v in sorted(arch_counts.items(), key=lambda x: x[1], reverse=True) if v > 0]
top_benchmarks = [(k, v) for k, v in sorted(benchmark_counts.items(), key=lambda x: x[1], reverse=True) if v > 0]
top_themes = [(k, v) for k, v in sorted(theme_counts.items(), key=lambda x: x[1], reverse=True) if v > 0]
top_authors = authors.most_common(20)

# Common bigrams in titles
from collections import defaultdict
bigram_counts = defaultdict(int)
for title in all_titles:
    words = re.findall(r'\b[a-zA-Z]+\b', title.lower())
    for i in range(len(words) - 1):
        bigram = f"{words[i]} {words[i+1]}"
        bigram_counts[bigram] += 1
top_bigrams = sorted(bigram_counts.items(), key=lambda x: x[1], reverse=True)[:30]

# Print summary
print("\n" + "="*60)
print("ARXIV PAPERS ANALYSIS SUMMARY")
print("="*60)

print(f"\nQuery Date: {data['query_date']}")
print(f"Date Range: {data['query_params']['date_from']} to {data['query_params']['date_to']}")
print(f"Categories: {', '.join(data['query_params']['categories'])}")
print(f"Keywords: {', '.join(data['query_params']['keywords'])}")

print("\n--- CATEGORIES ---")
for cat, count in primary_categories.most_common():
    print(f"  {cat}: {count}")

print("\n--- KEYWORDS MATCHED ---")
for kw, count in keywords_matched.most_common():
    print(f"  {kw}: {count}")

print("\n--- TOP ARCHITECTURES MENTIONED ---")
for arch, count in top_architectures[:15]:
    print(f"  {arch}: {count}")

print("\n--- TOP BENCHMARKS MENTIONED ---")
for bench, count in top_benchmarks[:20]:
    print(f"  {bench}: {count}")

print("\n--- TOP RESEARCH THEMES ---")
for theme, count in top_themes[:20]:
    print(f"  {theme}: {count}")

print("\n--- TOP TITLE BIGRAMS ---")
for bigram, count in top_bigrams[:20]:
    print(f"  '{bigram}': {count}")

print("\n--- TOP AUTHORS ---")
for author, count in top_authors[:15]:
    print(f"  {author}: {count}")

# Save processed insights
insights = {
    "analysis_date": datetime.now().isoformat(),
    "query_info": data['query_params'],
    "total_papers": len(papers),
    "statistics": {
        "categories": dict(primary_categories),
        "keywords_matched": dict(keywords_matched),
        "top_architectures": top_architectures[:15],
        "top_benchmarks": top_benchmarks[:20],
        "top_themes": top_themes[:20],
        "top_bigrams": top_bigrams[:20],
        "top_authors": top_authors[:15]
    },
    "papers": papers
}

os.makedirs('data/processed', exist_ok=True)
with open('data/processed/paper_insights.json', 'w') as f:
    json.dump(insights, f, indent=2)

print("\n✓ Analysis complete. Results saved to data/processed/paper_insights.json")
