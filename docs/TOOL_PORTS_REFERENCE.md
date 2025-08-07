# 🔗 AI PM Toolkit - Working Tools & Access Reference

Quick reference for accessing all currently implemented tools in your AI PM Toolkit.

## 🌐 Core Web Dashboard

| Tool | Port | Direct Link | Status | Purpose |
|------|------|-------------|---------|---------|
| **AI PM Dashboard** | 3000 | http://localhost:3000 | ✅ Working | Main interface for all tools |

**Start the dashboard:**
```bash
python3 web/app.py
```

## 🛠️ Working Tools (Current Implementation)

### 🎙️ Audio Intelligence
- **Web Access:** http://localhost:3000 → Audio Transcription
- **CLI Access:** `python3 src/audio_transcription.py`
- **Purpose:** Speech-to-text with PM-specific insight extraction
- **Formats:** MP3, WAV, M4A, FLAC, AAC, OGG
- **Features:** 6 PM workflow templates, pain point extraction, decision tracking

### 🤖 AI Chat Assistant
- **Web Access:** http://localhost:3000 → AI Chat Assistant
- **CLI Access:** `python3 src/ai_chat.py --mode pm_assistant --interactive`
- **Purpose:** Strategic PM brainstorming and analysis
- **Models:** qwen2.5, deepseek-r1, llama3.2 (via Ollama)
- **Features:** PM-specific modes, conversation saving

### 📊 Data Generation
- **Web Access:** http://localhost:3000 → Data Generation
- **CLI Access:** `python3 src/data_generator.py`
- **Purpose:** Synthetic personas and test data creation
- **Features:** Industry-specific personas, survey data, CSV/JSON export

### 🔍 Market Research
- **Web Access:** http://localhost:3000 → Market Research
- **CLI Access:** `python3 src/market_research.py`
- **Purpose:** Company lookup and competitive analysis
- **Features:** Business intelligence, financial data, competitive positioning

### 🐳 Workflow Automation
- **Web Access:** http://localhost:3000 → Workflow Automation
- **CLI Access:** `./orchestrate-workflows.sh`
- **Purpose:** Docker-based workflow tools management
- **Features:** n8n, Langflow, ToolJet orchestration (when Docker containers are running)

## 💻 Command Line Tools (All Working)

### Audio Processing Commands
```bash
# Check Whisper status
python3 src/audio_transcription.py --status

# List PM workflow templates
python3 src/pm_audio_workflows.py --list

# Process audio file
python3 src/audio_transcription.py audio.mp3 --use-case user_interviews
```

### AI Chat Commands
```bash
# Start interactive PM assistant
python3 src/ai_chat.py --mode pm_assistant --interactive

# Strategic analysis mode
python3 src/ai_chat.py --mode analysis --model qwen2.5

# Check available AI models
python3 src/ai_chat.py --status
```

### Data Generation Commands
```bash
# Generate user personas
python3 src/data_generator.py --personas 50 --industry saas

# Create survey responses
python3 src/data_generator.py --surveys 100 --topic "product satisfaction"

# Get help with options
python3 src/data_generator.py --help
```

### Market Research Commands
```bash
# Research a company
python3 src/market_research.py --company "Notion"

# Industry analysis
python3 src/market_research.py --industry "productivity software"

# Get research options
python3 src/market_research.py --help
```

### Workflow Management Commands
```bash
# Check workflow tools status
./orchestrate-workflows.sh status

# Start Docker workflow containers
./orchestrate-workflows.sh start

# Stop all workflow containers
./orchestrate-workflows.sh stop
```

## 🐳 Docker Workflow Tools (When Running)

**Start workflow tools:**
```bash
./orchestrate-workflows.sh start
```

| Tool | Port | Direct Link | Purpose |
|------|------|-------------|---------|
| **n8n** | 5678 | http://localhost:5678 | Workflow automation |
| **Langflow** | 7860 | http://localhost:7860 | Visual AI app builder |
| **ToolJet** | 8082 | http://localhost:8082 | Low-code app builder |

**Note:** These tools require Docker and must be started via the orchestration script.

## 🔍 System Status & Testing

### Check Everything is Working
```bash
# Quick system test (2 minutes)
./run_tests.sh --quick

# Full system test (15 minutes)
./run_tests.sh --full

# New user experience test
./run_tests.sh --new-user
```

### Individual Status Checks
```bash
# Audio system status
python3 src/audio_transcription.py --status

# AI chat system status
python3 src/ai_chat.py --status

# Web dashboard status (after starting)
curl -s http://localhost:3000/api/status

# Workflow tools status
./orchestrate-workflows.sh status
```

## 🚨 Troubleshooting Common Issues

### Web Dashboard Not Loading
```bash
# Start the dashboard
python3 web/app.py

# Check if port 3000 is busy
lsof -ti:3000 | xargs kill 2>/dev/null || true

# Then restart
python3 web/app.py
```

### Audio Processing Issues
```bash
# Check Whisper installation
python3 src/audio_transcription.py --status

# Reinstall if needed
pip3 install openai-whisper
```

### AI Chat Not Working
```bash
# Check if Ollama is running
curl -s http://localhost:11434/api/tags

# Start Ollama if needed
ollama serve &

# Check available models
ollama list
```

### Docker Workflow Tools Issues
```bash
# Check Docker is running
docker --version && docker info

# Clean up containers
./orchestrate-workflows.sh stop
docker system prune -f

# Restart workflow tools
./orchestrate-workflows.sh start
```

## 📋 What's Currently NOT Implemented

**Tools mentioned in old documentation but not yet working:**
- Most `aipm_*` command aliases (only infrastructure exists)
- OpenBB Terminal integration
- Jupyter Lab auto-launch
- Gemini CLI integration
- promptfoo/prompttools setup
- Obsidian vault automation
- Excalidraw local hosting

**These may be implemented in future phases.**

## 🎯 Real PM Workflows (What Actually Works)

### User Research Analysis
1. **Record user interview** on your phone
2. **Upload to:** http://localhost:3000 → Audio Transcription
3. **Select:** "User Interview Analysis" workflow
4. **Get:** Structured insights with pain points and feature requests

### Competitive Intelligence
1. **Open:** http://localhost:3000 → Market Research
2. **Enter:** Competitor company name
3. **Get:** Business model analysis and competitive positioning

### Strategic Planning Support
1. **Open:** http://localhost:3000 → AI Chat Assistant
2. **Ask:** Strategic questions about your product challenges
3. **Get:** Structured frameworks and analysis approaches

### Synthetic Data for Testing
1. **Open:** http://localhost:3000 → Data Generation
2. **Generate:** User personas for your industry
3. **Export:** CSV/JSON for use in your existing tools

## 💡 Pro Tips for Current Implementation

- **Start with the web dashboard** - Most approachable interface
- **Bookmark http://localhost:3000** for quick access
- **Use command line for batch processing** - More powerful for multiple files
- **Run quick tests regularly** - `./run_tests.sh --quick` catches issues early
- **Focus on audio intelligence first** - It's the most fully-featured tool currently

---

**This reference reflects the current working state of the toolkit.** For future planned features, see the main README.md file.