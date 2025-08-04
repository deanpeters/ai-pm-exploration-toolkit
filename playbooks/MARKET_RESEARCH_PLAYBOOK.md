# Market Research Suite: AI-Powered Competitive Intelligence

This suite provides powerful tools for competitive and market analysis. The progression moves from simple queries to autonomous, multi-step research, ending with comprehensive market intelligence gathering.

**The PM Superpower:** Get research that would normally take weeks of manual work done in minutes, with AI-powered analysis and insights.

---

## What the Market Research Suite Does for Product Managers

**Think of these as:**
- **Gemini CLI** = Your AI research analyst (instant expert-level insights)
- **OpenBB Terminal** = Bloomberg Terminal for product managers (financial + business intelligence)
- **Deep Researcher** = Your autonomous research team (multi-step investigation and synthesis)

**Real PM Use Cases:**
- Analyze competitor business models and strategies
- Research market size and growth trends
- Track competitor funding, hiring, and product launches
- Validate market opportunities with financial data
- Generate comprehensive competitive analysis reports
- Monitor industry trends and emerging threats

---

## Tier 1: Quick Insights with Gemini CLI

**Goal:** Get a fast, AI-powered answer to a market question without leaving your terminal.

**Time Investment:** 5 minutes  
**Skill Level:** Complete beginner  
**PM Value:** Expert-level market analysis in seconds

### Getting Started: Your AI Research Assistant

```bash
aipm_gemini_setup
```

**What happens:** This walks you through connecting to Google's Gemini AI (free tier gives you lots of queries per month).

### Walkthrough: Strategic Market Questions

#### Step 1: Ask Your First Market Question
```bash
gemini "What are the top 3 business risks for a company entering the product management training and coaching market in 2025?"
```

**What you get:** A structured, AI-generated analysis that considers:
- Market saturation and competition
- Economic conditions affecting corporate training budgets  
- Technology disruption (AI tools replacing traditional coaching)
- Regulatory or certification requirements

#### Step 2: Dive Deeper with Follow-up Questions
```bash
gemini "Based on the previous analysis, what would be the most effective differentiation strategy for a new PM training company? Include specific tactics."
```

#### Step 3: Get Actionable Insights
```bash
gemini "Create a 90-day go-to-market plan for launching a PM training business that addresses the risks we identified. Include specific milestones and success metrics."
```

### Quick Win Use Cases for Tier 1

#### Competitive Positioning
```bash
gemini "Compare the business models of Figma vs Adobe XD vs Sketch. What strategic advantages does each have, and where are the gaps?"
```

#### Market Entry Analysis  
```bash
gemini "What are the key success factors for B2B SaaS companies entering the European market? Include regulatory considerations and cultural differences."
```

#### Feature Prioritization Research
```bash
gemini "What are the most requested features in project management software based on 2024 user feedback trends? Rank by potential business impact."
```

#### Technology Trend Analysis
```bash
gemini "How will AI integration affect the competitive landscape for note-taking apps like Notion, Obsidian, and Roam Research over the next 2 years?"
```

### Pro Tips for Tier 1
- **Be specific:** Include your industry, company stage, target market
- **Ask for structure:** Request bullet points, rankings, or frameworks
- **Chain questions:** Build on previous responses for deeper insights
- **Save good responses:** Copy valuable insights to your strategy docs

### Common Beginner Wins
- **Before board meetings:** Get quick industry context and competitive updates
- **During strategy sessions:** Real-time market research to support discussions
- **For PRD writing:** Market context and competitive analysis sections
- **Weekly planning:** Quick competitive intelligence updates

---

## Tier 2: Financial Data with OpenBB Terminal

**Goal:** Look up specific financial and corporate data for public competitors - understand their business performance, market position, and strategic moves.

**Time Investment:** 30 minutes  
**Skill Level:** Comfortable with basic commands  
**PM Value:** Deep financial intelligence on any public company

### Getting Started: Launch Your Financial Research Terminal

```bash
aipm_openbb
```

**What happens:** You enter a Bloomberg Terminal-style interface with access to financial data, news, and market intelligence.

### Walkthrough: Analyzing a Competitor

#### Step 1: Load Your Target Company
```
stocks
load AAPL
```

**What happens:** You're now analyzing Apple (use any ticker symbol). All subsequent commands will focus on this company.

#### Step 2: Get the Strategic Overview
```
overview
```

**What you see:**
- Business description and sector
- Market cap, revenue, employee count
- Key financial ratios
- Recent performance metrics

#### Step 3: Understand Financial Health
```
income
```

**What you get:** 
- Revenue trends over time
- Profit margins and growth rates
- Operating efficiency metrics
- Year-over-year comparisons

#### Step 4: Competitive Benchmarking
```
compare AAPL MSFT GOOGL
```

**What you see:**
- Side-by-side financial comparison
- Market performance relative to peers
- Valuation multiples and ratios

#### Step 5: Recent Strategic Moves
```
news
```

**What you get:**
- Latest company announcements
- Product launches and strategic initiatives  
- Market analyst opinions
- Industry trend coverage

### Advanced Tier 2: Strategic Analysis

#### Market Positioning Analysis
```
load ZOOM
sectors performance
```
**Use Case:** Understand how Zoom performs relative to the broader software sector

#### Investment and Growth Patterns
```
load NOTION  # (if public)
insider
analyst
```
**Use Case:** See insider trading patterns and analyst recommendations for strategic insights

#### Industry Trend Analysis
```
etf QQQ
holdings
```
**Use Case:** Understand which tech companies are gaining/losing institutional investor confidence

### Pro Tips for Tier 2
- **Start with competitors:** Always analyze 3-5 companies in your space
- **Look for patterns:** Compare financial trends across competitors
- **Watch the ratios:** P/E, revenue growth, profit margins tell the strategic story
- **Check news timing:** Connect financial events to product/strategy announcements

### Real PM Applications
- **Board presentations:** Include competitive financial context
- **Strategic planning:** Understand competitor resource constraints and advantages
- **Partnership evaluation:** Assess potential partner financial stability
- **Fundraising preparation:** Benchmark your metrics against public competitors

---

## Tier 3: Autonomous Research with Deep Researcher

**Goal:** Delegate a broad research topic to an AI agent that conducts multi-step investigation and synthesizes comprehensive reports.

**Time Investment:** 2 hours (mostly AI working autonomously)  
**Skill Level:** Comfortable directing AI research  
**PM Value:** Get consultant-level research reports without the consultant cost

### Getting Started: Launch Your AI Research Team

```bash
aipm_research
```

**What happens:** This starts the LangGraph research server. You'll access the UI at `http://localhost:8123`.

### Walkthrough: Comprehensive Market Research

#### Step 1: Define Your Research Objective
Go to `http://localhost:8123` and provide a high-level research brief:

> "Generate a comprehensive report on the competitive landscape for AI-powered note-taking applications, focusing on market trends, key players, and emerging technologies. Include business model analysis and strategic recommendations for a new entrant."

#### Step 2: Watch the AI Research Process
The AI agent will show you its work in real-time:
1. **Search Strategy:** What search terms and sources it's using
2. **Source Discovery:** Finding relevant articles, reports, company pages
3. **Data Collection:** Gathering information from multiple sources
4. **Analysis Phase:** Synthesizing insights and identifying patterns
5. **Report Generation:** Creating structured findings and recommendations

#### Step 3: Guide the Research Direction
You can interrupt and redirect:
- "Focus more on pricing strategies"
- "Include mobile app user adoption trends"
- "Add analysis of team collaboration features"

#### Step 4: Get Your Comprehensive Report
The final output includes:
- **Executive Summary:** Key findings and strategic implications
- **Market Overview:** Size, growth, and trend analysis
- **Competitive Analysis:** Player profiles and positioning
- **Technology Trends:** Emerging capabilities and disruptions
- **Strategic Recommendations:** Specific actions for market entry
- **Appendix:** Source citations and raw data

### Advanced Tier 3: Specialized Research Projects

#### Technology Feasibility Study
**Research Brief:** 
> "Investigate the current state of AI-powered code generation tools. Analyze technical capabilities, adoption barriers, competitive landscape, and market opportunity for developer tools companies. Include assessment of business model viability."

#### Customer Segment Analysis
**Research Brief:**
> "Research the specific needs and pain points of product managers at Series B-C SaaS companies. Include compensation trends, tool usage patterns, career progression challenges, and unmet educational needs."

#### Regulatory and Compliance Research
**Research Brief:**
> "Analyze the regulatory landscape for AI-powered healthcare applications in the US and EU. Include compliance requirements, approval processes, competitive implications, and strategic recommendations for product development."

#### Market Entry Strategy Research
**Research Brief:**
> "Evaluate the opportunity for US-based productivity software companies to enter the Japanese market. Include cultural considerations, local competitors, partnership opportunities, and go-to-market strategies."

### Pro Tips for Tier 3
- **Be specific about scope:** Define geographic, temporal, and industry boundaries
- **Include decision context:** Explain what decision this research will inform
- **Ask for specific formats:** Request frameworks, SWOT analysis, or recommendation matrices
- **Iterate based on findings:** Use initial results to refine follow-up research questions

### When to Use Tier 3
- **Before major product decisions:** Validate market opportunity and competitive threats
- **For strategic planning cycles:** Annual/quarterly strategy development
- **During fundraising:** Support your market size and competitive analysis
- **For board presentations:** Provide comprehensive market context
- **When considering pivots:** Research adjacent markets and opportunities

---

## Mastery: Combining All Research Tiers

The real power comes from **layering these research capabilities**:

### Example: Complete Competitive Analysis Pipeline
1. **Tier 1 (Gemini):** Quick competitive landscape overview and key players identification
2. **Tier 2 (OpenBB):** Financial analysis of public competitors
3. **Tier 3 (Deep Researcher):** Comprehensive strategy analysis and recommendations
4. **Synthesis:** Combine insights into executive-ready strategic brief

### Example: Market Entry Decision Framework
1. **Tier 3:** Comprehensive market research and opportunity assessment
2. **Tier 2:** Financial analysis of key players and market dynamics
3. **Tier 1:** Quick validation of specific strategic hypotheses
4. **Action:** Data-driven go/no-go decision with supporting evidence

### Example: Product Strategy Validation
1. **Tier 1:** Quick competitor feature analysis and positioning research
2. **Tier 3:** Deep dive on customer needs and market gaps
3. **Tier 2:** Financial performance analysis of different business models
4. **Output:** Validated product strategy with competitive differentiation

---

## Research Quality and Validation

### Ensuring High-Quality Insights
- **Cross-reference sources:** Compare findings across different research methods
- **Check recency:** Ensure data is current and relevant
- **Validate assumptions:** Test AI conclusions against your domain knowledge
- **Document methodology:** Keep track of research approaches that work well

### Common Research Pitfalls
- **Over-relying on AI:** Always validate key findings with human judgment
- **Information bubbles:** Ensure diverse source types and perspectives
- **Analysis paralysis:** Set time boundaries for research phases
- **Confirmation bias:** Ask AI to challenge your existing assumptions

---

## Troubleshooting

### "Gemini CLI won't authenticate"
```bash
# Check your Google account setup
aipm_gemini_auth_reset

# Verify API quota
aipm_gemini_status
```

### "OpenBB Terminal is slow"
- **Check internet connection:** Financial data requires stable connectivity
- **Verify API limits:** Some data sources have rate limits
- **Restart the terminal:** `Ctrl+C` then `aipm_openbb`

### "Deep Researcher gets stuck"
- **Simplify the query:** Break complex research into smaller questions
- **Check the logs:** Look for specific error messages
- **Restart the service:** `aipm_research_restart`

### "Research results are too generic"
- **Add more context:** Include your industry, company stage, specific constraints
- **Use follow-up questions:** Drill down into interesting findings
- **Provide examples:** Show the AI what good analysis looks like

---

## Next Steps

**Mastered Tier 1?** → Combine with [Aider Playbook](AIDER_PLAYBOOK.md) to turn research into strategic documents

**Ready for deeper analysis?** → Use [Workflow Playbook](WORKFLOW_PLAYBOOK.md) to automate ongoing competitive monitoring

**Want comprehensive intelligence?** → Build dashboards using research data with ToolJet from the Workflow Suite

**Need to convince stakeholders?** → Use research findings to build compelling demos and prototypes

---

## Research Templates

### Quick Competitive Analysis (Tier 1)
```bash
gemini "Analyze [Competitor Name]'s business model, key strengths, and potential vulnerabilities. Include 3 strategic recommendations for competing against them."
```

### Financial Health Check (Tier 2)
```
load [TICKER]
overview
income  
compare [TICKER] [COMPETITOR1] [COMPETITOR2]
news
```

### Market Opportunity Assessment (Tier 3)
> "Evaluate the market opportunity for [Product Category] focusing on [Target Segment]. Include market size, growth trends, competitive landscape, key success factors, and strategic recommendations for a [Company Stage] company."

---

**Remember:** Research is only valuable if it **changes decisions**. Every research session should end with specific actions, hypotheses to test, or strategic implications for your product roadmap.

**The goal:** Transform from intuition-based to evidence-based product decisions, with research capabilities that rival expensive consulting firms.