# 🤖 AI PM Toolkit Commands Reference

Complete reference for working AI PM Toolkit commands and consultation methods.

---

## 🚀 AI Consultation Methods

### Multi-Modal AI Integration

The toolkit provides **three consultation pathways** to match your technical comfort level:

#### 1. External AI Systems (Drag & Drop Context)
**Purpose:** Strategic consultation using Claude, ChatGPT, or Gemini  
**Setup:** Upload 6 context files for immediate AI assistance
**Usage:**
```bash
# Files to drag into AI conversation:
AI_CONSULTATION_CONTEXT.md          # Strategic overview
TECHNICAL_SPECIFICATION.md          # Architecture details  
CONSULTATION_TEMPLATES.md           # Ready-to-use prompts
TOOLKIT_CONFIG_REFERENCE.json       # System configuration
SAMPLE_OUTPUTS.md                   # Real examples
QUICK_CONTEXT_SETUP.md              # 30-second setup
```

#### 2. Native Goose CLI Integration (Local AI Agent)
**Purpose:** Autonomous AI analysis with direct toolkit access  
**Usage:**
```bash
# Strategic analysis sessions
goose session --name pm_strategy_analysis
goose session --name feasibility_check
goose session --name competitor_analysis
goose session --name feature_prioritization
goose session --name user_research_analysis
```

#### 3. VS Code + Continue Integration (Developer-Friendly)
**Purpose:** AI assistance directly in development environment  
**Usage:**
```bash
# Open toolkit in VS Code
code /Users/deanpeters/ai-pm-exploration-toolkit

# Continue shortcuts:
# Ctrl+I: Implementation questions
# Ctrl+L: Strategic discussions
# Ctrl+K: Documentation generation
```

---

## 🎯 Working Toolkit Commands

### Audio Intelligence Processing
#### `python3 shared/audio_transcription.py [audio_file] [options]`
**Purpose:** Extract structured PM insights from audio recordings  
**Parameters:**
- `audio_file` (string): Path to MP3/WAV file
- `--use-case` (string): user_interviews, strategy_sessions, feedback_calls
**Usage:**
```bash
python3 shared/audio_transcription.py interview.mp3 --use-case user_interviews
python3 shared/audio_transcription.py --status  # Check system status
```
**Returns:** Structured insights with pain points, feature requests, action items

### AI Strategic Thinking Partner
#### `python3 shared/ai_chat.py [options]`
**Purpose:** Interactive strategic guidance for product decisions  
**Parameters:**
- `--mode` (string): pm_assistant, analysis, planning
- `--interactive` (flag): Enable interactive chat mode
- `--model` (string): qwen2.5, deepseek-r1 (AI model selection)
**Usage:**
```bash
python3 shared/ai_chat.py --mode pm_assistant --interactive
python3 shared/ai_chat.py --mode analysis --model qwen2.5
```
**Returns:** Strategic frameworks, decision structures, investigation approaches

### Synthetic Data Generation
#### `python3 shared/data_generator.py [options]`
**Purpose:** Create realistic user data for assumption testing  
**Parameters:**
- `--personas` (int): Number of personas to generate
- `--industry` (string): saas, ecommerce, fintech, healthcare
- `--role` (string): product_manager, developer, end_user
**Usage:**
```bash
python3 shared/data_generator.py --personas 50 --industry saas
python3 shared/data_generator.py --personas 25 --industry ecommerce --role end_user
```
**Returns:** JSON/CSV files with demographics, pain points, goals, scenarios

### Market Research Automation
#### `python3 shared/market_research.py [options]`
**Purpose:** Competitive intelligence and market analysis  
**Parameters:**
- `--company` (string): Company name to research
- `--industry` (string): Industry sector focus
- `--depth` (string): basic, detailed, comprehensive
**Usage:**
```bash
python3 shared/market_research.py --company "Notion"
python3 shared/market_research.py --industry "project_management" --depth detailed
```
**Returns:** Business model analysis, competitive positioning, strategic insights

#### `aipm experiment [description]`
**Purpose:** Synthetic Data Simulations - Model system behavior at scale  
**Parameters:**
- `description` (string): Simulation scenario to model
**Usage:**
```bash
aipm experiment "simulate 10k users hitting freemium conversion funnel"
aipm experiment "model 50k concurrent usage on AI feature"
```
**Returns:** Synthetic data simulation results and insights  
**Status:** 🚨 **BROKEN** - Currently just echoes description

#### `aipm compete [description]`
**Purpose:** Vibe-Coded Probes - Build convincing fake frontend for testing  
**Parameters:**
- `description` (string): Competitive analysis or prototype to build
**Usage:**
```bash
aipm compete "fake frontend + semi-plausible backend for competitor analysis"
aipm compete "build competitor analysis dashboard"
```
**Returns:** Interactive prototype for user testing  
**Status:** 🚨 **BROKEN** - Currently just echoes description

---

## 🔍 Research & Intelligence

### `aipm_research_quick [query]`
**Purpose:** Instant AI-powered market analysis and research  
**Parameters:**
- `query` (string, required): Research question to analyze
**Usage:**
```bash
aipm_research_quick "AI trends in product management"
aipm_research_quick "competitive landscape for no-code platforms"
```
**Returns:** Expert-level research analysis with strategic insights  
**Status:** 🚨 **BROKEN** - Currently shows usage only

### `aipm_company_lookup [ticker]`
**Purpose:** Financial intelligence on public companies  
**Parameters:**
- `ticker` (string, required): Stock ticker symbol
**Usage:**
```bash
aipm_company_lookup ZOOM
aipm_company_lookup MSFT
```
**Returns:** Financial data, strategic context, competitive position  
**Status:** 🚨 **BROKEN** - Currently shows usage only

### `aipm_market_research`
**Purpose:** Launch comprehensive market research tools  
**Parameters:** None  
**Usage:**
```bash
aipm_market_research
```
**Returns:** Access to OpenBB Terminal and research platforms  
**Status:** 🚨 **BROKEN** - Currently just echoes text

---

## ✍️ AI Collaboration

### `aipm_brainstorm`
**Purpose:** Start AI pair programming session  
**Parameters:** None  
**Usage:**
```bash
aipm_brainstorm
```
**Returns:** Interactive AI coding session with Aider  
**Status:** ✅ **WORKING** - Launches Aider correctly

### `aipm_write [filename]`
**Purpose:** Co-create documents with AI assistance  
**Parameters:**
- `filename` (string, optional): File to create or edit
**Usage:**
```bash
aipm_write product_brief.md
aipm_write
```
**Returns:** AI writing session for document creation  
**Status:** 🚨 **BROKEN** - Currently just shows instruction

### `aipm_prototype_demo [filename]`
**Purpose:** Build interactive demos with AI  
**Parameters:**
- `filename` (string, optional): HTML file to create
**Usage:**
```bash
aipm_prototype_demo dashboard.html
aipm_prototype_demo
```
**Returns:** Interactive demo creation session  
**Status:** 🚨 **BROKEN** - Currently just shows instruction

---

## 🔧 Visual Builders & Automation

### `aipm_workflows`
**Purpose:** Start all visual workflow tools with health checks  
**Parameters:** None  
**Usage:**
```bash
aipm_workflows
```
**Returns:** Running n8n, ToolJet, Langflow with direct access URLs  
**Status:** ✅ **WORKING** - Actually starts containers and waits for readiness

### `aipm_workflows_status`
**Purpose:** Check which workflow tools are running  
**Parameters:** None  
**Usage:**
```bash
aipm_workflows_status
```
**Returns:** Status report of all workflow tools  
**Status:** ✅ **WORKING**

### `aipm_workflows_fix`
**Purpose:** Interactive troubleshooting for workflow issues  
**Parameters:** None  
**Usage:**
```bash
aipm_workflows_fix
```
**Returns:** Interactive menu to resolve common problems  
**Status:** ✅ **WORKING**

### `aipm_workflows_restart`
**Purpose:** Stop and restart all workflow tools  
**Parameters:** None  
**Usage:**
```bash
aipm_workflows_restart
```
**Returns:** Fresh restart of all workflow containers  
**Status:** ✅ **WORKING**

### `aipm_workflows_stop`
**Purpose:** Stop all workflow tools cleanly  
**Parameters:** None  
**Usage:**
```bash
aipm_workflows_stop
```
**Returns:** All workflow containers stopped  
**Status:** ✅ **WORKING**

### `aipm_automate`
**Purpose:** Launch n8n workflow builder  
**Parameters:** None  
**Usage:**
```bash
aipm_automate
```
**Returns:** Direct access to n8n at http://localhost:5678  
**Status:** 🚨 **BROKEN** - Just echoes URL, doesn't ensure n8n is running

### `aipm_demo_builder`
**Purpose:** Launch ToolJet dashboard builder  
**Parameters:** None  
**Usage:**
```bash
aipm_demo_builder
```
**Returns:** Direct access to ToolJet at http://localhost:8082  
**Status:** 🚨 **BROKEN** - Just echoes URL, doesn't ensure ToolJet is running

---

## 📊 Data & Analysis

### `aipm_lab`
**Purpose:** Launch Jupyter Lab data analysis environment  
**Parameters:** None  
**Usage:**
```bash
aipm_lab
```
**Returns:** Jupyter Lab running at http://localhost:8888  
**Status:** ✅ **WORKING** - Actually starts Jupyter Lab

### `aipm_data_generator`
**Purpose:** Generate synthetic data for testing and validation  
**Parameters:** None  
**Usage:**
```bash
aipm_data_generator
```
**Returns:** Interactive synthetic data generation tools  
**Status:** 🚨 **BROKEN** - Currently just echoes text

---

## 🎨 Design & Knowledge

### `aipm_design`
**Purpose:** Create diagrams and mockups  
**Parameters:** None  
**Usage:**
```bash
aipm_design
```
**Returns:** Excalidraw opened for diagram creation  
**Status:** ✅ **WORKING** - Opens Excalidraw in browser

### `aipm_knowledge`
**Purpose:** Knowledge management and idea linking  
**Parameters:** None  
**Usage:**
```bash
aipm_knowledge
```
**Returns:** Obsidian vault opened for knowledge management  
**Status:** ✅ **WORKING** - Opens Obsidian with toolkit vault

---

## 🛠️ System & Utilities

### `aipm_help`
**Purpose:** Display comprehensive command reference  
**Parameters:** None  
**Usage:**
```bash
aipm_help
```
**Returns:** Complete toolkit command reference with examples  
**Status:** ✅ **WORKING**

### `aipm_status`
**Purpose:** Check toolkit installation and component status  
**Parameters:** None  
**Usage:**
```bash
aipm_status
```
**Returns:** System health and installation status report  
**Status:** 🚨 **NOT IMPLEMENTED** - Shows "not implemented yet"

---

## 📊 Command Status Summary

| Status | Count | Commands |
|--------|-------|----------|
| ✅ **Working** | 8 | `aipm_brainstorm`, `aipm_lab`, `aipm_design`, `aipm_knowledge`, `aipm_workflows*`, `aipm_help` |
| 🚨 **Broken/Echo Only** | 11 | `aipm_research_quick`, `aipm_company_lookup`, `aimp_market_research`, `aipm_data_generator`, `aipm_automate`, `aipm_demo_builder`, All PoL commands |
| ⚠️ **Not Implemented** | 1 | `aipm_status` |

## 🔧 Priority Fixes Needed

### **High Priority (User Expects These to Work)**
1. **PoL Probe Framework** - Core value proposition, completely non-functional
2. **Research Commands** - `aipm_research_quick`, `aipm_company_lookup`
3. **Data Generation** - `aipm_data_generator`
4. **Individual Tool Access** - `aipm_automate`, `aipm_demo_builder`

### **Medium Priority**
1. **Writing Commands** - `aipm_write`, `aipm_prototype_demo`
2. **Status Command** - `aipm_status` implementation

---

## 🎯 Expected Behavior vs Current Behavior

### **What Users Expect:**
```bash
aipm_research_quick "AI trends in PM"
# → Should return actual research analysis
```

### **What Actually Happens:**
```bash
aipm_research_quick "AI trends in PM"  
# → "Usage: aipm_research_quick "your research question""
# → User gets frustrated and stops using toolkit
```

This documentation serves as both an API reference and a bug tracking system for fixing the broken command implementations.