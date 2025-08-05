#!/bin/bash
# AI PM Toolkit - Brainstorm Script
# Smart AI collaboration with fallback options

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🤖 AI PM Brainstorm - Smart AI Collaboration${NC}"
echo "=============================================="

# Check for local AI models first
if command -v ollama >/dev/null 2>&1 && ollama list 2>/dev/null | grep -q llama; then
    echo -e "${GREEN}✅ Local AI models available${NC}"
    echo -e "${YELLOW}Using Ollama for private, cost-free collaboration${NC}"
    echo
    
    # Use Aider with Ollama
    export AIDER_MODEL="ollama/llama3.2"
    aider --model ollama/llama3.2 "$@"
    
elif command -v aider >/dev/null 2>&1; then
    echo -e "${YELLOW}⚠️  No local AI models found${NC}"
    echo "Options:"
    echo "1. Set up free local AI: ollama pull llama3.2"
    echo "2. Use Aider with API keys (will prompt for setup)"
    echo "3. Exit and set up local AI first"
    echo
    
    read -p "Choose option (1-3): " choice
    
    case $choice in
        1)
            echo -e "${YELLOW}🚀 Setting up local AI...${NC}"
            if command -v ollama >/dev/null 2>&1; then
                ollama pull llama3.2
                echo -e "${GREEN}✅ Local AI ready! Restarting brainstorm session...${NC}"
                export AIDER_MODEL="ollama/llama3.2"
                aider --model ollama/llama3.2 "$@"
            else
                echo -e "${RED}❌ Ollama not installed${NC}"
                echo "Install with: brew install ollama"
                exit 1
            fi
            ;;
        2)
            echo -e "${YELLOW}🔑 Starting Aider with API setup...${NC}"
            echo "Aider will guide you through API key setup"
            aider "$@"
            ;;
        3)
            echo "Setting up local AI first:"
            echo "  brew install ollama"
            echo "  ollama pull llama3.2"
            echo "  aipm_brainstorm"
            exit 0
            ;;
        *)
            echo "Invalid option"
            exit 1
            ;;
    esac
    
else
    echo -e "${RED}❌ Aider not installed${NC}"
    echo
    echo -e "${YELLOW}💡 Install AI collaboration tools:${NC}"
    echo "  pip install aider-chat"
    echo "  brew install ollama"
    echo "  ollama pull llama3.2"
    echo "  aipm_brainstorm"
    exit 1
fi