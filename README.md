# AI PM Exploration Toolkit 🧪

> **Proof-of-Life Probes for product managers**
> Show before Tell, Touch before Sell. Prototype product ideas at the speed of thought.

## Philosophy

*"The most expensive way to test your idea is to build production-quality software."* — Jeff Patton

Every prototype tells a story. Some whisper feasibility. Others lie beautifully and confidently. As a strategic PM, you need **Proof-of-Life (PoL) Probes** — lightweight, disposable, narrow in scope, and brutally honest.

**The Rule:** *Use the cheapest prototype that tells the harshest truth. If it doesn't sting, it's probably just theater.*

**Five Flavors of PoL Probes:**
- **Feasibility Checks** — 1–2 day spike-and-delete tests with AI assistance
- **Task-Focused Tests** — Validate make-or-break user moments without friction
- **Narrative Prototypes** — Loom-style walkthroughs and explainer videos that earn "hell yes"
- **Synthetic Data Simulations** — Model system behavior without burning prod
- **Vibe-Coded Probes** — Fake frontend + semi-plausible backend for real user signals

*Vibe First. Validate Fast. Verify Fit.*

## The Four Pillars: Education → Experimentation → Exploration → Explanation

These four words perfectly capture the core value loop of the AI PM Exploration Toolkit. It's a journey that starts with a need for **Education** and ends with the ability to provide a powerful **Explanation**.

### 🎓 1. Education
**Your Personal AI Classroom**: This is the primary goal of the toolkit - to serve as a personal, private classroom for the strategic PM who feels they are falling behind the AI curve. 

* **Problem Solved:** Directly combats the feeling of being "AI illiterate" and bewildered by jargon like 'evals' or 'langchain'
* **How the Toolkit Helps:** Provides a safe, local-first sandbox to learn by doing, free from fear of high API costs or exposing sensitive ideas. Built around learning through action with structured guidance and hands-on scenarios.

### 🧪 2. Experimentation  
**Evidence Over Opinion**: The practical method for learning. The toolkit provides a controlled environment where a product manager can form a hypothesis and test it rigorously with data, moving beyond opinion to evidence.

* **Problem Solved:** Eliminates dependency on production systems or real user data to validate assumptions
* **How the Toolkit Helps:** The `aipm experiment` command runs "Synthetic Data Simulations" to model system behavior without burning prod. Generate thousands of realistic user profiles with Faker and Mimesis to test AI features at scale.

### 🔍 3. Exploration
**Discovery Without Limits**: About discovery and building intuition without a rigid hypothesis. For the PM who wants to "tinker" with AI building blocks to understand what's possible.

* **Problem Solved:** Addresses the PM's "OpenAI Curiosity" and the feeling of not knowing where to start
* **How the Toolkit Helps:** 40+ tools ready out-of-the-box. Launch Jupyter Lab with `aipm_lab`, construct AI workflows with Langflow, investigate market data with OpenBB Terminal. Free-form exploration builds foundational understanding.

### 📊 4. Explanation
**Show Before Tell, Touch Before Sell**: The ultimate outcome of the other three pillars. After educating yourself through exploration and experimentation, you're equipped to provide clear, confident, compelling explanations of your product strategy.

* **Problem Solved:** The antidote to being "sandbagged" in meetings and losing control of the narrative
* **How the Toolkit Helps:** Create artifacts of great explanation. `aipm prototype` builds narrative prototypes like walkthrough videos. `aipm_story` creates storyboards. Armed with tangible proofs, explain your vision with self-generated evidence.

## Quick Start

```bash
git clone https://github.com/deanpeters/ai-pm-exploration-toolkit.git
cd ai-pm-exploration-toolkit
chmod +x setup.sh configure-apis.sh
./configure-apis.sh  # Configure API keys (optional but recommended)
./setup.sh           # Install all tools (~15-20 minutes)
```

**🚨 CRITICAL NEXT STEPS:** After setup completes:
```bash
# 1. Follow the complete first-run guide
cat ~/ai-pm-toolkit/FIRST_RUN_GUIDE.md

# 2. Setup GitHub CLI for maximum toolkit power
gh auth login
```

**Done.** You now have a comprehensive AI toolkit with 40+ tools optimized for rapid PoL Probes, market research, and competitive intelligence - offline-first and cost-contained.

> 🆕 **Recent Updates**: Added market research capabilities (OpenBB Terminal, Deep Researcher, Gemini CLI), enhanced with 15+ new tools for workflow automation, prompt testing, synthetic data, AI monitoring, design tools, and comprehensive uninstall support.

## First Experiments to Try

```bash
# Explain the core product value to a skeptical stakeholder
aipm prototype "Explain our product value prop to a skeptical stakeholder"

# Validate the real friction in an onboarding flow
aipm fast "Identify most likely frustration points in our first-time user onboarding"

# Simulate behavior across pricing tiers
aipm experiment "Generate synthetic user journeys for 3 pricing tiers over 14 days"

# Prototype an AI teammate concept
aipm compete "Build a vibe-coded mockup of an AI assistant inside our support dashboard"

# Spike feasibility of a semantic search enhancement
aipm learn "Evaluate if local embedding-based search is feasible for our document library"
```

## Proof-of-Life Probes

### 🔬 Feasibility Checks
```bash
aipm learn "GenAI prompt chains for customer support automation - is this viable?"
```

### 🎯 Task-Focused Tests
```bash
aipm fast "test this checkout flow field label for conversion drop-off"
```

### 📖 Narrative Prototypes
```bash
aipm prototype "Loom-style walkthrough of AI-powered dashboard experience"
```

### 🧪 Synthetic Data Simulations
```bash
aipm experiment "simulate 10k users hitting our freemium conversion funnel"
```

### 🎨 Vibe-Coded Probes
```bash
aipm compete "fake frontend + semi-plausible backend for competitor analysis"
```

## What You Get

**🎓 Education & Learning Infrastructure:**
- 🦙 **Ollama** — Local AI server (no API costs, safe learning environment)
- 🏠 **LocalAI** — Privacy-first local AI server with OpenAI API compatibility
- 🤖 **DeepSeek R1** — Strategic writing, prompt engineering, and feasibility analysis
- ⚡ **Llama 3.2** — Fast iteration model for rapid learning cycles
- 🛠️ **Aider** — AI coding assistant (learn by building)
- 🎙️ **OpenAI Whisper** — Speech-to-text for transcribing PM meetings and demos
- 📊 **Jupyter Lab** — Data exploration playground for hands-on learning

**🔍 Exploration & Discovery Tools:**
- 📈 **OpenBB Terminal** — Financial research and market data exploration
- 🔍 **Local Deep Researcher** — AI-powered research automation for discovery
- 💎 **Gemini CLI** — Google's AI model for advanced market exploration
- 🌊 **Langflow** — Visual LLM application builder for intuitive exploration
- 🎨 **Gradio** — Interactive ML interface builder for rapid AI app prototyping
- 🔗 **n8n** — Workflow automation platform for process discovery
- 🔧 **ToolJet** — Low-code app builder for rapid prototyping
- 💬 **Typebot** — Conversational form/chatbot builder
- 💻 **VS Code + Continue** — Enhanced IDE with AI coding assistant
- 🤖 **Continue Extension** — Local AI coding help for exploration

**🧪 Experimentation & Testing:**
- 🎯 **promptfoo** — LLM evaluation framework for systematic testing
- 🔧 **prompttools** — Python-based prompt experimentation toolkit
- 🔬 **Phoenix Arize** — AI observability and ML model evaluation platform
- 📊 **Faker** — Basic synthetic data generation for testing
- 🎭 **Mimesis** — Advanced synthetic data with localization
- 🧬 **Gretel** — AI-powered synthetic data platform for complex scenarios
- 🤖 **ChatterBot** — Machine learning conversational engine for user testing
- 👥 **persona-chat CLI** — Custom persona-based chat interface
- 🔬 **LangSmith** — LLM application development and monitoring
- 📊 **Arize** — ML observability platform for AI features

**📊 Explanation & Storytelling:**
- 🎨 **Excalidraw** — Hand-drawn style diagrams for visual explanations
- 🖌️ **Penpot** — Open-source design tool for creating compelling visual narratives
- 📝 **MarkText** — Beautiful WYSIWYG markdown editor for PoL Probe documentation
- ⚡ **Pulsar** — Advanced text editor for technical documentation and code
- 🎨 **Gradio** — Interactive demo builder for stakeholder presentations
- 📖 **Wonder Unit Storyboarder** — Digital storyboarding for narrative creation
- 🧠 **Obsidian** — Knowledge management with idea linking for structured explanations
- 🔌 **MCP Servers** — Model Context Protocol for enhanced AI integration
- 🦙 **llama-cpp-agent** — Local AI agent with advanced tool calling
- 🛠️ **devon-agent** — AI software engineering automation

**Additional Local Tools:**
- 🎙 **pyttsx3** — Offline text-to-speech for narrated walkthroughs
- 🖼 **mermaid-cli** — Markdown to diagram for user journeys, flows
- 📽 **ffmpeg** — Assembles video assets from frames + audio
- 🌐 **shoelace + htmx** — HTML scaffolding for interactive demos

**Organized PM Workspace:**
```
~/ai-pm-toolkit/
├── toolkit-config.yaml        # Comprehensive tool configuration
├── static/lib/                 # Local JS libraries (shoelace, htmx)
├── experiments/                # Synthetic data simulations and wind tunnel testing
├── prototypes/                 # Narrative walkthroughs and vibe-coded probes
├── data/                       # Generated datasets for assumption testing
├── insights/                   # De-risked decisions and validated assumptions
├── notebooks/                  # Feasibility spikes and technical exploration
├── workflow-tools/             # Docker configs for n8n, ToolJet, Typebot
├── prompt-testing/             # Prompt evaluation configs and results
├── synthetic-data/             # Persona generation and test data
├── monitoring/                 # AI performance monitoring and reports
├── design/                     # Storyboards, diagrams, and visual assets
├── obsidian-vault/             # Knowledge management and linked ideas
├── mcp-servers/                # Model Context Protocol servers and AI agents
├── market-research/            # OpenBB Terminal reports and competitive analysis
└── competitive-intel/          # Deep research outputs and market insights
```

## Enhanced Features (Optional)

Run `./configure-apis.sh` to enable:
- Cloud API models (Claude, OpenAI, M365 Copilot, Gemini)
- Advanced strategic analysis and market research
- Competitive intelligence with GitHub, Perplexity, financial data APIs
- 10M+ tokens/month via free API tiers
- OpenBB Terminal with financial data access
- Automated research workflows with Local Deep Researcher

## Data Exploration
```bash
aipm_lab
```
Launches Jupyter Lab at [http://localhost:8888](http://localhost:8888) for data slicing, synthetic persona modeling, or feasibility scaffolding.

## Requirements

- **macOS** (Intel or Apple Silicon)
- **10 GB free disk space**
- **Internet** (only for setup)

> *Everything runs locally after install.* No subscriptions required beyond what you already have.

## Real PoL Probe Examples: The 4E Framework in Action

### 🎓 Education: Learn AI Through Hands-On Practice
```bash
aipm learn "spike feasibility for using LLMs in moderation workflows"
aipm_lab                                 # Jupyter playground for AI experimentation
aipm_obsidian vault                      # Knowledge management for learning
# Build understanding through guided exploration and safe experimentation
```

### 🔍 Exploration: Discover What's Possible  
```bash
aipm_workflows                           # Start all workflow tools for discovery
aipm_market                              # Explore market research capabilities
aipm_openbb                              # Investigate financial data and trends
# Then access visual builders:
# • Langflow (localhost:7860) - Visual LLM apps
# • n8n (localhost:5678) - Workflow automation  
# • ToolJet (localhost:8082) - Internal tools
# • Typebot (localhost:8083) - Conversational forms
```

### 🧪 Experimentation: Test Hypotheses with Data
```bash
aipm experiment "simulate 50k concurrent usage on AI feature"
aipm_prompts eval                        # Test prompts systematically
aipm_data full                           # Generate synthetic datasets
aipm_personas generate --count 100       # Create test user personas
# Generate evidence, not opinions
```

### 📊 Explanation: Show Before Tell, Touch Before Sell
```bash
aipm prototype "generate explainer video of smart alerting flow"
aipm fast "test this onboarding step for friction"
aipm compete "build a fake product dashboard with AI wiring"  
aipm_story template feature-demo         # Create visual narratives
aipm_design web                          # Generate diagrams for stakeholders
# Create artifacts that turn skepticism into buy-in
```

### Synthetic Data Generation
```bash
aipm_data full                           # Generate complete dataset
aipm_personas generate --count 50        # Create user personas
aipm_personas chat --scenario onboarding # Generate conversations
```

### AI Monitoring & Analysis
```bash
aipm_monitor start                       # Initialize monitoring
aipm_monitor dashboard                   # View performance metrics
aipm_monitor report                      # Generate insights report
```

### Design & Storytelling
```bash
aipm_design web                          # Launch Excalidraw
aipm_story template feature-demo "new-ai-feature"  # Create storyboard
aipm_story export "new-ai-feature"       # Export as PDF/PNG
```

### Market Research & Competitive Intelligence
```bash
aipm_market research "competitor analysis"     # Launch OpenBB Terminal research
aipm_research deep "fintech trends 2024"       # Deep research automation
aipm_gemini market "AI product landscape"      # Advanced market analysis
aipm_competitive report "startup funding"      # Generate competitive reports
```

### Knowledge Management & AI Integration
```bash
aipm_obsidian vault                      # Open AI PM knowledge vault
aipm_obsidian new-probe "ai-feature-test" # Create new PoL Probe with templates
aipm_mcp start                           # Start MCP servers for enhanced AI
aipm_mcp status                          # Check MCP server status
```

## Quick Command Reference

### Essential Commands
```bash
# Core PoL Probes
aipm learn "technical feasibility check"
aipm fast "user friction validation"  
aipm prototype "narrative demonstration"
aipm experiment "synthetic data simulation"
aipm compete "vibe-coded testing probe"

# Tool Categories
aipm_workflows      # Visual/low-code builders
aipm_prompts        # Prompt engineering & testing
aipm_data          # Synthetic data generation
aipm_personas      # User persona creation
aipm_monitor       # AI performance monitoring
aipm_design        # Diagram and design tools
aipm_story         # Visual storytelling
aipm_market        # Market research & competitive intelligence
aipm_research      # Deep research automation
aipm_gemini        # Advanced AI market analysis
aipm_competitive   # Competitive intelligence reports
aipm_obsidian      # Knowledge management & idea linking
aipm_mcp           # AI integration & agent coordination

# New AI Infrastructure & Specialized Tools
aipm_localai       # Local AI server management
aipm_phoenix       # AI observability & ML monitoring
aipm_gradio        # Interactive ML interface builder
aipm_whisper       # Speech-to-text transcription
aipm_penpot        # Open-source design tool

# Documentation & Writing Tools
aipm_marktext      # Beautiful markdown editor
aipm_pulsar        # Advanced text editor

# Data & Lab Work
aipm_lab           # Launch Jupyter for analysis
```

## Why Local AI for Product Managers?

- **Speed** — No API latency, fast iteration
- **Cost** — Free after install; no per-token billing
- **Privacy** — Product ideas stay on your machine
- **Reliability** — Works offline for travel and workshops
- **Learning** — Total control over PoL probe tools
- **Scale** — From solo PM to enterprise product teams

## Uninstalling

To completely remove the toolkit:

```bash
cd ~/ai-pm-toolkit
./uninstall.sh
```

This will:
- Remove all toolkit files and data (~3GB)
- Stop all running services  
- Clean shell aliases and configurations
- Preserve backups of modified shell files
- Provide optional commands to remove packages

## Contributing

This toolkit is built for **product managers who prototype**. Contribute tools, workflows, or new PoL probe modes that help teams:
- De-risk faster
- Tell better product stories
- Validate with smaller budgets
- Escape "feature theater"

## Closing Philosophy

Traditional PM:
1. Write PRD
2. Pitch roadmap
3. Wait months
4. Launch
5. Learn it's wrong

PoL PM:
1. Spike feasibility
2. Validate friction
3. Prototype narrative
4. Simulate behavior
5. Show, touch, iterate

## Contributing

We welcome contributions that support product managers in their 4E journey! Whether you're submitting tools, documentation improvements, or PM scenarios, we'd love your input.

### 🛠️ Tool Submissions
Have a tool that helps PMs with Education, Experimentation, Exploration, or Explanation? We want to hear about it!

**Requirements for tool submissions:**
- 🏠 **Privacy-first**: Core functionality runs 100% offline
- 🎯 **PM focus**: Clear value for product managers doing PoL Probes  
- 🎓 **4E alignment**: Supports Education, Experimentation, Exploration, or Explanation
- 📖 **Quality docs**: Public installation guide with working example
- 🔒 **Ethical**: AI bias/ethics statement for AI-related tools

### 📝 How to Contribute
1. **Read our [Contributing Guide](CONTRIBUTING.md)** for detailed requirements
2. **Use our evaluation template** to assess your tool against 4E framework  
3. **Submit a GitHub issue** with our tool submission template
4. **Engage in the review process** with maintainers and community

### 🏆 Recognition
We recognize valuable contributors in our README and provide speaking opportunities within the strategic PM community.

### 💡 Suggestions Welcome
Not technical? No problem! Submit tool suggestions via GitHub issues and community members may help with integration.

**See [CONTRIBUTING.md](CONTRIBUTING.md) for complete guidelines.**

---

**🎯 Show before Tell. Touch before Sell.**
**💡 Use the cheapest prototype that tells the harshest truth.**
