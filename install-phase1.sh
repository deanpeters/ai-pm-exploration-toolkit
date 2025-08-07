#!/bin/bash
# AI PM Toolkit - Phase 1 Installer
# Simple, reliable setup with symlink and basic commands

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
TOOLKIT_NAME="AI PM Exploration Toolkit"
REPO_DIR="$HOME/ai-pm-exploration-toolkit"
SYMLINK_DIR="$HOME/aipm-toolkit"
PYTHON_MIN_VERSION="3.8"

# Logging functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

log_header() {
    echo -e "${CYAN}${1}${NC}"
}

# Check if we're in the right directory
check_installation_directory() {
    log_info "Checking installation directory..."
    
    if [[ ! -f "toolkit.json" || ! -d "web" || ! -d "cli" ]]; then
        log_error "This doesn't appear to be the AI PM Toolkit directory"
        log_error "Please run this script from the ai-pm-exploration-toolkit directory"
        log_error "Expected files: toolkit.json, web/, cli/"
        exit 1
    fi
    
    CURRENT_DIR=$(pwd)
    log_success "Installation directory confirmed: $CURRENT_DIR"
}

# Check Python version
check_python() {
    log_info "Checking Python installation..."
    
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed"
        log_error "Please install Python 3.8 or later and try again"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    log_success "Python $PYTHON_VERSION found"
    
    # Basic version check (not perfect but good enough)
    if python3 -c "import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)"; then
        log_success "Python version is compatible"
    else
        log_error "Python $PYTHON_VERSION is too old (requires 3.8+)"
        exit 1
    fi
}

# Install Python dependencies
install_dependencies() {
    log_info "Installing Python dependencies..."
    
    # Check if pip is available
    if ! command -v pip3 &> /dev/null; then
        log_error "pip3 is not available"
        log_error "Please install pip and try again"
        exit 1
    fi
    
    # Install required packages
    log_info "Installing Flask for web dashboard..."
    pip3 install --user flask 2>/dev/null || {
        log_warning "Failed to install Flask with --user, trying without..."
        pip3 install flask || {
            log_error "Failed to install Flask"
            exit 1
        }
    }
    
    log_info "Installing Rich for CLI dashboard..."
    pip3 install --user rich 2>/dev/null || {
        log_warning "Failed to install Rich with --user, trying without..."
        pip3 install rich || {
            log_error "Failed to install Rich"
            exit 1
        }
    }
    
    log_success "Python dependencies installed"
}

# Create convenience symlink
create_symlink() {
    log_info "Creating convenience symlink..."
    
    # Remove existing symlink if it exists
    if [[ -L "$SYMLINK_DIR" ]]; then
        log_info "Removing existing symlink..."
        rm "$SYMLINK_DIR"
    elif [[ -d "$SYMLINK_DIR" || -f "$SYMLINK_DIR" ]]; then
        log_error "File/directory already exists at $SYMLINK_DIR"
        log_error "Please remove it manually and try again"
        exit 1
    fi
    
    # Create symlink
    ln -sf "$CURRENT_DIR" "$SYMLINK_DIR"
    
    if [[ -L "$SYMLINK_DIR" ]]; then
        log_success "Symlink created: $SYMLINK_DIR -> $CURRENT_DIR"
    else
        log_error "Failed to create symlink"
        exit 1
    fi
}

# Create command scripts
create_commands() {
    log_info "Creating aipm commands..."
    
    # Create local bin directory
    LOCAL_BIN="$HOME/.local/bin"
    mkdir -p "$LOCAL_BIN"
    
    # Create aipm hub command
    cat > "$LOCAL_BIN/aipm" << 'EOF'
#!/bin/bash
# AI PM Toolkit - Main command dispatcher

TOOLKIT_DIR="$HOME/aipm-toolkit"

if [[ ! -d "$TOOLKIT_DIR" ]]; then
    echo "❌ AI PM Toolkit not found at $TOOLKIT_DIR"
    echo "Please run the installer first"
    exit 1
fi

case "${1:-help}" in
    "hub"|"web")
        echo "🌐 Starting AI PM Toolkit Web Dashboard..."
        cd "$TOOLKIT_DIR/web" && python3 app.py
        ;;
    "dashboard"|"cli")
        echo "💻 Starting AI PM Toolkit CLI Dashboard..."
        cd "$TOOLKIT_DIR" && python3 cli/dashboard.py
        ;;
    "status")
        echo "📊 AI PM Toolkit Status:"
        echo "  Version: $(cat "$TOOLKIT_DIR/toolkit.json" | grep version | cut -d'"' -f4)"
        echo "  Location: $TOOLKIT_DIR"
        echo "  Web: http://localhost:3000 (run 'aipm hub' to start)"
        echo "  CLI: run 'aipm dashboard' to start"
        ;;
    "help"|*)
        echo "🧪 AI PM Toolkit - Proof-of-Life Probes for Product Managers"
        echo ""
        echo "Commands:"
        echo "  aipm hub       - Start web dashboard (http://localhost:3000)"
        echo "  aipm dashboard - Start CLI dashboard"
        echo "  aipm status    - Show system status"
        echo "  aipm help      - Show this help"
        echo ""
        echo "Phase 1 Status: Foundation complete ✅"
        echo "Next: Individual tool implementations (Phase 2)"
        ;;
esac
EOF
    
    # Make command executable
    chmod +x "$LOCAL_BIN/aipm"
    
    log_success "Command created: aipm"
    
    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
        log_warning "~/.local/bin is not in your PATH"
        log_info "Add this line to your ~/.bashrc or ~/.zshrc:"
        echo -e "${CYAN}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
        log_info "Or run: echo 'export PATH=\"\$HOME/.local/bin:\$PATH\"' >> ~/.$(basename $SHELL)rc"
    fi
}

# Test installation
test_installation() {
    log_info "Testing installation..."
    
    # Test symlink
    if [[ -L "$SYMLINK_DIR" && -d "$SYMLINK_DIR" ]]; then
        log_success "Symlink working: $SYMLINK_DIR"
    else
        log_error "Symlink test failed"
        return 1
    fi
    
    # Test Python imports
    if python3 -c "import flask, rich" 2>/dev/null; then
        log_success "Python dependencies working"
    else
        log_error "Python dependencies test failed"
        return 1
    fi
    
    # Test configuration file
    if python3 -c "import json; json.load(open('$CURRENT_DIR/toolkit.json'))" 2>/dev/null; then
        log_success "Configuration file valid"
    else
        log_error "Configuration file test failed"
        return 1
    fi
    
    # Test command
    if [[ -x "$HOME/.local/bin/aipm" ]]; then
        log_success "Command script created and executable"
    else
        log_error "Command script test failed"
        return 1
    fi
    
    log_success "All tests passed!"
}

# Show completion message
show_completion() {
    log_header ""
    log_header "🎉 Phase 1 Installation Complete!"
    log_header "=================================="
    
    echo ""
    log_success "✅ Core configuration system"
    log_success "✅ Web dashboard interface"
    log_success "✅ CLI dashboard interface"
    log_success "✅ Command-line tools"
    log_success "✅ Convenience symlink"
    
    echo ""
    log_header "Quick Start:"
    echo -e "${CYAN}  aipm hub       ${NC}# Start web dashboard at http://localhost:3000"
    echo -e "${CYAN}  aipm dashboard ${NC}# Start CLI dashboard with menu"
    echo -e "${CYAN}  aipm status    ${NC}# Check system status"
    
    echo ""
    log_header "What's Next:"
    echo "• Phase 2: Individual tool implementations"
    echo "• Phase 3: Tool integration & polish"
    echo "• Phase 4: Community preparation"
    
    echo ""
    log_info "If ~/.local/bin is not in your PATH, restart your terminal or run:"
    echo -e "${CYAN}  source ~/.$(basename $SHELL)rc${NC}"
    
    echo ""
    log_success "Ready to explore AI tools for Product Management!"
}

# Main installation flow
main() {
    log_header ""
    log_header "🧪 AI PM Toolkit - Phase 1 Installer"
    log_header "====================================="
    log_header ""
    
    check_installation_directory
    check_python
    install_dependencies
    create_symlink
    create_commands
    test_installation
    show_completion
}

# Run main function
main "$@"