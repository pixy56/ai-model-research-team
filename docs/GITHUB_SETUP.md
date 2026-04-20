# GitHub Setup Guide

## Option 1: Create Repository via Web Interface (Recommended)

### Step 1: Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `ai-model-research-team`
3. Description: `SAFe Agentic Research Team - Tracking the latest AI models`
4. Visibility: Public or Private (your choice)
5. **DO NOT** initialize with README (we already have one)
6. **DO NOT** add .gitignore (we'll add one)
7. **DO NOT** add license (we'll add MIT)
8. Click "Create repository"

### Step 2: Push Local Repository

After creating the empty repository, run these commands locally:

```bash
cd ~/ai-model-research-team

# Add the remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/ai-model-research-team.git

# Push the code
git push -u origin master

# Or if your default branch is main:
git branch -m main
git push -u origin main
```

### Step 3: Verify

Visit `https://github.com/YOUR_USERNAME/ai-model-research-team` to verify the push worked.

---

## Option 2: Using GitHub CLI (gh)

### Install gh

```bash
# macOS
brew install gh

# Ubuntu/Debian
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
sudo chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# Windows
winget install --id GitHub.cli
```

### Authenticate

```bash
gh auth login
# Follow prompts: HTTPS → Paste token
```

### Create Repository

```bash
cd ~/ai-model-research-team
gh repo create ai-model-research-team --public --source . --push
```

---

## Option 3: Using Personal Access Token (PAT)

### Generate PAT

1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes:
   - `repo` (full control of private repositories)
   - `workflow` (update GitHub Action workflows)
4. Generate and copy the token

### Create Repository via API

```bash
# Replace YOUR_TOKEN with your actual token
# Replace YOUR_USERNAME with your GitHub username

export GITHUB_TOKEN=YOUR_TOKEN
export GITHUB_USER=YOUR_USERNAME

# Create repository
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user/repos \
  -d '{
    "name": "ai-model-research-team",
    "description": "SAFe Agentic Research Team - Tracking the latest AI models",
    "private": false,
    "auto_init": false
  }'

# Push existing code
git remote add origin https://$GITHUB_TOKEN@github.com/$GITHUB_USER/ai-model-research-team.git
git push -u origin master
```

---

## Post-Setup Tasks

After pushing to GitHub, complete these tasks:

### 1. Set up Branch Protection (Optional but Recommended)

Go to Settings → Branches → Add rule:
- Branch name pattern: `master` or `main`
- Require pull request reviews before merging: ✓
- Require status checks to pass: ✓

### 2. Enable GitHub Issues

Already enabled by default.

### 3. Create Project Board (Kanban)

1. Go to Projects → New project
2. Select "Board" template
3. Name: "AI Model Research - PI-1"
4. Add columns: Backlog, Ready, In Progress, Review, Done

### 4. Create Issues for Iteration 1

From the repository, create 5 issues:

1. **Story 1.1: Model Metadata Schema** (Label: `literature-review`, Points: 3)
2. **Story 1.2: arXiv Query Automation** (Label: `literature-review`, Points: 5)
3. **Story 1.3: Model Database** (Label: `dev-team`, Points: 8)
4. **Story 1.4: Set up llm-wiki** (Label: `literature-review`, Points: 2)
5. **Story 1.5: Knowledge Categories** (Label: `literature-review`, Points: 2)

### 5. Add Labels

Create these labels:
- `literature-review` (color: #0052CC)
- `data-analysis` (color: #5319E7)
- `writing` (color: #0E8A16)
- `integration` (color: #F9D0C4)
- `dev-team` (color: #B60205)
- `story-points: 2` through `story-points: 13`

---

## Repository URL

Once set up, your repository will be at:
```
https://github.com/YOUR_USERNAME/ai-model-research-team
```

---

## Troubleshooting

### Authentication Failed

If you get "Authentication failed":
1. Check your token has `repo` scope
2. Try HTTPS with token: `git remote set-url origin https://TOKEN@github.com/USER/REPO.git`
3. Or use SSH: `git remote set-url origin git@github.com:USER/REPO.git`

### Branch Name Mismatch

If GitHub expects `main` but you have `master`:
```bash
git branch -m main
git push -u origin main
```

### Large Files

If you have large files in data/, consider:
```bash
git lfs track "data/**/*.json"
git add .gitattributes
```

---

## Next Steps After GitHub Setup

1. ✅ Repository created and code pushed
2. 🔄 Create GitHub Issues for Iteration 1 stories
3. 🔄 Set up Project Board
4. 🔄 Add team members (Settings → Manage access)
5. 🔄 Configure branch protection
6. 🚀 Start Story 1.1 with Literature Review Agent

---

**Questions?** Check the full documentation in `docs/PI-1-Planning.md`