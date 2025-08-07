# 🚀 Langflow PM Workflow Templates

This directory contains pre-built Langflow workflow templates designed specifically for **Product Managers** using the AI PM Toolkit.

## 🎯 Available Templates

### **Essential PM Workflows**

#### 1. **PM Market Research Pipeline** 
- **Purpose**: Automated competitive intelligence and market analysis
- **Data Sources**: Real financial data via yfinance API
- **AI Models**: DeepSeek R1 7B for strategic analysis
- **Output**: Structured market research reports with actionable insights

#### 2. **AI Chat Assistant for PMs**
- **Purpose**: PM-focused conversational AI with domain expertise
- **AI Models**: Llama 3.2 3B for rapid responses, DeepSeek R1 for complex analysis
- **Capabilities**: Product strategy, roadmap planning, user research guidance
- **Output**: Interactive chat interface with PM-specific knowledge

#### 3. **Competitive Analysis Workflow**
- **Purpose**: Multi-company analysis with financial benchmarking
- **Data Integration**: Live market data + AI-powered analysis
- **AI Models**: DeepSeek R1 7B for strategic competitive insights
- **Output**: Comparative analysis dashboards and strategic recommendations

## 🔧 Integration with AI PM Toolkit

### **Connected Infrastructure**
- **Ollama Integration**: Direct access to local DeepSeek R1 7B and Llama 3.2 3B models
- **Market Research API**: Real-time financial data via `shared/market_research.py`
- **Jupyter Lab**: Export workflow results to notebook templates for further analysis
- **Web Dashboard**: Seamless integration with main toolkit interface

### **Data Flow Architecture**
```
Langflow Workflows → Ollama AI Models → Market Research API → Jupyter Analysis → PM Insights
```

## 📊 Template Categories

### **🔍 Research & Analysis**
- Market sizing and opportunity assessment
- Competitive landscape mapping  
- User research synthesis and insights
- Feature prioritization frameworks

### **🎯 Strategy & Planning**
- Product roadmap validation
- Go-to-market strategy workflows
- Risk assessment and mitigation
- Stakeholder alignment processes

### **💬 Communication & Collaboration**
- Executive presentation preparation
- Customer feedback analysis
- Team alignment and decision-making
- Stakeholder update automation

## 🚀 Getting Started

### **Prerequisites**
1. **Langflow Running**: Ensure `aipm_workflows` has started Langflow (http://localhost:7860)
2. **Ollama Models**: Verify DeepSeek R1 7B and Llama 3.2 3B are available
3. **Market Research API**: Confirm real financial data integration is working

### **Loading Templates**
1. **Access Langflow**: Open http://localhost:7860 in your browser
2. **Import Templates**: Use Langflow's import feature to load `.json` template files
3. **Configure Connections**: Verify Ollama endpoints point to `http://host.docker.internal:11434`
4. **Test Workflows**: Run sample workflows to ensure proper integration

## 🎨 Template Development Philosophy

These templates follow **Dean Peters' PoL Probe Framework**:

### **"Use the cheapest prototype that tells the harshest truth"**
- **Rapid Experimentation**: Visual workflows enable quick hypothesis testing
- **Real Data Integration**: No synthetic data - direct connection to live market intelligence  
- **Brutal Honesty**: AI models configured for direct, actionable insights
- **Disposable by Design**: Templates built for iteration, not perfection

### **4E Framework Alignment**
- **🎓 Education**: Learn AI concepts through visual workflow building
- **🧪 Experimentation**: Test product hypotheses with real data flows
- **🔍 Exploration**: Discover AI possibilities through drag-and-drop interfaces  
- **📊 Explanation**: Create workflow demos for stakeholder presentations

## 📁 Template File Structure
```
langflow-templates/
├── pm-market-research.json          # Market intelligence workflow
├── ai-chat-assistant.json            # PM conversational AI
├── competitive-analysis.json         # Multi-company benchmarking  
├── user-research-synthesis.json      # Customer insight aggregation
├── roadmap-validation.json           # Strategic planning workflow
└── executive-presentation.json       # Stakeholder communication
```

## 🔗 Integration Points

### **Ollama AI Models**
- **Endpoint**: `http://host.docker.internal:11434`
- **DeepSeek R1 7B**: Complex strategic analysis and reasoning
- **Llama 3.2 3B**: Rapid responses and conversational interactions

### **Market Research API**
- **Endpoint**: Internal toolkit API for live financial data
- **Data Sources**: yfinance for real-time market intelligence
- **Output Format**: JSON structured for Langflow consumption

### **Web Dashboard Integration**
- **Access**: Templates manageable via main toolkit dashboard
- **Status Monitoring**: Real-time workflow execution tracking
- **Results Export**: Direct integration with Jupyter Lab for deeper analysis

---

**🎯 Purpose**: Enable Product Managers to create sophisticated AI workflows through visual drag-and-drop interfaces, leveraging real market data and local AI models for strategic decision-making.