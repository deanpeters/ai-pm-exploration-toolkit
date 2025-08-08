# AI PM Exploration Toolkit 🎓

> **The AI Skills Learning Platform for Product Managers**  
> Close your AI PM skills gap through hands-on exploration and practical application. Transform from AI-curious to AI-confident.

## Philosophy

**Primary Mission:** Bridge the AI skills gap that's leaving product managers behind.

As AI transforms product development, strategic PMs need hands-on fluency with AI tools, not just conceptual understanding. This toolkit provides a **safe learning environment** where you can experiment, fail fast, and build confidence with AI-powered product management techniques.

**The Learning Journey:**
- **🎓 Education**: Personal AI classroom for skill building
- **🔍 Exploration**: Discover what's possible through guided experimentation  
- **🧪 Experimentation**: Learn by doing with real product management scenarios
- **📊 Explanation**: Apply new skills to create compelling product narratives

**Secondary Benefit:** Once you've learned the tools, use them for **Proof-of-Life (PoL) Probes** — lightweight, disposable tests that de-risk product decisions without burning engineering resources.

*Learn First. Apply Second. Lead Confidently.*

## Get Started in 2 Steps

**Ready to turn product ideas into evidence? Let's get you set up.**

### Step 1: Download the Toolkit
```bash
git clone https://github.com/deanpeters/ai-pm-exploration-toolkit.git
cd ai-pm-exploration-toolkit
```

### Step 2: Install & Start
```bash
python3 core/installer.py
```

**🎉 You're ready!** The web dashboard will be available at [http://localhost:3000](http://localhost:3000)

## What You Actually Get

**Currently Implemented & Working:**

### 🌐 **Web Dashboard** (Immediate Visual Access)
- **Audio Transcription Tool** - Upload MP3/WAV files for AI-powered PM analysis
- **AI Chat Assistant** - Brainstorm and analyze with local LLMs
- **Data Generation** - Create synthetic personas and test data
- **Market Research** - Company lookup and competitive analysis
- **Workflow Automation** - Access to Docker-based workflow tools

### 💻 **Command Line Tools**
- **Audio Processing**: `python3 shared/audio_transcription.py interview.mp3 --use-case user_interviews`
- **AI Strategic Chat**: `python3 shared/ai_chat.py --mode pm_assistant --interactive`
- **Data Generation**: `python3 shared/data_generator.py --personas 50 --industry saas`
- **Market Research**: `python3 shared/market_research.py --company "CompanyName"`

### 🚀 **AI Consultation Methods** (Multiple Options)

#### External AI Systems (Drag & Drop Context)
Perfect for strategic consultation using Claude, ChatGPT, or Gemini:
1. Upload these 6 context files to your AI project:
   - `AI_CONSULTATION_CONTEXT.md`
   - `TECHNICAL_SPECIFICATION.md` 
   - `CONSULTATION_TEMPLATES.md`
   - `TOOLKIT_CONFIG_REFERENCE.json`
   - `SAMPLE_OUTPUTS.md`
   - `QUICK_CONTEXT_SETUP.md`
2. Use ready-made templates for common PM scenarios
3. Get strategic guidance with full toolkit context

#### Native Goose CLI Integration (Local AI Agent)
Autonomous AI analysis with direct toolkit access:
```bash
# Start strategic analysis session
goose session --name pm_strategy_analysis

# Pre-built workflows for common PM challenges
goose session --name feasibility_check
goose session --name competitor_analysis
goose session --name feature_prioritization
```

#### VS Code + Continue Integration (Developer-Friendly)
AI assistance directly in your development environment:
```bash
# Open toolkit in VS Code
code /Users/deanpeters/ai-pm-exploration-toolkit

# Use Continue shortcuts:
# Ctrl+I: Ask about implementation
# Ctrl+L: Strategic AI discussions
# Ctrl+K: Generate PM documentation
```

#### Visual Documentation (All Users)
Beautiful markdown reading experience with MarkText:
```bash
# Enhanced documentation viewing (requires MarkText installation)
open -a MarkText AI_CONSULTATION_CONTEXT.md

# Or use the aipm_marktext alias if setup.sh was run
aipm_marktext AI_CONSULTATION_CONTEXT.md
```
- **`python3 shared/audio_transcription.py`** - Speech-to-text with PM insights
- **`python3 shared/ai_chat.py`** - Interactive AI conversations
- **`python3 shared/market_research.py`** - Company research automation
- **`python3 shared/data_generator.py`** - Synthetic data creation
- **`./orchestrate-workflows.sh`** - Docker workflow management

### 🎙️ **Audio Intelligence System** (Phase 7.1 Complete)
- **OpenAI Whisper Integration** - Local speech-to-text processing
- **6 PM Workflow Templates**:
  - User Interview Analysis
  - Stakeholder Meeting Summaries
  - Product Demo Feedback
  - Competitive Research Processing
  - PM Voice Memo Conversion
  - Customer Support Analysis
- **Smart Insight Extraction** - Pain points, features, decisions automatically identified
- **Multiple Audio Formats** - MP3, WAV, M4A, FLAC support

### 🤖 **AI Chat & Analysis**
- **Local LLM Integration** - Works with Ollama (qwen2.5, deepseek-r1, llama3.2)
- **PM-Specific Modes** - Strategic analysis, brainstorming, competitive analysis
- **Conversation Management** - Save and resume discussions
- **Model Auto-Detection** - Automatically finds available AI models

### 📊 **Data & Research Tools**
- **Synthetic Data Generation** - Create realistic user personas and datasets
- **Market Research Engine** - Company information lookup and analysis
- **Workflow Automation** - Docker-based n8n and Langflow (ToolJet, Typebot, Penpot have compatibility issues)

### 🦢 **Goose CLI Integration** (Phase 7 Complete)
- **Alternative AI Assistant** - Claude Code-like experience at lower cost
- **Multi-step Task Automation** - Complex PM workflows with AI guidance
- **Local Configuration** - Works with your existing Ollama setup

## Core Tools Status

| Tool | Status | Web Access | CLI Access | Description |
|------|--------|------------|------------|-------------|
| **Audio Intelligence** | ✅ Production | ✅ Upload Interface | ✅ Full CLI | Whisper-powered transcription with PM analysis |
| **AI Chat System** | ✅ Production | ✅ Chat Interface | ✅ Full CLI | Local LLM for PM brainstorming |
| **Data Generation** | ✅ Production | ✅ Web Form | ✅ Full CLI | Synthetic personas and datasets |
| **Market Research** | ✅ Working | ✅ Company Lookup | ✅ Full CLI | Basic company research |
| **Workflow Automation** | ⚠️ Partial | ✅ Status Page | ✅ Docker Scripts | n8n and Langflow (others broken) |

## Real Example Commands

**Audio Processing:**
```bash
# Process a user interview
python3 src/audio_transcription.py interview.mp3 --use-case user_interviews

# Get PM workflow options
python3 src/pm_audio_workflows.py --list
```

**AI Chat:**
```bash
# Start interactive PM assistant
python3 src/ai_chat.py --mode pm_assistant --interactive

# Analyze with specific model
python3 src/ai_chat.py --mode analysis --model qwen2.5
```

**Data Generation:**
```bash
# Generate user personas
python3 src/data_generator.py --personas 50 --industry saas

# Create survey responses
python3 src/data_generator.py --surveys 100 --topic "product satisfaction"
```

**Research & Workflows:**
```bash
# Look up company information
python3 src/market_research.py --company "Notion"

# Start workflow tools
workflows/orchestrate-workflows.sh start
```

## Architecture & Files

**Clean Directory Structure:**
```
ai-pm-exploration-toolkit/
├── 📁 core/                          # System essentials
│   ├── installer.py                   # Main installer
│   ├── toolkit.json                   # Tool configuration
│   └── run_tests.sh                   # System validation
├── 📁 src/                          # Core implementations
│   ├── audio_transcription.py         # Audio processing engine (678 lines)
│   ├── pm_audio_workflows.py          # PM workflow templates (775 lines) 
│   ├── ai_chat.py                     # AI chat system (613 lines)
│   ├── market_research.py             # Research tools (400+ lines)
│   └── data_generator.py              # Data generation (300+ lines)
├── 📁 web/                          # Web dashboard
│   ├── app.py                         # Flask server
│   ├── templates/                     # HTML interfaces
│   └── tools/                         # Web tool pages
├── 📁 workflows/                    # Docker orchestration
│   └── orchestrate-workflows.sh       # Container management
├── 📁 outputs/                      # All generated content (organized!)
│   ├── research/                     # Company research & analysis
│   ├── transcripts/                  # Audio processing results
│   ├── personas/                     # Generated user data
│   ├── conversations/                # AI chat logs
│   └── reports/                      # Analysis reports
├── 📁 docs/                         # User documentation
├── README.md                         # This file
└── CLAUDE.md                         # Project context
```

## Installation Requirements

- **Python 3.8+** with pip
- **10 GB free disk space**
- **Internet** (for initial setup)
- **Docker** (optional, for workflow tools)
- **Git** (for installation)

**Platform Support:**
- ✅ macOS (Intel & Apple Silicon)
- ✅ Linux (Ubuntu 20.04+)
- ⚠️ Windows (basic support)

## Quick Test

After installation, verify everything works:
```bash
# Quick system validation
core/run_tests.sh --quick

# Test core systems individually
python3 src/audio_transcription.py --status
python3 src/ai_chat.py --status  
python3 web/app.py &  # Starts web server

# Open browser to http://localhost:3000
```

## What's Next

**Phase 8 Planned Features:**
- More workflow tool integrations
- Advanced prompt engineering tools
- Real-time collaboration features
- Extended AI model support

## The 4E Framework in Practice

### 🎓 Education: Learn Through Doing
- Use the web dashboard to upload audio and see AI analysis
- Experiment with different AI models through the chat interface
- Generate synthetic data to understand AI capabilities

### 🔍 Exploration: Discover Possibilities  
- Try different audio workflow templates
- Test AI chat with various PM scenarios
- Explore market research capabilities

### 🧪 Experimentation: Test with Data
- Process real user interview recordings
- Generate personas for your product scenarios
- Use AI to analyze competitive intelligence

### 📊 Explanation: Create Compelling Stories
- Use processed insights in stakeholder presentations
- Generate supporting data for product decisions
- Create evidence-based narratives with AI assistance

## Contributing

We welcome contributions that enhance the PM learning and exploration experience:

- **Tool improvements** - Enhance existing functionality
- **New integrations** - Add tools that fit the 4E framework
- **Documentation** - Help other PMs succeed
- **Bug fixes** - Make the toolkit more reliable

See [CONTRIBUTORS_TEST_PLAN.md](CONTRIBUTORS_TEST_PLAN.md) for testing requirements.

## Philosophy in Action

Traditional PM approach:
1. Write requirements
2. Wait for development
3. Launch and hope
4. Learn after release

**AI PM Exploration approach:**
1. Generate synthetic data
2. Process user insights with AI
3. Create evidence-based narratives
4. De-risk decisions before committing resources

---

**🎯 Show before Tell. Touch before Sell.**  
**💡 Use the cheapest prototype that tells the harshest truth.**

*Built for Product Managers who need evidence, not opinions.*