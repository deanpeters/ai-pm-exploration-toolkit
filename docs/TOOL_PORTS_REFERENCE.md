# 🔗 AI PM Toolkit - Tool Ports & Direct Access Reference

Quick reference for accessing all web-based tools in your AI PM Toolkit.

## 🚀 Visual Workflow Builders

| Tool | Port | Direct Link | Purpose |
|------|------|-------------|---------|
| **n8n** | 5678 | http://localhost:5678 | Workflow automation & integration |
| **Langflow** | 7860 | http://localhost:7860 | Visual AI application builder |
| **ToolJet** | 8082 | http://localhost:8082 | Low-code dashboard & app builder |
| **Typebot** | 3001 | http://localhost:3001 | Conversational chatbot builder |

## 📊 Data & Analysis Tools

| Tool | Port | Direct Link | Purpose |
|------|------|-------------|---------|
| **Jupyter Lab** | 8888 | http://localhost:8888 | Data analysis & notebook environment |
| **OpenBB Terminal** | - | `openbb-terminal` (CLI) | Financial data & market research |

## 🎨 Design & Knowledge Tools

| Tool | Access Method | Link/Command | Purpose |
|------|---------------|--------------|---------|
| **Excalidraw** | Web Browser | https://excalidraw.com | Hand-drawn style diagrams |
| **Obsidian** | Desktop App | `open -a Obsidian ~/ai-pm-toolkit/obsidian-vault` | Knowledge management |

## 🤖 AI & LLM Tools

| Tool | Access Method | Command | Purpose |
|------|---------------|---------|---------|
| **Ollama** | Local API | `ollama list` | Local AI model management |
| **Aider** | CLI | `aider` | AI pair programming |
| **Continue** | VS Code Extension | Open VS Code | AI coding assistant |

## 🔍 Research & Intelligence

| Tool | Access Method | Command | Purpose |
|------|---------------|---------|---------|
| **Gemini CLI** | CLI | `gemini` | Google AI research assistant |
| **Deep Researcher** | CLI | `deep-research` | Automated research workflows |

## 🧪 Testing & Validation Tools

| Tool | Access Method | Command | Purpose |
|------|---------------|---------|---------|
| **promptfoo** | CLI | `promptfoo` | LLM evaluation framework |
| **prompttools** | Python | `python -m prompttools` | Prompt experimentation |

## 🚨 Troubleshooting Common Issues

### Port Conflicts
If a tool won't start due to port conflicts:
```bash
# Check what's using a port
sudo lsof -i :PORT_NUMBER

# Kill process using a port
sudo lsof -ti:PORT_NUMBER | xargs kill

# Kill all processes on common ports
sudo lsof -ti:5678,7860,8082,8888,3001 | xargs kill
```

### Docker Services Not Starting
```bash
# Restart Docker daemon
sudo systemctl restart docker  # Linux
# or restart Docker Desktop on macOS/Windows

# Clean up Docker resources
docker system prune

# Restart specific services
docker-compose down && docker-compose up -d
```

### Tool Not Found Errors
```bash
# Check toolkit status
aipm_status

# Reload shell environment
source ~/.zshrc  # or ~/.bashrc

# Verify installation
which [tool-name]
```

## 📝 Quick Access Commands

### Start All Visual Tools (NEW - Actually Starts Containers!)
```bash
aipm_workflows              # Start all tools and wait for them to be ready
aipm_workflows_status       # Check which tools are running  
aipm_workflows_fix          # Fix common startup issues
aipm_workflows_restart      # Stop and restart all tools
```

### Individual Tool Launches
```bash
aipm_lab                    # Jupyter Lab
aipm_automate              # n8n workflows  
aipm_demo_builder          # ToolJet dashboards
aipm_design                # Excalidraw diagrams
aipm_knowledge             # Obsidian vault
```

### Research & Analysis
```bash
aipm_research_quick "question"     # Quick AI research
aipm_company_lookup TICKER         # Financial intelligence
aipm_market_research               # Comprehensive research tools
```

## 🎯 PM-Specific Use Cases

### Competitive Analysis Dashboard
1. Launch ToolJet: http://localhost:8082
2. Connect data sources via n8n: http://localhost:5678
3. Create visual reports and presentations

### AI-Powered Market Research
1. Use `aipm_research_quick` for instant analysis
2. Launch Jupyter Lab for data exploration: http://localhost:8888
3. Document findings in Obsidian knowledge vault

### Stakeholder Demo Creation
1. Create diagrams with Excalidraw
2. Build interactive prototypes with ToolJet
3. Use Langflow for AI-powered workflows: http://localhost:7860

## 💡 Pro Tips

- **Bookmark these URLs** in your browser for quick access
- **Use `aipm_help`** anytime for the complete command reference
- **Check the learning guide** at `learning-guide/index.html` for hands-on tutorials
- **Join the community** Slack workspace for tips and examples from other PMs

---

**Need help?** Run `aipm_help` or check `PM_FIRST_STEPS.md` for guided tutorials.