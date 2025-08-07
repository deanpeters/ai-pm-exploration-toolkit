# Technical Specification - AI PM Exploration Toolkit

## Architecture Overview

### Core AI Infrastructure (Local-First)
- **Ollama** - Local AI server for privacy, speed, and zero API costs
- **DeepSeek R1 7B** - Primary model for complex product analysis and strategic thinking
- **Llama 3.2 3B** - Fast model for rapid product iteration and feedback
- **Aider** - AI coding assistant for building disposable prototypes
- **Jupyter Lab** - Data exploration and synthetic user generation

### Development & AI Coding Stack
- **VS Code + Continue Extension** - Enhanced IDE with local AI coding assistance
- **Continue Extension** - Integrated AI help with custom PM-focused system messages
- **llama-cpp-agent** - Local AI agent with advanced tool calling capabilities
- **devon-agent** - AI software engineering automation for prototype development

### Market Research & Intelligence
- **OpenBB Terminal** - Open-source financial research and market data platform
- **Local Deep Researcher** - AI-powered research automation for competitive analysis
- **Gemini CLI** - Google's AI model for advanced market research and strategic analysis

### Visual/Low-Code Workflow Tools
- **Langflow** - Visual LLM application builder for non-technical PMs
- **n8n** - Workflow automation platform (Docker-based) for process orchestration
- **ToolJet** - Low-code app builder for internal PM tools and dashboards
- **Typebot** - Conversational form/chatbot builder for user research

### Synthetic Data & Testing Infrastructure
- **Faker** - Basic synthetic data generation (Python & CLI)
- **Mimesis** - Advanced synthetic data with localization support
- **Gretel** - AI-powered synthetic data platform for complex scenarios
- **ChatterBot** - Machine learning conversational engine for user simulation
- **persona-chat CLI** - Custom persona-based chat interface for testing

### Prompt Engineering & Evaluation
- **promptfoo** - LLM evaluation framework for systematic prompt testing
- **prompttools** - Python-based prompt experimentation toolkit
- **LangSmith** - LLM application development and monitoring platform

### AI Monitoring & Observability
- **Arize** - ML observability platform for AI features in production
- **LangSmith** - Development-time monitoring and debugging for LLM applications

## Project Structure

```
~/ai-pm-exploration-toolkit/
├── core/                    # System infrastructure
│   ├── installer.py         # Installation and setup automation
│   ├── toolkit.json         # Configuration and tool definitions
│   └── dependencies/        # Package and environment management
│
├── shared/                  # Core PoL Probe implementations
│   ├── audio_transcription.py    # Audio intelligence processing
│   ├── ai_chat.py              # Strategic AI conversation partner
│   ├── data_generator.py       # Synthetic data and persona creation
│   ├── market_research.py      # Competitive intelligence automation
│   └── pm_audio_workflows.py   # PM-specific workflow templates
│
├── web/                     # Dashboard and visual interfaces
│   ├── app.py              # Main web dashboard (localhost:3000)
│   ├── templates/          # Web interface components
│   └── static/             # Assets and styling
│
├── experiments/            # Synthetic data simulations and testing
├── prototypes/            # Narrative walkthroughs and vibe-coded probes  
├── data/                  # Generated datasets for assumption testing
├── insights/              # De-risked decisions and validated assumptions
├── notebooks/             # Feasibility spikes and technical exploration
│
├── workflow-tools/        # Docker orchestration for visual tools
│   ├── docker-compose.yml # n8n, ToolJet, Typebot configuration
│   └── configs/           # Tool-specific configurations
│
├── prompt-testing/        # Prompt evaluation and optimization
├── synthetic-data/        # Persona generation and test scenarios
├── monitoring/            # AI performance monitoring and reports
├── design/                # Storyboards, diagrams, and visual assets
├── obsidian-vault/        # Knowledge management and linked ideas
└── mcp-servers/           # Model Context Protocol servers and agents
```

## Core Implementation Details

### Audio Intelligence Pipeline
**File:** `shared/audio_transcription.py`
**Architecture:** 
- Audio file processing with Whisper integration
- PM-specific use case templates (user interviews, strategy sessions, feedback calls)
- Structured output generation for stakeholder presentations
- Support for batch processing of multiple audio files

### AI Strategic Thinking Partner
**File:** `shared/ai_chat.py`  
**Architecture:**
- Interactive conversation with local AI models
- PM-specific system prompts and strategic frameworks
- Mode-based conversations (analysis, planning, decision-making)
- Conversation export for documentation and sharing

### Synthetic Data Generation
**File:** `shared/data_generator.py`
**Architecture:**
- Industry-specific persona generation (SaaS, e-commerce, fintech)
- Configurable persona count and demographic distributions
- Pain point, goal, and scenario generation for testing
- Export formats: CSV, JSON for integration with existing tools

### Market Research Automation  
**File:** `shared/market_research.py`
**Architecture:**
- Company lookup and analysis using multiple data sources
- Business model analysis and competitive positioning
- Integration with OpenBB Terminal for financial data
- Structured output for strategic planning sessions

### Web Dashboard
**File:** `web/app.py`
**Architecture:**
- Flask-based web interface at `http://localhost:3000`
- Real-time audio processing and AI interaction
- Data generation and export capabilities
- Visual workflow integration with Docker tools

## Integration Specifications

### Local AI Model Requirements
- **Minimum RAM:** 8GB for Llama 3.2 3B, 16GB recommended for DeepSeek R1 7B
- **Storage:** 50GB for full model collection
- **CPU:** Modern multi-core processor for acceptable inference speeds
- **GPU:** Optional but recommended for faster processing

### Docker Workflow Tools
- **n8n:** Port 5678 - Visual workflow automation
- **ToolJet:** Port 3001 - Low-code app builder  
- **Typebot:** Port 3002 - Conversational interface builder
- **Resource Requirements:** 4GB RAM, 20GB storage for all services

### External Integration Points
- **VS Code Continue Extension:** Local model integration via Ollama API
- **Goose CLI:** Native toolkit file access and autonomous analysis
- **Obsidian:** Knowledge management with AI plugin support
- **MarkText:** Enhanced markdown reading for documentation

## Performance Specifications

### Response Time Targets
- Audio transcription: < 2 minutes for 1-hour interview
- AI strategic conversations: < 5 seconds per response
- Synthetic data generation: < 30 seconds for 50 personas
- Market research: < 1 minute for basic company analysis
- Web dashboard: < 3 seconds for all page loads

### Scalability Considerations
- Local processing eliminates API rate limits
- Docker containerization enables resource isolation
- Modular architecture supports selective tool deployment
- Synthetic data generation scales linearly with available compute

### Security & Privacy
- **Local-first architecture** - No external API calls for core functionality
- **Data isolation** - All processing happens on local machine
- **No cloud dependencies** - Works offline after initial setup
- **Configurable model selection** - Choose privacy vs performance trade-offs

## Development Guidelines

### PoL Probe Quality Standards
- **Rapid reconnaissance focus** - Optimize for learning speed over code elegance
- **Self-documenting assumptions** - Code should surface what's being tested
- **Disposable by design** - Built to extract learning then be discarded
- **Just enough fidelity** - Sufficient realism to catch authentic signals

### Extension Development
- **5-minute setup rule** - New tools must provide value in < 5 minutes
- **Strategic product focus** - Every tool should enable assumption testing
- **Integration-first** - Leverage existing infrastructure over custom builds
- **Documentation-driven** - Include consultation templates with implementation

This architecture enables product managers to conduct sophisticated AI-assisted reconnaissance missions while maintaining complete control over their data and intellectual property.