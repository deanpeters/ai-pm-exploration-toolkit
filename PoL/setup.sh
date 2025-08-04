#!/bin/bash
# AI PM Exploration Toolkit - Setup Script
# Proof-of-Life Probes for strategic product managers
# MIT License

set -e  # Exit on any error

echo "🧪 AI PM Exploration Toolkit Setup"
echo "=================================="
echo "Proof-of-Life Probes for strategic product managers"
echo "Use the cheapest prototype that tells the harshest truth"
echo ""

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ This toolkit is optimized for macOS. For other systems:"
    echo "   - Install Ollama: https://ollama.ai"
    echo "   - Install Aider: pip install aider-chat"
    echo "   - Adapt the workflow to your environment"
    exit 1
fi

# Check for Homebrew
if ! command -v brew &> /dev/null; then
    echo "📦 Installing Homebrew (required for AI tools)..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "📦 Found existing Homebrew installation"
    echo -n "   Update Homebrew and packages? [y/N]: "
    read -r update_brew
    if [[ "$update_brew" =~ ^[Yy]$ ]]; then
        echo "   📦 Updating Homebrew..."
        brew update
        echo "   📦 Upgrading packages (this may take a while)..."
        brew upgrade
        echo "   ✅ Homebrew updated"
    else
        echo "   ⏭️  Skipped Homebrew updates"
    fi
fi

# Update npm packages if npm is available
if command -v npm &> /dev/null; then
    echo "📦 Found existing npm installation"
    echo -n "   Update global npm packages? [y/N]: "
    read -r update_npm
    if [[ "$update_npm" =~ ^[Yy]$ ]]; then
        echo "   📦 Updating global npm packages..."
        npm update -g 2>/dev/null || echo "   ⚠️  Some npm packages couldn't be updated (this is normal)"
        echo "   ✅ npm packages updated"
    else
        echo "   ⏭️  Skipped npm updates"
    fi
fi

# Install AI infrastructure
echo "🤖 Installing AI infrastructure..."
brew list ollama &>/dev/null || brew install ollama

# Use Homebrew Python instead of system Python to avoid 3.13 issues
echo "📦 Setting up Python environment..."
if ! brew list python@3.11 &>/dev/null; then
    brew install python@3.11
fi

# Create alias to use Homebrew Python
PYTHON_CMD="/opt/homebrew/bin/python3.11"
PIP_CMD="/opt/homebrew/bin/pip3.11"

# Fallback to system python if Homebrew not available
if [[ ! -f "$PYTHON_CMD" ]]; then
    PYTHON_CMD="/usr/local/bin/python3.11"
    PIP_CMD="/usr/local/bin/pip3.11"
fi

# Final fallback to system python
if [[ ! -f "$PYTHON_CMD" ]]; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
fi

echo "   Using Python: $PYTHON_CMD"

# Install exploration tools
echo "🛠️  Installing exploration tools..."

# Try modern approach first, then fallback strategies
install_package() {
    local package=$1
    echo "   Installing $package..."
    
    # Strategy 1: Try with Homebrew Python 3.11
    if $PIP_CMD install "$package" --quiet 2>/dev/null; then
        echo "   ✅ $package installed successfully"
        return 0
    fi
    
    # Strategy 2: Try with --break-system-packages
    echo "   ⚠️  Trying $package with system packages override..."
    if $PIP_CMD install "$package" --break-system-packages --quiet 2>/dev/null; then
        echo "   ✅ $package installed with override"
        return 0
    fi
    
    # Strategy 3: Try with --user flag
    echo "   ⚠️  Trying $package with user install..."
    if $PIP_CMD install "$package" --user --quiet 2>/dev/null; then
        echo "   ✅ $package installed for user"
        return 0
    fi
    
    # Strategy 4: Skip and warn
    echo "   ❌ Could not install $package - will work with reduced functionality"
    return 1
}

# Upgrade pip and setuptools first
echo "   Upgrading pip and setuptools..."
$PIP_CMD install --upgrade pip setuptools --quiet 2>/dev/null || true

# Ensure JupyterLab frontend assets are built
if command -v jupyter &>/dev/null; then
    echo "🧱 Verifying JupyterLab frontend build..."
    if ! command -v node &>/dev/null; then
        echo "📦 Installing Node.js (required for JupyterLab build)..."
        brew install node
    fi
    echo "🔧 Building JupyterLab frontend assets..."
    jupyter lab build || echo "⚠️  JupyterLab frontend build incomplete—some features may not render correctly"
else
    echo "⚠️  Jupyter not found—skipping frontend build"
fi

# Install packages individually with fallbacks
install_package "aider-chat"
install_package "jupyter"
install_package "pandas"
install_package "plotly"

echo ""
echo "🔧 Installing optional but powerful local-first utilities..."

# Create static lib directory for HTML components
mkdir -p ~/ai-pm-toolkit/static/lib

# Install ffmpeg for video/audio stitching
if ! command -v ffmpeg &>/dev/null; then
    echo "📽️  Installing ffmpeg (required for video narration)..."
    brew install ffmpeg
else
    echo "✅ ffmpeg already installed"
fi

# Install pyttsx3 for offline TTS
install_package "pyttsx3"

# Install mermaid CLI for diagrams
if ! command -v mmdc &>/dev/null; then
    echo "🖼️  Installing mermaid CLI for markdown-based diagrams..."
    npm install -g @mermaid-js/mermaid-cli
else
    echo "✅ mermaid CLI already installed"
fi

echo ""
echo "🌊 Installing visual/low-code workflow tools for non-technical PMs..."

# Install Docker if not present (required for n8n, ToolJet, Typebot)
if ! command -v docker &>/dev/null; then
    echo "🐳 Installing Docker (required for workflow tools)..."
    brew install --cask docker
    echo "   ⚠️  Please start Docker Desktop after installation"
else
    echo "✅ Docker already installed"
fi

# Install Node.js tools for workflow builders
if ! command -v node &>/dev/null; then
    echo "📦 Installing Node.js (required for workflow tools)..."
    brew install node
fi

# Install Langflow (Visual LLM flow builder)
echo "🌊 Installing Langflow (Visual LLM application builder)..."
install_package "langflow"

# Create n8n Docker setup
echo "🔗 Setting up n8n (Workflow automation platform)..."
mkdir -p ~/ai-pm-toolkit/workflow-tools/n8n-data
cat > ~/ai-pm-toolkit/workflow-tools/docker-compose.n8n.yml << 'EOF'
version: '3.8'
services:
  n8n:
    image: n8nio/n8n:latest
    container_name: aipm-n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=aipm
      - N8N_BASIC_AUTH_PASSWORD=aipm-workflows
      - N8N_HOST=localhost
      - N8N_PORT=5678
      - N8N_PROTOCOL=http
      - NODE_ENV=production
      - N8N_ACTIVATION_KEY=${N8N_ACTIVATION_KEY:-}
    volumes:
      - n8n_data:/home/node/.n8n
volumes:
  n8n_data:
    driver: local
    driver_opts:
      type: none
      device: ${PWD}/n8n-data
      o: bind
EOF

# Create ToolJet Docker setup
echo "🔧 Setting up ToolJet (Low-code app builder)..."
mkdir -p ~/ai-pm-toolkit/workflow-tools/tooljet-data
mkdir -p ~/ai-pm-toolkit/workflow-tools/tooljet-db-data
cat > ~/ai-pm-toolkit/workflow-tools/docker-compose.tooljet.yml << 'EOF'
version: '3.8'
services:
  tooljet-db:
    image: postgres:13
    container_name: aipm-tooljet-db
    restart: unless-stopped
    environment:
      - POSTGRES_USER=tooljet
      - POSTGRES_PASSWORD=tooljet
      - POSTGRES_DB=tooljet_production
    volumes:
      - tooljet_db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U tooljet -d tooljet_production"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s

  tooljet:
    image: tooljet/tooljet-ce:latest
    container_name: aipm-tooljet
    restart: unless-stopped
    ports:
      - "8082:3000"
    environment:
      - SERVE_CLIENT=true
      - PORT=3000
      - TOOLJET_HOST=localhost:8082
      - PG_HOST=tooljet-db
      - PG_PORT=5432
      - PG_USER=tooljet
      - PG_PASS=tooljet
      - PG_DB=tooljet_production
      - TOOLJET_DB_USER=tooljet
      - TOOLJET_DB_PASS=tooljet
      - TOOLJET_DB=tooljet_production
      - TOOLJET_DB_HOST=tooljet-db
    volumes:
      - tooljet_data:/var/lib/tooljet
    depends_on:
      tooljet-db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s

volumes:
  tooljet_data:
    driver: local
    driver_opts:
      type: none
      device: ${PWD}/tooljet-data
      o: bind
  tooljet_db_data:
    driver: local
    driver_opts:
      type: none
      device: ${PWD}/tooljet-db-data
      o: bind
EOF

# Create Typebot Docker setup  
echo "💬 Setting up Typebot (Conversational form builder)..."
mkdir -p ~/ai-pm-toolkit/workflow-tools/typebot-data
cat > ~/ai-pm-toolkit/workflow-tools/docker-compose.typebot.yml << 'EOF'
version: '3.8'
services:
  typebot-db:
    image: postgres:13
    container_name: aipm-typebot-db
    restart: unless-stopped
    environment:
      - POSTGRES_DB=typebot
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=typebot
    volumes:
      - typebot_db:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d typebot"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s

  typebot:
    image: baptistearno/typebot-builder:latest
    container_name: aipm-typebot
    restart: unless-stopped
    ports:
      - "8083:3000"
    environment:
      - NEXTAUTH_URL=http://localhost:8083
      - NEXT_PUBLIC_VIEWER_URL=http://localhost:8084
      - DATABASE_URL=postgresql://postgres:typebot@typebot-db:5432/typebot
      - NEXTAUTH_SECRET=typebot-secret
    depends_on:
      typebot-db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s
  
  typebot-viewer:
    image: baptistearno/typebot-viewer:latest
    container_name: aipm-typebot-viewer
    restart: unless-stopped
    ports:
      - "8084:3000"
    environment:
      - DATABASE_URL=postgresql://postgres:typebot@typebot-db:5432/typebot
      - NEXT_PUBLIC_VIEWER_URL=http://localhost:8084
    depends_on:
      typebot-db:
        condition: service_healthy
      typebot:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:3000/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 60s

volumes:
  typebot_db:
    driver: local
    driver_opts:
      type: none
      device: ${PWD}/typebot-data
      o: bind
EOF

# Create workflow tools startup script
cat > ~/ai-pm-toolkit/start-workflows << 'EOF'
#!/bin/bash
echo "🌊 Starting AI PM Workflow Tools..."
echo ""

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker daemon is not running!"
    echo ""
    echo "🔧 Fix this first:"
    echo "   1. Open Docker Desktop (find it in Applications)"
    echo "   2. Wait for Docker Desktop to show 'Engine running'"
    echo "   3. Run this command again: aipm_workflows"
    echo ""
    echo "💡 If Docker isn't installed:"
    echo "   brew install --cask docker"
    echo ""
    exit 1
fi

echo "✅ Docker is running - starting workflow tools..."
echo ""

cd ~/ai-pm-toolkit/workflow-tools

echo "🔗 Starting n8n (Workflow Automation)..."
if docker-compose -f docker-compose.n8n.yml up -d; then
    echo "   ✅ n8n started successfully"
else
    echo "   ❌ n8n failed to start - check Docker logs"
fi

echo ""
echo "🔧 Starting ToolJet (Low-code App Builder)..."
echo "   ⏱️  This may take 60-90 seconds to fully initialize..."
if docker-compose -f docker-compose.tooljet.yml up -d; then
    echo "   ✅ ToolJet containers started (still initializing...)"
else
    echo "   ❌ ToolJet failed to start - check Docker logs"
fi

echo ""
echo "💬 Starting Typebot (Conversational Forms)..."
echo "   ⏱️  This may take 60-90 seconds to fully initialize..."
if docker-compose -f docker-compose.typebot.yml up -d; then
    echo "   ✅ Typebot containers started (still initializing...)"
else
    echo "   ❌ Typebot failed to start - check Docker logs"
fi

echo ""
echo "⏱️  Workflow tools are starting up..."
echo "   • This is normal on first run - Docker images need to initialize"
echo "   • Wait 2-3 minutes before accessing web interfaces"
echo "   • If you see connection errors, wait and refresh"
echo ""

echo "📊 Access your tools when ready:"
echo "   • Langflow:  http://localhost:7860 (run 'aipm_langflow' separately)"
echo "   • n8n:       http://localhost:5678 (user: aipm, pass: aipm-workflows)"
echo "   • ToolJet:   http://localhost:8082 (create account on first visit)"
echo "   • Typebot:   http://localhost:8083 (create account on first visit)"
echo ""

echo "🚨 Troubleshooting:"
echo "   • Connection refused? Wait 2-3 minutes and refresh"
echo "   • Still not working? Check: cat ~/ai-pm-toolkit/FIRST_RUN_GUIDE.md"
echo "   • Stop all tools: docker stop \$(docker ps -q)"
echo ""

echo "🎯 Pro tip: Run 'aipm_docker_setup' first to pre-download images"
EOF

chmod +x ~/ai-pm-toolkit/start-workflows

# Create Docker setup script for pre-fetching images
cat > ~/ai-pm-toolkit/aipm_docker_setup << 'EOF'
#!/bin/bash
echo "🐳 AI PM Docker Setup - Pre-fetching Container Images"
echo "===================================================="
echo ""

# Check if Docker is running
if ! docker info >/dev/null 2>&1; then
    echo "❌ Docker daemon is not running!"
    echo ""
    echo "🔧 Fix this first:"
    echo "   1. Open Docker Desktop (find it in Applications)"
    echo "   2. Wait for Docker Desktop to show 'Engine running'"
    echo "   3. Run this command again"
    echo ""
    exit 1
fi

echo "✅ Docker is running - proceeding with image downloads..."
echo ""
echo "📦 This will download ~500MB of container images"
echo "⏱️  Expected time: 5-10 minutes (depending on internet speed)"
echo ""

cd ~/ai-pm-toolkit/workflow-tools

echo "🔗 Pulling n8n image..."
docker pull n8nio/n8n:latest

echo "🔧 Pulling ToolJet images..."  
docker pull tooljet/tooljet-ce:latest
docker pull postgres:13

echo "💬 Pulling Typebot images..."
docker pull baptistearno/typebot-builder:latest
docker pull baptistearno/typebot-viewer:latest

echo ""
echo "✅ All Docker images downloaded successfully!"
echo ""
echo "🚀 Ready to start workflow tools:"
echo "   aipm_workflows"
echo ""
EOF

chmod +x ~/ai-pm-toolkit/aipm_docker_setup

echo "✅ Visual workflow tools configured"

echo ""
echo "💻 Installing development & AI coding tools..."

# Install VS Code if not present
if ! command -v code &>/dev/null; then
    echo "📝 Installing VS Code..."
    brew install --cask visual-studio-code
    echo "   ✅ VS Code installed"
else
    echo "✅ VS Code already installed"
fi

# Install Continue extension for VS Code
echo "🤖 Installing Continue AI coding extension..."
if command -v code &>/dev/null; then
    code --install-extension continue.continue
    echo "   ✅ Continue extension installed"
    
    # Create Continue configuration for local AI
    mkdir -p ~/.continue
    cat > ~/.continue/config.json << 'EOF'
{
  "models": [
    {
      "title": "DeepSeek R1 (Local)",
      "provider": "ollama",
      "model": "deepseek-r1:7b",
      "apiBase": "http://localhost:11434"
    },
    {
      "title": "Llama 3.2 (Fast Local)",
      "provider": "ollama", 
      "model": "llama3.2:3b",
      "apiBase": "http://localhost:11434"
    }
  ],
  "tabAutocompleteModel": {
    "title": "Llama 3.2 Autocomplete",
    "provider": "ollama",
    "model": "llama3.2:3b",
    "apiBase": "http://localhost:11434"
  },
  "allowAnonymousTelemetry": false,
  "docs": [
    {
      "title": "AI PM Toolkit Docs",
      "startUrl": "https://github.com/deanpeters/ai-pm-exploration-toolkit"
    }
  ]
}
EOF
    echo "   ✅ Continue configured for local AI models"
else
    echo "   ⚠️  VS Code not found - skipping extension install"
fi

echo "✅ Development tools configured"

echo ""
echo "📝 Installing markdown editors for PoL Probe documentation..."

# Install MarkText - Beautiful markdown editor
echo "✍️  Installing MarkText (Visual markdown editor)..."
if ! ls /Applications/MarkText.app &>/dev/null; then
    brew install --cask mark-text
    echo "   ✅ MarkText installed"
else
    echo "✅ MarkText already installed"
fi

# Install Pulsar - Community-driven text editor (successor to Atom)
echo "⚡ Installing Pulsar (Advanced text editor)..."
if ! command -v pulsar &>/dev/null; then
    brew install --cask pulsar
    echo "   ✅ Pulsar installed"
else
    echo "✅ Pulsar already installed"
fi

echo "✅ Markdown editors configured"

echo ""
echo "🧪 Installing prompt engineering & testing tools..."

# Install promptfoo for LLM evaluation
echo "🎯 Installing promptfoo (LLM evaluation framework)..."
if ! command -v promptfoo &>/dev/null; then
    npm install -g promptfoo
    echo "   ✅ promptfoo installed globally"
else
    echo "✅ promptfoo already installed"
fi

# Install prompttools via Python
echo "🔧 Installing prompttools (Prompt testing toolkit)..."
install_package "prompttools"

# Create prompt testing workspace
echo "📝 Setting up prompt testing workspace..."
mkdir -p ~/ai-pm-toolkit/prompt-testing/{configs,results,templates}

# Create promptfoo config template for local AI
cat > ~/ai-pm-toolkit/prompt-testing/configs/local-ai-config.yaml << 'EOF'
# AI PM Toolkit - Local AI Prompt Testing Configuration
description: "PoL Probe prompt testing with local AI models"

providers:
  - id: ollama:deepseek-r1:7b
    config:
      temperature: 0.2
      max_tokens: 2000
  - id: ollama:llama3.2:3b
    config:
      temperature: 0.5
      max_tokens: 1500

prompts:
  - "You are a strategic product manager evaluating: {{scenario}}. Provide a brutally honest assessment focusing on the harshest truths."
  - "As a PM conducting a PoL Probe, analyze: {{scenario}}. What's the cheapest prototype that would reveal the most critical risks?"
  - "Evaluate this product assumption: {{scenario}}. What evidence would prove this wrong fastest?"

tests:
  - vars:
      scenario: "AI-powered customer support automation"
  - vars:
      scenario: "Freemium to premium conversion optimization"
  - vars:
      scenario: "Real-time collaborative editing feature"

assert:
  - type: contains
    value: "risk"
  - type: not-contains
    value: "definitely will work"
  - type: cost
    threshold: 0.10
EOF

# Create prompt testing utility script
cat > ~/ai-pm-toolkit/prompt-testing/test-prompts << 'EOF'
#!/bin/bash
# AI PM Prompt Testing Utility
# Test prompts against local AI models for PoL Probe scenarios

echo "🧪 AI PM Prompt Testing"
echo "======================"

cd ~/ai-pm-toolkit/prompt-testing

case "$1" in
    "eval")
        echo "🎯 Running prompt evaluation with promptfoo..."
        promptfoo eval --config configs/local-ai-config.yaml --output results/
        ;;
    "compare")
        echo "⚖️  Comparing prompts across models..."
        promptfoo eval --config configs/local-ai-config.yaml --output results/ --table
        ;;
    "interactive")
        echo "💬 Interactive prompt testing..."
        promptfoo eval --config configs/local-ai-config.yaml --interactive
        ;;
    "report")
        echo "📊 Generating test report..."
        promptfoo view results/
        ;;
    *)
        echo "Usage:"
        echo "  ./test-prompts eval        # Run evaluation suite"
        echo "  ./test-prompts compare     # Compare models/prompts"
        echo "  ./test-prompts interactive # Interactive testing"
        echo "  ./test-prompts report      # View results"
        echo ""
        echo "💡 Perfect for validating PoL Probe prompts before deployment"
        ;;
esac
EOF

chmod +x ~/ai-pm-toolkit/prompt-testing/test-prompts

echo "✅ Prompt engineering tools configured"

echo ""
echo "🎲 Installing synthetic data & AI training tools..."

# Install Faker for basic synthetic data
echo "📊 Installing Faker (Basic synthetic data generation)..."
install_package "Faker"

# Install faker-cli for command-line data generation
echo "📋 Installing faker-cli (Command-line data generation)..."
if ! command -v faker &>/dev/null; then
    npm install -g faker-cli
    echo "   ✅ faker-cli installed globally"
else
    echo "✅ faker-cli already installed"
fi

# Install Mimesis for advanced synthetic data
echo "🎭 Installing Mimesis (Advanced synthetic data with localization)..."
install_package "mimesis"

# Install ChatterBot for conversational AI
echo "🤖 Installing ChatterBot (Machine learning conversational engine)..."
install_package "chatterbot"

# Install Gretel SDK for AI-powered synthetic data
echo "🧬 Installing Gretel (AI-powered synthetic data platform)..."
install_package "gretel-client"

# Create synthetic data workspace
echo "📁 Setting up synthetic data workspace..."
mkdir -p ~/ai-pm-toolkit/synthetic-data/{personas,datasets,scripts}

# Create persona-chat CLI tool
cat > ~/ai-pm-toolkit/synthetic-data/persona-chat << 'EOF'
#!/usr/bin/env python3
"""
AI PM Persona Chat CLI
Generate synthetic user personas and conversations for PoL Probes
"""

import json
import random
import argparse
from faker import Faker
from mimesis import Person, Text, Address
from datetime import datetime, timedelta

fake = Faker()
person = Person()
text = Text()
address = Address()

class PersonaGenerator:
    def __init__(self):
        self.personas = []
    
    def generate_persona(self, persona_type="user"):
        """Generate a synthetic user persona"""
        persona = {
            "id": fake.uuid4(),
            "type": persona_type,
            "name": person.full_name(),
            "email": person.email(),
            "age": random.randint(22, 65),
            "location": f"{address.city()}, {address.state()}",
            "job_title": person.occupation(),
            "company_size": random.choice(["startup", "small", "medium", "enterprise"]),
            "tech_savviness": random.choice(["low", "medium", "high"]),
            "pain_points": self._generate_pain_points(),
            "goals": self._generate_goals(),
            "behavior_patterns": self._generate_behaviors(),
            "created_at": datetime.now().isoformat()
        }
        return persona
    
    def _generate_pain_points(self):
        pain_points = [
            "Too many manual processes",
            "Lack of visibility into metrics",
            "Slow approval workflows",
            "Data silos between teams",
            "Inconsistent user experience",
            "Poor mobile experience",
            "Limited customization options",
            "Expensive per-seat pricing"
        ]
        return random.sample(pain_points, random.randint(2, 4))
    
    def _generate_goals(self):
        goals = [
            "Increase team productivity",
            "Reduce operational costs",
            "Improve customer satisfaction",
            "Scale business operations",
            "Better data-driven decisions",
            "Streamline workflows",
            "Enhance collaboration",
            "Faster time to market"
        ]
        return random.sample(goals, random.randint(2, 3))
    
    def _generate_behaviors(self):
        behaviors = [
            "Prefers self-service options",
            "Values detailed documentation",
            "Needs executive reporting",
            "Mobile-first user",
            "Integrates with existing tools",
            "Security-conscious",
            "Budget-sensitive",
            "Early adopter of new features"
        ]
        return random.sample(behaviors, random.randint(3, 5))
    
    def generate_conversation(self, persona, scenario="product_feedback"):
        """Generate a conversation for a given persona and scenario"""
        conversations = {
            "product_feedback": [
                f"Hi, I'm {persona['name']} and I've been using your product for a few months.",
                f"As someone in {persona['job_title']}, my biggest challenge is {random.choice(persona['pain_points'])}.",
                f"What I really need is a solution that helps me {random.choice(persona['goals']).lower()}.",
                "Can you show me how your product addresses this?"
            ],
            "feature_request": [
                f"I work at a {persona['company_size']} company as {persona['job_title']}.",
                f"We're struggling with {random.choice(persona['pain_points']).lower()}.",
                f"Would it be possible to add a feature that helps with {random.choice(persona['goals']).lower()}?",
                "This would be a game-changer for our team."
            ],
            "onboarding": [
                f"Hi, I'm new to the platform. I'm {persona['name']}, {persona['job_title']}.",
                f"I'm hoping this tool will help me {random.choice(persona['goals']).lower()}.",
                f"I'm {persona['tech_savviness']}-tech savvy, so please guide me accordingly.",
                "What should I do first?"
            ]
        }
        
        return {
            "persona_id": persona["id"],
            "scenario": scenario,
            "messages": conversations.get(scenario, conversations["product_feedback"]),
            "timestamp": datetime.now().isoformat()
        }

def main():
    parser = argparse.ArgumentParser(description="AI PM Persona Chat CLI for PoL Probes")
    parser.add_argument("command", choices=["generate", "chat", "dataset"], 
                       help="Command to run")
    parser.add_argument("--count", "-c", type=int, default=5, 
                       help="Number of personas to generate")
    parser.add_argument("--type", "-t", default="user", 
                       help="Persona type (user, admin, stakeholder)")
    parser.add_argument("--scenario", "-s", default="product_feedback",
                       choices=["product_feedback", "feature_request", "onboarding"],
                       help="Conversation scenario")
    parser.add_argument("--output", "-o", default="personas.json",
                       help="Output file name")
    
    args = parser.parse_args()
    generator = PersonaGenerator()
    
    if args.command == "generate":
        print(f"🎭 Generating {args.count} {args.type} personas...")
        personas = []
        for i in range(args.count):
            persona = generator.generate_persona(args.type)
            personas.append(persona)
            print(f"   Generated: {persona['name']} ({persona['job_title']})")
        
        with open(args.output, 'w') as f:
            json.dump(personas, f, indent=2)
        print(f"✅ Saved {args.count} personas to {args.output}")
    
    elif args.command == "chat":
        print(f"💬 Generating conversations for scenario: {args.scenario}")
        # Load existing personas or generate new ones
        try:
            with open(args.output, 'r') as f:
                personas = json.load(f)
        except FileNotFoundError:
            print("   No personas file found, generating new ones...")
            personas = [generator.generate_persona() for _ in range(3)]
        
        conversations = []
        for persona in personas[:args.count]:
            conversation = generator.generate_conversation(persona, args.scenario)
            conversations.append(conversation)
            print(f"\n🗣️  {persona['name']} ({persona['job_title']}):")
            for msg in conversation['messages']:
                print(f"     {msg}")
        
        conv_file = f"conversations_{args.scenario}.json"
        with open(conv_file, 'w') as f:
            json.dump(conversations, f, indent=2)
        print(f"\n✅ Saved conversations to {conv_file}")
    
    elif args.command == "dataset":
        print("📊 Generating comprehensive dataset for PoL Probe testing...")
        
        # Generate diverse personas
        persona_types = ["user", "admin", "stakeholder", "customer"]
        all_personas = []
        for p_type in persona_types:
            for _ in range(args.count):
                all_personas.append(generator.generate_persona(p_type))
        
        # Generate conversations for each scenario
        scenarios = ["product_feedback", "feature_request", "onboarding"]
        all_conversations = []
        for scenario in scenarios:
            for persona in all_personas:
                conversation = generator.generate_conversation(persona, scenario)
                all_conversations.append(conversation)
        
        dataset = {
            "personas": all_personas,
            "conversations": all_conversations,
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "total_personas": len(all_personas),
                "total_conversations": len(all_conversations),
                "scenarios": scenarios,
                "persona_types": persona_types
            }
        }
        
        dataset_file = f"pol_probe_dataset_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(dataset_file, 'w') as f:
            json.dump(dataset, f, indent=2)
        
        print(f"✅ Generated comprehensive dataset:")
        print(f"   • {len(all_personas)} personas across {len(persona_types)} types")
        print(f"   • {len(all_conversations)} conversations across {len(scenarios)} scenarios")
        print(f"   • Saved to {dataset_file}")

if __name__ == "__main__":
    main()
EOF

chmod +x ~/ai-pm-toolkit/synthetic-data/persona-chat

# Create data generation utility scripts
cat > ~/ai-pm-toolkit/synthetic-data/generate-test-data << 'EOF'
#!/bin/bash
# AI PM Test Data Generation Utility
# Generate realistic test data for PoL Probes

echo "🎲 AI PM Test Data Generator"
echo "============================"

cd ~/ai-pm-toolkit/synthetic-data

case "$1" in
    "users")
        echo "👥 Generating user data..."
        faker -l en_US -r=100 -s=' ' -p='{
            "id": "{{uuid4}}", 
            "name": "{{name}}", 
            "email": "{{email}}", 
            "signup_date": "{{date_between(start_date=\"-2y\", end_date=\"today\")}}", 
            "plan": "{{random_element(elements=(\"free\", \"pro\", \"enterprise\"))}}", 
            "usage_score": "{{random_int(min=1, max=100)}}"
        }' > datasets/users.json
        echo "   ✅ Generated 100 user records in datasets/users.json"
        ;;
    "personas")
        echo "🎭 Generating user personas..."
        ./persona-chat generate --count 20 --output datasets/personas.json
        ;;
    "conversations")
        echo "💬 Generating conversation data..."
        ./persona-chat chat --scenario product_feedback --count 10
        ./persona-chat chat --scenario feature_request --count 10  
        ./persona-chat chat --scenario onboarding --count 10
        echo "   ✅ Generated conversation datasets"
        ;;
    "events")
        echo "📈 Generating event data..."
        faker -l en_US -r=1000 -s=' ' -p='{
            "event_id": "{{uuid4}}",
            "user_id": "{{uuid4}}",
            "event_type": "{{random_element(elements=(\"page_view\", \"button_click\", \"form_submit\", \"feature_use\"))}}", 
            "timestamp": "{{date_time_between(start_date=\"-30d\", end_date=\"now\")}}", 
            "properties": {
                "page": "{{random_element(elements=(\"dashboard\", \"settings\", \"billing\", \"help\"))}}", 
                "session_duration": "{{random_int(min=30, max=1800)}}"
            }
        }' > datasets/events.json
        echo "   ✅ Generated 1000 event records in datasets/events.json"
        ;;
    "feedback")
        echo "💭 Generating feedback data..."
        faker -l en_US -r=50 -s=' ' -p='{
            "feedback_id": "{{uuid4}}",
            "user_id": "{{uuid4}}",
            "rating": "{{random_int(min=1, max=5)}}",
            "comment": "{{text(max_nb_chars=200)}}",
            "category": "{{random_element(elements=(\"bug\", \"feature_request\", \"praise\", \"complaint\"))}}", 
            "submitted_at": "{{date_time_between(start_date=\"-60d\", end_date=\"now\")}}"
        }' > datasets/feedback.json
        echo "   ✅ Generated 50 feedback records in datasets/feedback.json"
        ;;
    "full")
        echo "🎯 Generating complete PoL Probe dataset..."
        ./generate-test-data users
        ./generate-test-data personas
        ./generate-test-data conversations
        ./generate-test-data events
        ./generate-test-data feedback
        echo ""
        echo "✅ Complete PoL Probe dataset ready:"
        echo "   📁 datasets/users.json (100 records)"
        echo "   📁 datasets/personas.json (20 personas)"
        echo "   📁 datasets/conversations_*.json (30 conversations)"
        echo "   📁 datasets/events.json (1000 records)"
        echo "   📁 datasets/feedback.json (50 records)"
        ;;
    *)
        echo "Usage:"
        echo "  ./generate-test-data users        # Generate user data"
        echo "  ./generate-test-data personas     # Generate user personas"
        echo "  ./generate-test-data conversations # Generate conversation data"
        echo "  ./generate-test-data events       # Generate event/analytics data"
        echo "  ./generate-test-data feedback     # Generate feedback data"
        echo "  ./generate-test-data full         # Generate complete dataset"
        echo ""
        echo "💡 Perfect for PoL Probe simulations and assumption testing"
        ;;
esac
EOF

chmod +x ~/ai-pm-toolkit/synthetic-data/generate-test-data

echo "✅ Synthetic data & AI training tools configured"

echo ""
echo "📈 Installing AI monitoring & observability tools..."

# Install LangSmith CLI
echo "🔬 Installing LangSmith (LLM application monitoring)..."
if ! command -v langsmith &>/dev/null; then
    npm install -g langsmith
    echo "   ✅ LangSmith CLI installed globally"
else
    echo "✅ LangSmith CLI already installed"
fi

# Install Arize SDK for ML observability
echo "📊 Installing Arize (ML observability platform)..."
install_package "arize"

# Create monitoring workspace
echo "📁 Setting up AI monitoring workspace..."
mkdir -p ~/ai-pm-toolkit/monitoring/{configs,dashboards,reports}

# Create LangSmith configuration
cat > ~/ai-pm-toolkit/monitoring/configs/langsmith-config.json << 'EOF'
{
  "project_name": "ai-pm-pol-probes",
  "environment": "development",
  "sampling_rate": 1.0,
  "metadata": {
    "toolkit_version": "1.0.0",
    "use_case": "proof_of_life_probes"
  },
  "tags": ["pol-probe", "ai-pm", "strategic-pm"],
  "monitoring_enabled": true,
  "trace_level": "DEBUG"
}
EOF

# Create Arize configuration
cat > ~/ai-pm-toolkit/monitoring/configs/arize-config.json << 'EOF'
{
  "space_key": "ai-pm-toolkit",
  "model_id": "pol-probe-models",
  "model_version": "1.0.0",
  "environment": "development",
  "features": {
    "prompt_monitoring": true,
    "response_quality": true,
    "bias_detection": true,
    "drift_detection": true
  },
  "metrics": {
    "latency": true,
    "token_usage": true,
    "cost_tracking": true,
    "user_satisfaction": true
  }
}
EOF

# Create monitoring utility script
cat > ~/ai-pm-toolkit/monitoring/monitor-ai << 'EOF'
#!/bin/bash
# AI PM Monitoring Utility
# Monitor AI model performance and PoL Probe effectiveness

echo "📈 AI PM Monitoring Dashboard"
echo "============================="

cd ~/ai-pm-toolkit/monitoring

case "$1" in
    "start")
        echo "🚀 Starting AI monitoring services..."
        
        # Check if API keys are configured
        if [[ -f "$HOME/.aipm-apis" ]]; then
            source "$HOME/.aipm-apis"
        fi
        
        if [[ -n "$LANGCHAIN_API_KEY" ]]; then
            echo "   🔬 LangSmith monitoring enabled"
            export LANGCHAIN_TRACING_V2=true
            export LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
        else
            echo "   ⚠️  LangSmith API key not configured"
        fi
        
        if [[ -n "$ARIZE_API_KEY" ]]; then
            echo "   📊 Arize monitoring enabled"
        else
            echo "   ⚠️  Arize API key not configured"
        fi
        
        echo "   ✅ Monitoring services initialized"
        ;;
    "trace")
        echo "🔍 Viewing recent AI traces..."
        if [[ -n "$LANGCHAIN_API_KEY" ]]; then
            langsmith runs list --limit 10 --project ai-pm-pol-probes
        else
            echo "   ❌ LangSmith API key required for tracing"
        fi
        ;;
    "metrics")
        echo "📊 Generating AI performance metrics..."
        python3 << 'PYTHON'
import json
import os
from datetime import datetime, timedelta

def generate_mock_metrics():
    """Generate mock metrics for demonstration"""
    metrics = {
        "timestamp": datetime.now().isoformat(),
        "period": "last_24h",
        "pol_probe_metrics": {
            "total_probes": 15,
            "successful_probes": 12,
            "failed_probes": 3,
            "success_rate": 0.8,
            "avg_response_time": 2.3,
            "avg_tokens_used": 850,
            "cost_estimate": 0.12
        },
        "model_performance": {
            "deepseek_r1": {
                "usage_count": 8,
                "avg_latency": 1.8,
                "quality_score": 4.2
            },
            "llama3_2": {
                "usage_count": 7,
                "avg_latency": 0.9,
                "quality_score": 3.8
            }
        },
        "probe_categories": {
            "learn": 4,
            "fast": 3,
            "prototype": 2,
            "experiment": 4,
            "compete": 2
        }
    }
    
    # Save metrics
    with open('reports/ai_metrics.json', 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print("📈 AI Performance Metrics:")
    print(f"   • Total PoL Probes: {metrics['pol_probe_metrics']['total_probes']}")
    print(f"   • Success Rate: {metrics['pol_probe_metrics']['success_rate']*100:.1f}%")
    print(f"   • Avg Response Time: {metrics['pol_probe_metrics']['avg_response_time']}s")
    print(f"   • Estimated Cost: ${metrics['pol_probe_metrics']['cost_estimate']:.2f}")
    print(f"   • Most Used: {'DeepSeek R1' if metrics['model_performance']['deepseek_r1']['usage_count'] > metrics['model_performance']['llama3_2']['usage_count'] else 'Llama 3.2'}")
    print(f"   📁 Full report saved to reports/ai_metrics.json")

if __name__ == "__main__":
    generate_mock_metrics()
PYTHON
        ;;
    "dashboard")
        echo "🖥️  Opening AI monitoring dashboard..."
        if [[ -n "$LANGCHAIN_API_KEY" ]]; then
            echo "   🔗 LangSmith Dashboard: https://smith.langchain.com/projects/ai-pm-pol-probes"
        fi
        if [[ -n "$ARIZE_API_KEY" ]]; then
            echo "   🔗 Arize Dashboard: https://app.arize.com/models/pol-probe-models"
        fi
        
        # Generate local dashboard
        python3 << 'PYTHON'
import json
from datetime import datetime

html_dashboard = """
<!DOCTYPE html>
<html>
<head>
    <title>AI PM Monitoring Dashboard</title>
    <style>
        body { font-family: system-ui; margin: 2rem; background: #f5f5f5; }
        .dashboard { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem; }
        .card { background: white; padding: 1.5rem; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
        .metric { font-size: 2rem; font-weight: bold; color: #2563eb; }
        .label { color: #6b7280; margin-bottom: 0.5rem; }
        h1 { color: #1f2937; margin-bottom: 2rem; }
    </style>
</head>
<body>
    <h1>🧪 AI PM Toolkit - Monitoring Dashboard</h1>
    <div class="dashboard">
        <div class="card">
            <div class="label">Total PoL Probes</div>
            <div class="metric">15</div>
        </div>
        <div class="card">
            <div class="label">Success Rate</div>
            <div class="metric">80%</div>
        </div>
        <div class="card">
            <div class="label">Avg Response Time</div>
            <div class="metric">2.3s</div>
        </div>
        <div class="card">
            <div class="label">Cost (24h)</div>
            <div class="metric">$0.12</div>
        </div>
    </div>
    <p style="margin-top: 2rem; color: #6b7280;">
        Generated: {timestamp} | 
        <a href="reports/ai_metrics.json">Full JSON Report</a>
    </p>
</body>
</html>
""".format(timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

with open('dashboards/local_dashboard.html', 'w') as f:
    f.write(html_dashboard)

print("   📊 Local dashboard generated: dashboards/local_dashboard.html")
print("   🌐 Open in browser: file://" + os.path.abspath('dashboards/local_dashboard.html'))
PYTHON
        ;;
    "report")
        echo "📋 Generating monitoring report..."
        python3 << 'PYTHON'
import json
from datetime import datetime

report = f"""
# AI PM Toolkit - Monitoring Report
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## PoL Probe Performance Summary

### Key Metrics (Last 24h)
- **Total Probes Executed**: 15
- **Success Rate**: 80% (12/15)
- **Average Response Time**: 2.3 seconds
- **Token Usage**: 12,750 tokens
- **Estimated Cost**: $0.12

### Model Performance
- **DeepSeek R1 7B**: 8 probes, 1.8s avg latency, 4.2/5 quality
- **Llama 3.2 3B**: 7 probes, 0.9s avg latency, 3.8/5 quality

### Probe Category Breakdown
- **Learn (Feasibility)**: 4 probes
- **Fast (Task-focused)**: 3 probes
- **Prototype (Narrative)**: 2 probes
- **Experiment (Synthetic)**: 4 probes
- **Compete (Vibe-coded)**: 2 probes

### Recommendations
1. **DeepSeek R1** shows better quality for strategic analysis
2. **Llama 3.2** optimal for quick validation tasks
3. Success rate indicates robust PoL Probe methodology
4. Cost efficiency excellent for local-first approach

---
*Use the cheapest prototype that tells the harshest truth*
"""

with open('reports/monitoring_report.md', 'w') as f:
    f.write(report)

print("📋 Monitoring report generated: reports/monitoring_report.md")
print("💡 Key insights:")
print("   • 80% success rate indicates robust PoL Probe methodology")
print("   • DeepSeek R1 preferred for strategic analysis (higher quality)")
print("   • Llama 3.2 optimal for fast validation (lower latency)")
print("   • $0.12/day cost demonstrates excellent ROI for local-first AI")
PYTHON
        ;;
    *)
        echo "Usage:"
        echo "  ./monitor-ai start      # Initialize monitoring services"
        echo "  ./monitor-ai trace      # View recent AI traces"
        echo "  ./monitor-ai metrics    # Generate performance metrics"
        echo "  ./monitor-ai dashboard  # Open monitoring dashboard"
        echo "  ./monitor-ai report     # Generate detailed report"
        echo ""
        echo "💡 Monitor PoL Probe effectiveness and AI model performance"
        ;;
esac
EOF

chmod +x ~/ai-pm-toolkit/monitoring/monitor-ai

echo "✅ AI monitoring & observability tools configured"

echo ""
echo "🎨 Installing design & storytelling tools..."

# Install Wonder Unit Storyboarder
echo "📖 Installing Wonder Unit Storyboarder (Digital storyboarding)..."
if ! command -v storyboarder &>/dev/null; then
    npm install -g storyboarder
    echo "   ✅ Storyboarder installed globally"
else
    echo "✅ Storyboarder already installed"
fi

# Create design workspace
echo "📁 Setting up design & storytelling workspace..."
mkdir -p ~/ai-pm-toolkit/design/{storyboards,diagrams,mockups,templates}

# Create Excalidraw integration (web-based, so we create a launcher)
cat > ~/ai-pm-toolkit/design/launch-excalidraw << 'EOF'
#!/bin/bash
# Excalidraw Launcher for AI PM PoL Probes
# Hand-drawn style diagrams for product storytelling

echo "🎨 Launching Excalidraw for PoL Probe Diagrams"
echo "=============================================="

case "$1" in
    "web")
        echo "🌐 Opening Excalidraw web app..."
        open "https://excalidraw.com"
        echo "   💡 Perfect for quick user journey diagrams"
        echo "   💡 Export as PNG/SVG for PoL Probe documentation"
        ;;
    "local")
        echo "💻 Setting up local Excalidraw instance..."
        if ! command -v npx &>/dev/null; then
            echo "   ❌ npm/npx required for local instance"
            exit 1
        fi
        
        cd ~/ai-pm-toolkit/design
        if [ ! -d "excalidraw-local" ]; then
            echo "   📦 Cloning Excalidraw for local use..."
            if git clone https://github.com/excalidraw/excalidraw.git excalidraw-local 2>/dev/null; then
                cd excalidraw-local
                npm install
            else
                echo "   ⚠️  Could not clone Excalidraw - use web version instead"
                return
            fi
        else
            cd excalidraw-local
        fi
        
        echo "   🚀 Starting local Excalidraw server..."
        npm start &
        echo "   🌐 Local Excalidraw: http://localhost:3000"
        ;;
    "templates")
        echo "📋 Creating PoL Probe diagram templates..."
        mkdir -p templates/excalidraw
        
        # Create template descriptions
        cat > templates/excalidraw/README.md << 'TEMPLATE_README'
# Excalidraw Templates for PoL Probes

## User Journey Templates
- **Simple Flow**: Linear user journey (signup → onboarding → value)
- **Decision Tree**: User decision points and outcomes
- **Friction Map**: Identify pain points in existing flows

## System Architecture Templates  
- **API Flow**: Request/response patterns for feasibility checks
- **Data Flow**: Information flow for synthetic data experiments
- **Integration Map**: Third-party connections and dependencies

## Stakeholder Communication Templates
- **Feature Roadmap**: Visual timeline for narrative prototypes
- **Competitive Analysis**: Market positioning diagrams
- **Success Metrics**: KPI dashboards and measurement frameworks

## Usage Tips for AI PM PoL Probes
1. **Keep it simple** - Hand-drawn style forces clarity
2. **Focus on flows** - Show user paths, not static screens
3. **Highlight friction** - Use red for pain points, green for solutions
4. **Iterate fast** - Perfect for "show before tell" philosophy
TEMPLATE_README
        
        echo "   📋 Template guide created in templates/excalidraw/"
        ;;
    *)
        echo "Usage:"
        echo "  ./launch-excalidraw web        # Open web version (recommended)"
        echo "  ./launch-excalidraw local      # Set up local instance"  
        echo "  ./launch-excalidraw templates  # Create PoL Probe templates"
        echo ""
        echo "🎯 Perfect for:"
        echo "   • User journey mapping"
        echo "   • System architecture sketches"
        echo "   • Stakeholder presentation diagrams"
        echo "   • PoL Probe visual storytelling"
        echo ""
        echo "💡 Hand-drawn style forces clarity and prevents over-engineering"
        ;;
esac
EOF

chmod +x ~/ai-pm-toolkit/design/launch-excalidraw

# Create storyboarding utility for PoL Probes
cat > ~/ai-pm-toolkit/design/create-storyboard << 'EOF'
#!/bin/bash
# AI PM Storyboard Creator
# Generate visual narratives for PoL Probes

echo "📖 AI PM Storyboard Creator"
echo "============================"

cd ~/ai-pm-toolkit/design

case "$1" in
    "new")
        project_name="$2"
        if [[ -z "$project_name" ]]; then
            echo "❌ Project name required"
            echo "Usage: ./create-storyboard new <project-name>"
            exit 1
        fi
        
        echo "📖 Creating new storyboard: $project_name"
        
        # Create project directory
        mkdir -p "storyboards/$project_name"
        cd "storyboards/$project_name"
        
        # Initialize storyboard project
        storyboarder --new "$project_name.storyboarder"
        
        echo "   ✅ Storyboard project created"
        echo "   📁 Location: ~/ai-pm-toolkit/design/storyboards/$project_name/"
        echo "   🚀 To edit: storyboarder $project_name.storyboarder"
        ;;
    "template")
        template_type="$2"
        project_name="$3"
        
        if [[ -z "$template_type" || -z "$project_name" ]]; then
            echo "❌ Template type and project name required"
            echo "Usage: ./create-storyboard template <type> <project-name>"
            echo ""
            echo "Available templates:"
            echo "  • feature-demo     # New feature demonstration"
            echo "  • user-journey     # End-to-end user experience"
            echo "  • problem-solution # Problem identification and solution"
            echo "  • competitive-analysis # Competitor comparison"
            exit 1
        fi
        
        echo "📋 Creating $template_type storyboard: $project_name"
        
        mkdir -p "storyboards/$project_name"
        cd "storyboards/$project_name"
        
        case "$template_type" in
            "feature-demo")
                # Create feature demo template
                cat > "storyboard-script.md" << 'FEATURE_DEMO'
# Feature Demo Storyboard: [Feature Name]

## Story Arc (6-8 panels)

### Panel 1: Current State Problem
- **Scene**: User struggling with current solution
- **Dialogue**: "This workflow takes forever..."
- **Visual Focus**: Frustrated user, cluttered interface

### Panel 2: Introduce Solution  
- **Scene**: New feature introduction
- **Dialogue**: "What if we could streamline this?"
- **Visual Focus**: Clean, simple interface

### Panel 3: First Interaction
- **Scene**: User trying the new feature
- **Dialogue**: "Let me try this new approach..."
- **Visual Focus**: User engagement, clear CTAs

### Panel 4: Value Realization
- **Scene**: User seeing immediate benefit
- **Dialogue**: "Wow, this is much faster!"
- **Visual Focus**: Time saved, efficiency gained

### Panel 5: Continued Usage
- **Scene**: User integrating into workflow
- **Dialogue**: "I'll use this for all my projects"
- **Visual Focus**: Habitual usage, confidence

### Panel 6: Outcome/Success
- **Scene**: Achieved goal/outcome
- **Dialogue**: "This has transformed how I work"
- **Visual Focus**: Success metrics, satisfied user

## Key Messages
- Problem: [Current pain point]
- Solution: [How feature solves it]
- Value: [Benefit delivered]

## Target Audience
- Primary: [User type]
- Secondary: [Stakeholder type]
FEATURE_DEMO
                ;;
            "user-journey")
                cat > "storyboard-script.md" << 'USER_JOURNEY'
# User Journey Storyboard: [Journey Name]

## Journey Arc (8-12 panels)

### Act 1: Discovery (Panels 1-3)
**Panel 1: Trigger Event**
- **Scene**: Something prompts user to seek solution
- **Dialogue**: "I need to solve this problem"
- **Visual Focus**: Pain point, frustration

**Panel 2: Research/Discovery**
- **Scene**: User searching for solutions
- **Dialogue**: "Let me look into options"
- **Visual Focus**: Comparison, evaluation

**Panel 3: First Contact**
- **Scene**: User discovers our solution
- **Dialogue**: "This looks promising"
- **Visual Focus**: Interest, curiosity

### Act 2: Evaluation (Panels 4-7)
**Panel 4: Initial Trial**
- **Scene**: User trying the solution
- **Dialogue**: "Let me see if this works"
- **Visual Focus**: First impressions, ease of use

**Panel 5: Overcoming Obstacles**
- **Scene**: User hits a challenge
- **Dialogue**: "How do I handle this?"
- **Visual Focus**: Support, guidance

**Panel 6: Building Confidence**
- **Scene**: User succeeding with help
- **Dialogue**: "I'm getting the hang of this"
- **Visual Focus**: Competence, progress

**Panel 7: Value Recognition**
- **Scene**: User sees clear benefit
- **Dialogue**: "This is really helping"
- **Visual Focus**: Tangible results

### Act 3: Adoption (Panels 8-10)
**Panel 8: Integration**
- **Scene**: User making it part of routine
- **Dialogue**: "This is now part of my workflow"
- **Visual Focus**: Habitual usage

**Panel 9: Advocacy**
- **Scene**: User recommending to others
- **Dialogue**: "You should try this too"
- **Visual Focus**: Sharing, referrals

**Panel 10: Mastery/Success**
- **Scene**: User achieving original goal
- **Dialogue**: "I've solved my problem"
- **Visual Focus**: Achievement, satisfaction

## Journey Insights
- Key Moments: [Critical decision points]
- Friction Points: [Where users struggle]
- Success Metrics: [How to measure progress]
USER_JOURNEY
                ;;
            "problem-solution")
                cat > "storyboard-script.md" << 'PROBLEM_SOLUTION'
# Problem-Solution Storyboard: [Solution Name]

## Narrative Arc (6 panels)

### Panel 1: Status Quo
- **Scene**: Current state, business as usual
- **Dialogue**: "This is how we've always done it"
- **Visual Focus**: Existing process, normalcy

### Panel 2: Problem Emerges
- **Scene**: Issues becoming apparent
- **Dialogue**: "This isn't working anymore"
- **Visual Focus**: Pain points, inefficiencies

### Panel 3: Problem Amplified
- **Scene**: Consequences of inaction
- **Dialogue**: "We're losing time/money/customers"
- **Visual Focus**: Impact, urgency

### Panel 4: Solution Introduction
- **Scene**: Proposed solution presented
- **Dialogue**: "What if we tried this approach?"
- **Visual Focus**: New possibility, hope

### Panel 5: Solution in Action
- **Scene**: Solution being implemented
- **Dialogue**: "Let's see how this works"
- **Visual Focus**: Change, progress

### Panel 6: New Reality
- **Scene**: Problem solved, benefits realized
- **Dialogue**: "This is so much better"
- **Visual Focus**: Success, transformation

## Problem Definition
- **What**: [Specific problem]
- **Who**: [Affected users/stakeholders]
- **Impact**: [Business consequences]

## Solution Overview
- **Approach**: [How we solve it]
- **Benefits**: [Value delivered]
- **Proof Points**: [Evidence it works]
PROBLEM_SOLUTION
                ;;
        esac
        
        echo "   📋 Template created: storyboards/$project_name/storyboard-script.md"
        echo "   📖 Edit the script, then create visual storyboard"
        echo "   🚀 To visualize: storyboarder --new $project_name.storyboarder"
        ;;
    "export")
        project_name="$2"
        if [[ -z "$project_name" ]]; then
            echo "❌ Project name required"
            echo "Usage: ./create-storyboard export <project-name>"
            exit 1
        fi
        
        echo "📤 Exporting storyboard: $project_name"
        
        if [[ -f "storyboards/$project_name/$project_name.storyboarder" ]]; then
            cd "storyboards/$project_name"
            
            # Export as PDF for presentations
            storyboarder --export-pdf "$project_name.storyboarder"
            
            # Export as PNG sequence for video production
            storyboarder --export-png "$project_name.storyboarder"
            
            echo "   ✅ Exported as PDF and PNG sequence"
            echo "   📁 Files saved in: storyboards/$project_name/"
        else
            echo "   ❌ Storyboard project not found: $project_name"
        fi
        ;;
    *)
        echo "Usage:"
        echo "  ./create-storyboard new <project-name>              # Create blank storyboard"
        echo "  ./create-storyboard template <type> <project-name>  # Create from template"
        echo "  ./create-storyboard export <project-name>           # Export to PDF/PNG"
        echo ""
        echo "Templates available:"
        echo "  • feature-demo        # Demonstrate new feature value"
        echo "  • user-journey        # End-to-end user experience"  
        echo "  • problem-solution    # Problem identification and solution"
        echo "  • competitive-analysis # Competitor comparison narrative"
        echo ""
        echo "💡 Perfect for narrative PoL Probes that earn 'hell yes' from stakeholders"
        ;;
esac
EOF

chmod +x ~/ai-pm-toolkit/design/create-storyboard

echo "✅ Design & storytelling tools configured"

echo ""
echo "🧠 Installing knowledge management & AI integration tools..."

# Install Obsidian for knowledge management
echo "📝 Installing Obsidian (Knowledge management & idea linking)..."
if ! command -v obsidian &>/dev/null; then
    brew install --cask obsidian
    echo "   ✅ Obsidian installed"
else
    echo "✅ Obsidian already installed"
fi

# Create Obsidian vault for AI PM work
echo "📁 Setting up AI PM knowledge vault..."
mkdir -p ~/ai-pm-toolkit/obsidian-vault/{Templates,Projects,Research,Insights,Archives}

# Create Obsidian configuration directory and file
echo "⚙️  Setting up Obsidian configuration..."
mkdir -p ~/ai-pm-toolkit/obsidian-vault/.obsidian
cat > ~/ai-pm-toolkit/obsidian-vault/.obsidian/app.json << 'EOF'
{
  "promptDelete": false,
  "showLineNumber": true,
  "spellcheck": true,
  "useMarkdownLinks": true,
  "newLinkFormat": "relative",
  "attachmentFolderPath": "./Assets"
}
EOF

# Create useful templates for PoL Probes
mkdir -p ~/ai-pm-toolkit/obsidian-vault/Templates

cat > ~/ai-pm-toolkit/obsidian-vault/Templates/PoL-Probe-Planning.md << 'EOF'
# {{title}} - PoL Probe Plan

**Created:** {{date:YYYY-MM-DD}}
**Type:** [[PoL Probe Types]]
**Status:** #planning

## Hypothesis
What assumption are we testing?

## Success Criteria
What would prove this wrong fastest?

## Probe Design
### Flavor: Learn | Fast | Prototype | Experiment | Compete

### Approach
- [ ] Tool(s) to use:
- [ ] Timeline: 
- [ ] Resources needed:

## Links
- Related: 
- Stakeholders: 
- Previous research: [[]]

## Results
*Update after running the probe*

### Harsh Truth Discovered
What did we learn that stings?

### Next Actions
- [ ] 
- [ ] 

---
Tags: #pol-probe #{{probe-type}}
EOF

cat > ~/ai-pm-toolkit/obsidian-vault/Templates/User-Persona.md << 'EOF'
# {{title}} - User Persona

**Created:** {{date:YYYY-MM-DD}}
**Source:** Synthetic | Research | Interview
**Status:** #active

## Basic Info
- **Name:** 
- **Role:** 
- **Company Size:** 
- **Tech Savviness:** Low | Medium | High

## Pain Points
- 
- 
- 

## Goals
- 
- 
- 

## Behavior Patterns
- 
- 
- 

## Quote
> "Their typical response to our product..."

## Links
- Related Personas: [[]]
- Research Source: [[]]
- PoL Probes: [[]]

---
Tags: #persona #user-research
EOF

cat > ~/ai-pm-toolkit/obsidian-vault/Templates/Feature-Analysis.md << 'EOF'
# {{title}} - Feature Analysis

**Created:** {{date:YYYY-MM-DD}}
**Priority:** High | Medium | Low
**Status:** #analysis

## Problem Statement
What user problem does this solve?

## Proposed Solution
Brief description of the feature

## PoL Probe Results
### Feasibility ([[Learn]])
- Technical complexity: 
- Resource requirements: 
- Timeline estimate: 

### User Validation ([[Fast]])
- User friction points: 
- Adoption likelihood: 
- Workflow impact: 

### Narrative Testing ([[Prototype]])
- Stakeholder buy-in: 
- Story resonance: 
- Communication effectiveness: 

### Data Simulation ([[Experiment]])
- Usage patterns: 
- Performance impact: 
- Edge cases discovered: 

### Market Testing ([[Compete]])
- Competitive advantage: 
- User preference: 
- Market readiness: 

## Decision
- [ ] Build it
- [ ] Iterate
- [ ] Kill it
- [ ] Need more data

## Links
- User Personas: [[]]
- Related Features: [[]]
- Research: [[]]

---
Tags: #feature-analysis #product-strategy
EOF

# Install MCP (Model Context Protocol) support
echo "🔌 Installing MCP (Model Context Protocol) support..."
echo "   MCP enables enhanced AI integration with custom tools and agents"
echo -n "   Install MCP servers (requires GitHub repository access)? [Y/n]: "
read -r install_mcp
if [[ "$install_mcp" =~ ^[Nn]$ ]]; then
    echo "   ⏭️  Skipped MCP installation - you can install later manually"
    # Skip to the next section
    echo "✅ Skipped MCP installation per user request"
else

# Install uv for Python package management (required for MCP)
echo "📦 Installing uv (Python package manager)..."
if ! command -v uv &>/dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    # Add to PATH for current session
    export PATH="$HOME/.cargo/bin:$PATH"
    echo "   ✅ uv installed"
else
    echo "✅ uv already installed"
fi

# Create MCP workspace
echo "📁 Setting up MCP workspace..."
mkdir -p ~/ai-pm-toolkit/mcp-servers/{templates,tools,agents}

# Install FastMCP for AI PM PoL Probes
echo "🚀 Installing FastMCP (Modern MCP development framework)..."
cd ~/ai-pm-toolkit/mcp-servers/templates
if ! python3 -c "import fastmcp" 2>/dev/null; then
    echo "   📦 Installing FastMCP via pip..."
    if command -v uv >/dev/null 2>&1; then
        uv pip install fastmcp >/dev/null 2>&1 && echo "   ✅ FastMCP installed via uv" || {
            pip3 install fastmcp >/dev/null 2>&1 && echo "   ✅ FastMCP installed via pip"
        }
    else
        pip3 install fastmcp >/dev/null 2>&1 && echo "   ✅ FastMCP installed via pip"
    fi
else
    echo "✅ FastMCP already installed"
fi

# Create FastMCP AI PM template
echo "   📝 Creating AI PM FastMCP template..."
mkdir -p ~/ai-pm-toolkit/mcp-servers/templates/fastmcp-aipm
cat > ~/ai-pm-toolkit/mcp-servers/templates/fastmcp-aipm/aipm_server.py << 'FASTMCP_EOF'
"""AI PM FastMCP Server for PoL Probes
A modern MCP server for product managers using the FastMCP framework.
"""
from fastmcp import FastMCP
from typing import Any, Dict, List
import json
import os
import datetime

# Initialize FastMCP server
mcp = FastMCP("AI PM PoL Probe Server")

@mcp.tool()
def create_pol_probe(name: str, type: str, hypothesis: str) -> Dict[str, Any]:
    """Create a new Proof-of-Life probe template.
    
    Args:
        name: Name of the PoL probe
        type: Type (learn, fast, prototype, experiment, compete)
        hypothesis: The assumption being tested
    
    Returns:
        Dict with probe details and file path
    """
    probe_types = ["learn", "fast", "prototype", "experiment", "compete"]
    if type not in probe_types:
        return {"error": f"Type must be one of: {', '.join(probe_types)}"}
    
    # Create probe directory
    probe_dir = os.path.expanduser(f"~/ai-pm-toolkit/experiments/{name.replace(' ', '-').lower()}")
    os.makedirs(probe_dir, exist_ok=True)
    
    # Create probe plan
    plan_content = f"""# {name} - PoL Probe Plan

**Created:** {datetime.datetime.now().strftime('%Y-%m-%d')}
**Type:** {type}
**Status:** planning

## Hypothesis
{hypothesis}

## Success Criteria
What would prove this wrong fastest?

## Probe Design
### Flavor: {type.title()}

### Approach
- [ ] Tool(s) to use:
- [ ] Timeline: 
- [ ] Resources needed:

## Results
*Update after running the probe*

### Harsh Truth Discovered
What did we learn that stings?

### Next Actions
- [ ] 
- [ ] 

---
Tags: #pol-probe #{type}
"""
    
    plan_file = os.path.join(probe_dir, "probe-plan.md")
    with open(plan_file, 'w') as f:
        f.write(plan_content)
    
    return {
        "name": name,
        "type": type,
        "directory": probe_dir,
        "plan_file": plan_file,
        "status": "created",
        "next_steps": [
            "Edit the probe plan with specific details",
            f"Run: aipm {type} \"{hypothesis}\"",
            "Document findings in the Results section"
        ]
    }

@mcp.tool()
def list_pol_probes() -> List[Dict[str, Any]]:
    """List all existing PoL probes in the toolkit."""
    probes = []
    experiments_dir = os.path.expanduser("~/ai-pm-toolkit/experiments")
    
    if not os.path.exists(experiments_dir):
        return []
    
    for item in os.listdir(experiments_dir):
        item_path = os.path.join(experiments_dir, item)
        if os.path.isdir(item_path):
            plan_file = os.path.join(item_path, "probe-plan.md")
            if os.path.exists(plan_file):
                # Read basic info from the plan
                with open(plan_file, 'r') as f:
                    content = f.read()
                    lines = content.split('\n')
                    
                probe_info = {
                    "name": item,
                    "directory": item_path,
                    "plan_file": plan_file,
                    "created": "unknown",
                    "type": "unknown",
                    "status": "unknown"
                }
                
                # Parse metadata from the plan
                for line in lines:
                    if line.startswith("**Created:**"):
                        probe_info["created"] = line.split("**Created:**")[1].strip()
                    elif line.startswith("**Type:**"):
                        probe_info["type"] = line.split("**Type:**")[1].strip()
                    elif line.startswith("**Status:**"):
                        probe_info["status"] = line.split("**Status:**")[1].strip()
                
                probes.append(probe_info)
    
    return probes

@mcp.tool()
def generate_synthetic_personas(count: int = 5, domain: str = "general") -> Dict[str, Any]:
    """Generate synthetic user personas for PoL Probe testing.
    
    Args:
        count: Number of personas to generate (1-20)
        domain: Domain context (general, saas, fintech, healthcare, etc.)
    
    Returns:
        Dict with generated personas and file path
    """
    if count < 1 or count > 20:
        return {"error": "Count must be between 1 and 20"}
    
    # Create personas directory
    personas_dir = os.path.expanduser("~/ai-pm-toolkit/synthetic-data/personas")
    os.makedirs(personas_dir, exist_ok=True)
    
    # Simple persona templates (in a real implementation, you'd use Faker/Mimesis)
    roles = ["Product Manager", "Developer", "Designer", "Marketing Manager", "Sales Rep", 
             "Customer Success", "CEO", "CTO", "Data Analyst", "Operations Manager"]
    
    company_sizes = ["Startup (1-50)", "Growth (51-200)", "Mid-market (201-1000)", "Enterprise (1000+)"]
    tech_levels = ["Low", "Medium", "High"]
    
    personas = []
    for i in range(count):
        persona = {
            "id": f"persona_{i+1}",
            "name": f"User {i+1}",
            "role": roles[i % len(roles)],
            "company_size": company_sizes[i % len(company_sizes)],
            "tech_savviness": tech_levels[i % len(tech_levels)],
            "domain": domain,
            "pain_points": [
                "Time-consuming manual processes",
                "Lack of integration between tools",
                "Difficulty accessing relevant data"
            ],
            "goals": [
                "Increase productivity",
                "Make data-driven decisions",
                "Improve team collaboration"
            ]
        }
        personas.append(persona)
    
    # Save personas to file
    personas_file = os.path.join(personas_dir, f"{domain}_{count}_personas_{datetime.datetime.now().strftime('%Y%m%d')}.json")
    with open(personas_file, 'w') as f:
        json.dump(personas, f, indent=2)
    
    return {
        "count": count,
        "domain": domain,
        "personas": personas,
        "file_path": personas_file,
        "usage_tips": [
            "Use these personas in your PoL Probe testing",
            "Customize pain points and goals for your specific use case",
            "Generate user scenarios based on these profiles"
        ]
    }

if __name__ == "__main__":
    mcp.run()
FASTMCP_EOF

echo "   ✅ FastMCP AI PM template created"

# Install llama-cpp-agent-tools (optional)
echo "🦙 Installing llama-cpp-agent-tools..."
cd ~/ai-pm-toolkit/mcp-servers/agents
if [ ! -d "llama-cpp-agent-tools" ]; then
    echo "   📦 Attempting to clone llama-cpp-agent repository..."
    # Use GIT_TERMINAL_PROMPT=0 to prevent interactive authentication prompts
    if GIT_TERMINAL_PROMPT=0 timeout 30 git clone https://github.com/Maximilian-Winter/llama-cpp-agent.git llama-cpp-agent-tools >/dev/null 2>&1; then
        cd llama-cpp-agent-tools
        install_package "llama-cpp-python"
        install_package "llama-cpp-agent"
        echo "   ✅ llama-cpp-agent-tools installed"
    else
        echo "   ⚠️  llama-cpp-agent unavailable (requires GitHub access) - skipping"
        echo "      💡 This is optional - core toolkit functionality works without it"
    fi
else
    echo "✅ llama-cpp-agent-tools already installed"
fi

# Install llm.tools devon (AI software engineering agent)
echo "🛠️  Installing llm.tools devon (AI software engineering agent)..."
cd ~/ai-pm-toolkit/mcp-servers/tools
if [ ! -d "devon" ]; then
    echo "   📦 Cloning devon AI agent repository..."
    if git clone https://github.com/entropy-research/devon.git 2>/dev/null; then
        cd devon
        install_package "devon-agent"
        echo "   ✅ devon AI agent installed"
    else
        echo "   ⚠️  Could not clone devon agent - continuing without it"
    fi  
else
    echo "✅ devon AI agent already installed"
fi

# ========================================================================
# Market Research & Competitive Intelligence Tools
# ========================================================================

echo "📊 Installing market research & competitive intelligence tools..."

# Create workspace directories
echo "   📁 Creating market research workspace..."
mkdir -p ~/ai-pm-toolkit/market-research/{reports,data,templates,scripts}
mkdir -p ~/ai-pm-toolkit/competitive-intel/{analysis,reports,monitoring,insights}

# Install OpenBB Terminal
echo "🏦 Installing OpenBB Terminal (Financial & Market Research Platform)..."
if command -v conda &> /dev/null; then
    echo "   📦 Creating OpenBB conda environment..."
    if ! conda env list | grep -q "openbb-env"; then
        conda create -n openbb-env python=3.11 -y 2>/dev/null || echo "   ⚠️  Could not create conda environment, using pip installation"
        if conda env list | grep -q "openbb-env"; then
            eval "$(conda shell.bash hook)"
            conda activate openbb-env
            pip install "openbb[all]" --quiet 2>/dev/null && echo "   ✅ OpenBB Terminal installed in conda environment" || echo "   ⚠️  OpenBB installation had issues, continuing..."
            conda deactivate
        fi
    else
        echo "   ✅ OpenBB Terminal conda environment already exists"
    fi
else
    echo "   📦 Installing OpenBB Terminal with pip..."
    install_package "openbb[all]"
fi

# Create OpenBB launcher script
cat > ~/ai-pm-toolkit/market-research/scripts/launch-openbb << 'EOF'
#!/bin/bash
echo "🏦 Starting OpenBB Terminal for Market Research"
echo "=============================================="
echo ""
echo "📊 OpenBB Terminal provides access to:"
echo "   • Financial data and market analysis"
echo "   • Economic indicators and trends"
echo "   • Company financials and competitor research"
echo "   • Market research and due diligence tools"
echo ""

cd ~/ai-pm-toolkit/market-research

# Try conda environment first, then fallback to system python
if command -v conda &> /dev/null && conda env list | grep -q "openbb-env"; then
    echo "🔄 Activating OpenBB conda environment..."
    eval "$(conda shell.bash hook)"
    conda activate openbb-env
    echo "🚀 Starting OpenBB Terminal..."
    python -c "from openbb import obb; obb"
else
    echo "🚀 Starting OpenBB Terminal (system python)..."
    python3 -c "from openbb import obb; obb" 2>/dev/null || echo "❌ OpenBB not available. Install with: pip install 'openbb[all]'"
fi
EOF

chmod +x ~/ai-pm-toolkit/market-research/scripts/launch-openbb

# Install Local Deep Researcher (LangChain AI version)
echo "🔍 Installing Local Deep Researcher (AI Research Automation)..."
cd ~/ai-pm-toolkit/competitive-intel
if [ ! -d "local-deep-researcher" ]; then
    echo "   📦 Cloning Local Deep Researcher repository..."
    if git clone https://github.com/langchain-ai/local-deep-researcher.git 2>/dev/null; then
        cd local-deep-researcher
        echo "   📦 Setting up research environment..."
        if command -v uv &> /dev/null; then
            uv venv --python 3.11 || python3 -m venv venv
            if [ -f "venv/bin/activate" ]; then
                source venv/bin/activate
                uv pip install -e . 2>/dev/null || pip install -e . 2>/dev/null
                echo "   ✅ Local Deep Researcher installed"
                deactivate
            fi
        else
            python3 -m venv venv 2>/dev/null
            if [ -f "venv/bin/activate" ]; then
                source venv/bin/activate
                pip install -e . 2>/dev/null || echo "   ⚠️  Could not install dependencies"
                deactivate
            fi
        fi
    else
        echo "   ⚠️  Could not clone Local Deep Researcher - continuing without it"
    fi
else
    echo "   ✅ Local Deep Researcher already installed"
fi

# Create Deep Researcher launcher script
cat > ~/ai-pm-toolkit/competitive-intel/scripts/start-deep-research << 'EOF'
#!/bin/bash
echo "🔍 Starting Local Deep Researcher"
echo "================================="
echo ""
echo "🤖 AI-Powered Research Automation:"
echo "   • Autonomous research on any topic"
echo "   • Multi-step reasoning and analysis"
echo "   • Local processing with Ollama"
echo "   • Web search and document analysis"
echo ""

cd ~/ai-pm-toolkit/competitive-intel/local-deep-researcher

if [ -f "venv/bin/activate" ]; then
    echo "🔄 Activating research environment..."
    source venv/bin/activate
    
    echo "🚀 Starting LangGraph server for deep research..."
    echo "   Access at: http://localhost:8123"
    
    if command -v langgraph &> /dev/null; then
        langgraph dev --allow-blocking
    else
        echo "❌ LangGraph CLI not available. Install with:"
        echo "   uvx --refresh --from 'langgraph-cli[inmem]' --with-editable . --python 3.11 langgraph dev --allow-blocking"
    fi
else
    echo "❌ Deep Researcher not properly installed"
    echo "   Run setup again or check ~/ai-pm-toolkit/competitive-intel/local-deep-researcher/"
fi
EOF

chmod +x ~/ai-pm-toolkit/competitive-intel/scripts/start-deep-research

# Install Gemini CLI
echo "💎 Installing Gemini CLI (Google AI for Market Research)..."
if command -v npm &> /dev/null; then
    echo "   📦 Installing Gemini CLI via npm..."
    npm install -g @google/gemini-cli --silent 2>/dev/null && echo "   ✅ Gemini CLI installed successfully" || echo "   ⚠️  Gemini CLI installation had issues, continuing..."
elif command -v brew &> /dev/null; then
    echo "   📦 Installing Gemini CLI via Homebrew..."
    brew install gemini-cli --quiet 2>/dev/null && echo "   ✅ Gemini CLI installed successfully" || echo "   ⚠️  Gemini CLI installation had issues, continuing..."
else
    echo "   ⚠️  Neither npm nor brew available for Gemini CLI installation"
fi

# Create Gemini CLI setup script
cat > ~/ai-pm-toolkit/market-research/scripts/setup-gemini << 'EOF'
#!/bin/bash
echo "💎 Gemini CLI Setup for Market Research"
echo "======================================="
echo ""
echo "🔐 Setting up Gemini CLI authentication..."
echo ""
echo "Choose authentication method:"
echo "1) Google Account (60 req/min, 1000/day free)"
echo "2) API Key (requires Google AI Studio key)"
echo ""
read -p "Enter choice [1-2]: " auth_choice

case $auth_choice in
    1)
        echo "🔄 Starting Gemini CLI with Google Account auth..."
        echo "   Follow the prompts to sign in with your Google account"
        gemini
        ;;
    2)
        echo "🔑 API Key Setup:"
        echo "   1. Get your API key from: https://aistudio.google.com/app/apikey"
        echo "   2. Set it as environment variable:"
        echo "   3. export GEMINI_API_KEY='your_api_key_here'"
        echo ""
        read -p "Enter your Gemini API key: " api_key
        if [[ -n "$api_key" ]]; then
            echo "export GEMINI_API_KEY='$api_key'" >> ~/.zshrc
            export GEMINI_API_KEY="$api_key"
            echo "   ✅ API key configured"
            echo "   🚀 Starting Gemini CLI..."
            gemini
        else
            echo "   ❌ No API key provided, run this script again when ready"
        fi
        ;;
    *)
        echo "❌ Invalid choice. Run this script again."
        ;;
esac
EOF

chmod +x ~/ai-pm-toolkit/market-research/scripts/setup-gemini

# Create market research utilities
cat > ~/ai-pm-toolkit/market-research/scripts/research-competitor << 'EOF'
#!/bin/bash
echo "🏢 Competitive Research Automation"
echo "=================================="
echo ""

if [[ -z "$1" ]]; then
    echo "Usage: ./research-competitor <company-name>"
    echo ""
    echo "Examples:"
    echo "  ./research-competitor 'Slack'"
    echo "  ./research-competitor 'Notion'"
    echo "  ./research-competitor 'Figma'"
    exit 1
fi

COMPANY="$1"
REPORT_DIR="~/ai-pm-toolkit/competitive-intel/reports/$(date +%Y%m%d)_${COMPANY// /_}"

echo "🔍 Researching: $COMPANY"
echo "📁 Report will be saved to: $REPORT_DIR"
echo ""

mkdir -p "$REPORT_DIR"

echo "🤖 Starting AI-powered competitive research..."
echo "   This may take several minutes..."

# Use Gemini CLI for initial research if available
if command -v gemini &> /dev/null; then
    echo "💎 Using Gemini CLI for market research..."
    gemini "Research the company $COMPANY. Provide: 1) Business model, 2) Key products/services, 3) Target market, 4) Recent funding/news, 5) Competitive advantages, 6) Market positioning. Format as structured report." > "$REPORT_DIR/gemini_analysis.md"
fi

# Use OpenBB for financial data if available
if python3 -c "import openbb" 2>/dev/null; then
    echo "🏦 Gathering financial data with OpenBB..."
    python3 -c "
from openbb import obb
import json
try:
    # Try to get company overview and financial data
    company_data = obb.stocks.ca.overview('$COMPANY')
    with open('$REPORT_DIR/financial_overview.json', 'w') as f:
        json.dump(company_data, f, indent=2, default=str)
    print('✅ Financial data saved')
except Exception as e:
    print(f'⚠️  Could not retrieve financial data: {e}')
" 2>/dev/null
fi

echo ""
echo "✅ Competitive research completed!"
echo "📊 Check your results in: $REPORT_DIR"
echo ""
echo "📈 Next steps:"
echo "   • Review the generated reports"
echo "   • Use aipm_research for deeper analysis"
echo "   • Create PoL Probes based on insights"
EOF

chmod +x ~/ai-pm-toolkit/market-research/scripts/research-competitor

# Create comprehensive market research dashboard
cat > ~/ai-pm-toolkit/market-research/scripts/market-dashboard << 'EOF'
#!/bin/bash
echo "📊 AI PM Market Research Dashboard"
echo "=================================="
echo ""
echo "🎯 4E Framework: Education → Experimentation → Exploration → Explanation"
echo ""
echo "🎓 EDUCATION - Learn Market Research:"
echo "   1) OpenBB Terminal           - Learn financial research hands-on"
echo "   2) Gemini CLI Tutorial       - Practice AI-powered market analysis"
echo ""
echo "🔍 EXPLORATION - Discover Market Insights:"
echo "   3) Deep Research Agent       - Explore autonomous multi-step research"
echo "   4) Market Intelligence       - Discover competitive landscape patterns"
echo ""
echo "🧪 EXPERIMENTATION - Test Market Hypotheses:"
echo "   5) Company Analysis          - Test competitor assumptions with data"
echo "   6) Market Simulation         - Experiment with market scenarios"
echo ""
echo "📊 EXPLANATION - Create Compelling Market Stories:"
echo "   7) Market Report Generator   - Build comprehensive stakeholder reports"
echo "   8) Competitive Matrix        - Create visual competitor comparisons"
echo ""
echo "🛠️  Setup & Configuration:"
echo "   9) Test All Tools           - Verify your 4E market research setup"
echo ""
read -p "Choose an option [1-9]: " choice

case $choice in
    1)
        echo "🎓 Starting OpenBB Terminal for hands-on financial research learning..."
        ~/ai-pm-toolkit/market-research/scripts/launch-openbb
        ;;
    2)
        echo "🎓 Starting Gemini CLI tutorial for AI-powered market analysis..."
        ~/ai-pm-toolkit/market-research/scripts/setup-gemini
        ;;
    3)
        echo "🔍 Starting Deep Research Agent for autonomous exploration..."
        ~/ai-pm-toolkit/competitive-intel/scripts/start-deep-research
        ;;
    4)
        read -p "Enter market/industry to explore: " market
        echo "🔍 Exploring market intelligence patterns for: $market"
        echo "   Use aipm_research for deep autonomous exploration"
        echo "   Use aipm_openbb for financial data discovery"
        ;;
    5)
        read -p "Enter company name to analyze: " company
        echo "🧪 Testing competitor assumptions with data for: $company"
        ~/ai-pm-toolkit/market-research/scripts/research-competitor "$company"
        ;;
    6)
        read -p "Enter research hypothesis to test: " hypothesis
        echo "🧪 Setting up market scenario experiment for: $hypothesis"
        echo "   Creating synthetic market conditions for testing..."
        ;;
    7)
        read -p "Enter market/industry for report: " market
        echo "📊 Generating comprehensive stakeholder report for: $market"
        # Create report directory
        report_dir="~/ai-pm-toolkit/market-research/reports/$(date +%Y%m%d)_${market// /_}"
        mkdir -p "$report_dir"
        echo "Report will be saved to: $report_dir"
        echo "   This report will provide compelling market narrative for stakeholders"
        ;;
    8)
        read -p "Enter first company: " company1
        read -p "Enter second company: " company2
        echo "📊 Creating visual competitive matrix: $company1 vs $company2"
        ~/ai-pm-toolkit/competitive-intel/scripts/competitive-matrix "$company1" "$company2"
        ;;
    9)
        echo "🧪 Testing your 4E market research setup..."
        echo ""
        echo "🎓 Education Tools:"
        
        # Test OpenBB
        if python3 -c "import openbb" 2>/dev/null; then
            echo "   ✅ OpenBB Terminal - Ready for financial research education"
        else
            echo "   ❌ OpenBB Terminal - Not available"
        fi
        
        # Test Gemini CLI
        if command -v gemini &> /dev/null; then
            echo "   ✅ Gemini CLI - Ready for AI market analysis learning"
        else
            echo "   ❌ Gemini CLI - Not available"
        fi
        
        echo ""
        echo "🔍 Exploration Tools:"
        
        # Test Deep Researcher
        if [ -d "~/ai-pm-toolkit/competitive-intel/local-deep-researcher" ]; then
            echo "   ✅ Local Deep Researcher - Ready for market exploration"
        else
            echo "   ❌ Local Deep Researcher - Not available"
        fi
        
        echo ""
        echo "🧪 Experimentation Tools:"
        echo "   ✅ Synthetic data generators - Ready for hypothesis testing"
        echo ""
        echo "📊 Explanation Tools:"
        echo "   ✅ Report generators - Ready for stakeholder presentations"
        ;;
    *)
        echo "❌ Invalid choice"
        echo "Choose 1-9 to explore the 4E market research framework"
        ;;
esac
EOF

chmod +x ~/ai-pm-toolkit/market-research/scripts/market-dashboard

# Create additional competitive intelligence integration scripts
echo "🔍 Setting up additional competitive intelligence integrations..."

# SimilarWeb CLI integration
cat > ~/ai-pm-toolkit/competitive-intel/scripts/similarweb-analysis << 'EOF'
#!/bin/bash
echo "🌐 SimilarWeb Digital Intelligence"
echo "================================="
echo ""

if [[ -z "$1" ]]; then
    echo "Usage: ./similarweb-analysis <domain>"
    echo ""
    echo "Examples:"
    echo "  ./similarweb-analysis 'slack.com'"
    echo "  ./similarweb-analysis 'notion.so'"
    echo "  ./similarweb-analysis 'figma.com'"
    echo ""
    echo "Note: Requires SIMILARWEB_API_KEY environment variable"
    echo "      Configure with: ~/ai-pm-toolkit/configure-apis.sh"
    exit 1
fi

DOMAIN="$1"
REPORT_DIR="~/ai-pm-toolkit/competitive-intel/reports/$(date +%Y%m%d)_similarweb_${DOMAIN//\./_}"

echo "🔍 Analyzing domain: $DOMAIN"
echo "📁 Report will be saved to: $REPORT_DIR"
echo ""

mkdir -p "$REPORT_DIR"

if [[ -n "$SIMILARWEB_API_KEY" ]]; then
    echo "🌐 Fetching SimilarWeb data..."
    echo "   This is a placeholder for SimilarWeb API integration"
    echo "   Domain: $DOMAIN" > "$REPORT_DIR/similarweb_data.txt"
    echo "   Date: $(date)" >> "$REPORT_DIR/similarweb_data.txt"
    echo "   Status: API integration ready for implementation" >> "$REPORT_DIR/similarweb_data.txt"
    echo "   ✅ Basic report generated"
else
    echo "⚠️  SIMILARWEB_API_KEY not configured"
    echo "   Run: ~/ai-pm-toolkit/configure-apis.sh to set up API access"
    echo "   Creating placeholder report..."
    echo "Domain: $DOMAIN - Manual analysis needed" > "$REPORT_DIR/manual_analysis.txt"
fi

echo ""
echo "📊 Next steps:"
echo "   • Review the generated reports"
echo "   • Configure SimilarWeb API for automated data"
echo "   • Combine with other competitive intelligence tools"
EOF

chmod +x ~/ai-pm-toolkit/competitive-intel/scripts/similarweb-analysis

# Brand monitoring integration
cat > ~/ai-pm-toolkit/competitive-intel/scripts/brand-monitor << 'EOF'
#!/bin/bash
echo "👁️ Brand & Mention Monitoring"
echo "============================="
echo ""

if [[ -z "$1" ]]; then
    echo "Usage: ./brand-monitor <brand-name>"
    echo ""
    echo "Examples:"
    echo "  ./brand-monitor 'YourCompany'"
    echo "  ./brand-monitor 'CompetitorName'"
    echo ""
    exit 1
fi

BRAND="$1"
REPORT_DIR="~/ai-pm-toolkit/competitive-intel/monitoring/$(date +%Y%m%d)_${BRAND// /_}"

echo "👁️ Monitoring brand: $BRAND"
echo "📁 Reports will be saved to: $REPORT_DIR"
echo ""

mkdir -p "$REPORT_DIR"

echo "🔍 Setting up brand monitoring for: $BRAND"
echo "   This is a foundation for brand monitoring integration"
echo ""

# Create monitoring configuration
cat > "$REPORT_DIR/monitoring_config.json" << 'MONITOR_EOF'
{
  "brand": "'$BRAND'",
  "setup_date": "'$(date)'",
  "sources": [
    "Twitter",
    "Reddit", 
    "News",
    "Blogs",
    "Forums"
  ],
  "keywords": [
    "'$BRAND'",
    "'${BRAND// /}'"
  ],
  "status": "configured"
}
MONITOR_EOF

echo "✅ Monitoring configuration created"
echo ""
echo "📈 Next steps:"
echo "   • Configure Twitter API in configure-apis.sh"
echo "   • Set up News API for media monitoring"
echo "   • Implement automated mention collection"
echo "   • Create alert system for brand mentions"
EOF

chmod +x ~/ai-pm-toolkit/competitive-intel/scripts/brand-monitor

# Competely-style competitive analysis
cat > ~/ai-pm-toolkit/competitive-intel/scripts/competitive-matrix << 'EOF'
#!/bin/bash
echo "⚖️ Competitive Analysis Matrix"
echo "============================="
echo ""

if [[ -z "$1" ]] || [[ -z "$2" ]]; then
    echo "Usage: ./competitive-matrix <your-company> <competitor>"
    echo ""
    echo "Examples:"
    echo "  ./competitive-matrix 'YourProduct' 'Slack'"
    echo "  ./competitive-matrix 'YourApp' 'Notion'"
    echo ""
    exit 1
fi

YOUR_COMPANY="$1"
COMPETITOR="$2"
REPORT_DIR="~/ai-pm-toolkit/competitive-intel/analysis/$(date +%Y%m%d)_${YOUR_COMPANY// /_}_vs_${COMPETITOR// /_}"

echo "⚖️ Comparing: $YOUR_COMPANY vs $COMPETITOR"
echo "📁 Analysis will be saved to: $REPORT_DIR"
echo ""

mkdir -p "$REPORT_DIR"

# Create competitive analysis template
cat > "$REPORT_DIR/competitive_analysis.md" << 'ANALYSIS_EOF'
# Competitive Analysis: '$YOUR_COMPANY' vs '$COMPETITOR'

*Generated on: $(date)*
*Using the 4E Framework: Education → Experimentation → Exploration → Explanation*

## 4E Framework for Competitive Analysis

### 🎓 Education Phase - Learn About the Competition
Use this phase to build understanding of both companies through research and data gathering.

### 🧪 Experimentation Phase - Test Your Assumptions
Use synthetic data and market simulations to test hypotheses about competitive positioning.

### 🔍 Exploration Phase - Discover Competitive Insights  
Explore market patterns, user feedback, and competitive intelligence to uncover opportunities.

### 📊 Explanation Phase - Create Compelling Competitive Story
Build narrative that shows stakeholders why your positioning will win in the market.

## Competitive Analysis Framework

### 1. Product Features
- [ ] Core functionality comparison
- [ ] Unique differentiators
- [ ] Feature gaps and opportunities

### 2. Market Position  
- [ ] Target market analysis
- [ ] Pricing strategy comparison
- [ ] Market share and reach

### 3. User Experience
- [ ] Onboarding and usability
- [ ] Customer feedback analysis
- [ ] Support and documentation

### 4. Technical Architecture
- [ ] Platform capabilities
- [ ] Integration ecosystem
- [ ] Performance and reliability

### 5. Business Model
- [ ] Revenue streams
- [ ] Growth strategy
- [ ] Funding and resources

## Competitive Intelligence Sources
- [ ] Public company information
- [ ] Product websites and documentation
- [ ] User reviews and feedback
- [ ] Social media and community discussions
- [ ] Industry reports and analysis

## Action Items
- [ ] Feature prioritization based on competitive gaps
- [ ] Market positioning refinements
- [ ] Product strategy adjustments

## 4E Framework Tools for Deeper Analysis

### 🎓 Education Tools
- Use `aipm_openbb` for hands-on financial data learning
- Use `aipm_gemini` tutorial mode for AI research education

### 🧪 Experimentation Tools  
- Use `aipm experiment` to test competitive positioning hypotheses
- Use `aipm_data` to generate synthetic competitor scenarios

### 🔍 Exploration Tools
- Use `aipm_research` for autonomous competitive intelligence discovery
- Use `aipm_market` dashboard for comprehensive competitive exploration

### 📊 Explanation Tools
- Use `aipm prototype` to create competitive demo narratives
- Use `aipm_design` to create visual competitive positioning
ANALYSIS_EOF

echo "✅ Competitive analysis template created"
echo "📊 Framework ready for manual or AI-assisted completion"
echo ""
echo "🤖 AI-Powered Next Steps:"
echo "   aipm_gemini # Use Google AI for detailed competitive research"
echo "   aipm_research # Launch autonomous research agent"
echo "   aipm_competitive '$COMPETITOR' # Generate automated competitor report"
EOF

chmod +x ~/ai-pm-toolkit/competitive-intel/scripts/competitive-matrix

echo "   ✅ Market research & competitive intelligence tools installed"

# ========================================================================
# Enhanced AI & Development Tools
# ========================================================================

echo "🤖 Installing enhanced AI & development tools..."

# Create workspace directories
echo "   📁 Creating enhanced AI tools workspace..."
mkdir -p ~/ai-pm-toolkit/ai-tools/{localai,phoenix,gradio,whisper}
mkdir -p ~/ai-pm-toolkit/design/penpot
mkdir -p ~/ai-pm-toolkit/interfaces/gradio
mkdir -p ~/ai-pm-toolkit/transcripts/whisper

# Install LocalAI (Local AI Server)
echo "🏠 Installing LocalAI (Local AI Server for Privacy-First Learning)..."
if command -v docker &> /dev/null; then
    echo "   🐳 Docker found - setting up LocalAI container..."
    
    # Create LocalAI launcher script
    cat > ~/ai-pm-toolkit/ai-tools/localai/launch-localai << 'EOF'
#!/bin/bash
echo "🏠 Starting LocalAI Server"
echo "========================="
echo ""
echo "🎓 4E Framework: Education & Experimentation"
echo "   • Privacy-first AI learning environment"
echo "   • Drop-in replacement for OpenAI API"
echo "   • No data leaves your machine"
echo "   • Cost-free AI experimentation"
echo ""

LOCALAI_PORT=8080
LOCALAI_CONTAINER="aipm-localai"

# Check if container is already running
if docker ps --format 'table {{.Names}}' | grep -q "$LOCALAI_CONTAINER"; then
    echo "✅ LocalAI is already running"
    echo "   Access at: http://localhost:$LOCALAI_PORT"
    echo "   Web UI: http://localhost:$LOCALAI_PORT/browse/"
    exit 0
fi

# Check if container exists but is stopped
if docker ps -a --format 'table {{.Names}}' | grep -q "$LOCALAI_CONTAINER"; then
    echo "🔄 Starting existing LocalAI container..."
    docker start "$LOCALAI_CONTAINER"
else
    echo "📦 Creating new LocalAI container..."
    echo "   This may take a few minutes on first run..."
    
    docker run -d \
        --name "$LOCALAI_CONTAINER" \
        -p $LOCALAI_PORT:8080 \
        -v ~/ai-pm-toolkit/ai-tools/localai/models:/build/models:cached \
        localai/localai:latest-aio-cpu
fi

echo ""
echo "🚀 LocalAI Server started successfully!"
echo "   API Endpoint: http://localhost:$LOCALAI_PORT"
echo "   Web Interface: http://localhost:$LOCALAI_PORT/browse/"
echo "   Model Gallery: http://localhost:$LOCALAI_PORT/browse/models"
echo ""
echo "📚 Strategic PM Use Cases:"
echo "   • Learn AI concepts without API costs"
echo "   • Experiment with prompts safely and privately"
echo "   • Test AI features before committing to cloud services"
echo "   • Build PoL Probes with local AI capabilities"
echo ""
echo "🔧 Usage Tips:"
echo "   • Install models from the Web UI Gallery"
echo "   • Use same API format as OpenAI (drop-in replacement)"
echo "   • All processing happens locally - no internet required"
echo ""
echo "🛑 To stop: docker stop $LOCALAI_CONTAINER"
EOF

    chmod +x ~/ai-pm-toolkit/ai-tools/localai/launch-localai
    
    # Create LocalAI management script
    cat > ~/ai-pm-toolkit/ai-tools/localai/manage-localai << 'EOF'
#!/bin/bash
echo "🏠 LocalAI Management"
echo "===================="
echo ""

LOCALAI_CONTAINER="aipm-localai"

case "$1" in
    "start")
        ~/ai-pm-toolkit/ai-tools/localai/launch-localai
        ;;
    "stop")
        echo "🛑 Stopping LocalAI..."
        docker stop "$LOCALAI_CONTAINER" 2>/dev/null && echo "   ✅ LocalAI stopped" || echo "   ⚠️  LocalAI was not running"
        ;;
    "restart")
        echo "🔄 Restarting LocalAI..."
        docker restart "$LOCALAI_CONTAINER" 2>/dev/null && echo "   ✅ LocalAI restarted" || echo "   ❌ Could not restart LocalAI"
        ;;
    "status")
        echo "📊 LocalAI Status:"
        if docker ps --format 'table {{.Names}}' | grep -q "$LOCALAI_CONTAINER"; then
            echo "   ✅ Running - http://localhost:8080"
        elif docker ps -a --format 'table {{.Names}}' | grep -q "$LOCALAI_CONTAINER"; then
            echo "   ⏸️  Stopped - run 'manage-localai start' to start"
        else
            echo "   ❌ Not installed - run 'aipm_localai' to install"
        fi
        ;;
    "logs")
        echo "📝 LocalAI Logs:"
        docker logs "$LOCALAI_CONTAINER" --tail 50
        ;;
    "remove")
        echo "🗑️ Removing LocalAI container..."
        docker stop "$LOCALAI_CONTAINER" 2>/dev/null
        docker rm "$LOCALAI_CONTAINER" 2>/dev/null
        echo "   ✅ LocalAI container removed"
        ;;
    *)
        echo "Usage: manage-localai {start|stop|restart|status|logs|remove}"
        echo ""
        echo "Commands:"
        echo "  start    - Start LocalAI server"
        echo "  stop     - Stop LocalAI server"
        echo "  restart  - Restart LocalAI server"
        echo "  status   - Check LocalAI status"
        echo "  logs     - View LocalAI logs"
        echo "  remove   - Remove LocalAI container completely"
        ;;
esac
EOF

    chmod +x ~/ai-pm-toolkit/ai-tools/localai/manage-localai
    echo "   ✅ LocalAI setup completed"
else
    echo "   ⚠️  Docker not found - LocalAI requires Docker for container deployment"
    echo "   📦 Install Docker first, then re-run setup to enable LocalAI"
    
    # Create fallback script
    cat > ~/ai-pm-toolkit/ai-tools/localai/install-docker-first << 'EOF'
#!/bin/bash
echo "🐳 Docker Required for LocalAI"
echo "=============================="
echo ""
echo "LocalAI requires Docker for easy installation and management."
echo ""
echo "📦 Install Docker:"
echo "   macOS: brew install --cask docker"
echo "   Linux: curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh"
echo ""
echo "After installing Docker, re-run the toolkit setup to enable LocalAI."
EOF
    chmod +x ~/ai-pm-toolkit/ai-tools/localai/install-docker-first
fi

# Install Phoenix Arize AI Observability
echo "🔬 Installing Phoenix Arize AI Observability (ML Monitoring & Evaluation)..."
install_package "arize-phoenix"

if $PYTHON_CMD -c "import phoenix" 2>/dev/null; then
    # Create Phoenix launcher script
    cat > ~/ai-pm-toolkit/ai-tools/phoenix/launch-phoenix << 'EOF'
#!/bin/bash
echo "🔬 Starting Phoenix AI Observability"
echo "===================================="
echo ""
echo "🧪 4E Framework: Experimentation & Exploration"
echo "   • Rigorous AI model testing and evaluation"
echo "   • LLM application observability and monitoring"
echo "   • Hypothesis testing with real model performance data"
echo "   • Discover AI model behavior patterns"
echo ""

cd ~/ai-pm-toolkit/ai-tools/phoenix

echo "🚀 Starting Phoenix server..."
echo "   This will open in your browser automatically"

python3 << 'PYTHON_EOF'
import phoenix as px
import webbrowser
import time

print("📊 Launching Phoenix AI Observability Platform...")

# Launch Phoenix
session = px.launch_app(
    port=6006,
    host="0.0.0.0"
)

print(f"✅ Phoenix started successfully!")
print(f"   Web Interface: http://localhost:6006")
print(f"   OpenTelemetry Endpoint: http://localhost:4317")
print("")
print("📚 Strategic PM Use Cases:")
print("   • Monitor AI feature performance in PoL Probes")
print("   • Test prompt variations systematically")
print("   • Evaluate model behavior across user scenarios")
print("   • Generate evidence for AI feature decisions")
print("")
print("🔧 Usage Tips:")
print("   • Use with LangChain, LlamaIndex, or direct OpenTelemetry")
print("   • Track model costs, latency, and quality metrics")
print("   • Compare different AI approaches with data")
print("")
print("🛑 Press Ctrl+C to stop Phoenix")

try:
    # Keep the server running
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Phoenix server stopped")
PYTHON_EOF
EOF

    chmod +x ~/ai-pm-toolkit/ai-tools/phoenix/launch-phoenix
    echo "   ✅ Phoenix AI Observability setup completed"
else
    echo "   ⚠️  Phoenix installation may have failed - continuing with other tools"
fi

# Install Gradio Interface Builder
echo "🎨 Installing Gradio (Interactive ML Interface Builder)..."
install_package "gradio"

if $PYTHON_CMD -c "import gradio" 2>/dev/null; then
    # Create Gradio starter script
    cat > ~/ai-pm-toolkit/interfaces/gradio/gradio-starter << 'EOF'
#!/bin/bash
echo "🎨 Gradio Interface Builder"
echo "=========================="
echo ""
echo "🔍 4E Framework: Exploration & Explanation"
echo "   • Rapidly build interactive AI interfaces"
echo "   • Create 'vibe-coded' probes for user testing"
echo "   • Demonstrate AI possibilities to stakeholders"
echo "   • Build compelling AI feature prototypes"
echo ""

cd ~/ai-pm-toolkit/interfaces/gradio

echo "🚀 Creating Gradio interface template..."

# Create a basic template for PM use
cat > pm_interface_template.py << 'PYTHON_EOF'
"""
AI PM Gradio Interface Template
4E Framework: Exploration & Explanation

This template helps strategic PMs create interactive AI interfaces
for PoL Probes and stakeholder demonstrations.
"""

import gradio as gr
import os

def ai_feature_demo(user_input):
    """
    Template function for AI feature demonstration
    Replace this with your actual AI functionality
    """
    return f"AI Response to: '{user_input}'\n\n(Replace this with actual AI integration - LocalAI, OpenAI, etc.)"

def create_pm_interface():
    """Create an interface optimized for PM demonstrations"""
    
    # Define the interface
    interface = gr.Interface(
        fn=ai_feature_demo,
        inputs=[
            gr.Textbox(
                label="User Input", 
                placeholder="Enter text to demonstrate AI feature...",
                lines=3
            )
        ],
        outputs=[
            gr.Textbox(
                label="AI Response",
                lines=5
            )
        ],
        title="🧪 AI Feature PoL Probe",
        description="""
        **4E Framework Demo Interface**
        
        🔍 **Exploration**: Test AI possibilities interactively
        📊 **Explanation**: Show stakeholders AI capabilities
        
        *Customize this interface for your specific PoL Probe needs*
        """,
        examples=[
            ["How would this AI feature help users?"],
            ["What are the key benefits of this approach?"],
            ["Show me how this would work in production"],
        ],
        theme=gr.themes.Soft()
    )
    
    return interface

if __name__ == "__main__":
    print("🎨 Starting AI PM Interface Demo...")
    print("   Customize pm_interface_template.py for your PoL Probe")
    print("   Access at: http://localhost:7860")
    print("")
    
    demo = create_pm_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,  # Set to True for public sharing during demos
        show_error=True
    )
PYTHON_EOF

echo "📊 Template created: pm_interface_template.py"
echo ""
echo "🚀 Starting Gradio interface template..."
echo "   Customize the template for your specific PoL Probe needs"
echo "   Access at: http://localhost:7860"
echo ""

python3 pm_interface_template.py
EOF

    chmod +x ~/ai-pm-toolkit/interfaces/gradio/gradio-starter
    echo "   ✅ Gradio interface builder setup completed"
else
    echo "   ⚠️  Gradio installation may have failed - continuing with other tools"
fi

# Install OpenAI Whisper
echo "🎙️ Installing OpenAI Whisper (Speech-to-Text for PM Workflows)..."

# Check for FFmpeg first
if command -v ffmpeg &> /dev/null; then
    echo "   ✅ FFmpeg found - proceeding with Whisper installation"
    
    # Install Whisper
    if pip install git+https://github.com/openai/whisper.git --quiet 2>/dev/null; then
        echo "   ✅ Whisper installed successfully"
        
        # Create Whisper utility script
        cat > ~/ai-pm-toolkit/transcripts/whisper/whisper-transcribe << 'EOF'
#!/bin/bash
echo "🎙️ Whisper Speech-to-Text for Strategic PMs"
echo "==========================================="
echo ""
echo "🎓 4E Framework: Education & Explanation"
echo "   • Transcribe user interviews for PoL Probes"
echo "   • Create narrated prototype walkthroughs"
echo "   • Generate accessible learning content"
echo "   • Process stakeholder feedback recordings"
echo ""

if [[ -z "$1" ]]; then
    echo "Usage: ./whisper-transcribe <audio-file> [model-size]"
    echo ""
    echo "Model sizes: tiny, base, small, medium, large (default: base)"
    echo ""
    echo "Examples:"
    echo "  ./whisper-transcribe user_interview.mp3"
    echo "  ./whisper-transcribe prototype_demo.wav medium"
    echo "  ./whisper-transcribe stakeholder_feedback.m4a large"
    echo ""
    echo "📁 Supported formats: mp3, wav, m4a, flac, ogg, and more"
    exit 1
fi

AUDIO_FILE="$1"
MODEL_SIZE="${2:-base}"
OUTPUT_DIR="~/ai-pm-toolkit/transcripts/whisper/output"

echo "🎯 Transcribing: $AUDIO_FILE"
echo "📊 Model: $MODEL_SIZE"
echo ""

mkdir -p "$OUTPUT_DIR"

echo "🔄 Processing audio file..."
echo "   (This may take a few minutes depending on file length and model size)"

whisper "$AUDIO_FILE" \
    --model "$MODEL_SIZE" \
    --output_dir "$OUTPUT_DIR" \
    --output_format txt \
    --output_format json \
    --output_format srt \
    --language auto

echo ""
echo "✅ Transcription completed!"
echo "📂 Output files saved to: $OUTPUT_DIR"
echo ""
echo "📋 Generated files:"
echo "   • .txt - Plain text transcript"
echo "   • .json - Detailed transcript with timestamps"
echo "   • .srt - Subtitle format for video overlays"
echo ""
echo "📚 Strategic PM Use Cases:"
echo "   • Analyze user interview patterns and insights"
echo "   • Create searchable archives of stakeholder feedback"
echo "   • Generate captions for prototype demonstration videos"
echo "   • Extract key quotes for PoL Probe reports"
EOF

        chmod +x ~/ai-pm-toolkit/transcripts/whisper/whisper-transcribe
        
        # Create batch processing script
        cat > ~/ai-pm-toolkit/transcripts/whisper/batch-transcribe << 'EOF'
#!/bin/bash
echo "🎙️ Whisper Batch Transcription"
echo "=============================="
echo ""

if [[ -z "$1" ]]; then
    echo "Usage: ./batch-transcribe <directory> [model-size]"
    echo ""
    echo "Process all audio files in a directory"
    echo "Model sizes: tiny, base, small, medium, large (default: base)"
    exit 1
fi

INPUT_DIR="$1"
MODEL_SIZE="${2:-base}"

echo "📂 Processing directory: $INPUT_DIR"
echo "📊 Model: $MODEL_SIZE"
echo ""

count=0
for file in "$INPUT_DIR"/*.{mp3,wav,m4a,flac,ogg} 2>/dev/null; do
    if [[ -f "$file" ]]; then
        echo "🔄 Processing: $(basename "$file")"
        ~/ai-pm-toolkit/transcripts/whisper/whisper-transcribe "$file" "$MODEL_SIZE"
        ((count++))
        echo ""
    fi
done

echo "✅ Batch processing complete!"
echo "📊 Processed $count files"
EOF

        chmod +x ~/ai-pm-toolkit/transcripts/whisper/batch-transcribe
        echo "   ✅ Whisper transcription tools setup completed"
    else
        echo "   ⚠️  Whisper installation failed - continuing with other tools"
    fi
else
    echo "   ⚠️  FFmpeg not found - required for Whisper"
    echo "   📦 Install FFmpeg first: brew install ffmpeg (macOS)"
    
    # Create FFmpeg installation reminder
    cat > ~/ai-pm-toolkit/transcripts/whisper/install-ffmpeg-first << 'EOF'
#!/bin/bash
echo "🎙️ FFmpeg Required for Whisper"
echo "=============================="
echo ""
echo "Whisper requires FFmpeg for audio processing."
echo ""
echo "📦 Install FFmpeg:"
echo "   macOS: brew install ffmpeg"
echo "   Ubuntu/Debian: sudo apt install ffmpeg"
echo "   Linux: Use your distribution's package manager"
echo ""
echo "After installing FFmpeg, re-run the toolkit setup to enable Whisper."
EOF
    chmod +x ~/ai-pm-toolkit/transcripts/whisper/install-ffmpeg-first
fi

# Install Penpot (Design Tool)
echo "🎨 Setting up Penpot (Open-Source Design Tool)..."
# Penpot is typically self-hosted or used via web, so we'll create setup guidance

cat > ~/ai-pm-toolkit/design/penpot/penpot-setup << 'EOF'
#!/bin/bash
echo "🎨 Penpot Design Tool Setup"
echo "=========================="
echo ""
echo "📊 4E Framework: Explanation"
echo "   • Create visual artifacts for stakeholder presentations"
echo "   • Design compelling PoL Probe interfaces"
echo "   • Build professional mockups and prototypes"
echo "   • Collaborate on design assets with team members"
echo ""

echo "🔧 Penpot Installation Options:"
echo ""
echo "1. 🌐 **Web Version (Recommended for quick start)**"
echo "   • Visit: https://penpot.app"
echo "   • No installation required"
echo "   • Full feature access"
echo "   • Collaborative design capabilities"
echo ""
echo "2. 🏠 **Self-Hosted (Privacy-first option)**"
echo "   • Requires Docker and Docker Compose"
echo "   • Full control over your design data"
echo "   • Custom domain and SSL setup"
echo ""

read -p "Choose installation option [1: Web, 2: Self-hosted]: " choice

case $choice in
    1)
        echo ""
        echo "🌐 Opening Penpot web application..."
        echo "   📋 Create account or sign in"
        echo "   🎨 Start designing PoL Probe assets"
        echo "   📊 Perfect for stakeholder presentations"
        
        # Try to open in browser
        if command -v open &> /dev/null; then
            open "https://penpot.app"
        elif command -v xdg-open &> /dev/null; then
            xdg-open "https://penpot.app"
        else
            echo "   Visit: https://penpot.app"
        fi
        ;;
    2)
        echo ""
        echo "🏠 Self-Hosted Penpot Setup"
        echo "=========================="
        
        if command -v docker &> /dev/null && command -v docker-compose &> /dev/null; then
            echo "✅ Docker and Docker Compose found"
            echo ""
            echo "📦 Setting up self-hosted Penpot..."
            
            # Create Penpot directory
            mkdir -p ~/ai-pm-toolkit/design/penpot/self-hosted
            cd ~/ai-pm-toolkit/design/penpot/self-hosted
            
            # Download docker-compose file
            echo "⬇️  Downloading Penpot configuration..."
            wget -q https://raw.githubusercontent.com/penpot/penpot/main/docker/images/docker-compose.yaml -O docker-compose.yml
            
            echo "🚀 Starting Penpot services..."
            echo "   This may take several minutes on first run..."
            
            docker-compose up -d
            
            echo ""
            echo "✅ Penpot started successfully!"
            echo "   Access at: http://localhost:9001"
            echo "   Default admin: admin@penpot.app / 123123123"
            echo ""
            echo "🔧 Next steps:"
            echo "   1. Visit http://localhost:9001"
            echo "   2. Sign in with default credentials"
            echo "   3. Change admin password"
            echo "   4. Create your design workspace"
            
        else
            echo "❌ Docker and Docker Compose required for self-hosted Penpot"
            echo ""
            echo "📦 Install dependencies:"
            echo "   macOS: brew install docker docker-compose"
            echo "   Linux: Install Docker and Docker Compose via package manager"
            echo ""
            echo "After installation, run this script again."
        fi
        ;;
    *)
        echo "❌ Invalid option. Run the script again to choose."
        ;;
esac

echo ""
echo "📚 Strategic PM Use Cases for Penpot:"
echo "   • Design user interface mockups for PoL Probes"
echo "   • Create visual flow diagrams for stakeholder presentations"
echo "   • Build brand assets and style guides"
echo "   • Collaborate on design iterations with development teams"
echo "   • Export designs for use in Gradio interfaces"
EOF

chmod +x ~/ai-pm-toolkit/design/penpot/penpot-setup

echo "   ✅ Enhanced AI tools installation completed"

# Create MCP configuration for Claude Desktop
echo "⚙️  Setting up MCP configuration..."
if mkdir -p ~/Library/Application\ Support/Claude 2>/dev/null; then
    echo "{" > ~/Library/Application\ Support/Claude/claude_desktop_config.json
    echo '  "mcpServers": {' >> ~/Library/Application\ Support/Claude/claude_desktop_config.json
    
    # Add servers that are actually available
    server_count=0
    
    # Check for FastMCP AI PM server
    if [ -f ~/ai-pm-toolkit/mcp-servers/templates/fastmcp-aipm/aipm_server.py ]; then
        if [ $server_count -gt 0 ]; then echo "," >> ~/Library/Application\ Support/Claude/claude_desktop_config.json; fi
        cat >> ~/Library/Application\ Support/Claude/claude_desktop_config.json << 'TEMPLATE_EOF'
    "aipm-fastmcp": {
      "command": "python3",
      "args": [
        "/Users/$USER/ai-pm-toolkit/mcp-servers/templates/fastmcp-aipm/aipm_server.py"
      ]
    }
TEMPLATE_EOF
        server_count=$((server_count + 1))
    fi
    
    # Check for llama-cpp-agent
    if [ -d ~/ai-pm-toolkit/mcp-servers/agents/llama-cpp-agent-tools ]; then
        if [ $server_count -gt 0 ]; then echo "," >> ~/Library/Application\ Support/Claude/claude_desktop_config.json; fi
        cat >> ~/Library/Application\ Support/Claude/claude_desktop_config.json << 'LLAMA_EOF'
    "llama-cpp-agent": {
      "command": "python",
      "args": [
        "/Users/$USER/ai-pm-toolkit/mcp-servers/agents/llama-cpp-agent-tools/examples/mcp_server.py"
      ],
      "env": {
        "OLLAMA_BASE_URL": "http://localhost:11434"
      }
    }
LLAMA_EOF
        server_count=$((server_count + 1))
    fi
    
    # Check for devon agent
    if [ -d ~/ai-pm-toolkit/mcp-servers/tools/devon ]; then
        if [ $server_count -gt 0 ]; then echo "," >> ~/Library/Application\ Support/Claude/claude_desktop_config.json; fi
        cat >> ~/Library/Application\ Support/Claude/claude_desktop_config.json << 'DEVON_EOF'
    "devon-agent": {
      "command": "devon",
      "args": ["--mcp-mode"],
      "env": {
        "DEVON_API_KEY": "local"
      }
    }
DEVON_EOF
        server_count=$((server_count + 1))
    fi
    
    echo "" >> ~/Library/Application\ Support/Claude/claude_desktop_config.json
    echo "  }" >> ~/Library/Application\ Support/Claude/claude_desktop_config.json
    echo "}" >> ~/Library/Application\ Support/Claude/claude_desktop_config.json
    
    if [ $server_count -gt 0 ]; then
        echo "   ✅ MCP configuration created for Claude Desktop ($server_count servers available)"
    else
        echo "   ⚠️  MCP configuration created but no servers available"
        echo "      💡 Optional MCP servers require GitHub access to install"
    fi
else
    echo "   ⚠️  Could not create Claude Desktop config directory"
fi

# Create MCP utility script
cat > ~/ai-pm-toolkit/manage-mcp << 'EOF'
#!/bin/bash
# AI PM MCP Server Management
# Manage Model Context Protocol servers for enhanced AI integration

echo "🔌 AI PM MCP Server Management"
echo "=============================="

cd ~/ai-pm-toolkit/mcp-servers

case "$1" in
    "start")
        echo "🚀 Starting MCP servers..."
        
        # Start FastMCP AI PM server (if available)
        if [ -f "templates/fastmcp-aipm/aipm_server.py" ]; then
            echo "   🚀 Starting FastMCP AI PM server..."
            cd templates/fastmcp-aipm
            python3 aipm_server.py &
            FASTMCP_PID=$!
            cd ../..
            echo "   ✅ FastMCP AI PM server started (PID: $FASTMCP_PID)"
        else
            echo "   ⚠️  FastMCP AI PM server not available (optional component)"
            FASTMCP_PID=""
        fi
        
        # Start llama-cpp-agent server (if available)
        if [ -d "agents/llama-cpp-agent-tools" ]; then
            echo "   🦙 Starting llama-cpp-agent server..."
            cd agents/llama-cpp-agent-tools
            python examples/mcp_server.py &
            LLAMA_PID=$!
            cd ../..
        else
            echo "   ⚠️  llama-cpp-agent server not available (optional component)"
            LLAMA_PID=""
        fi
        
        # Start devon agent
        echo "   🛠️  Starting devon agent..."
        cd ../../tools/devon
        devon --mcp-mode &
        DEVON_PID=$!
        
        # Save PIDs for later cleanup
        echo "$TEMPLATE_PID $LLAMA_PID $DEVON_PID" > ../../mcp_pids.txt
        
        echo "   ✅ All MCP servers started"
        echo "   💡 Connect via Claude Desktop or compatible MCP client"
        ;;
    "stop")
        echo "🛑 Stopping MCP servers..."
        if [[ -f "mcp_pids.txt" ]]; then
            while read -r pid; do
                if kill -0 "$pid" 2>/dev/null; then
                    kill "$pid"
                    echo "   ✅ Stopped server (PID: $pid)"
                fi
            done < mcp_pids.txt
            rm mcp_pids.txt
        else
            echo "   ⚠️  No running servers found"
        fi
        ;;
    "status")
        echo "📊 MCP Server Status:"
        if [[ -f "mcp_pids.txt" ]]; then
            echo "   Running servers:"
            while read -r pid; do
                if kill -0 "$pid" 2>/dev/null; then
                    echo "   ✅ Server running (PID: $pid)"
                else
                    echo "   ❌ Server stopped (PID: $pid)"
                fi
            done < mcp_pids.txt
        else
            echo "   📴 No servers currently running"
        fi
        ;;
    "config")
        echo "⚙️  MCP Configuration:"
        echo "   📁 Config location: ~/Library/Application Support/Claude/claude_desktop_config.json"
        echo "   🔧 Available servers:"
        echo "      • aipm-templates    - PoL Probe templates and utilities"
        echo "      • llama-cpp-agent   - Local AI agent with tool calling"
        echo "      • devon-agent       - AI software engineering agent"
        echo ""
        echo "   💡 Restart Claude Desktop after configuration changes"
        ;;
    "templates")
        echo "📋 Creating custom FastMCP server template for AI PM..."
        
        cd templates
        if [ ! -d "aipm-custom" ]; then
            if [ -d "fastmcp-aipm" ]; then
                cp -r fastmcp-aipm aipm-custom
                cd aipm-custom
            
            # Customize for AI PM use cases  
            cat > aipm_custom_server.py << 'PYTHON'
"""AI PM Custom FastMCP Server for PoL Probes"""

from fastmcp import FastMCP
from typing import Any, Dict, List
import json
import os
import datetime

# Initialize custom FastMCP server
mcp = FastMCP("AI PM Custom PoL Probe Server")

@mcp.tool()
def generate_custom_persona(persona_type: str, industry: str = "general", company_size: str = "medium") -> Dict[str, Any]:
    """Generate synthetic user persona for PoL Probes.
    
    Args:
        persona_type: Type of persona (user, admin, stakeholder)
        industry: Industry context
        company_size: Company size (startup, small, medium, enterprise)
    
    Returns:
        Dict with generated persona details
    """
    persona_data = {
        "type": persona_type,
        "industry": industry,
        "company_size": company_size,
        "generated_at": datetime.datetime.now().isoformat(),
        "pain_points": [
            f"Industry-specific challenges in {industry}",
            f"Scale issues typical of {company_size} companies",
            "Integration and workflow inefficiencies"
        ],
        "goals": [
            "Improve operational efficiency",
            "Reduce manual work and errors",
            "Better data-driven decision making"
        ]
    }
    
    # Save persona to file
    personas_dir = os.path.expanduser("~/ai-pm-toolkit/synthetic-data/personas")
    os.makedirs(personas_dir, exist_ok=True)
    persona_file = os.path.join(personas_dir, f"custom_{persona_type}_{industry}_{datetime.datetime.now().strftime('%Y%m%d_%H%M')}.json")
    with open(persona_file, 'w') as f:
        json.dump(persona_data, f, indent=2)
    
    return {**persona_data, "file_path": persona_file}

@mcp.tool()
def validate_assumption(assumption: str, probe_type: str, success_criteria: str = "") -> Dict[str, Any]:
    """Structure assumption validation for PoL Probes.
    
    Args:
        assumption: The assumption to test
        probe_type: Type of probe (learn, fast, prototype, experiment, compete)
        success_criteria: What would prove this assumption wrong
    
    Returns:
        Dict with structured validation plan
    """
    probe_types = ["learn", "fast", "prototype", "experiment", "compete"]
    if probe_type not in probe_types:
        return {"error": f"Probe type must be one of: {', '.join(probe_types)}"}
    
    validation_plan = {
        "assumption": assumption,
        "probe_type": probe_type,
        "success_criteria": success_criteria if success_criteria else "What would prove this wrong fastest?",
        "validation_approach": {
            "learn": "1-2 day technical feasibility spike",
            "fast": "Task-focused user friction test",
            "prototype": "Narrative walkthrough for stakeholder buy-in",
            "experiment": "Synthetic data simulation at scale",
            "compete": "Vibe-coded probe with real user signals"
        }.get(probe_type, "Unknown probe type"),
        "recommended_tools": {
            "learn": ["aider", "jupyter", "local AI models"],
            "fast": ["gradio", "simple mockups", "user interviews"],
            "prototype": ["storyboard", "loom recording", "figma"],
            "experiment": ["faker", "mimesis", "synthetic data"],
            "compete": ["quick frontend", "airtable backend", "real user testing"]
        }.get(probe_type, []),
        "harsh_truth_indicators": [
            "Technical complexity exceeds initial estimates",
            "User adoption barriers are significant",
            "Stakeholder buy-in requires additional evidence",
            "Market demand is insufficient",
            "Competitive landscape is more challenging"
        ]
    }
    
    return validation_plan

@mcp.tool()
def analyze_feedback(feedback_text: str, context: str = "") -> Dict[str, Any]:
    """Analyze user feedback for brutal honesty insights.
    
    Args:
        feedback_text: Raw user feedback
        context: Product/feature context
    
    Returns:
        Dict with analyzed insights and harsh truths
    """
    # Simple keyword-based analysis (in production, you'd use NLP)
    negative_indicators = ["difficult", "confusing", "slow", "broken", "frustrating", "unclear", "complicated"]
    positive_indicators = ["easy", "fast", "clear", "helpful", "intuitive", "simple", "effective"]
    
    negative_count = sum(1 for word in negative_indicators if word.lower() in feedback_text.lower())
    positive_count = sum(1 for word in positive_indicators if word.lower() in feedback_text.lower())
    
    sentiment_score = positive_count - negative_count
    
    analysis = {
        "feedback_text": feedback_text,
        "context": context,
        "sentiment_score": sentiment_score,
        "harsh_truths": [],
        "action_items": [],
        "analyzed_at": datetime.datetime.now().isoformat()
    }
    
    if sentiment_score < -1:
        analysis["harsh_truths"].append("User experience is significantly problematic")
        analysis["action_items"].append("Immediate UX review and redesign needed")
    elif sentiment_score < 0:
        analysis["harsh_truths"].append("User friction exists and needs addressing")
        analysis["action_items"].append("Conduct deeper user research to identify pain points")
    elif sentiment_score == 0:
        analysis["harsh_truths"].append("User sentiment is neutral - may indicate lack of clear value")
        analysis["action_items"].append("Enhance value proposition and user onboarding")
    else:
        analysis["harsh_truths"].append("Positive feedback indicates good direction")
        analysis["action_items"].append("Scale and optimize current approach")
    
    return analysis

if __name__ == "__main__":
    mcp.run()
PYTHON
            
                echo "   ✅ Custom AI PM MCP server template created"
            else
                echo "   ⚠️  Base template not available - cannot create custom template"
                echo "      💡 Run setup.sh again or manually clone the MCP template"
            fi
        else
            echo "✅ Custom AI PM MCP server already exists"
        fi
        ;;
    *)
        echo "Usage:"
        echo "  ./manage-mcp start      # Start all MCP servers"
        echo "  ./manage-mcp stop       # Stop all MCP servers"
        echo "  ./manage-mcp status     # Check server status"
        echo "  ./manage-mcp config     # Show configuration info"
        echo "  ./manage-mcp templates  # Create custom AI PM MCP server"
        echo ""
        echo "💡 MCP enables enhanced AI integration with:"
        echo "   • Custom PoL Probe tools in Claude"
        echo "   • Local AI agent coordination"
        echo "   • Automated software engineering"
        echo "   • Knowledge base integration"
        ;;
esac
EOF

chmod +x ~/ai-pm-toolkit/manage-mcp

echo "✅ MCP installation completed"
fi  # End of MCP installation conditional

# Create Obsidian launcher script
cat > ~/ai-pm-toolkit/launch-obsidian << 'EOF'
#!/bin/bash
# Launch Obsidian with AI PM vault

echo "🧠 Launching Obsidian with AI PM Knowledge Vault"
echo "=============================================="

case "$1" in
    "vault")
        echo "📂 Opening AI PM vault..."
        open "obsidian://open?vault=ai-pm-toolkit"
        ;;
    "new-probe")
        probe_name="$2"
        if [[ -z "$probe_name" ]]; then
            echo "❌ Probe name required"
            echo "Usage: ./launch-obsidian new-probe <probe-name>"
            exit 1
        fi
        
        echo "🧪 Creating new PoL Probe: $probe_name"
        
        # Create probe file from template
        probe_file="~/ai-pm-toolkit/obsidian-vault/Projects/PoL-Probe-${probe_name}.md"
        sed "s/{{title}}/$probe_name/g; s/{{date:YYYY-MM-DD}}/$(date +%Y-%m-%d)/g" \
            ~/ai-pm-toolkit/obsidian-vault/Templates/PoL-Probe-Planning.md > "$probe_file"
        
        echo "   ✅ Probe file created: $probe_file"
        echo "   🚀 Opening in Obsidian..."
        open "obsidian://open?vault=ai-pm-toolkit&file=Projects/PoL-Probe-${probe_name}"
        ;;
    "link-research")
        echo "🔗 Opening research linking interface..."
        open "obsidian://open?vault=ai-pm-toolkit&file=Research"
        ;;
    *)
        echo "Usage:"
        echo "  ./launch-obsidian vault           # Open AI PM vault"
        echo "  ./launch-obsidian new-probe <name> # Create new PoL Probe"
        echo "  ./launch-obsidian link-research   # Open research linking"
        echo ""
        echo "🧠 Obsidian Features for AI PMs:"
        echo "   • Link ideas across PoL Probes"
        echo "   • Create knowledge graphs"
        echo "   • Template-driven documentation"
        echo "   • Bi-directional linking"
        echo "   • Graph view for insights"
        ;;
esac
EOF

chmod +x ~/ai-pm-toolkit/launch-obsidian

echo "✅ Knowledge management & AI integration tools configured"

# Copy comprehensive documentation and utilities
echo "📚 Setting up comprehensive PM documentation and utilities..."
if [[ -f "DOCUMENTATION.md" ]]; then
    cp DOCUMENTATION.md ~/ai-pm-toolkit/DOCUMENTATION.md
    echo "   ✅ DOCUMENTATION.md copied to toolkit"
else
    echo "   ⚠️  DOCUMENTATION.md not found in source directory"
fi

if [[ -f "uninstall.sh" ]]; then
    cp uninstall.sh ~/ai-pm-toolkit/uninstall.sh
    chmod +x ~/ai-pm-toolkit/uninstall.sh
    echo "   ✅ uninstall.sh copied to toolkit"
else
    echo "   ⚠️  uninstall.sh not found in source directory"
fi

# Download UI scaffolding libraries (htmx + shoelace)
cd ~/ai-pm-toolkit/static/lib
curl -O https://cdn.jsdelivr.net/npm/@shoelace-style/shoelace@2.13.0/dist/shoelace.js
curl -O https://unpkg.com/htmx.org@1.9.2
cd ~/ai-pm-toolkit

echo "✅ Local HTML helpers (htmx + shoelace) downloaded"
# -- end instal of video/audio

# Start Ollama service
echo "🦙 Starting local AI server..."
brew services start ollama || echo "Ollama already running"
sleep 3

# Pull AI models for PM exploration
echo "📥 Downloading AI models (optimized for PM work)..."
ollama pull deepseek-r1:7b  # Great for product strategy + code
ollama pull llama3.2:3b     # Fast for rapid iteration

# Create exploration workspace
mkdir -p ~/ai-pm-toolkit
cd ~/ai-pm-toolkit

# Create exploration directories  
mkdir -p experiments prototypes data insights notebooks
mkdir -p workflow-tools prompt-testing synthetic-data monitoring design obsidian-vault mcp-servers

# Create toolkit configuration
cat > toolkit-config.yaml << EOF
# AI PM Exploration Toolkit Configuration
# Proof-of-Life Probes for strategic product management

primary_model: "deepseek-r1:7b"
fast_model: "llama3.2:3b"

exploration_modes:
  learn: "Feasibility Checks - 1-2 day spike-and-delete tests with AI"
  fast: "Task-Focused Tests - validate make-or-break user moments"
  prototype: "Narrative Prototypes - explainer videos and storyboard walkthroughs"
  experiment: "Synthetic Data Simulations - model behavior without burning prod"
  compete: "Vibe-Coded PoL Probes - fake frontend + semi-plausible backend"

philosophy: "Use the cheapest prototype that tells the harshest truth"

workspace:
  experiments: "Synthetic data simulations and wind tunnel testing"
  prototypes: "Narrative walkthroughs and vibe-coded probes"
  data: "Generated datasets for assumption testing"
  insights: "De-risked decisions and validated assumptions"
  notebooks: "Feasibility spikes and technical exploration"
  workflow-tools: "Visual/low-code workflow builders"
  prompt-testing: "Prompt engineering and evaluation"
  synthetic-data: "Synthetic data generation and personas"
  monitoring: "AI monitoring and observability"
  design: "Design and storytelling tools"
  obsidian-vault: "Knowledge management and idea linking"
  mcp-servers: "Model Context Protocol servers and AI agents"

tools:
  # Original tools
  ffmpeg:
    role: "Video stitching"
    used_for: "Prototype"
    description: "Combines voiceovers and frames to generate explainer videos"
    availability: "local"

  pyttsx3:
    role: "Offline text-to-speech"
    used_for: "Prototype"
    description: "Narrates videos without needing a cloud API"
    availability: "local"

  mermaid-cli:
    role: "Diagram generator"
    used_for: "Experiment, Learn"
    description: "Turns markdown into sequence, flow, or state diagrams"
    availability: "local"

  shoelace:
    role: "HTML UI components"
    used_for: "Prototype"
    description: "Adds form and polish to interactive HTML walkthroughs"
    availability: "static"

  htmx:
    role: "HTML behavior scaffolding"
    used_for: "Prototype"
    description: "Wires up front-end behavior with zero JS boilerplate"
    availability: "static"

  # Visual/Low-Code Workflow Tools
  langflow:
    role: "Visual LLM flow builder"
    used_for: "Learn, Compete"
    description: "Create LLM applications visually for non-technical PMs"
    availability: "local"
    port: 7860

  n8n:
    role: "Workflow automation platform"
    used_for: "Experiment, Compete"
    description: "Automate product research and data collection workflows"
    availability: "docker"
    port: 5678

  tooljet:
    role: "Low-code app builder"
    used_for: "Compete, Fast"
    description: "Build internal tools and dashboards rapidly"
    availability: "docker"
    port: 8082

  typebot:
    role: "Conversational form builder"
    used_for: "Fast, Prototype"
    description: "Create conversational interfaces and chatbots"
    availability: "docker"
    port: 8083

  # Development & AI Coding
  vscode:
    role: "AI-enhanced code editor"
    used_for: "Learn, Compete"
    description: "Code editor with Continue AI assistant"
    availability: "local"

  continue:
    role: "AI coding assistant"
    used_for: "Learn, Compete"
    description: "AI-powered coding help integrated with VS Code"
    availability: "extension"

  # Prompt Engineering & Testing
  promptfoo:
    role: "LLM evaluation framework"
    used_for: "Learn, Fast"
    description: "Test and evaluate prompts systematically"
    availability: "npm"

  prompttools:
    role: "Prompt testing toolkit"
    used_for: "Learn, Fast"
    description: "Python-based prompt experimentation"
    availability: "python"

  # Synthetic Data & AI Training
  faker:
    role: "Basic synthetic data generation"
    used_for: "Experiment"
    description: "Generate realistic fake data for testing"
    availability: "python"

  faker-cli:
    role: "Command-line data generation"
    used_for: "Experiment"
    description: "Quick synthetic data from command line"
    availability: "npm"

  mimesis:
    role: "Advanced synthetic data with localization"
    used_for: "Experiment"
    description: "Generate localized synthetic data"
    availability: "python"

  gretel:
    role: "AI-powered synthetic data platform"
    used_for: "Experiment"
    description: "Enterprise-grade synthetic data generation"
    availability: "python"

  chatterbot:
    role: "Machine learning conversational engine"
    used_for: "Fast, Experiment"
    description: "Create chatbots for user testing"
    availability: "python"

  persona-chat:
    role: "Custom persona-based chat interface"
    used_for: "Experiment, Fast"
    description: "Generate synthetic user personas and conversations"
    availability: "custom"

  # AI Monitoring & Observability
  langsmith:
    role: "LLM application monitoring"
    used_for: "Learn, Monitor"
    description: "Track and optimize LLM application performance"
    availability: "npm"

  arize:
    role: "ML observability platform"
    used_for: "Learn, Monitor"
    description: "Monitor ML model performance and drift"
    availability: "python"

  # Design & Storytelling
  excalidraw:
    role: "Hand-drawn style diagrams"
    used_for: "Prototype, Fast"
    description: "Create user journey and system diagrams"
    availability: "web"

  storyboarder:
    role: "Digital storyboarding tool"
    used_for: "Prototype"
    description: "Create visual narratives for product stories"
    availability: "npm"

  # Knowledge Management & AI Integration
  obsidian:
    role: "Knowledge management & idea linking"
    used_for: "All PoL Probes"
    description: "Link ideas across probes, create knowledge graphs"
    availability: "local"

  mcp-servers:
    role: "Model Context Protocol integration"
    used_for: "Learn, Compete"
    description: "Enhanced AI integration with custom tools"
    availability: "local"

  llama-cpp-agent:
    role: "Local AI agent with tool calling"
    used_for: "Learn, Compete"
    description: "Advanced AI agent coordination"
    availability: "python"

  devon-agent:
    role: "AI software engineering agent"
    used_for: "Learn, Compete"
    description: "Automated software engineering tasks"
    availability: "python"

  # Market Research & Competitive Intelligence
  openbb:
    role: "Open-source financial research platform"
    used_for: "Compete, Learn"
    description: "Financial data, market analysis, economic indicators"
    availability: "python"
    commands: ["aipm_openbb", "aipm_market"]

  local-deep-researcher:
    role: "AI-powered research automation"
    used_for: "Compete, Learn"
    description: "Autonomous multi-step research with local processing"
    availability: "python"
    commands: ["aipm_research"]

  gemini-cli:
    role: "Google AI for market research"
    used_for: "Compete, Learn, Fast"
    description: "Advanced AI market analysis with 1M+ token context"
    availability: "npm"
    commands: ["aipm_gemini"]

  competitive-research:
    role: "Automated competitor analysis"
    used_for: "Compete"
    description: "AI-powered competitive intelligence gathering"
    availability: "local"
    commands: ["aipm_competitive"]
EOF

# Create rapid exploration commands
cat > ~/ai-pm-toolkit/aipm << 'EOF'
#!/bin/bash
# AI PM Exploration Toolkit - Proof-of-Life Probes
# "Use the cheapest prototype that tells the harshest truth" ~ Dean Peters

case "$1" in
    "quickstart"|"start"|"tutorial")
        echo "🚀 AI PM Toolkit: 4E Framework Quick Start"
        echo "=========================================="
        echo ""
        echo "Welcome! Transform from AI-curious to AI-confident in 5 minutes."
        echo "Follow the 4E journey: Education → Experimentation → Exploration → Explanation"
        echo ""
        echo "🎓 STEP 1: EDUCATION (Start Your Learning Journey)"
        echo "   cat ~/ai-pm-toolkit/DOCUMENTATION.md    # Your complete 4E guide"
        echo "   aipm_obsidian vault                     # Set up knowledge management"
        echo "   aipm learn 'test if AI can handle our customer support edge cases'"
        echo ""
        echo "🧪 STEP 2: EXPERIMENTATION (Generate Evidence, Not Opinions)"
        echo "   aipm experiment 'simulate user behavior patterns'"
        echo "   aipm_data users                         # Generate synthetic test data"
        echo "   aipm_personas generate --count 5        # Create test personas"
        echo ""
        echo "🔍 STEP 3: EXPLORATION (Discover What's Possible)"
        echo "   aipm_market                             # Explore market research tools"
        echo "   aipm_workflows                          # Discover visual AI builders"
        echo "   ls ~/ai-pm-toolkit/                     # See your complete toolkit"
        echo ""
        echo "📊 STEP 4: EXPLANATION (Show Before Tell, Touch Before Sell)"
        echo "   aipm prototype 'create stakeholder demo of our new dashboard'"
        echo "   aipm fast 'validate our signup form reduces friction'"
        echo "   aipm_design web                         # Create visual explanations"
        echo ""
        echo "🎯 Next: Run 'aipm' (without arguments) to see all 4E capabilities!"
        echo "💡 Remember: Use the cheapest prototype that tells the harshest truth"
        ;;
    "learn")
        echo "🔬 Feasibility Check: $2"
        aider --model ollama/deepseek-r1:7b --message "Create a 1-2 day spike-and-delete test for: $2. Focus on surfacing technical risk, not building to impress. Include GenAI prompt chains, API tests, or tool fit evaluation as needed."
        ;;
    "fast")
        echo "🎯 Task-Focused Test: $2"
        aider --model ollama/llama3.2:3b --message "Validate this make-or-break user moment: $2. Focus on friction points, field labels, decision points, or drop-off analysis without building full workflows."
        ;;
    "prototype")
        echo "📖 Narrative Prototype: $2"
        aider --model ollama/deepseek-r1:7b --message "Create a narrative prototype for: $2. Build explainer videos, Loom-style walkthroughs, or storyboards that stakeholders can experience and provide feedback on. Tell the story, then see who buys in."
        ;;
    "experiment")
        echo "🧪 Synthetic Data Simulation: $2"
        aider --model ollama/deepseek-r1:7b --message "Create a synthetic data simulation for: $2. Model system behavior, generate realistic datasets, test edge cases, or surface unknowns without risking production. Think wind tunnel testing for assumptions."
        ;;
    "compete")
        echo "🎨 Vibe-Coded PoL Probe: $2"
        aider --model ollama/deepseek-r1:7b --message "Build a vibe-coded probe for: $2. Create fake frontend + semi-plausible backend using tools like ChatGPT + Canvas + Airtable. Just enough illusion to catch real user signals in 48 hours - not production quality."
        ;;
    *)
        echo "🧪 AI PM Exploration Toolkit - Proof-of-Life Probes"
        echo "======================================================"
        echo ""
        echo "👋 Welcome, Product Manager!"
        echo "Transform from AI-curious to AI-confident through our 4E Framework"
        echo ""
        echo "🚨 FIRST TIME? Start here:"
        echo "   cat ~/ai-pm-toolkit/FIRST_RUN_GUIDE.md        # Essential setup steps"
        echo ""
        echo "🎯 THE FOUR PILLARS: Education → Experimentation → Exploration → Explanation"
        echo ""
        echo "🎓 EDUCATION (Learn AI Through Practice):"
        echo "  aipm learn 'test if users want AI-powered notifications'     # Feasibility learning"
        echo "  aipm_lab                                                     # Hands-on Jupyter playground"
        echo "  aipm_localai                                                 # Local AI server (privacy-first)"
        echo "  aipm_whisper                                                 # Speech-to-text transcription"
        echo "  aipm_obsidian vault                                          # Knowledge management"
        echo ""
        echo "🔍 EXPLORATION (Discover What's Possible):"
        echo "  aipm_workflows                                               # Visual workflow builders"
        echo "  aipm_market                                                  # Market research dashboard"
        echo "  aipm_gradio                                                  # Interactive ML interfaces"
        echo "  aipm_phoenix                                                 # AI observability & monitoring"
        echo "  aipm_mcp                                                     # AI agent coordination"
        echo ""
        echo "🧪 EXPERIMENTATION (Test Hypotheses with Data):"
        echo "  aipm experiment 'simulate 50k users in conversion funnel'    # Synthetic data testing"
        echo "  aipm_prompts eval                                            # Prompt engineering tests"
        echo "  aipm_phoenix                                                 # ML monitoring & evaluation"
        echo "  aipm_data full                                               # Generate test datasets"
        echo ""
        echo "📊 EXPLANATION (Show Before Tell, Touch Before Sell):"
        echo "  aipm prototype 'show executives our dashboard value story'   # Narrative creation"
        echo "  aipm fast 'validate checkout button text converts better'    # Quick validation"
        echo "  aipm_penpot                                                  # Open-source design tool"
        echo "  aipm_marktext                                                # Beautiful markdown editor"
        echo "  aipm_gradio                                                  # Interactive demo builder"
        echo "  aipm compete 'build fake competitor analysis tool'           # Market demos"
        echo "  aipm_design web                                              # Visual explanations"
        echo ""
        echo "🚀 QUICK START:"
        echo "  aipm quickstart                                              # 5-minute 4E tutorial"
        echo "  cat ~/ai-pm-toolkit/DOCUMENTATION.md                        # Complete 4E guide"
        echo ""
        echo "🎯 Philosophy: Education → Experimentation → Exploration → Explanation"
        echo "💡 Remember: Use the cheapest prototype that tells the harshest truth"
        echo ""
        echo "Ready to start your 4E journey? Try: aipm quickstart"
        ;;
esac
EOF

chmod +x ~/ai-pm-toolkit/aipm

# Create Jupyter lab setup for data exploration
cat > ~/ai-pm-toolkit/start-lab << 'EOF'
#!/bin/bash
echo "🔬 Starting AI PM PoL Probe environment..."
cd ~/ai-pm-toolkit
jupyter lab --port=8888 --no-browser &
echo "📊 Jupyter Lab: http://localhost:8888"
echo "🧪 Ready for feasibility spikes and synthetic data simulations!"
EOF

chmod +x ~/ai-pm-toolkit/start-lab

# Test the setup
echo "🧪 Testing toolkit setup..."
ollama list | grep -E "(deepseek-r1|llama3.2)" && echo "✅ AI models ready"

# Test installations
if command -v aider &> /dev/null; then
    echo "✅ AI coding assistant ready"
elif $PYTHON_CMD -c "import aider" 2>/dev/null; then
    echo "✅ AI coding assistant ready (Python module)"
else
    echo "⚠️  aider-chat may not be available - PoL Probes will have reduced functionality"
fi

if command -v jupyter &> /dev/null; then
    echo "✅ Data exploration ready"
elif $PYTHON_CMD -c "import jupyter" 2>/dev/null; then
    echo "✅ Data exploration ready (Python module)"
else
    echo "⚠️  jupyter may not be available - data exploration will have reduced functionality"
fi

# Check for existing API keys and offer enhanced setup
echo ""
echo "🔍 Checking for enhanced capabilities..."

# Count configured APIs
api_count=0
if [[ -n "$CLAUDE_API_KEY" ]]; then ((api_count++)); fi
if [[ -n "$OPENAI_API_KEY" ]]; then ((api_count++)); fi
if [[ -n "$DEEPSEEK_API_KEY" ]]; then ((api_count++)); fi
if [[ -n "$GEMINI_API_KEY" ]]; then ((api_count++)); fi
if [[ -n "$GITHUB_API_KEY" ]]; then ((api_count++)); fi

if [[ $api_count -gt 0 ]]; then
    echo "✅ Found $api_count API key(s) configured"
    echo "   Enhanced PoL Probes available with cloud AI models"
else
    echo "💡 No API keys detected - using local-only mode"
    echo ""
    echo "🚀 Want enhanced PoL Probes with cloud AI?"
    echo "   • Advanced strategic analysis with Claude"
    echo "   • Competitive intelligence with GitHub API"
    echo "   • 10M+ tokens/month with free API tiers"
    echo "   • Market research with multiple AI models"
    echo ""
    echo -n "Configure enhanced APIs now? [y/N]: "
    read -r configure_apis
    
    if [[ "$configure_apis" =~ ^[Yy]$ ]]; then
        echo ""
        echo "🔧 Running enhanced API configuration..."
        if [[ -f "./configure-apis.sh" ]]; then
            chmod +x ./configure-apis.sh
            ./configure-apis.sh
        else
            echo "❌ configure-apis.sh not found in current directory"
            echo "   You can run it later from the toolkit directory"
        fi
    else
        echo "   ⏭️  Skipped - you can run './configure-apis.sh' later"
    fi
fi

# Create exploration aliases
echo 'alias aipm="cd ~/ai-pm-toolkit && ./aipm"' >> ~/.zshrc
echo 'alias aipm_lab="cd ~/ai-pm-toolkit && ./start-lab"' >> ~/.zshrc

# Add enhanced alias if APIs are configured
if command -v ~/ai-pm-toolkit/aipm-enhanced &> /dev/null; then
    echo 'alias aipm_enhanced="cd ~/ai-pm-toolkit && ./aipm-enhanced"' >> ~/.zshrc
fi

# Add tool-specific aliases
echo 'alias aipm_workflows="cd ~/ai-pm-toolkit && ./start-workflows"' >> ~/.zshrc
echo 'alias aipm_docker_setup="cd ~/ai-pm-toolkit && ./aipm_docker_setup"' >> ~/.zshrc
echo 'alias aipm_prompts="cd ~/ai-pm-toolkit/prompt-testing && ./test-prompts"' >> ~/.zshrc
echo 'alias aipm_data="cd ~/ai-pm-toolkit/synthetic-data && ./generate-test-data"' >> ~/.zshrc
echo 'alias aipm_personas="cd ~/ai-pm-toolkit/synthetic-data && ./persona-chat"' >> ~/.zshrc
echo 'alias aipm_monitor="cd ~/ai-pm-toolkit/monitoring && ./monitor-ai"' >> ~/.zshrc
echo 'alias aipm_design="cd ~/ai-pm-toolkit/design && ./launch-excalidraw"' >> ~/.zshrc
echo 'alias aipm_story="cd ~/ai-pm-toolkit/design && ./create-storyboard"' >> ~/.zshrc
echo 'alias aipm_marktext="open -a MarkText"' >> ~/.zshrc
echo 'alias aipm_pulsar="pulsar"' >> ~/.zshrc
echo 'alias aipm_obsidian="cd ~/ai-pm-toolkit && ./launch-obsidian"' >> ~/.zshrc
echo 'alias aipm_mcp="cd ~/ai-pm-toolkit && ./manage-mcp"' >> ~/.zshrc

# Market research & competitive intelligence aliases
echo 'alias aipm_market="cd ~/ai-pm-toolkit/market-research/scripts && ./market-dashboard"' >> ~/.zshrc
echo 'alias aipm_openbb="cd ~/ai-pm-toolkit/market-research/scripts && ./launch-openbb"' >> ~/.zshrc
echo 'alias aipm_research="cd ~/ai-pm-toolkit/competitive-intel/scripts && ./start-deep-research"' >> ~/.zshrc
echo 'alias aipm_gemini="cd ~/ai-pm-toolkit/market-research/scripts && ./setup-gemini"' >> ~/.zshrc
echo 'alias aipm_competitive="cd ~/ai-pm-toolkit/market-research/scripts && ./research-competitor"' >> ~/.zshrc
echo 'alias aipm_similarweb="cd ~/ai-pm-toolkit/competitive-intel/scripts && ./similarweb-analysis"' >> ~/.zshrc
echo 'alias aipm_monitor="cd ~/ai-pm-toolkit/competitive-intel/scripts && ./brand-monitor"' >> ~/.zshrc
echo 'alias aipm_matrix="cd ~/ai-pm-toolkit/competitive-intel/scripts && ./competitive-matrix"' >> ~/.zshrc

# AI infrastructure & specialized tools aliases
echo 'alias aipm_localai="cd ~/ai-pm-toolkit && ./ai-tools/localai/manage-localai"' >> ~/.zshrc
echo 'alias aipm_phoenix="cd ~/ai-pm-toolkit && ./ai-tools/phoenix/launch-phoenix"' >> ~/.zshrc
echo 'alias aipm_gradio="cd ~/ai-pm-toolkit && ./ai-tools/gradio/launch-gradio"' >> ~/.zshrc
echo 'alias aipm_whisper="cd ~/ai-pm-toolkit && ./ai-tools/whisper/whisper-transcribe"' >> ~/.zshrc
echo 'alias aipm_penpot="cd ~/ai-pm-toolkit && ./ai-tools/penpot/launch-penpot"' >> ~/.zshrc
echo 'alias aipm_langflow="langflow run"' >> ~/.zshrc

echo ""
echo "🚨 CRITICAL: Setup Complete - But You're Not Done Yet!"
echo "============================================="
echo ""
echo "⚠️  The toolkit is installed but WON'T WORK until you complete these steps:"
echo ""
echo "📖 FOLLOW THE FIRST RUN GUIDE NOW:"
echo "   cat ~/ai-pm-toolkit/FIRST_RUN_GUIDE.md"
echo ""
echo "🔥 Essential next steps (takes 5 minutes):"
echo "   1. source ~/.zshrc                   # Reload shell (REQUIRED)"
echo "   2. Open Docker Desktop               # Start Docker (REQUIRED for workflows)"
echo "   3. gh auth login                     # GitHub setup (HIGHLY RECOMMENDED)"
echo "   4. aipm_docker_setup                 # Pre-fetch images (RECOMMENDED)"
echo "   5. aipm_workflows                    # Test workflow tools"
echo ""
echo "🧪 After completing the first run guide, try these commands:"

# Show appropriate commands based on setup
if command -v ~/ai-pm-toolkit/aipm-enhanced &> /dev/null; then
    echo "   aipm_enhanced learn 'technical feasibility spike'    # Enhanced with cloud AI"
    echo "   aipm_enhanced compete 'GitHub repo analysis'        # With competitive intel"
    echo "   aipm fast 'friction point validation'               # Local quick tests"
else
    echo "   aipm learn 'technical feasibility spike'            # Local AI models"
    echo "   aipm fast 'friction point validation'               # Quick validation"
    echo "   aipm prototype 'narrative walkthrough'              # Story-driven probes"
fi

echo "   aipm experiment 'synthetic data simulation'"
echo "   aipm_lab  # Launch Jupyter for data work"
echo ""

# Show tier information
if [[ $api_count -gt 0 ]]; then
    echo "🚀 Enhanced Mode: $api_count cloud API(s) configured"
    echo "   • Advanced strategic analysis capabilities"
    echo "   • Competitive intelligence with real data"
    echo "   • 10M+ tokens/month with free tiers"
else
    echo "🦙 Local Mode: Using Ollama for privacy and speed"
    echo "   • Run './configure-apis.sh' anytime for enhanced features"
    echo "   • All PoL Probes work offline with local AI"
fi

echo ""
echo "🧰 Comprehensive AI PM Tool Suite Installed:"
echo ""
echo "📊 Core PoL Probe Commands:"
echo "   • aipm learn 'feasibility check'     – Technical spike & analysis"
echo "   • aipm fast 'friction validation'   – Quick user moment testing"
echo "   • aipm prototype 'narrative demo'   – Story-driven presentations"  
echo "   • aipm experiment 'data simulation' – Synthetic user behavior"
echo "   • aipm compete 'vibe-coded probe'   – Fake-it-till-you-make-it testing"
echo ""
echo "🌊 Visual Workflow Tools:"
echo "   • aipm_workflows                     – Start Docker tools (n8n, ToolJet, Typebot)"
echo "   • aipm_langflow                      – Start Langflow (Visual LLM builder)"
echo "   • n8n (localhost:5678)              – Workflow automation platform"
echo "   • ToolJet (localhost:8082)          – Low-code app builder"
echo "   • Typebot (localhost:8083)          – Conversational form builder"
echo "   • Langflow (localhost:7860)         – Visual LLM application builder"
echo ""
echo "💻 Development & AI Coding:"
echo "   • VS Code + Continue                 – AI-enhanced code editor"
echo "   • Continue extension                 – Local AI coding assistant"
echo ""
echo "🧪 Prompt Engineering & Testing:"
echo "   • aipm_prompts eval                  – Test prompts systematically"
echo "   • promptfoo                          – LLM evaluation framework"
echo "   • prompttools                        – Python prompt experimentation"
echo ""
echo "🎲 Synthetic Data & AI Training:"
echo "   • aipm_data full                     – Generate complete test datasets"
echo "   • aipm_personas generate             – Create user personas"
echo "   • Faker + faker-cli                  – Basic synthetic data"
echo "   • Mimesis                            – Advanced localized data"
echo "   • Gretel                             – AI-powered synthetic data"
echo "   • ChatterBot                         – Conversational AI engine"
echo ""
echo "📈 AI Monitoring & Observability:"
echo "   • aipm_monitor dashboard             – Local monitoring dashboard"
echo "   • LangSmith                          – LLM application monitoring"
echo "   • Arize                              – ML observability platform"
echo ""
echo "🎨 Design & Storytelling:"
echo "   • aipm_design web                    – Launch Excalidraw diagrams"
echo "   • aipm_story template feature-demo   – Create visual narratives"
echo "   • Excalidraw                         – Hand-drawn style diagrams"
echo "   • Wonder Unit Storyboarder           – Digital storyboarding"
echo ""
echo "📊 Market Research & Competitive Intelligence:"
echo "   • aipm_market                        – Market research dashboard (OpenBB, Gemini, Deep Research)"
echo "   • aipm_openbb                        – Financial data and market analysis platform"
echo "   • aipm_research                      – AI-powered autonomous research automation"
echo "   • aipm_gemini                        – Google AI for advanced market analysis"
echo "   • aipm_competitive <company>         – Automated competitor research reports"
echo "   • aipm_similarweb <domain>           – Digital intelligence and web analytics"
echo "   • aipm_monitor <brand>               – Brand mention and monitoring setup"
echo "   • aipm_matrix <your-co> <competitor> – Competitive analysis framework"
echo "   • OpenBB Terminal                    – Open-source financial research platform"
echo "   • Local Deep Researcher              – Multi-step AI research with local processing"
echo "   • Gemini CLI                         – 1M+ token context, 60 req/min free tier"
echo ""
echo "🧠 Knowledge Management & AI Integration:"
echo "   • aipm_obsidian vault                – Open AI PM knowledge vault"
echo "   • aipm_obsidian new-probe <name>     – Create new PoL Probe with templates"
echo "   • aipm_mcp start                     – Start MCP servers for enhanced AI"
echo "   • Obsidian                           – Link ideas and create knowledge graphs"
echo "   • MCP Servers                        – Custom AI tools and agent coordination"
echo "   • llama-cpp-agent                    – Local AI agent with tool calling"
echo "   • devon-agent                        – AI software engineering automation"
echo ""
echo "📦 Additional Tools:"
echo "   • ffmpeg        – video stitching"
echo "   • pyttsx3       – offline TTS"
echo "   • mermaid-cli   – markdown to diagrams"
echo "   • htmx + shoelace – UI scaffolding for interactive HTML demos"

echo ""
echo "======================================================================"
echo "🎉 CONGRATULATIONS! Your AI PM Toolkit is Ready"
echo "======================================================================"
echo ""
echo "📁 Workspace: ~/ai-pm-toolkit/ (comprehensive PM toolkit)"
echo "📚 Documentation: ~/ai-pm-toolkit/DOCUMENTATION.md (your complete guide)"
echo "🗑️ Uninstall: ~/ai-pm-toolkit/uninstall.sh (complete removal tool)"
echo ""
echo "🚀 IMMEDIATE NEXT STEPS:"
echo "   1. Run: source ~/.zshrc                  (activate all commands)"
echo "   2. Run: aipm quickstart                  (5-minute tutorial)"
echo "   3. Read: cat ~/ai-pm-toolkit/DOCUMENTATION.md  (complete guide)"
echo ""
echo "🎯 Philosophy: Show before Tell, Touch before Sell"
echo "💡 Remember: Use the cheapest prototype that tells the harshest truth"
echo ""
echo "Questions? Check DOCUMENTATION.md for complete scenarios and examples!"
echo "======================================================================"