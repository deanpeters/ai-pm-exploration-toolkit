# Pre-Built Goose Workflows for Product Managers

## Ready-to-Run Strategic Analysis Sessions

These workflows are optimized for common PM challenges using the AI PM Exploration Toolkit. Each provides autonomous, multi-step analysis with actionable outputs.

## Core PM Workflows

### 1. Feature Feasibility Analysis
**Session Command:** `goose session --name feasibility_check`

**Workflow Prompt:**
```
Execute a comprehensive feasibility analysis for [FEATURE_NAME]:

Phase 1 - Technical Assessment:
1. Examine toolkit AI capabilities to model implementation complexity
2. Generate synthetic edge cases to test feature robustness
3. Analyze resource requirements using current infrastructure specs
4. Identify technical risks and mitigation strategies

Phase 2 - Market Validation:
1. Research competitive landscape for similar features  
2. Generate synthetic user scenarios to model adoption patterns
3. Create usage projections based on existing user data
4. Assess differentiation potential in current market

Phase 3 - Strategic Recommendation:
1. Build PoL probe designs to test core assumptions
2. Create timeline estimates with confidence intervals
3. Generate resource allocation recommendations
4. Provide go/no-go decision framework

Deliverable: Executive summary with specific next steps and risk assessment.
```

**Expected Output:**
- Technical complexity score (1-10)
- Resource requirement estimation
- Risk assessment matrix
- 3 specific PoL probe recommendations
- Timeline with milestones
- Go/no-go recommendation with rationale

### 2. Competitive Intelligence Deep Dive  
**Session Command:** `goose session --name competitor_analysis`

**Workflow Prompt:**
```
Conduct comprehensive competitive analysis for [COMPETITOR_NAME] or [MARKET_SEGMENT]:

Phase 1 - Market Position Analysis:
1. Use market research tools to gather business model data
2. Analyze public feature sets and pricing strategies  
3. Identify core value propositions and target markets
4. Map competitive strengths and vulnerabilities

Phase 2 - Strategic Implications:
1. Compare capabilities against our toolkit features
2. Identify market gaps and positioning opportunities
3. Generate synthetic user data for competitive scenarios
4. Model potential responses to our strategic moves

Phase 3 - Action Planning:  
1. Recommend defensive and offensive strategies
2. Create monitoring frameworks for ongoing intelligence
3. Design PoL probes to test competitive assumptions
4. Build scenarios for different competitive responses

Deliverable: Strategic positioning report with actionable recommendations.
```

**Expected Output:**
- Competitive landscape map
- SWOT analysis with market data
- Strategic positioning recommendations  
- Monitoring dashboard design
- 5 specific strategic actions with timelines

### 3. User Research Synthesis Engine
**Session Command:** `goose session --name user_research_analysis`

**Workflow Prompt:**
```
Synthesize user research insights from available data sources:

Phase 1 - Data Processing:
1. Process any audio transcripts in experiments/ directory
2. Analyze existing user data and feedback patterns
3. Generate additional synthetic users to expand sample size
4. Create comprehensive user behavior models

Phase 2 - Pattern Recognition:
1. Identify recurring pain points across data sources
2. Extract feature requests with frequency analysis
3. Map user journey friction points and opportunities
4. Generate user personas based on combined insights

Phase 3 - Strategic Application:
1. Create feature prioritization framework based on user needs
2. Design PoL probes to validate top user assumptions  
3. Build narrative prototypes for key user scenarios
4. Generate roadmap recommendations aligned with user research

Deliverable: User research report with persona profiles and strategic recommendations.
```

**Expected Output:**
- 5-10 detailed user personas
- Pain point frequency analysis
- Feature opportunity scoring
- User journey optimization recommendations
- Prototype concepts for top 3 opportunities

### 4. Roadmap Prioritization Framework
**Session Command:** `goose session --name feature_prioritization`

**Workflow Prompt:**
```
Create evidence-based feature prioritization for upcoming quarter:

Phase 1 - Data Foundation:
1. Generate synthetic user data for different market segments
2. Model usage scenarios for each potential feature
3. Analyze technical implementation complexity using AI tools
4. Research competitive feature priorities and market trends

Phase 2 - Scoring Framework:
1. Create multi-factor scoring matrix (impact, effort, risk, strategic value)
2. Apply framework to candidate features with quantitative analysis
3. Generate confidence intervals for each score component
4. Model different prioritization scenarios and outcomes

Phase 3 - Strategic Validation:
1. Design PoL probes to test prioritization assumptions
2. Create narrative prototypes for top-ranked features
3. Build business case presentations for stakeholder alignment
4. Generate implementation timeline with resource allocation

Deliverable: Prioritized feature roadmap with supporting evidence and validation plan.
```

**Expected Output:**
- Prioritization framework with scoring methodology
- Ranked feature list with confidence scores
- Resource allocation recommendations
- PoL probe designs for top 5 features
- Executive presentation materials

### 5. Executive Presentation Builder
**Session Command:** `goose session --name executive_prep`

**Workflow Prompt:**
```
Build compelling executive presentation for [PROPOSAL_TOPIC]:

Phase 1 - Evidence Generation:
1. Process user research data for compelling customer insights
2. Generate synthetic scenarios that demonstrate market opportunity
3. Create competitive analysis showing strategic positioning  
4. Build financial projections using realistic assumptions

Phase 2 - Narrative Construction:
1. Develop "show before tell" demonstrations using toolkit capabilities
2. Create user journey narratives that highlight value proposition
3. Build risk mitigation strategies with specific PoL probe examples
4. Generate success metrics and measurement frameworks

Phase 3 - Presentation Assets:
1. Create executive summary with key decision points
2. Build supporting data visualizations and evidence
3. Generate FAQ responses for anticipated executive questions
4. Design follow-up action plan with timelines and ownership

Deliverable: Complete presentation package with speaker notes and supporting materials.
```

**Expected Output:**
- Executive presentation slides (PDF/PPT format)
- Speaker notes with key talking points
- Supporting data appendix
- FAQ document with responses
- Next steps action plan

## Specialized Workflows

### 6. Technical Spike Planning
**Session Command:** `goose session --name spike_planning`

**Workflow Purpose:** Design focused technical experiments to validate core assumptions

**Workflow Prompt:**
```
Design technical spike to validate [TECHNICAL_ASSUMPTION]:

1. Define spike success criteria and measurement methods
2. Create test scenarios using synthetic data generation
3. Identify minimum viable test implementation
4. Generate resource estimates and timeline boundaries  
5. Design results analysis framework
6. Build spike retrospective template for learning capture

Focus on "cheapest prototype that tells harshest truth" principle.
```

### 7. Market Entry Analysis
**Session Command:** `goose session --name market_entry`

**Workflow Purpose:** Evaluate new market opportunities with data-driven analysis

**Workflow Prompt:**
```
Analyze market entry opportunity for [MARKET/VERTICAL]:

1. Research market size, growth, and competitive landscape
2. Generate synthetic user profiles for target market segments
3. Model adoption scenarios and revenue projections
4. Identify market entry risks and mitigation strategies
5. Design PoL probes to validate market assumptions
6. Create go-to-market strategy recommendations

Provide specific market validation experiments and success metrics.
```

### 8. Product-Market Fit Validation
**Session Command:** `goose session --name pmf_validation`

**Workflow Purpose:** Assess and improve product-market fit using systematic analysis

**Workflow Prompt:**
```
Evaluate product-market fit for [PRODUCT/FEATURE]:

1. Analyze user behavior data for engagement patterns
2. Generate synthetic user cohorts to model retention scenarios  
3. Identify value realization points and friction areas
4. Create experiments to test core value hypotheses
5. Build measurement frameworks for PMF indicators
6. Generate improvement recommendations with priority ranking

Focus on leading indicators of PMF rather than lagging metrics.
```

## Workflow Execution Guidelines

### Session Preparation
```bash
# Ensure toolkit is accessible
cd /Users/deanpeters/ai-pm-exploration-toolkit

# Check system status before starting
python3 -c "import sys; print(f'Python: {sys.version}')"
ls shared/ web/ core/  # Verify file structure

# Start session with clear working directory context
goose session --name [workflow_name] --cwd $(pwd)
```

### Best Practices for Goose Sessions

#### Effective Prompting
- **Be specific** about the feature, market, or decision you're analyzing
- **Provide context** about your product, users, and constraints  
- **Set clear deliverable expectations** in your initial prompt
- **Ask for interim summaries** during long analysis workflows

#### Session Management
```bash
# Save important analysis sessions
goose session --name competitive_analysis --save competitive_q2_2024

# Resume complex workflows across multiple sessions  
goose session --name feature_prioritization --resume

# Export findings for stakeholder sharing
goose export session_results.md --format markdown
```

#### Quality Control
- **Validate recommendations** by asking Goose to explain its reasoning
- **Request supporting evidence** for key strategic claims
- **Cross-check analysis** with multiple data sources when possible
- **Test assumptions** with follow-up PoL probe designs

### Integration with Other Tools

#### Goose → Web Dashboard
```
1. Use Goose for strategic analysis and recommendations
2. Switch to web interface for data generation and processing
3. Return to Goose to analyze generated outputs
4. Export final insights for stakeholder presentations
```

#### Goose → External AI Consultation
```
1. Run comprehensive Goose analysis for deep investigation
2. Export key findings and recommendations
3. Use external AI (Claude/ChatGPT) for strategic refinement
4. Return to Goose for implementation planning
```

#### Team Collaboration Workflows
```bash
# Share session state for team review
goose session --name team_analysis --share

# Collaborative planning sessions
goose session --name q2_planning --multi-user --invite team@company.com

# Handoff analysis to implementation teams
goose export technical_requirements.md --audience developers
```

## Success Metrics for Workflows

### Decision Quality Improvements
- **Faster assumption identification** - From days to hours
- **More comprehensive risk assessment** - Systematic vs ad-hoc analysis  
- **Better stakeholder alignment** - Evidence-based vs opinion-based discussions
- **Higher feature success rates** - Validated assumptions before development

### Process Efficiency Gains
- **Reduced analysis time** - Autonomous workflows vs manual research
- **Standardized frameworks** - Consistent analysis approach across PMs
- **Reusable insights** - Session results inform future decisions  
- **Improved collaboration** - Shared analysis context for team discussions

---

**Key Benefits**: These workflows provide autonomous, repeatable analysis that transforms product management from intuition-based to evidence-based decision making. Each workflow is designed to generate specific, actionable outputs within 30-60 minutes of autonomous analysis.