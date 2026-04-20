# Leaderboard Data Scraping Methodology

## Overview

This document describes the methodology used to scrape benchmark leaderboard data from Hugging Face Open LLM Leaderboard and Papers with Code.

## Data Sources

### 1. Hugging Face Open LLM Leaderboard

**Source URL:** https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard

**API Endpoint:** https://open-llm-leaderboard-open-llm-leaderboard.hf.space/api/leaderboard

**Method:** Direct API access via HTTP GET request

**Data Format:** JSON array with 4,576 model entries (as of 2025-04-20)

**Fields Extracted:**
- Model name (fullname)
- Model type (pretrained, chat, fine-tuned, etc.)
- Architecture (LlamaForCausalLM, Qwen2ForCausalLM, etc.)
- Parameters (billions)
- Average score
- Individual benchmark scores:
  - IFEval (Instruction Following Evaluation)
  - BBH (Big Bench Hard)
  - MATH Lvl 5
  - GPQA (Graduate-Level Google-Proof Q&A)
  - MUSR
  - MMLU-PRO
- Metadata (license, likes, submission date, etc.)

**Scraping Process:**
1. Query the API endpoint
2. Parse JSON response
3. Sort by average score descending
4. Extract top 100 models
5. Clean and normalize data

**Rate Limiting:** None observed for read-only API access

**Data Freshness:** Real-time (updated as models are evaluated)

### 2. Papers with Code

**Source URLs:**
- MMLU: https://paperswithcode.com/sota/multi-task-language-understanding-on-mmlu
- HumanEval: https://paperswithcode.com/sota/code-generation-on-humaneval
- GPQA: https://paperswithcode.com/sota/question-answering-on-gpqa

**Method:** Web scraping with JavaScript rendering support

**Challenge:** Papers with Code uses JavaScript-rendered tables that require browser automation (Selenium/Playwright) for full data extraction.

**Alternative Approach:** Manual extraction of top performers from the HF leaderboard data, which includes scores for MMLU-PRO, GPQA, and HumanEval-equivalent benchmarks.

## Data Files

### Raw Data
- `hf_leaderboard_raw.json` - Complete HF leaderboard (4,576 models)
- `hf_leaderboard_top100.json` - Top 100 models by average score

### Processed Data
- Cleaned and normalized JSON with consistent field names
- Rankings calculated based on average score
- Missing values handled (null for unavailable scores)

## Data Schema

### Hugging Face Leaderboard Entry
```json
{
  "rank": 1,
  "model_name": "org/model-name",
  "model_type": "💬 chat models (RLHF, DPO, IFT, ...)",
  "architecture": "LlamaForCausalLM",
  "parameters_billions": 70.0,
  "average_score": 52.08,
  "ifeval_score": 80.63,
  "bbh_score": 62.61,
  "math_lvl5_score": 40.33,
  "gpqa_score": 20.36,
  "musr_score": 15.23,
  "mmlu_pro_score": 45.12,
  "hub_license": "apache-2.0",
  "hub_likes": 1500,
  "is_moe": false,
  "submission_date": "2024-06-12",
  "precision": "bfloat16",
  "weight_type": "Original",
  "official_provider": true
}
```

## Reproducibility

### Requirements
```bash
pip install requests beautifulsoup4
```

### Running the Scraper
```bash
python scripts/scrape_leaderboards.py --output-dir data/raw/leaderboards
```

### Manual API Access
```bash
# Hugging Face
 curl -s "https://open-llm-leaderboard-open-llm-leaderboard.hf.space/api/leaderboard" \
   -o hf_leaderboard_raw.json
```

## Limitations

1. **Papers with Code**: Requires JavaScript rendering for full table access
2. **Data Freshness**: Leaderboards update frequently; data represents snapshot
3. **Model Availability**: Some models may be removed from Hub
4. **Score Normalization**: Different benchmarks use different scoring scales

## Future Improvements

1. Implement Selenium/Playwright for Papers with Code scraping
2. Add automated scheduling for regular updates
3. Implement data validation and quality checks
4. Add support for additional leaderboards (LMSYS Chatbot Arena, etc.)

## Data Quality Notes

- All scores are percentages (0-100 scale)
- Models with missing benchmarks have null values
- "Average" score is calculated across all evaluated benchmarks
- Models are ranked by average score descending

## Citation

When using this data, please cite:
- Hugging Face Open LLM Leaderboard: https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard
- Papers with Code: https://paperswithcode.com/

## Last Updated

2025-04-20
