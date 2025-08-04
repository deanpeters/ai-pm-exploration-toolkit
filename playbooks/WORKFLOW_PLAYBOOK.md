# Visual Workflow Suite: Build Prototypes Without Code

This suite allows for building prototypes and automation without code. The progression moves from simple event-based automation to visual AI chaining, ending with full internal tool creation.

**The PM Superpower:** Create working demonstrations of complex workflows that stakeholders can actually use, without waiting for engineering resources.

---

## What the Visual Workflow Suite Does for Product Managers

**Think of these as:**
- **n8n** = Zapier Pro (but more powerful and private)
- **Langflow** = Visual AI logic builder (drag-and-drop intelligence)
- **ToolJet** = Internal tool builder (create dashboards in hours, not months)
- **Typebot** = Conversational UX designer (build chatbots visually)

**Real PM Use Cases:**
- Automate competitive intelligence gathering
- Build AI-powered product demos for stakeholder meetings
- Create internal dashboards for team metrics
- Prototype conversational interfaces for user research
- Connect disparate tools and data sources
- Build "wizard of oz" experiments to test product concepts

---

## Tier 1: Simple Automation with n8n

**Goal:** Create a simple workflow that automates a common PM task, like tracking competitor news.

**Time Investment:** 20 minutes  
**Skill Level:** Complete beginner  
**PM Value:** Stop doing manual competitive research

### Getting Started: Access Your Workflow Builder

```bash
aipm_workflows
```

**What happens:** This command starts all your workflow tools. n8n will be available at `http://localhost:5678`.

### Walkthrough: Competitive Intelligence Automation

#### Step 1: Create Your First Workflow
1. **Open n8n:** Go to `http://localhost:5678` in your browser
2. **Create a New Workflow:** Click "Add workflow" 
3. **Give it a name:** "Competitor News Tracker"

#### Step 2: Set Up the Information Source
1. **Add a Trigger Node:** Click the `+` icon and search for "RSS Feed"
2. **Configure the RSS Feed:** 
   - URL: Enter your competitor's blog RSS feed (e.g., `https://blog.competitor.com/feed`)
   - Poll Times: Set to check every 4 hours
3. **Test it:** Click "Test step" to see if it finds recent posts

#### Step 3: Add Your Notification Destination
1. **Add an Action Node:** Click `+` after the RSS node
2. **Search for "Slack"** and select it
3. **Connect to Slack:** Follow the authentication prompts
4. **Configure the Message:** 
   - Channel: Choose your competitive intelligence channel
   - Message: `🚨 New from [competitor]: {{ $json.title }} - {{ $json.link }}`

#### Step 4: Activate and Test
1. **Save your workflow**
2. **Toggle the switch to "Active"**
3. **You're done!** You'll now get Slack notifications whenever your competitor publishes

### More Tier 1 Automation Ideas

#### Product Launch Monitoring
- **Trigger:** RSS feed from Product Hunt
- **Filter:** Only products in your category
- **Action:** Email summary to product team

#### Customer Feedback Aggregation  
- **Trigger:** New Typeform responses
- **Process:** Extract key insights
- **Action:** Add to Notion database with sentiment scores

#### Team Metrics Dashboard
- **Trigger:** Daily schedule (every morning at 9 AM)
- **Collect:** Pull data from Jira, GitHub, Slack
- **Action:** Post team productivity summary to leadership channel

### Pro Tips for Tier 1
- **Start simple:** One trigger, one action, then expand
- **Use real data:** Connect to tools you actually use daily
- **Test frequently:** Use the "Test step" button liberally
- **Name things clearly:** Future you will thank you

---

## Tier 2: Visual AI Prototyping with Langflow

**Goal:** Prototype an AI logic chain visually - perfect for validating AI product features before engineering builds them.

**Time Investment:** 1 hour  
**Skill Level:** Comfortable with drag-and-drop interfaces  
**PM Value:** Demo AI features to stakeholders with zero code

### Getting Started: Launch Your AI Builder

```bash
aipm_langflow
```

**What happens:** Langflow starts at `http://localhost:7860` - this is your visual AI development environment.

### Walkthrough: Building an AI Feature Demo

#### Step 1: Design Your AI Logic
**Scenario:** You want to demo an AI feature that takes customer support tickets and automatically categorizes them + suggests responses.

1. **Open Langflow:** Go to `http://localhost:7860`
2. **Create a New Flow:** Click "New Flow"
3. **Name it:** "Support Ticket AI Demo"

#### Step 2: Build the Input Layer
1. **Add a Text Input:** Drag "TextInput" component onto the canvas
2. **Configure it:**
   - Name: "Customer Message"
   - Placeholder: "Enter customer support request..."
3. **Add a Prompt Template:** Drag "PromptTemplate" onto canvas
4. **Configure the prompt:**
   ```
   Analyze this customer support message and provide:
   1. Category (Bug Report, Feature Request, Billing, Account)
   2. Priority (Low, Medium, High, Critical)  
   3. Suggested response (professional, helpful tone)
   
   Customer message: {customer_message}
   ```

#### Step 3: Add the AI Brain
1. **Drag an "Ollama" component** onto the canvas
2. **Configure it:**
   - Model: `deepseek-r1:7b`
   - Temperature: 0.3 (for consistent categorization)
3. **Connect the components:** 
   - Text Input → Prompt Template
   - Prompt Template → Ollama

#### Step 4: Format the Output
1. **Add an "Output Parser"** to structure the response
2. **Connect:** Ollama → Output Parser
3. **Test your flow:** Enter a sample support message and watch it process

#### Step 5: Make It Demo-Ready
1. **Add multiple test cases:** Create buttons for common scenarios
2. **Style the interface:** Use the chat interface for stakeholder demos
3. **Save and share:** Export the flow to show to your team

### Advanced Tier 2: Multi-Step AI Workflows

#### Content Moderation Pipeline
**Flow:** User Input → Toxicity Detection → Content Classification → Automated Action
**Use Case:** Demo automated content moderation for community features

#### Smart Onboarding Assistant  
**Flow:** User Profile → Personalization Engine → Customized Walkthrough → Progress Tracking
**Use Case:** Show how AI could personalize user onboarding

#### Competitive Analysis AI
**Flow:** Company Name → Web Research → Financial Data → SWOT Analysis → Strategic Recommendations
**Use Case:** Demonstrate AI-powered competitive intelligence

### Pro Tips for Tier 2
- **Think user journey first:** Map the workflow before building
- **Use real examples:** Test with actual customer data (anonymized)
- **Create multiple paths:** Show how AI handles edge cases
- **Document assumptions:** Note what the AI does well vs poorly

---

## Tier 3: Internal Dashboarding with ToolJet

**Goal:** Build a simple, data-driven dashboard that stakeholders can interact with - perfect for product metrics, team dashboards, or competitive tracking.

**Time Investment:** 2 hours  
**Skill Level:** Comfortable with data and basic SQL  
**PM Value:** Create executive dashboards without waiting for data team

### Getting Started: Launch Your Dashboard Builder

```bash
aipm_tooljet
```

**What happens:** ToolJet starts at `http://localhost:8082` - this is your internal tool and dashboard builder.

### Walkthrough: Product Metrics Dashboard

#### Step 1: Connect Your Data Sources
1. **Open ToolJet:** Go to `http://localhost:8082` and create an account
2. **Create a New App:** Click "Create new application"
3. **Add Data Sources:** Go to "Data Sources" tab
   - **Option A:** Connect to your actual database (PostgreSQL, MySQL, etc.)
   - **Option B:** Use REST APIs (Google Analytics, Mixpanel, etc.)
   - **Option C:** Upload CSV files for quick prototyping

#### Step 2: Create Your First Query
1. **Go to Query Panel:** Click "Queries" at the bottom
2. **Create a new query:** Select your data source
3. **Write your query:** Example for user metrics:
   ```sql
   SELECT 
     DATE(created_at) as date,
     COUNT(*) as new_users,
     COUNT(DISTINCT user_id) as active_users
   FROM users 
   WHERE created_at >= '2024-01-01'
   GROUP BY DATE(created_at)
   ORDER BY date DESC
   ```

#### Step 3: Build Your Dashboard UI
1. **Drag widgets from the component library:**
   - **Chart** for user growth trends
   - **Table** for detailed breakdowns  
   - **Number cards** for key metrics
   - **Filters** for date ranges

2. **Configure each widget:**
   - **Chart Widget:** Set data to `{{ queries.user_metrics.data }}`
   - **Chart Type:** Line chart for trends
   - **X-axis:** date field
   - **Y-axis:** new_users field

#### Step 4: Add Interactivity
1. **Add filter controls:** Date picker, dropdown for segments
2. **Connect filters to queries:** Update queries based on filter selections
3. **Add drill-down capability:** Click chart to see detailed data

#### Step 5: Make It Executive-Ready
1. **Add key insights text:** Use Text widgets to highlight important trends
2. **Color-code performance:** Green for good metrics, red for concerning trends
3. **Add refresh functionality:** Button to pull latest data
4. **Set up sharing:** Generate shareable links for stakeholders

### Advanced Tier 3: Specialized Dashboards

#### Competitive Intelligence Dashboard
**Data Sources:** Web scraping APIs, financial data, news feeds
**Widgets:** Competitor comparison tables, market share charts, news timeline
**Use Case:** Weekly competitive reviews with leadership

#### Customer Health Score Dashboard
**Data Sources:** Support tickets, usage analytics, NPS surveys
**Widgets:** Health score trends, at-risk customer alerts, intervention recommendations
**Use Case:** Proactive customer success management

#### Product Experiment Dashboard
**Data Sources:** A/B testing platforms, analytics tools
**Widgets:** Experiment results, statistical significance, recommendation engine
**Use Case:** Data-driven product decision making

### Pro Tips for Tier 3
- **Start with mockups:** Sketch your dashboard first
- **Focus on actions:** Every metric should lead to a decision
- **Use real-time data when possible:** Stakeholders love live updates
- **Test with actual users:** Get feedback from dashboard consumers

---

## Bonus Tier: Conversational UX with Typebot

**Goal:** Prototype conversational interfaces for user research or customer support scenarios.

**Time Investment:** 1 hour  
**Skill Level:** Anyone who's used a survey tool  
**PM Value:** Test conversational UX concepts before development

### Getting Started: Launch Typebot

```bash
aipm_typebot
```

**What happens:** Typebot builder opens at `http://localhost:8083`, viewer at `http://localhost:8084`.

### Quick Wins with Typebot

#### User Research Interview Bot
- **Start:** Welcome message explaining the research
- **Branch:** Different paths based on user type (new/existing)
- **Collect:** Pain points, feature requests, satisfaction scores
- **End:** Thank you + calendar link for follow-up

#### Product Feedback Collector
- **Trigger:** After specific user actions in your product
- **Collect:** Feature usage feedback, improvement suggestions
- **Route:** High-value feedback to product team, bugs to support

#### Onboarding Experience Prototype
- **Simulate:** Multi-step onboarding conversations
- **Test:** Different explanation approaches
- **Measure:** Drop-off points, confusion indicators

---

## Mastery: Orchestrating the Full Suite

The real power comes from **connecting these tools together**:

### Example: Complete Competitive Intelligence System
1. **n8n:** Monitors competitor websites, social media, job postings
2. **Langflow:** Analyzes gathered data for strategic insights
3. **ToolJet:** Displays findings in executive dashboard
4. **Typebot:** Collects team insights on competitive moves

### Example: AI Product Feature Pipeline
1. **Typebot:** Collects user feature requests conversationally
2. **Langflow:** Categorizes and prioritizes requests using AI
3. **n8n:** Routes high-priority items to product backlog
4. **ToolJet:** Shows feature request analytics to product team

---

## Troubleshooting

### "The tools won't start"
```bash
# Check if Docker is running
docker --version

# Restart the workflow tools
aipm_workflows_restart
```

### "I can't connect to the web interfaces"
- **Check the ports:** n8n (5678), Langflow (7860), ToolJet (8082), Typebot (8083)
- **Wait a few minutes:** Tools need time to fully start
- **Try `localhost` instead of `127.0.0.1`**

### "My workflows aren't saving"
- **Check disk space:** These tools store data locally
- **Ensure Docker has enough memory:** At least 4GB recommended
- **Don't close browser tabs while saving**

### "The AI responses are inconsistent"
- **Lower the temperature:** Use 0.1-0.3 for consistent outputs
- **Improve your prompts:** Be more specific about desired format
- **Add examples:** Show the AI what good output looks like

---

## Next Steps

**Mastered Tier 1?** → Try the [Market Research Playbook](MARKET_RESEARCH_PLAYBOOK.md) for competitive intelligence

**Ready for advanced demos?** → Combine with [Aider Playbook](AIDER_PLAYBOOK.md) to create comprehensive PoL Probes

**Want to measure everything?** → Build monitoring dashboards for all your PM experiments

**Need stakeholder buy-in?** → Use these tools to create "art of the possible" demonstrations

---

**Remember:** These aren't just tools - they're your **product validation laboratory**. Every workflow you build should answer a specific product question or de-risk a specific assumption. 

**The goal:** Show stakeholders what's possible, test concepts with real users, and validate ideas before committing engineering resources.