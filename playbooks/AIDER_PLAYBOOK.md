# Aider Playbook: Your AI Partner for Product Strategy

`aider` is your AI partner for thinking, drafting, and prototyping. Forget writing code; your primary job is to **direct the AI** to create the **Proof-of-Life (PoL) Probes** that answer your most pressing questions.

**The Philosophy:** Your goal is not to become a developer. Your goal is to use `aider` to create the cheapest artifact that tells you the harshest truth about your ideas.

---

## What Aider Does for Product Managers

Think of `aider` as **ChatGPT that can create and edit files**. But unlike ChatGPT:
- ✅ **Creates actual files** you can share with stakeholders  
- ✅ **Edits existing documents** without losing your work
- ✅ **Runs locally** so your product secrets stay private
- ✅ **Iterates quickly** - no copy/paste friction

**Real PM Use Cases:**
- Draft product briefs and PRDs
- Create user stories and acceptance criteria
- Build simple HTML prototypes for stakeholder demos
- Generate test data and user personas
- Write technical feasibility scripts
- Create competitive analysis documents

---

## Tier 1: Essentials (Drafting Your First Product Doc)

**Goal:** Use `aider` as a thinking partner to brainstorm and structure a one-pager for a new feature.

**Time Investment:** 15 minutes  
**Skill Level:** Complete beginner  
**PM Value:** Turn blank page paralysis into structured thinking

### Walkthrough: Brainstorming a One-Pager

#### Step 1: Start Your AI Assistant
```bash
cd ~/ai-pm-toolkit/prototypes
aider new-feature-one-pager.md
```

**What happens:** Aider starts and creates a new Markdown file. You'll see a friendly prompt waiting for your instruction.

#### Step 2: Give Your First Instruction
At the `>` prompt, type:

> You are a senior product manager. Brainstorm a one-pager for a new feature called 'AI Smart Summaries'. Create sections for: 1. Problem Statement, 2. Proposed Solution, 3. Target Audience, and 4. Success Metrics.

**Watch the magic:** Aider will write a complete document structure with thoughtful content in each section.

#### Step 3: Refine Like You Would with Any Team Member
Continue the conversation:

> That's a good start, but make the Problem Statement more urgent. Emphasize the time wasted by users reading long documents.

> Add a competitive analysis section. Include 3 competitors and how our approach differs.

> Make the success metrics more specific. Include both engagement metrics and business outcomes.

#### Step 4: Export and Share
When you're happy with the document:
- Type `/quit` to exit aider
- Your file is saved in `~/ai-pm-toolkit/prototypes/`
- Open it in any text editor or convert to PDF for stakeholders

### Pro Tips for Tier 1
- **Start broad, then get specific:** Begin with structure, then refine details
- **Use PM language:** Say "user stories" not "requirements", "stakeholders" not "users"
- **Iterate like you would in meetings:** Ask follow-up questions, challenge assumptions
- **Save variations:** Use `aider feature-v2.md` to create alternate versions

### Common Beginner Mistakes
- **Don't overthink the commands** - Just talk to it like a colleague
- **Don't worry about perfect formatting** - Focus on content first
- **Don't try to learn Markdown** - Aider handles the formatting

---

## Tier 2: Advanced Exploration (Building a Visual Prototype)

**Goal:** Turn your one-pager into a tangible, "vibe-coded" HTML prototype that stakeholders can see and touch.

**Time Investment:** 45 minutes  
**Skill Level:** Comfortable with basic commands  
**PM Value:** Show before tell - create touchable demos

### Walkthrough: A Fake Dashboard

#### Step 1: Create Your Visual Prototype
```bash
cd ~/ai-pm-toolkit/prototypes
aider summary-dashboard.html
```

#### Step 2: Describe Your Vision
> Based on our one-pager for AI Smart Summaries, create an HTML prototype of the main dashboard. It should have:
> - A clean header with the product name
> - A large text area where users can paste long documents
> - A prominent "Generate Summary" button
> - A results area that shows the AI-generated summary
> - Simple, modern styling that looks professional

#### Step 3: Add Realistic Details
> Make this feel more realistic. Add placeholder text in the text area that shows what a user might paste. Include a sample output that demonstrates the summarization quality.

> Add a sidebar showing recent summaries with timestamps and document titles. This helps stakeholders visualize the usage patterns.

#### Step 4: Make It Interactive (The Magic Moment)
> Add JavaScript so when someone clicks "Generate Summary", it shows a loading animation for 2 seconds, then displays the sample summary. This makes the demo feel real.

### Advanced Tier 2 Techniques

#### Creating User Journey Prototypes
```bash
aider onboarding-flow.html
```

> Create a 3-step onboarding flow for new users. Each step should be a separate section that shows/hides when users click Next. Include: 1) Welcome & value prop, 2) Upload first document, 3) See their first summary

#### Building Comparison Tables
```bash
aider competitor-analysis.html
```

> Create an interactive comparison table showing our AI Smart Summaries vs 3 competitors. Include features, pricing, and our advantages. Make our column highlighted in green.

### Pro Tips for Tier 2
- **Think "demo, not development"** - It doesn't need to really work, just look convincing
- **Use real company colors/fonts** - Makes stakeholders take it seriously  
- **Add micro-interactions** - Hover effects and loading states feel professional
- **Include edge cases** - Show error states, empty states, loading states

---

## Tier 3: Expert Mode (AI-Assisted Scripting)

**Goal:** Use `aider` for technical validation, such as writing a simple script to test an API or process data.

**Time Investment:** 1-2 hours  
**Skill Level:** Comfortable directing technical work  
**PM Value:** Validate technical feasibility without engineering resources

### Walkthrough: A Technical Feasibility Check

#### Step 1: Test API Integration
```bash
cd ~/ai-pm-toolkit/prototypes
aider test_summary_api.py
```

#### Step 2: Give Technical Requirements
> Write a Python script that tests the feasibility of our AI Smart Summaries feature. The script should:
> - Use the `ollama` library to connect to our local AI
> - Send a sample long document to the `deepseek-r1` model
> - Request a summary in a specific format (bullet points, max 3 sentences)
> - Time how long the summarization takes
> - Test with 3 different document lengths (short, medium, long)
> - Output a feasibility report showing response times and quality

#### Step 3: Add Error Handling and Edge Cases
> Add comprehensive error handling. Test what happens when:
> - The AI service is down
> - The document is too long for the model
> - The model returns an unexpected format
> - Network connectivity is poor

#### Step 4: Create a Stakeholder Report
> Modify the script to generate a simple HTML report that I can share with stakeholders. Include charts showing response times vs document length, and examples of input/output quality.

### Advanced Tier 3 Use Cases

#### Market Research Automation
```bash
aider competitive_analysis.py
```

> Create a script that automatically researches our top 5 competitors by:
> - Scraping their pricing pages
> - Analyzing their feature lists  
> - Checking their recent blog posts for product announcements
> - Generating a weekly competitive intelligence report

#### User Feedback Analysis
```bash
aider sentiment_analysis.py
```

> Write a script that processes our customer support tickets and NPS survey responses to:
> - Identify the top 10 most mentioned pain points
> - Categorize feedback by product area
> - Track sentiment trends over time
> - Generate monthly insights for the product team

#### A/B Test Results Processor
```bash
aider ab_test_analyzer.py
```

> Create a script that takes our A/B test data and:
> - Calculates statistical significance
> - Generates clear insights for non-technical stakeholders  
> - Creates visualizations showing conversion impact
> - Recommends next steps based on the results

### Pro Tips for Tier 3
- **Start with pseudocode** - Describe what you want in plain English first
- **Ask for explanations** - Have aider explain any technical concepts you don't understand
- **Test incrementally** - Build and test small pieces before combining them
- **Document everything** - Have aider add comments explaining what each part does

### When to Use Tier 3
- **Before writing a technical PRD** - Validate what's actually possible
- **When engineering says "it's complicated"** - Get your own technical understanding
- **For competitive analysis** - Automate research that would take weeks manually
- **When you need data but IT is backlogged** - Create your own analysis tools

---

## Mastery: Combining All Tiers

The real power comes from **chaining these techniques** for complex product challenges:

### Example: New Feature Validation Pipeline
1. **Tier 1:** Draft the feature concept document
2. **Tier 2:** Create interactive prototypes for user testing  
3. **Tier 3:** Build technical feasibility scripts
4. **Back to Tier 1:** Update the PRD with real data and validated designs

### Example: Competitive Response Strategy
1. **Tier 3:** Automate competitor monitoring and analysis
2. **Tier 1:** Generate strategic response documents
3. **Tier 2:** Create comparison demos for sales team
4. **Tier 3:** Build metrics tracking for competitive positioning

---

## Troubleshooting

### "Aider isn't working"
```bash
# Check if aider is installed
aider --version

# If not installed
pip install aider-chat
```

### "The AI responses are too generic"
- **Be more specific in your prompts**
- **Provide context about your company/industry**
- **Ask for examples and iterate on them**

### "I don't understand the technical output"
- **Ask aider to explain in simple terms**
- **Request documentation and comments**
- **Start simpler and build up complexity**

### "Files aren't being created where I expect"
- **Always start aider from the directory where you want files**
- **Use `pwd` to check your current location**
- **Create directories first: `mkdir project-name`**

---

## Next Steps

**Completed Tier 1?** → Try the [Visual Workflow Playbook](WORKFLOW_PLAYBOOK.md) to build demos without code

**Mastered Tier 2?** → Explore the [Market Research Playbook](MARKET_RESEARCH_PLAYBOOK.md) for competitive intelligence

**Ready for Tier 3?** → Start combining aider with other toolkit features for advanced PoL Probes

**Want more examples?** → Check out `~/ai-pm-toolkit/examples/` for real PM use cases

---

**Remember:** You're not learning to code. You're learning to **direct AI to solve product problems**. Every conversation with aider should end with something you can share, test, or validate with real users.