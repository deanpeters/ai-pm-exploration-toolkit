# AI Consultation Context - AI PM Exploration Toolkit

## Strategic Overview

This is the **AI PM Exploration Toolkit** implementing Dean Peters' **Proof-of-Life (PoL) Probes** framework. The toolkit transforms product managers from AI-curious to AI-confident through a structured **4E Framework**: Education → Experimentation → Exploration → Explanation.

### Core Philosophy
*"The most expensive way to test your idea is to build production-quality software."* ~ Jeff Patton

**Use the cheapest prototype that tells the harshest truth. If it doesn't sting, it's probably just theater.**

## Target User: Strategic Product Managers

Product managers who combine:
- **Marty Cagan** strategic thinking - Outcomes-obsessed, evidence-driven decisions
- **DHH "Just ship it" mentality** - Prefer working software over documentation  
- **OpenAI Curiosity** - Constantly exploring AI/ML possibilities for product applications
- **Dean Peters PoL Mindset** - Use disposable probes to de-risk assumptions before roadmap commitments

These aren't traditional agile product owners managing backlogs. They're leaders who need to avoid building something nobody wants by validating assumptions with lightweight, disposable reconnaissance missions.

## The Four Pillars Framework

### 🎓 Education (Personal AI Classroom)
Combat AI illiteracy through safe, local-first learning environments with immediate feedback.

**Current Implementation:**
- Web dashboard at `http://localhost:3000` with Audio Intelligence, AI Chat Assistant, Data Generation
- Local AI models (DeepSeek R1, Llama 3.2) for privacy and speed
- Interactive learning through real PM scenarios

### 🧪 Experimentation (Evidence Over Opinion)  
Test hypotheses with synthetic data and wind tunnel simulations, not production systems.

**Current Implementation:**
- Synthetic data generation for 50+ personas per industry
- Audio transcription analysis for user interviews
- AI-powered strategic analysis with structured frameworks
- Competitive intelligence automation

### 🔍 Exploration (Discovery Without Limits)
Tinker with AI building blocks to understand possibilities through hands-on discovery.

**Current Implementation:**
- Market research automation with real-time competitive analysis
- Visual workflow builders (Langflow, n8n, ToolJet via Docker)
- Prompt engineering labs for systematic LLM optimization
- AI monitoring and observability tools

### 📊 Explanation (Show Before Tell, Touch Before Sell)
Create compelling narratives that turn stakeholder skepticism into buy-in through tangible proof.

**Current Implementation:**
- Structured PM insight reports from audio processing
- Strategic frameworks generated through AI conversations
- Synthetic data exports for supporting evidence
- Professional outputs ready for executive presentations

## Five Flavors of PoL Probes

1. **Feasibility Checks** - 1-2 day spike-and-delete tests with AI assistance
2. **Task-Focused Tests** - Validate make-or-break user moments without friction  
3. **Narrative Prototypes** - Loom walkthroughs and explainer videos that earn "hell yes"
4. **Synthetic Data Simulations** - Model system behavior without burning production resources
5. **Vibe-Coded Probes** - Fake frontend + semi-plausible backend for real user signals

## Real Working Examples

### Audio Intelligence for User Research
**Command:** `python3 shared/audio_transcription.py interview.mp3 --use-case user_interviews`
**Purpose:** Extract structured insights from user interviews without manual transcription
**Output:** Pain points, feature requests, user goals automatically identified and categorized

### AI Strategic Thinking Partner  
**Command:** `python3 shared/ai_chat.py --mode pm_assistant --interactive`
**Purpose:** Get structured strategic guidance for product decisions
**Output:** Strategic frameworks, investigation approaches, decision structures for complex PM challenges

### Synthetic Data for Assumption Testing
**Command:** `python3 shared/data_generator.py --personas 50 --industry saas`
**Purpose:** Generate realistic user data to test concepts without waiting for real users
**Output:** Demographics, pain points, goals, scenarios ready for analysis and testing

### Competitive Intelligence Automation
**Command:** `python3 shared/market_research.py --company "CompanyName"`
**Purpose:** Instant competitive analysis and market positioning research  
**Output:** Business model analysis, competitive strengths/weaknesses, market position insights

## Success Metrics for PoL Probes

### User Success Indicators
- Time from assumption to PoL Probe: < 30 minutes for task-focused tests
- Ability to de-risk decisions without engineering resources
- Number of "harsh truths" discovered before roadmap commitment
- Reduced feature hostage negotiations with executives

### Technical Success Indicators  
- Local AI models running smoothly for reconnaissance missions
- Feasibility spikes completing within time boundaries
- Synthetic data simulations generating realistic scenarios
- Narrative prototypes earning stakeholder "hell yes" responses

## Consultation Integration Options

This toolkit supports four consultation pathways:

1. **External AI Systems** - Drag these context files to Claude/ChatGPT/Gemini projects
2. **Native Goose CLI** - Local AI agent with full toolkit access and autonomous analysis  
3. **VS Code + Continue** - Direct code analysis with AI assistance integrated into development workflow
4. **Visual Documentation** - Enhanced markdown reading with MarkText for beautiful documentation review

Choose the pathway that matches your technical comfort level and collaboration needs.

### Enhanced Documentation Experience
For optimal reading of these context files, use MarkText (installed via setup.sh):
```bash
# Beautiful visual markdown reading
open -a MarkText AI_CONSULTATION_CONTEXT.md
aipm_marktext TECHNICAL_SPECIFICATION.md
```

Instead of terminal commands like `cat README.md`, use MarkText for a much better documentation experience with proper formatting, visual appeal, and cross-reference navigation.

---

**Key Mantras:**
- Use reconnaissance missions, not production builds
- Generate tiny acts of discovery (TADs), not MVPs  
- Create just enough illusion to catch real signals
- Avoid feature hostage negotiations through brutal honesty