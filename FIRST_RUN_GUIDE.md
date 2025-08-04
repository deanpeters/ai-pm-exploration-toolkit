# 🚀 First Run Guide - Get Your Toolkit Working in 10 Minutes

> **Critical:** If you just ran `setup.sh`, you MUST complete these steps before the toolkit will work properly.

## ✅ Step-by-Step First Run Checklist

### 1. Reload Your Shell (REQUIRED)
The setup script added new commands to your shell, but they won't work until you reload:

```bash
source ~/.zshrc
```

**Test it worked:**
```bash
aipm
```
If you see the AI PM Toolkit help, you're good to go. If you get "command not found", try:
- Close and reopen Terminal
- Or run: `echo 'source ~/.zshrc' >> ~/.zshrc && source ~/.zshrc`

### 2. Start Docker Desktop (REQUIRED for Workflow Tools)
The workflow tools (n8n, ToolJet, Typebot) require Docker to be running:

1. **Open Docker Desktop** (find it in Applications or Spotlight)
2. **Wait for it to fully start** (green light in menu bar)
3. **Verify Docker is running:**
   ```bash
   docker --version
   ```

**If Docker isn't installed:**
```bash
brew install --cask docker
# Then open Docker Desktop and wait for it to start
```

### 3. Setup GitHub CLI (Highly Recommended)
Many toolkit features work better with GitHub authentication:

```bash
# Install GitHub CLI if not already installed
brew install gh
```

**Expected output:**
```
==> Downloading https://formulae.brew.sh/api/formula.jws.json
==> Downloading https://formulae.brew.sh/api/cask.jws.json
==> Fetching downloads for: gh
...
🍺  /opt/homebrew/Cellar/gh/2.76.2: 214 files, 51.3MB
```

```bash
# Login to GitHub (interactive process)
gh auth login
```

**You'll see these prompts - here's what to select:**
```
? Where do you use GitHub? → GitHub.com
? What is your preferred protocol for Git operations on this host? → HTTPS  
? Authenticate Git with your GitHub credentials? → Yes
? How would you like to authenticate GitHub CLI? → Login with a web browser

! First copy your one-time code: 76B1-BEDC
Press Enter to open https://github.com/login/device in your browser...
```

**What happens:**
1. **Copy the code** (e.g., `76B1-BEDC`) - you'll need this
2. **Press Enter** - your browser opens to GitHub
3. **Paste the code** in the GitHub device authentication page
4. **Authorize the GitHub CLI** in your browser
5. **Return to terminal** - you'll see success messages

**Success looks like:**
```
✓ Authentication complete.
- gh config set -h github.com git_protocol https
✓ Configured git protocol
✓ Logged in as [your-username]
```

**Test it worked:**
```bash
gh auth status
# Should show: ✓ Logged in to github.com as [your-username]
```

**Why setup GitHub CLI?**
- **Aider works better**: Can push code changes directly to repos
- **MCP servers install**: Optional advanced features become available  
- **Competitive intelligence**: GitHub API for repo analysis
- **No more auth prompts**: Seamless git operations

### 4. Pre-fetch Docker Images (Recommended)
Download the workflow tool images now to avoid long waits later:

```bash
aipm_docker_setup
```

This will download ~500MB of Docker images and takes 5-10 minutes depending on your internet speed. It's better to do this now than wait during your first demo.

### 5. Test Your First Workflow Tool
Let's make sure everything works:

```bash
aipm_workflows
```

**Expected behavior:**
- Docker containers start (may take 30-60 seconds first time)
- You see URLs for accessing the tools
- No error messages about "Docker daemon" or "connection refused"

**If you see errors:**
- "Cannot connect to Docker daemon" → Docker Desktop isn't running (see Step 2)
- "Command not found: aipm_workflows" → Shell wasn't reloaded (see Step 1)

### 6. Access Your Tools
After `aipm_workflows` succeeds, open these URLs:

- **Langflow:** http://localhost:7860 (Visual LLM builder)
- **n8n:** http://localhost:5678 (Workflow automation) 
- **ToolJet:** http://localhost:8082 (Low-code app builder)
- **Typebot:** http://localhost:8083 (Conversational forms)

**First-time setup notes:**
- **n8n:** Create account with username `aipm` and password `aipm-workflows`
- **Langflow:** May take 30-60 seconds to fully load first time
- **ToolJet/Typebot:** If they show connection errors, wait 2 minutes and refresh

### 7. Quick Smoke Test
Run your first PoL Probe to make sure everything works:

```bash
aipm learn "test basic AI functionality"
```

This should create a new feasibility check in your toolkit workspace.

---

## 🐙 GitHub Integration for Advanced Features

Now that your toolkit is working, let's set up GitHub integration for maximum power:

### Setting Up a GitHub Repo for PoL Probes

Many PMs find it helpful to track their PoL Probes in git for collaboration and history:

```bash
# Navigate to your toolkit
cd ~/ai-pm-toolkit

# Initialize git repo (if not already done)
git init

# Create .gitignore for sensitive files
cat > .gitignore << 'EOF'
# API Keys and secrets
.env
.aipm-apis
**/api-keys.txt

# Docker volumes and data
**/n8n-data/
**/tooljet-data/
**/typebot-data/
**/obsidian-vault/.obsidian/

# Python cache
__pycache__/
*.pyc
.venv/

# Node modules
node_modules/

# OS files
.DS_Store
Thumbs.db
EOF

# Add and commit initial setup
git add .
git commit -m "Initial AI PM Toolkit setup"

# Create GitHub repo (replace 'your-username' with your GitHub username)
gh repo create ai-pm-exploration --private --description "My AI PM PoL Probes workspace"

# Push to GitHub
git branch -M main
git remote add origin https://github.com/your-username/ai-pm-exploration.git
git push -u origin main
```

### Using Aider with Your GitHub Repo

Aider works best when it can push changes to GitHub:

```bash
# Test aider with your repo
cd ~/ai-pm-toolkit
aider --help

# Example: Create a new PoL Probe with aider
aider experiments/new-feature-feasibility.py --message "Create a feasibility spike for new AI feature"

# Aider will:
# 1. Create the file
# 2. Make a git commit  
# 3. Optionally push to GitHub (if you want)
```

### GitHub API Key for Competitive Intelligence

Set up GitHub API access for competitive analysis tools:

```bash
# Create GitHub personal access token
gh auth token

# Add to your API configuration
./configure-apis.sh
# When prompted for GitHub API Key, paste the token from above
```

**What this enables:**
- Repository analysis for competitive intelligence
- Automated market research on open source projects
- Integration with `aipm_competitive` commands

### Working with GitHub in PoL Probes

**Common workflows:**

```bash
# Create a new branch for a PoL Probe
git checkout -b pol-probe/ai-notifications-feasibility

# Work on your probe...
aipm learn "test AI notification delivery feasibility"

# Commit your findings
git add experiments/
git commit -m "PoL Probe: AI notifications feasibility - harsh truth: requires 3 new services"

# Push for team review
git push origin pol-probe/ai-notifications-feasibility

# Create PR for stakeholder review
gh pr create --title "PoL Probe Results: AI Notifications" --body "Key findings from feasibility check..."
```

**Pro tips:**
- Use descriptive branch names: `pol-probe/feature-name`
- Commit early and often during exploration
- Use PR descriptions to share "harsh truths" with stakeholders
- Tag team members for specific expertise: `@jane-doe what do you think of the API limits issue?`

### Writing Great PoL Probe Documentation

The toolkit includes powerful markdown editors for documenting your findings:

```bash
# Beautiful WYSIWYG markdown editor - perfect for stakeholder reports
aipm_marktext experiments/ai-notifications-feasibility.md

# Advanced text editor with Git integration - ideal for technical docs
aipm_pulsar experiments/
```

**MarkText is perfect for:**
- PoL Probe final reports for stakeholders
- Executive summaries with images and formatting
- User story documentation
- "Harsh truth" findings with visual impact

**Pulsar is ideal for:**
- Technical feasibility documentation
- Code snippets and configuration files
- Multi-file project documentation
- Git integration and version control

---

## 🚨 Common First-Run Problems & Solutions

### "Command not found: aipm"
**Problem:** Shell aliases weren't loaded  
**Solution:** Run `source ~/.zshrc` or restart Terminal

### "Cannot connect to the Docker daemon"
**Problem:** Docker Desktop isn't running  
**Solution:** Open Docker Desktop, wait for green light, try again

### "Connection refused" for localhost:8082 or localhost:8083
**Problem:** ToolJet/Typebot containers are still starting up  
**Solution:** Wait 2-3 minutes, then refresh the page

### "FastMCP installation issues" during setup
**Problem:** Python package installation fails  
**Solution:** Ensure Python 3.8+ is installed. FastMCP installs via pip automatically - this is normal for optional advanced features

### n8n shows "502 Bad Gateway"
**Problem:** Container is still initializing  
**Solution:** Wait 60 seconds, refresh page

### Langflow won't load at localhost:7860
**Problem:** Langflow runs independently, not started by aipm_workflows  
**Solution:** Run `aipm_langflow` in a separate terminal window

### GitHub authentication errors during setup
**Problem:** Git prompts for username/password during MCP installation  
**Solution:** This is normal - run `gh auth login` first, or ignore (MCP servers are optional)

### Aider can't push to GitHub
**Problem:** Git credentials not configured  
**Solution:** Run `gh auth login` and ensure your repo has push permissions

### "gh: command not found"
**Problem:** GitHub CLI not installed  
**Solution:** Run `brew install gh`

---

## 🎯 What to Try First

Once everything is working, try these commands to explore the 4E Framework:

### 🎓 Education (Learn AI Through Practice)
```bash
aipm_lab                    # Jupyter playground
aipm_localai               # Start local AI server
aipm learn "feasibility"    # Spike a technical question
```

### 🔍 Exploration (Discover What's Possible)
```bash
aipm_workflows             # Visual workflow builders
aipm_market                # Market research tools
aipm_gradio                # Interactive ML interfaces
```

### 🧪 Experimentation (Test Hypotheses with Data)
```bash
aipm experiment "user behavior simulation"
aipm_data full             # Generate synthetic datasets
aipm_phoenix               # AI model monitoring
```

### 📊 Explanation (Show Before Tell, Touch Before Sell)
```bash
aipm prototype "stakeholder demo"
aipm_marktext              # Write beautiful PoL Probe reports
aipm_penpot                # Design compelling visuals
aipm_design web            # Create diagrams
```

---

## 📞 Still Having Problems?

1. **Check the logs:** Most tools print helpful error messages to the terminal
2. **Restart everything:** Sometimes a fresh start helps:
   ```bash
   # Stop all Docker containers
   docker stop $(docker ps -q)
   # Restart the workflow tools
   aipm_workflows
   ```
3. **Check disk space:** Docker images need ~2GB of free space
4. **Update Docker:** Old Docker versions can cause container issues

---

## ✅ Success! You're Ready

If you completed all steps without errors, you now have:
- 40+ AI tools ready for PoL Probes
- Visual workflow builders for non-technical exploration  
- Local AI servers for privacy-first learning
- Comprehensive market research capabilities
- A structured 4E Framework for becoming AI-confident

**Next:** Read `DOCUMENTATION.md` for comprehensive examples, or try `aipm quickstart` for a guided 5-minute tutorial.

**Remember the philosophy:** *Use the cheapest prototype that tells the harshest truth. If it doesn't sting, it's probably just theater.*