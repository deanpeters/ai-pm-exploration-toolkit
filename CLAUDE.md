# Claude Code Context - AI PM Exploration Toolkit

## Project Overview
This is the **AI PM Exploration Toolkit** - implementing Dean Peters' **Proof-of-Life (PoL) Probes** framework for product managers. When users run `/init` here, you're helping with a toolkit designed for PMs who need lightweight, disposable, brutally honest **tiny acts of discovery (TADs)** that de-risk decisions without burning engineering time.

**Core Philosophy**: *"The most expensive way to test your idea is to build production-quality software."* ~ Jeff Patton

## The Four Pillars: Education → Experimentation → Exploration → Explanation

The toolkit follows a structured value loop that transforms PMs from AI-curious to AI-confident:

1. **🎓 Education**: Personal AI classroom - combat AI illiteracy through safe, local-first learning
2. **🧪 Experimentation**: Evidence over opinion - test hypotheses with synthetic data, not production systems  
3. **🔍 Exploration**: Discovery without limits - tinker with AI building blocks to understand possibilities
4. **📊 Explanation**: Show before tell - create compelling narratives that turn skepticism into stakeholder buy-in

These aren't MVPs. They're reconnaissance missions to avoid feature hostage negotiations with HiPPOs and swoop-n-poop seagull managers.

## Target User Profile

**Product Managers** who need to de-risk assumptions before committing engineering resources. They combine:
- **Marty Cagan** - Strategic, outcomes-obsessed product thinking
- **DHH** - "Just ship it" mentality, prefer working software over documentation
- **OpenAI Curiosity** - Constantly exploring AI/ML possibilities for product applications
- **Dean Peters PoL Mindset** - Use the cheapest prototype that tells the harshest truth

These are **not** traditional agile product owners managing backlogs. They're leaders who need to avoid building something nobody wants by validating assumptions with lightweight, disposable probes before making roadmap commitments.

## Core Architecture

### AI Infrastructure (Local-First)
- **Ollama** - Local AI server (privacy, speed, no API costs)
- **DeepSeek R1 7B** - Primary model for complex product analysis and prototyping
- **Llama 3.2 3B** - Fast model for rapid product iteration
- **Aider** - AI coding assistant for building product prototypes
- **Jupyter Lab** - Data exploration and synthetic user generation

### Market Research & Competitive Intelligence
- **OpenBB Terminal** - Open-source financial research and market data platform
- **Local Deep Researcher** - AI-powered research automation for competitive analysis
- **Gemini CLI** - Google's AI model for advanced market research and analysis

### Visual/Low-Code Workflow Tools
- **Langflow** - Visual LLM application builder for non-technical PMs
- **n8n** - Workflow automation platform (Docker-based)
- **ToolJet** - Low-code app builder for internal tools
- **Typebot** - Conversational form/chatbot builder

### Development & AI Coding
- **VS Code + Continue** - Enhanced IDE with AI coding assistant
- **Continue Extension** - Local AI coding help integrated with VS Code

### Prompt Engineering & Testing
- **promptfoo** - LLM evaluation framework for systematic testing
- **prompttools** - Python-based prompt experimentation toolkit

### Synthetic Data & AI Training
- **Faker** - Basic synthetic data generation (Python & CLI)
- **Mimesis** - Advanced synthetic data with localization
- **Gretel** - AI-powered synthetic data platform
- **ChatterBot** - Machine learning conversational engine
- **persona-chat CLI** - Custom persona-based chat interface

### AI Monitoring & Observability
- **LangSmith** - LLM application development and monitoring
- **Arize** - ML observability platform for AI features

### Design & Storytelling
- **Excalidraw** - Hand-drawn style diagrams (web-based)
- **Wonder Unit Storyboarder** - Digital storyboarding tool

### Knowledge Management & AI Integration
- **Obsidian** - Knowledge management with idea linking and graph visualization
- **MCP Servers** - Model Context Protocol for enhanced AI integration
- **llama-cpp-agent** - Local AI agent with advanced tool calling
- **devon-agent** - AI software engineering automation

### Exploration Workspace
```
~/ai-pm-toolkit/
├── experiments/          # Synthetic data simulations and wind tunnel testing
├── prototypes/           # Narrative walkthroughs and vibe-coded probes
├── data/                # Generated datasets for assumption testing
├── insights/            # De-risked decisions and validated assumptions
├── notebooks/           # Feasibility spikes and technical exploration
├── workflow-tools/      # Docker configs for n8n, ToolJet, Typebot
├── prompt-testing/      # Prompt evaluation configs and results
├── synthetic-data/      # Persona generation and test data
├── monitoring/          # AI performance monitoring and reports
├── design/              # Storyboards, diagrams, and visual assets
├── obsidian-vault/      # Knowledge management and linked ideas
├── mcp-servers/         # Model Context Protocol servers and AI agents
├── market-research/     # OpenBB Terminal reports and competitive analysis
├── competitive-intel/   # Deep research outputs and market insights
└── aipm                 # Main PoL Probe interface
```

## Development Philosophy

*"The most expensive way to test your idea is to build production-quality software."* ~ Jeff Patton

**Use the cheapest prototype that tells the harshest truth. If it doesn't sting, it's probably just theater.**

Users need **Proof-of-Life Probes** - lightweight, disposable, narrow in scope, brutally honest. These tiny acts of discovery (TADs) exist to de-risk decisions, not justify ideas from HiPPOs or swoop-n-poop seagull managers.

**Five Flavors of PoL Probes:**
1. **Feasibility Checks** - 1-2 day spike-and-delete tests with AI assistance
2. **Task-Focused Tests** - Validate make-or-break user moments without friction
3. **Narrative Prototypes** - Loom walkthroughs and explainer videos that earn "hell yes"
4. **Synthetic Data Simulations** - Model system behavior without burning prod
5. **Vibe-Coded Probes** - Fake frontend + semi-plausible backend for real user signals

## Core Commands (Currently Implemented)

The main interface supports the **4E Framework** through both web dashboard and command line:

### 🎓 Education Commands (Learn AI Through Practice)
**Web Dashboard:** [http://localhost:3000](http://localhost:3000)
- **Audio Intelligence** - Learn by processing real user interviews and meetings
- **AI Chat Assistant** - Practice strategic thinking with AI conversation partner
- **Data Generation** - Understand AI capabilities through synthetic data creation

**Command Line:**
- `python3 shared/audio_transcription.py --status` - Check audio processing capabilities
- `python3 shared/ai_chat.py --mode pm_assistant --interactive` - Start AI learning session
- `python3 web/app.py` - Launch learning dashboard

### 🔍 Exploration Commands (Discover What's Possible)  
**Web Dashboard Tools:**
- **Market Research** - Explore competitive intelligence capabilities
- **Workflow Automation** - Discover Docker-based tool orchestration
- **Audio Workflow Templates** - Explore 6 different PM use case templates

**Command Line:**
- `python3 shared/market_research.py --company "CompanyName"` - Explore research capabilities
- `./orchestrate-workflows.sh status` - Discover workflow tool options
- `python3 shared/pm_audio_workflows.py --list` - Explore PM workflow templates

### 🧪 Experimentation Commands (Test Hypotheses with Data)
**Data Generation & Testing:**
- `python3 shared/data_generator.py --personas 50 --industry saas` - Generate test personas
- `python3 shared/audio_transcription.py audio.mp3 --use-case user_interviews` - Test audio analysis
- `python3 shared/ai_chat.py --mode analysis --model qwen2.5` - Test strategic analysis

**System Testing:**
- `./run_tests.sh --quick` - Test all systems in 2 minutes
- `./run_tests.sh --new-user` - Test first-time user experience
- `./run_tests.sh --full` - Complete system validation

### 📊 Explanation Commands (Show Before Tell, Touch Before Sell)
**Create Compelling Artifacts:**
- **Web Interface** - Generate professional outputs through dashboard
- **Audio Insights Export** - Turn recordings into stakeholder-ready summaries
- **Synthetic Data Export** - Create supporting evidence with generated personas
- **AI Analysis Output** - Structured strategic frameworks for presentations

**Command Line Output Formats:**
- All tools support `--help` for usage guidance
- Audio processing creates structured PM insight reports
- Data generation exports CSV/JSON for existing presentation tools
- AI chat saves conversations for documentation

## Real Working Examples: PoL Probes in Action

### 1. Audio Intelligence for User Research
**Current Implementation**: `python3 shared/audio_transcription.py interview.mp3 --use-case user_interviews`
**Purpose**: Extract structured insights from user interviews without manual transcription
**What It Does**: Processes audio → Identifies pain points, feature requests, user goals automatically
**Typical Use**: "Turn 1-hour user interview into structured insights in 2 minutes"

### 2. AI Strategic Thinking Partner
**Current Implementation**: `python3 shared/ai_chat.py --mode pm_assistant --interactive`
**Purpose**: Get structured strategic guidance for product decisions
**What It Does**: Interactive AI conversations → Strategic frameworks, investigation approaches, decision structures
**Typical Use**: "Help me create a framework to investigate churn rate issues"

### 3. Synthetic Data for Assumption Testing
**Current Implementation**: `python3 shared/data_generator.py --personas 50 --industry saas`
**Purpose**: Generate realistic user data to test concepts without waiting for real users
**What It Does**: Creates personas → Demographics, pain points, goals, scenarios ready for analysis
**Typical Use**: "Generate 50 SaaS user personas to test feature prioritization framework"

### 4. Competitive Intelligence Automation
**Current Implementation**: `python3 shared/market_research.py --company "CompanyName"`
**Purpose**: Instant competitive analysis and market positioning research
**What It Does**: Company lookup → Business model analysis, competitive strengths/weaknesses, market position
**Typical Use**: "Get competitive intelligence on Notion for partnership evaluation"

### 5. Voice Thoughts to Structured Analysis
**Current Implementation**: Web dashboard → Audio Transcription → PM Voice Memo Processing
**Purpose**: Turn scattered voice thoughts into organized, actionable PM insights
**What It Does**: Voice memo → Structured problem statements, solutions, action items for presentations
**Typical Use**: "Convert daily voice notes into stakeholder-ready strategic insights"

## When Helping Users: Apply the 4E Framework

### 🎓 Education Requests (Building AI Literacy)
**Goal**: Transform AI-curious PMs into AI-confident strategic leaders
- Create safe learning environments with local-first tools
- Provide hands-on scenarios that build intuition through action
- Focus on combating "AI illiteracy" and jargon confusion
- Guide through structured learning paths with immediate feedback
- Example: "Help me understand how AI can help with user research" → Use audio intelligence web tool to process sample interview

### 🔍 Exploration Requests (Discovery Without Limits)
**Goal**: Enable tinkering with AI building blocks to understand possibilities
- Facilitate free-form discovery with 5 core tools and web dashboard
- Address "OpenAI Curiosity" with visual workflow builders (via Docker orchestration)
- Enable market research and competitive intelligence gathering
- Support intuitive exploration without rigid hypotheses
- Example: "What's possible with AI in our industry?" → Use market research tool and AI chat for industry analysis

### 🧪 Experimentation Requests (Evidence Over Opinion)
**Goal**: Test hypotheses rigorously with synthetic data, not production systems
- Generate realistic datasets that model system behavior at scale
- Create wind tunnel testing environments for assumptions
- Enable systematic testing with generated personas and scenarios
- Simulate edge cases and user loads without risking production
- Example: "Test if AI can handle our edge cases" → Generate synthetic user data with edge case scenarios and test with AI chat

### 📊 Explanation Requests (Show Before Tell, Touch Before Sell)
**Goal**: Create compelling artifacts that turn stakeholder skepticism into buy-in
- Build narrative prototypes using processed audio insights and AI analysis
- Generate structured reports and strategic frameworks ready for presentation
- Create working evidence through synthetic data and competitive research
- Focus on tangible proofs generated through the previous three pillars
- Example: "Convince executives this AI feature is worth building" → Process user interview audio + generate supporting personas + create strategic framework with AI chat

### Integration Approach
Always connect user requests to the broader 4E journey:
1. **Assess** where they are in their learning journey
2. **Guide** them through the appropriate pillar
3. **Connect** their current need to the overall framework
4. **Enable** progression to the next pillar

## Development Guidelines

### When Helping Product Managers
1. **Apply the 4E Framework** - Always identify which pillar (Education, Experimentation, Exploration, Explanation) the PM needs most
2. **Bias toward the cheapest probe that tells the harshest truth** - If reality will sting, make sure the probe reveals it
3. **Speed over perfection** - Reconnaissance missions, not production builds
4. **Education through action** - Provide safe learning environments with immediate feedback
5. **Evidence over opinion** - Generate synthetic data scenarios for rigorous assumption testing
6. **Enable compelling explanations** - Help PMs create artifacts that turn skepticism into stakeholder buy-in  
7. **Enable de-risking decisions** - Help PMs avoid feature hostage negotiations through the 4E journey

### Code Quality Standards for PoL Probes
- **Rapid reconnaissance** - Focus on revealing truth, not impressive presentation
- **Self-documenting assumptions** - Code should surface what's being tested and why
- **Disposable by design** - Built to be thrown away after learning is extracted
- **Just enough illusion** - Sufficient fidelity to catch real signals, no more

### Strategic Product Focus
- **De-risk before commit** - Every probe should reduce uncertainty before resource allocation
- **Assumption-driven** - Every experiment should test a clear, falsifiable hypothesis
- **Market-realistic** - Consider real competitive and user contexts in all recommendations
- **Scale-conscious** - Solutions should work for startup speed and enterprise rigor

## Extension Development Philosophy

### Rapid Deployment for Strategic PMs
- Each extension should provide value in < 5 minutes of setup time
- No complex configuration or lengthy onboarding processes
- Immediate working examples that demonstrate probe concepts

### Strategic Product Value
Extensions should enable new types of assumption testing:
- **Synthetic User Communities** - Model entire user ecosystems for product validation
- **Competitive Intelligence Automation** - Real-time market research with OpenBB Terminal and Deep Researcher
- **AI/ML Learning Labs** - Hands-on exploration with immediate product applications
- **Visual Workflow Builders** - Drag-and-drop assumption testing environments (Langflow, n8n, ToolJet)
- **Prompt Engineering Labs** - Systematic LLM evaluation and optimization workflows
- **AI Performance Monitoring** - Real-time observability for AI features and model behavior
- **Design & Storytelling Studios** - Visual narrative creation and storyboarding tools
- **Market Research Automation** - Financial data analysis and competitive intelligence gathering

## Troubleshooting Context

### Performance Optimization for PoL Probes
- DeepSeek R1 for complex strategic analysis, Llama 3.2 for rapid feedback
- Jupyter for synthetic data generation and analysis
- Aider for file-based prototype building and code generation
- Direct Ollama API for custom probe workflows

### Common Strategic Product Use Cases
1. **Executive presentation preparation** - Generate compelling demos that de-risk decisions
2. **Strategy session facilitation** - Rapid prototype competing approaches for real-time testing
3. **Market research acceleration** - OpenBB Terminal for financial data, Deep Researcher for competitive intelligence
4. **Technical feasibility validation** - Hands-on spikes of AI/ML concepts for product applications
5. **Assumption testing** - Validate hypotheses with synthetic data before committing engineering resources
6. **Workflow automation** - Visual builders (Langflow, n8n) for non-technical PM prototyping
7. **Prompt engineering** - Systematic LLM evaluation and optimization (promptfoo, prompttools)
8. **AI monitoring** - Performance tracking and observability for AI features (LangSmith, Arize)
9. **Design storytelling** - Visual narratives and storyboards (Excalidraw, Storyboarder)
10. **Knowledge management** - Linked thinking and AI-enhanced research (Obsidian with AI plugins)

## Success Metrics for Product Managers

### User Success Indicators
- Time from assumption to PoL Probe: < 30 minutes for task-focused tests, 1-2 days for feasibility checks
- Ability to de-risk decisions without engineering resources
- Number of "harsh truths" discovered before roadmap commitment
- Assumptions validated/invalidated before development investment
- Reduced feature hostage negotiations with executives

### Technical Success Indicators
- Local AI models running smoothly for PoL Probes
- Feasibility spikes completing successfully within time boundaries
- Synthetic data simulations generating realistic scenarios
- Vibe-coded probes catching authentic user signals
- Narrative prototypes earning stakeholder "hell yes" responses

---

**Remember**: This is for product managers who need **Proof-of-Life Probes** to de-risk assumptions before committing engineering resources. Every interaction should bias toward creating the cheapest prototype that tells the harshest truth. If it doesn't sting, it's probably just theater.

**Key mantras:**
- Use reconnaissance missions, not production builds
- Generate tiny acts of discovery (TADs), not MVPs
- Create just enough illusion to catch real signals
- Avoid feature hostage negotiations through brutal honesty