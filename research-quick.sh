#!/bin/bash
# AI PM Toolkit - Quick Research Script
# Provides basic research functionality using available AI tools

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to show usage
show_usage() {
    echo -e "${BLUE}🔍 AIPM Quick Research${NC}"
    echo "Usage: aipm_research_quick \"your research question\""
    echo
    echo "Examples:"
    echo "  aipm_research_quick \"AI trends in product management\""
    echo "  aipm_research_quick \"competitive landscape for no-code platforms\""
    echo "  aipm_research_quick \"market size for B2B productivity tools\""
    echo
    echo "This will generate a structured research brief using available AI models."
}

# Check if query provided
if [ $# -eq 0 ]; then
    show_usage
    exit 1
fi

QUERY="$*"

echo -e "${BLUE}🔍 AI PM Quick Research${NC}"
echo "========================================"
echo -e "${YELLOW}Research Query:${NC} $QUERY"
echo

# Check if Ollama is available
if command -v ollama >/dev/null 2>&1; then
    echo -e "${GREEN}✅ Using local AI model for research${NC}"
    echo
    
    # Create a research prompt
    RESEARCH_PROMPT="You are an expert product management researcher. Provide a comprehensive research brief on the following topic:

Topic: $QUERY

Please structure your response as follows:

## Executive Summary
Brief 2-3 sentence overview of key findings

## Market Analysis
- Market size and growth trends
- Key players and competitive landscape
- Market dynamics and forces

## Strategic Insights
- Opportunities and threats
- Success factors
- Emerging trends

## Product Management Implications
- Key considerations for PMs
- Strategic recommendations
- Potential risks to watch

## Next Steps
- Suggested follow-up research
- Key metrics to track
- Action items

Please be specific, actionable, and focus on insights that would help a product manager make strategic decisions."

    echo -e "${YELLOW}🤖 Generating research brief...${NC}"
    echo
    
    # Use Ollama to generate research
    if ollama run llama3.2 "$RESEARCH_PROMPT" 2>/dev/null; then
        echo
        echo -e "${GREEN}✅ Research complete!${NC}"
        echo
        echo -e "${YELLOW}💡 Next steps:${NC}"
        echo "  • Deep dive: aipm_market_research"
        echo "  • Financial data: aipm_company_lookup [TICKER]"
        echo "  • Document findings: aipm_knowledge"
    else
        echo -e "${RED}❌ Local AI model not available${NC}"
        echo "Install and start Ollama with: brew install ollama && ollama pull llama3.2"
        echo
        echo -e "${YELLOW}💡 Alternative research options:${NC}"
        echo "  • Use online research tools manually"
        echo "  • Try: aipm_brainstorm for AI collaboration"
        echo "  • Launch: aipm_market_research for financial data tools"
    fi
    
elif command -v aider >/dev/null 2>&1; then
    echo -e "${YELLOW}⚡ Using Aider for research collaboration${NC}"
    echo
    echo "Starting AI research session with Aider..."
    echo "Ask your research question: $QUERY"
    echo
    aider --message "Help me research this topic: $QUERY. Provide a structured research brief with market analysis, strategic insights, and PM implications."
    
else
    echo -e "${RED}❌ No AI tools available for automated research${NC}"
    echo
    echo -e "${YELLOW}💡 Manual research options:${NC}"
    echo "  • Install Ollama: brew install ollama && ollama pull llama3.2"
    echo "  • Install Aider: pip install aider-chat"
    echo "  • Use web research manually"
    echo "  • Launch financial research: aipm_market_research"
fi

echo
echo -e "${BLUE}📚 Research Resources:${NC}"
echo "  • Save findings: aipm_knowledge"
echo "  • Create visualizations: aipm_design"
echo "  • Build prototypes: aipm_lab"