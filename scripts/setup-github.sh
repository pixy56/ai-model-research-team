#!/bin/bash
# GitHub Repository Setup Script for AI Model Research Team
# Run this script with your GitHub PAT to create the remote repository

set -e

echo "=========================================="
echo "GitHub Repository Setup"
echo "=========================================="
echo ""

# Check if we're in the right directory
if [ ! -f "README.md" ] || [ ! -d "agents" ]; then
    echo "Error: Please run this script from the ai-model-research-team directory"
    exit 1
fi

# Get GitHub credentials
echo "Enter your GitHub Personal Access Token (PAT):"
echo "(Token should start with 'ghp_' or 'github_pat_')"
read -s GITHUB_TOKEN
echo ""

echo "Enter your GitHub username:"
read GITHUB_USER

echo ""
echo "Repository name [ai-model-research-team]:"
read REPO_NAME
REPO_NAME=${REPO_NAME:-ai-model-research-team}

echo ""
echo "Make repository private? [y/N]:"
read IS_PRIVATE
if [[ $IS_PRIVATE =~ ^[Yy]$ ]]; then
    PRIVATE="true"
    VISIBILITY="private"
else
    PRIVATE="false"
    VISIBILITY="public"
fi

echo ""
echo "=========================================="
echo "Creating repository..."
echo "Username: $GITHUB_USER"
echo "Repository: $REPO_NAME"
echo "Visibility: $VISIBILITY"
echo "=========================================="
echo ""

# Create repository via GitHub API
RESPONSE=$(curl -s -X POST \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    https://api.github.com/user/repos \
    -d "{
        \"name\": \"$REPO_NAME\",
        \"description\": \"SAFe Agentic Research Team - Tracking the latest AI models\",
        \"private\": $PRIVATE,
        \"auto_init\": false,
        \"has_issues\": true,
        \"has_projects\": true,
        \"has_wiki\": true
    }")

# Check if creation was successful
if echo "$RESPONSE" | grep -q '"id":'; then
    echo "✓ Repository created successfully!"
    REPO_URL=$(echo "$RESPONSE" | grep -o '"html_url": "[^"]*"' | head -1 | cut -d'"' -f4)
    echo "Repository URL: $REPO_URL"
else
    echo "✗ Failed to create repository"
    echo "Response: $RESPONSE"
    exit 1
fi

echo ""
echo "=========================================="
echo "Pushing local code to GitHub..."
echo "=========================================="
echo ""

# Configure git remote and push
if git remote | grep -q "origin"; then
    git remote remove origin
fi

git remote add origin "https://$GITHUB_TOKEN@github.com/$GITHUB_USER/$REPO_NAME.git"

# Determine default branch
BRANCH=$(git branch --show-current)
echo "Pushing branch: $BRANCH"

git push -u origin "$BRANCH"

echo ""
echo "✓ Code pushed successfully!"

echo ""
echo "=========================================="
echo "Creating labels..."
echo "=========================================="
echo ""

# Create labels
LABELS='[
    {"name": "literature-review", "color": "0052CC", "description": "Literature Review Agent tasks"},
    {"name": "data-analysis", "color": "5319E7", "description": "Data Analysis Agent tasks"},
    {"name": "writing", "color": "0E8A16", "description": "Writing Agent tasks"},
    {"name": "integration", "color": "F9D0C4", "description": "Integration Agent tasks"},
    {"name": "dev-team", "color": "B60205", "description": "Dev Team tasks"},
    {"name": "story-points: 2", "color": "C2E0C6", "description": "2 story points"},
    {"name": "story-points: 3", "color": "C2E0C6", "description": "3 story points"},
    {"name": "story-points: 5", "color": "C2E0C6", "description": "5 story points"},
    {"name": "story-points: 8", "color": "C2E0C6", "description": "8 story points"},
    {"name": "story-points: 13", "color": "C2E0C6", "description": "13 story points"},
    {"name": "iteration-1", "color": "FEF2C0", "description": "Iteration 1: Foundation"},
    {"name": "iteration-2", "color": "FEF2C0", "description": "Iteration 2: Data Collection"},
    {"name": "iteration-3", "color": "FEF2C0", "description": "Iteration 3: Analysis"},
    {"name": "iteration-4", "color": "FEF2C0", "description": "Iteration 4: Insights"},
    {"name": "iteration-5", "color": "FEF2C0", "description": "Iteration 5: Synthesis"}
]'

echo "$LABELS" | python3 -c "
import json
import sys
labels = json.load(sys.stdin)
for label in labels:
    print(f'Creating label: {label[\"name\"]}')
"

echo "$LABELS" | python3 -c "
import json
import sys
import subprocess
import os

token = os.environ.get('GITHUB_TOKEN', '$GITHUB_TOKEN')
user = '$GITHUB_USER'
repo = '$REPO_NAME'

labels = json.load(sys.stdin)
for label in labels:
    cmd = [
        'curl', '-s', '-X', 'POST',
        '-H', f'Authorization: token {token}',
        '-H', 'Accept: application/vnd.github.v3+json',
        f'https://api.github.com/repos/{user}/{repo}/labels',
        '-d', json.dumps(label)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if '\"id\":' in result.stdout:
        print(f'✓ Created label: {label[\"name\"]}')
    elif 'already_exists' in result.stdout:
        print(f'• Label exists: {label[\"name\"]}')
    else:
        print(f'✗ Failed: {label[\"name\"]} - {result.stdout[:100]}')
"

echo ""
echo "=========================================="
echo "Creating GitHub Issues for Iteration 1..."
echo "=========================================="
echo ""

# Create issues for Iteration 1
python3 << 'EOF'
import json
import subprocess
import os

token = os.environ.get('GITHUB_TOKEN', '$GITHUB_TOKEN')
user = '$GITHUB_USER'
repo = '$REPO_NAME'

issues = [
    {
        "title": "Story 1.1: Model Metadata Schema",
        "body": """## Description
Create a standardized JSON schema for AI model metadata to ensure consistent data across the research team.

## Tasks
- [ ] Define JSON schema for model metadata
- [ ] Fields: name, lab, release_date, architecture, parameters, context_window, benchmarks, paper_url, announcement_url
- [ ] Create validation script
- [ ] Document schema in wiki

## Acceptance Criteria
- [ ] Schema documented in `docs/schemas/model-metadata.json`
- [ ] Validation script passes sample data
- [ ] Wiki updated with schema documentation

## Agent
Literature Review Agent

## Story Points
3""",
        "labels": ["literature-review", "story-points: 3", "iteration-1"]
    },
    {
        "title": "Story 1.2: arXiv Query Automation",
        "body": """## Description
Build automated queries to fetch latest AI model papers from arXiv.

## Tasks
- [ ] Set up arXiv API queries for AI model papers
- [ ] Filter by categories: cs.AI, cs.LG, cs.CL
- [ ] Filter by date range (last 30 days)
- [ ] Keywords: "large language model", "multimodal", "reasoning"
- [ ] Save results to data/raw/arxiv_papers.json

## Acceptance Criteria
- [ ] Script queries arXiv successfully
- [ ] Filters by date and category
- [ ] Saves structured JSON with paper metadata
- [ ] Minimum 50 papers per query

## Agent
Literature Review Agent

## Story Points
5""",
        "labels": ["literature-review", "story-points: 5", "iteration-1"]
    },
    {
        "title": "Story 1.3: Model Database",
        "body": """## Description
Create a database to store and query AI model information.

## Handoff from AI Agent
- Schema: `docs/schemas/model-metadata.json`
- Sample data: `data/raw/sample-models.json`

## Tasks
- [ ] Set up database (SQLite/PostgreSQL)
- [ ] Create tables matching schema
- [ ] Build data ingestion script
- [ ] Create API endpoints for CRUD operations
- [ ] Add search/filter functionality

## Acceptance Criteria
- [ ] Database schema created
- [ ] API supports: list, get, create, update, delete
- [ ] Search by lab, architecture, date range
- [ ] Tests pass
- [ ] Documentation updated

## Tech Stack
- Python FastAPI
- SQLAlchemy ORM
- Pydantic models

## Team
Dev Team

## Story Points
8""",
        "labels": ["dev-team", "story-points: 8", "iteration-1"]
    },
    {
        "title": "Story 1.4: Set up llm-wiki",
        "body": """## Description
Initialize and configure llm-wiki knowledge base for the research team.

## Tasks
- [ ] Initialize llm-wiki in wiki/ directory
- [ ] Configure categories (models, benchmarks, labs, architectures)
- [ ] Set up auto-ingestion from agents
- [ ] Document wiki structure

## Acceptance Criteria
- [ ] llm-wiki initialized
- [ ] Config file created: `wiki/.llm-wiki-config.yaml`
- [ ] Category directories created
- [ ] README documented

## Agent
Literature Review Agent

## Story Points
2""",
        "labels": ["literature-review", "story-points: 2", "iteration-1"]
    },
    {
        "title": "Story 1.5: Knowledge Categories",
        "body": """## Description
Create initial content structure for wiki categories.

## Tasks
- [ ] Create template files for each category
- [ ] Document category structure
- [ ] Add placeholder content for major labs
- [ ] Link to relevant resources

## Acceptance Criteria
- [ ] All 7 categories have README.md
- [ ] Templates created for model entries
- [ ] Lab profiles created for top 6 labs
- [ ] Cross-links between categories

## Agent
Literature Review Agent

## Story Points
2""",
        "labels": ["literature-review", "story-points: 2", "iteration-1"]
    }
]

for issue in issues:
    cmd = [
        'curl', '-s', '-X', 'POST',
        '-H', f'Authorization: token {token}',
        '-H', 'Accept: application/vnd.github.v3+json',
        f'https://api.github.com/repos/{user}/{repo}/issues',
        '-d', json.dumps(issue)
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if '"number":' in result.stdout:
        number = json.loads(result.stdout)['number']
        print(f'✓ Created issue #{number}: {issue["title"]}')
    else:
        print(f'✗ Failed: {issue["title"]} - {result.stdout[:100]}')
EOF

echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Repository: https://github.com/$GITHUB_USER/$REPO_NAME"
echo ""
echo "Next steps:"
echo "1. Visit your repository at the URL above"
echo "2. Go to Projects → Create a new project (Board template)"
echo "3. Add the 5 issues to your project board"
echo "4. Configure branch protection (Settings → Branches)"
echo "5. Invite team members (Settings → Manage access)"
echo ""
echo "Ready to start Iteration 1!"
