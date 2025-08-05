# 🎓 First Run Guide - Start Learning AI for Product Management

> **Just installed the toolkit?** You're 5 minutes away from your first AI-powered product management win.

---

## ✅ Quick Verification

### 1. Confirm Installation Success
Restart your terminal, then verify your toolkit is ready:

```bash
aipm_help
```

**Expected result:** You'll see a menu of AI-powered PM tools organized by category.

**If you see "command not found":**
- Restart your terminal completely
- Or run: `source ~/.zshrc` (Mac) or `source ~/.bashrc` (Linux)

### 2. Test Your AI Assistant
```bash
aipm_brainstorm
```

**Expected result:** Your AI writing partner (aider) starts and waits for your instruction.

**Type `/quit` to exit when you're done testing.**

---

## 🚀 Your Learning Path

### **New to AI Tools?** → Start Here
Follow the **[PM First Steps Guide](PM_FIRST_STEPS.md)** for a guided 10-minute introduction to AI-powered product management.

### **Want Quick Wins?** → Immediate Value  
Try the **[5-Minute Learning Wins](QUICK_WINS.md)** to build confidence with practical AI skills.

### **Ready to Deep Dive?** → Master Individual Tools
Choose your focus area:
- **[Aider Playbook](playbooks/AIDER_PLAYBOOK.md)** - AI collaboration for strategic thinking
- **[Workflow Playbook](playbooks/WORKFLOW_PLAYBOOK.md)** - Visual building without code
- **[Market Research Playbook](playbooks/MARKET_RESEARCH_PLAYBOOK.md)** - AI-powered competitive intelligence

---

## 🛠️ Optional: Advanced Setup

### Docker Tools (For Visual Workflows)
**Only needed if you want to use n8n, ToolJet, or Typebot:**

1. **Verify Docker is running:**
   ```bash
   docker --version
   ```

2. **If not installed:**
   ```bash
   brew install --cask docker
   ```
   Then open Docker Desktop and wait for it to start (green light in menu bar).

### GitHub Integration (Recommended)
**Enhances toolkit features with GitHub integration:**

```bash
# Install if not already installed
brew install gh

# Authenticate (optional but recommended)
gh auth login
```

---

## 🎯 What You Just Gained

**Your AI PM Skills Toolkit:**
- ✅ **AI Writing Partner** - Collaborate with AI on product briefs, strategies, and documentation
- ✅ **Instant Research Assistant** - Get competitive analysis and market insights in seconds
- ✅ **Visual Workflow Builder** - Create automation and demos without coding
- ✅ **Data Analysis Environment** - Experiment with synthetic data and user modeling
- ✅ **Design Tools** - Create diagrams, mockups, and visual narratives

**The Learning Journey:**
1. **Start simple** - AI brainstorming and document collaboration
2. **Build confidence** - Quick research wins and visual demos  
3. **Master advanced skills** - Comprehensive market research and technical validation
4. **Apply to real work** - Use new AI skills for actual product decisions

---

## 🆘 Troubleshooting

### "Commands don't work"
- **Restart your terminal completely**
- **Check shell configuration:** `echo $SHELL` should show your shell type
- **Manual source:** `source ~/.zshrc` or `source ~/.bashrc`

### "Docker tools won't start"  
- **Open Docker Desktop** and wait for green status indicator
- **Check memory:** Docker needs at least 4GB RAM allocated
- **Restart Docker** if containers seem stuck

### "AI tools give errors"
- **Most tools work offline** - no internet required
- **Some features need API keys** - these are clearly marked as optional
- **Python version:** The toolkit works with Python 3.11+ (you likely have 3.13)

### "Need help with specific tools"
- **Check the playbooks** in the `playbooks/` directory
- **Use command help:** Most commands show usage when run without arguments
- **Start simple:** Focus on basic AI collaboration before advanced features

---

## 🎓 Ready to Learn?

**Your next step:** Choose your learning adventure based on your comfort level and immediate needs.

**Remember:** This is a **learning platform first**. You're not trying to become a developer - you're building AI fluency to become a more effective product manager.

**The goal:** Transform from AI-curious to AI-confident through hands-on practice in a safe environment.