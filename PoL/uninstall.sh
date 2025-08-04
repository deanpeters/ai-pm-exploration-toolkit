#!/bin/bash
# AI PM Exploration Toolkit - Uninstall Script
# Complete removal of all toolkit components
# MIT License

set -e  # Exit on any error

echo "🗑️  AI PM Exploration Toolkit - Uninstall"
echo "========================================"
echo ""
echo "⚠️  WARNING: This will remove:"
echo "   • All toolkit files and directories (~3GB)"
echo "   • All generated data, personas, and PoL Probes"
echo "   • Shell aliases (but not the applications themselves)"
echo "   • MCP configurations for Claude Desktop"
echo "   • All synthetic data and notebooks"
echo ""
echo "🔒 This will NOT remove:"
echo "   • Homebrew or Node.js"
echo "   • Installed applications (Obsidian, VS Code, Docker, etc.)"
echo "   • Python packages (use pip uninstall manually if desired)"
echo "   • npm packages (use npm uninstall -g manually if desired)"
echo ""

# Confirmation prompt
echo -n "Are you sure you want to completely uninstall the AI PM Toolkit? [y/N]: "
read -r confirm_uninstall
if [[ ! "$confirm_uninstall" =~ ^[Yy]$ ]]; then
    echo "   ⏭️  Uninstall cancelled"
    echo "💡 No changes were made to your system"
    exit 0
fi

echo ""
echo "🗑️  Starting uninstall process..."

# Stop any running services first
echo "🛑 Stopping running services..."

# Stop Docker containers
if command -v docker &> /dev/null; then
    echo "   🐳 Stopping Docker containers..."
    docker stop aipm-n8n aipm-tooljet aipm-typebot aipm-typebot-viewer aipm-typebot-db 2>/dev/null || true
    docker rm aipm-n8n aipm-tooljet aipm-typebot aipm-typebot-viewer aipm-typebot-db 2>/dev/null || true
    echo "   ✅ Docker containers stopped and removed"
fi

# Stop MCP servers
if [[ -f ~/ai-pm-toolkit/mcp_pids.txt ]]; then
    echo "   🔌 Stopping MCP servers..."
    while read -r pid; do
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid" 2>/dev/null || true
        fi
    done < ~/ai-pm-toolkit/mcp_pids.txt
    echo "   ✅ MCP servers stopped"
fi

# Kill any Jupyter processes
echo "   📊 Stopping Jupyter Lab processes..."
pkill -f "jupyter.*lab" 2>/dev/null || true
echo "   ✅ Jupyter processes stopped"

# Remove main toolkit directory
echo ""
echo "📁 Removing toolkit files..."
if [[ -d ~/ai-pm-toolkit ]]; then
    echo "   🗑️  Removing ~/ai-pm-toolkit/ (including all PoL Probes and data)"
    rm -rf ~/ai-pm-toolkit
    echo "   ✅ Toolkit directory removed"
else
    echo "   ℹ️  Toolkit directory not found"
fi

# Remove API configuration
echo ""
echo "🔐 Removing API configurations..."
if [[ -f ~/.aipm-apis ]]; then
    echo "   🗑️  Removing ~/.aipm-apis (API keys)"
    rm -f ~/.aipm-apis
    echo "   ✅ API configuration removed"
else
    echo "   ℹ️  API configuration not found"
fi

# Remove Claude Desktop MCP configuration
echo ""
echo "🔌 Removing MCP configurations..."
if [[ -f ~/Library/Application\ Support/Claude/claude_desktop_config.json ]]; then
    echo "   🗑️  Removing Claude Desktop MCP configuration"
    rm -f ~/Library/Application\ Support/Claude/claude_desktop_config.json
    echo "   ✅ MCP configuration removed"
else
    echo "   ℹ️  MCP configuration not found"
fi

# Remove Continue AI configuration
echo ""
echo "🤖 Removing AI coding configurations..."
if [[ -d ~/.continue ]]; then
    echo "   🗑️  Removing Continue AI configuration"
    rm -rf ~/.continue
    echo "   ✅ Continue AI configuration removed"
else
    echo "   ℹ️  Continue AI configuration not found"
fi

# Remove shell aliases
echo ""
echo "🐚 Removing shell aliases..."

# Create backup of shell files
backup_dir="/tmp/aipm-uninstall-backup-$(date +%Y%m%d_%H%M%S)"
mkdir -p "$backup_dir"

for shell_file in ~/.zshrc ~/.bashrc ~/.bash_profile; do
    if [[ -f "$shell_file" ]]; then
        echo "   📄 Processing $shell_file..."
        
        # Create backup
        cp "$shell_file" "$backup_dir/"
        
        # Remove AI PM Toolkit sections
        # Remove the aliases and environment variables
        sed -i '' '/# AI PM Toolkit/,/^$/d' "$shell_file" 2>/dev/null || true
        sed -i '' '/alias aipm/d' "$shell_file" 2>/dev/null || true
        sed -i '' '/OLLAMA_API_BASE/d' "$shell_file" 2>/dev/null || true
        sed -i '' '/source.*aipm-apis/d' "$shell_file" 2>/dev/null || true
        
        # Remove empty lines that might be left behind
        sed -i '' '/^[[:space:]]*$/N;/^\n$/d' "$shell_file" 2>/dev/null || true
        
        echo "   ✅ Cleaned $shell_file"
    fi
done

echo "   📦 Shell file backups saved to: $backup_dir"

# Optional: Remove installed packages
echo ""
echo "📦 Optional package removal..."
echo "   The following were installed but can be removed manually if desired:"
echo ""
echo "   Python packages:"
echo "   pip uninstall aider-chat jupyter pandas plotly pyttsx3 prompttools"
echo "   pip uninstall Faker mimesis chatterbot gretel-client arize"
echo "   pip uninstall llama-cpp-python llama-cpp-agent devon-agent"
echo ""
echo "   npm packages:"
echo "   npm uninstall -g @mermaid-js/mermaid-cli promptfoo faker-cli"
echo "   npm uninstall -g langsmith storyboarder"
echo ""
echo "   Homebrew applications (if you want to remove them):"
echo "   brew uninstall ollama python@3.11 node ffmpeg"
echo "   brew uninstall --cask obsidian visual-studio-code docker"
echo ""

# Check for any remaining traces
echo "🔍 Checking for remaining traces..."
remaining_items=()

if [[ -d ~/ai-pm-toolkit ]]; then
    remaining_items+=("~/ai-pm-toolkit directory")
fi

if [[ -f ~/.aipm-apis ]]; then
    remaining_items+=("~/.aipm-apis file")
fi

if grep -q "aipm" ~/.zshrc 2>/dev/null; then
    remaining_items+=("aipm aliases in ~/.zshrc")
fi

if grep -q "aipm" ~/.bashrc 2>/dev/null; then
    remaining_items+=("aipm aliases in ~/.bashrc")
fi

if [[ ${#remaining_items[@]} -gt 0 ]]; then
    echo "   ⚠️  Some items may still remain:"
    for item in "${remaining_items[@]}"; do
        echo "      • $item"
    done
    echo "   💡 Check shell file backups in: $backup_dir"
else
    echo "   ✅ No remaining traces found"
fi

echo ""
echo "======================================================================"
echo "✅ AI PM Exploration Toolkit Uninstall Complete"
echo "======================================================================"
echo ""
echo "📊 What was removed:"
echo "   • ~/ai-pm-toolkit/ directory and all contents"
echo "   • ~/.aipm-apis API configuration"
echo "   • Claude Desktop MCP configuration"
echo "   • Continue AI configuration"
echo "   • All shell aliases (aipm, aipm_*, etc.)"
echo "   • All running services (Docker containers, MCP servers)"
echo ""
echo "📦 Shell file backups: $backup_dir"
echo ""
echo "🔄 Final steps:"
echo "   1. Restart terminal or run: source ~/.zshrc"
echo "   2. Optionally remove packages listed above"
echo "   3. Remove applications via Homebrew if no longer needed"
echo ""
echo "💡 If you reinstall later, your previous API keys are gone"
echo "   (You'll need to run ./configure-apis.sh again)"
echo ""
echo "Thank you for trying the AI PM Exploration Toolkit!"
echo "======================================================================"