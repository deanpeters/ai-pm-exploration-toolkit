#!/bin/bash
# AI PM Exploration Toolkit - API Configuration Script
# Enhanced PoL Probes with cloud AI capabilities
# MIT License

set -e  # Exit on any error

echo "🚀 AI PM Toolkit - Supercharge Your PoL Probes"
echo "==============================================="
echo ""
echo "✨ Transform your toolkit from good to AMAZING with cloud APIs!"
echo ""
echo "🎯 Why configure APIs? (100% optional but highly recommended):"
echo "   💰 FREE TIERS: 10M+ tokens/month across providers"
echo "   🧠 BETTER AI: Access GPT-4, Claude, Gemini for advanced analysis"
echo "   📊 REAL DATA: GitHub, financial data, competitive intelligence"
echo "   ⚡ SPEED: Cloud models for complex strategic analysis"
echo ""
echo "🔒 Privacy: Keys stored securely, only you have access"
echo "🏠 Local-first: All tools work offline, APIs just enhance them"
echo ""

# Check if we're in the right directory
if [[ ! -f "setup.sh" ]]; then
    echo "❌ Please run this script from the ai-pm-exploration-toolkit directory"
    exit 1
fi

# Create secure API key storage
API_CONFIG_FILE="$HOME/.aipm-apis"
TEMP_CONFIG="/tmp/aipm-api-setup"

echo "🔐 Setting up secure API key storage..."

# Function to securely prompt for API key
prompt_api_key() {
    local service_name="$1"
    local env_var_name="$2"
    local description="$3"
    local get_url="$4"
    
    echo ""
    echo "🔑 $service_name Configuration"
    echo "   $description"
    echo "   Get your key: $get_url"
    echo ""
    
    # Check if already configured (environment variable or config file)
    if [[ -n "${!env_var_name}" ]] || grep -q "export $env_var_name=" "$API_CONFIG_FILE" 2>/dev/null; then
        echo "   ✅ $service_name already configured"
        if [[ -n "${!env_var_name}" ]]; then
            echo "   Current source: Environment variable"
        else
            echo "   Current source: Config file"
        fi
        echo -n "   Update existing key? [y/N]: "
        read -r update_key
        if [[ ! "$update_key" =~ ^[Yy]$ ]]; then
            return
        fi
        # Remove existing key from config file
        grep -v "export $env_var_name=" "$API_CONFIG_FILE" > "$TEMP_CONFIG" 2>/dev/null || touch "$TEMP_CONFIG"
        mv "$TEMP_CONFIG" "$API_CONFIG_FILE"
    fi
    
    echo -n "   Enter your $service_name API key (or press Enter to skip): "
    read -r -s api_key
    echo ""
    
    if [[ -n "$api_key" ]]; then
        echo "export $env_var_name=\"$api_key\"" >> "$API_CONFIG_FILE"
        echo "   ✅ $service_name API key saved"
        # Set for current session
        export "$env_var_name"="$api_key"
    else
        echo "   ⏭️  Skipped $service_name"
    fi
}

# Create API config file if it doesn't exist
touch "$API_CONFIG_FILE"
chmod 600 "$API_CONFIG_FILE"  # Secure permissions

echo "🚀 Configure Enhanced AI PM Capabilities"
echo ""
echo "Enhanced PoL Probes with cloud AI provide:"
echo "• Advanced strategic analysis with Claude"
echo "• Competitive intelligence with GitHub API"
echo "• 10M+ tokens/month with free API tiers"
echo "• Market research with multiple AI models"
echo ""

# Configure APIs
prompt_api_key "Claude (Anthropic)" "CLAUDE_API_KEY" "Best for strategic product analysis and decision-making" "https://console.anthropic.com/account/keys"

prompt_api_key "OpenAI" "OPENAI_API_KEY" "GPT models for creative prototyping and content generation" "https://platform.openai.com/account/api-keys"

prompt_api_key "DeepSeek" "DEEPSEEK_API_KEY" "Cost-effective alternative for coding and analysis" "https://platform.deepseek.com/api_keys"

prompt_api_key "Google Gemini" "GEMINI_API_KEY" "Multimodal AI for document and image analysis" "https://makersuite.google.com/app/apikey"

prompt_api_key "GitHub" "GITHUB_API_KEY" "Competitive intelligence and repo analysis" "https://github.com/settings/tokens"

prompt_api_key "Perplexity" "PERPLEXITY_API_KEY" "Real-time market research and competitive analysis" "https://www.perplexity.ai/settings/api"

prompt_api_key "LangSmith" "LANGCHAIN_API_KEY" "LLM application monitoring and optimization" "https://smith.langchain.com/settings"

prompt_api_key "Arize" "ARIZE_API_KEY" "ML observability for AI product features" "https://app.arize.com/settings/api-keys"

# Market Research & Competitive Intelligence APIs
echo ""
echo "📊 Market Research & Competitive Intelligence APIs"
echo "=================================================="

prompt_api_key "SimilarWeb" "SIMILARWEB_API_KEY" "Digital intelligence and web analytics" "https://www.similarweb.com/corp/developer/api"

prompt_api_key "Alpha Vantage" "ALPHA_VANTAGE_API_KEY" "Financial data and market research (for OpenBB)" "https://www.alphavantage.co/support/#api-key"

prompt_api_key "Yahoo Finance" "YAHOO_FINANCE_API_KEY" "Stock market data and financial research (optional)" "https://finance.yahoo.com/"

prompt_api_key "News API" "NEWS_API_KEY" "Market news and competitive intelligence" "https://newsapi.org/account"

prompt_api_key "Twitter API" "TWITTER_BEARER_TOKEN" "Social media competitive intelligence" "https://developer.twitter.com/en/portal/dashboard"

# Workflow Tools (Optional Enterprise Features)
echo ""
echo "🌊 Workflow Tools - Enterprise Features (Optional)"
echo "=================================================="

prompt_api_key "n8n Enterprise" "N8N_ACTIVATION_KEY" "n8n enterprise license key for advanced workflow features (optional)" "https://n8n.io/pricing/"

# Update shell configuration
echo ""
echo "🔧 Updating shell configuration..."

# Add API config to shell profiles
for shell_config in ~/.zshrc ~/.bashrc ~/.bash_profile; do
    if [[ -f "$shell_config" ]]; then
        # Remove existing API config line
        grep -v "source.*aipm-apis" "$shell_config" > "${shell_config}.tmp" 2>/dev/null || cp "$shell_config" "${shell_config}.tmp"
        
        # Add new API config line
        echo "" >> "${shell_config}.tmp"
        echo "# AI PM Toolkit API Configuration" >> "${shell_config}.tmp"
        echo "if [[ -f \"$API_CONFIG_FILE\" ]]; then" >> "${shell_config}.tmp"
        echo "    source \"$API_CONFIG_FILE\"" >> "${shell_config}.tmp"
        echo "fi" >> "${shell_config}.tmp"
        
        mv "${shell_config}.tmp" "$shell_config"
        echo "   ✅ Updated $shell_config"
    fi
done

# Create enhanced aipm command if APIs are configured
api_count=$(grep -c "export.*API_KEY=" "$API_CONFIG_FILE" 2>/dev/null || echo "0")

if [[ $api_count -gt 0 ]]; then
    echo ""
    echo "🚀 Creating enhanced aipm commands..."
    
    # Create enhanced aipm script
    cat > ~/ai-pm-toolkit/aipm-enhanced << 'EOF'
#!/bin/bash
# AI PM Exploration Toolkit - Enhanced PoL Probes with Cloud APIs
# "Use the cheapest prototype that tells the harshest truth" ~ Dean Peters

# Source API keys
if [[ -f "$HOME/.aipm-apis" ]]; then
    source "$HOME/.aipm-apis"
fi

case "$1" in
    "learn")
        echo "🔬 Enhanced Feasibility Check: $2"
        if [[ -n "$CLAUDE_API_KEY" ]]; then
            aider --model anthropic/claude-3-5-sonnet-20241022 --message "Create a 1-2 day spike-and-delete test for: $2. Use advanced strategic analysis to surface technical risk and business implications. Include GenAI prompt chains, competitive analysis, API tests, or tool fit evaluation as needed."
        elif [[ -n "$OPENAI_API_KEY" ]]; then
            aider --model openai/gpt-4 --message "Create a 1-2 day spike-and-delete test for: $2. Focus on surfacing technical risk and business implications. Include GenAI prompt chains, API tests, or tool fit evaluation as needed."
        else
            aider --model ollama/deepseek-r1:7b --message "Create a 1-2 day spike-and-delete test for: $2. Focus on surfacing technical risk, not building to impress. Include GenAI prompt chains, API tests, or tool fit evaluation as needed."
        fi
        ;;
    "compete")
        echo "🎨 Enhanced Competitive Analysis: $2"
        if [[ -n "$GITHUB_API_KEY" && -n "$CLAUDE_API_KEY" ]]; then
            aider --model anthropic/claude-3-5-sonnet-20241022 --message "Build an enhanced competitive analysis probe for: $2. Use GitHub API to analyze competitor repositories, market positioning, and technical approaches. Create vibe-coded prototype with real competitive intelligence data."
        else
            aider --model ollama/deepseek-r1:7b --message "Build a vibe-coded probe for: $2. Create fake frontend + semi-plausible backend using tools like ChatGPT + Canvas + Airtable. Just enough illusion to catch real user signals in 48 hours - not production quality."
        fi
        ;;
    "research")
        echo "📊 Market Research Probe: $2"
        if [[ -n "$PERPLEXITY_API_KEY" ]]; then
            echo "Using Perplexity for real-time market intelligence..."
            # Add Perplexity integration here
        fi
        aider --model anthropic/claude-3-5-sonnet-20241022 --message "Create comprehensive market research analysis for: $2. Include competitive landscape, user personas, market sizing, and strategic recommendations."
        ;;
    "monitor")
        echo "📈 AI Monitoring Setup: $2"
        if [[ -n "$ARIZE_API_KEY" || -n "$LANGCHAIN_API_KEY" ]]; then
            aider --model anthropic/claude-3-5-sonnet-20241022 --message "Set up AI monitoring and observability for: $2. Include LLM performance tracking, prompt optimization, and user interaction analytics."
        else
            echo "⚠️  No monitoring APIs configured. Run ./configure-apis.sh to add Arize or LangSmith"
        fi
        ;;
    *)
        echo "🚀 AI PM Enhanced Toolkit - Cloud-Powered PoL Probes"
        echo ""
        echo "Enhanced capabilities with configured APIs:"
        echo "  ./aipm-enhanced learn 'technical feasibility + strategic analysis'   # Advanced analysis"
        echo "  ./aipm-enhanced compete 'real competitive intelligence probe'       # GitHub + Claude"
        echo "  ./aipm-enhanced research 'comprehensive market analysis'            # Multi-source research"
        echo "  ./aipm-enhanced monitor 'AI feature performance tracking'           # LLM observability"
        echo ""
        echo "Standard local commands also available:"
        echo "  ./aipm fast 'friction point validation'                            # Quick local tests"
        echo "  ./aipm prototype 'narrative walkthrough'                           # Story-driven probes"
        echo "  ./aipm experiment 'synthetic data simulation'                      # Data modeling"
        echo ""
        echo "💡 Cloud APIs configured: $api_count"
        echo "🎯 Focus: Show before Tell, Touch before Sell."
        ;;
esac
EOF

    chmod +x ~/ai-pm-toolkit/aipm-enhanced
    
    # Add enhanced alias
    echo 'alias aipm_enhanced="cd ~/ai-pm-toolkit && ./aipm-enhanced"' >> ~/.zshrc
    
    echo "   ✅ Enhanced aipm-enhanced command created"
fi

# Clean up
rm -f "$TEMP_CONFIG"

echo ""
echo "✅ API Configuration Complete!"
echo ""

if [[ $api_count -gt 0 ]]; then
    echo "🚀 Enhanced Mode: $api_count API(s) configured"
    echo "   • Advanced strategic analysis capabilities"
    echo "   • Competitive intelligence with real data"
    echo "   • 10M+ tokens/month with free tiers"
    echo ""
    echo "🧪 Try enhanced PoL Probes:"
    echo "   aipm_enhanced learn 'AI-powered user segmentation feasibility'"
    echo "   aipm_enhanced compete 'analyze competitor GitHub repositories'"
    echo "   aipm_enhanced research 'comprehensive market landscape analysis'"
    echo "   aipm_enhanced monitor 'set up LLM performance tracking'"
else
    echo "🦙 Local Mode: No APIs configured"
    echo "   • All PoL Probes work offline with local AI"
    echo "   • Run this script again anytime to add cloud capabilities"
fi

echo ""
echo "🔄 Restart terminal or run: source ~/.zshrc"
echo "📁 API keys stored securely in: $API_CONFIG_FILE"
echo ""
echo "💡 Remember: Use the cheapest prototype that tells the harshest truth"