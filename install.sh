#!/bin/bash
# AI PM Toolkit Installer for macOS/Linux
# Cross-platform entry point for the production installer

set -e  # Exit on any error

TIER_ARG="1" # Default to Tier 1

# Parse tier argument
case "$1" in
  essentials) TIER_ARG="1" ;;
  advanced) TIER_ARG="2" ;;
  full) TIER_ARG="3" ;;
  "") ;;
  *) echo "Invalid tier. Use 'essentials', 'advanced', or 'full'." >&2; exit 1 ;;
esac

echo "🚀 Launching AI PM Toolkit Installer for Tier ${TIER_ARG}..."

# Check for Python 3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found."
    echo "Please install Python 3 first:"
    
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "  brew install python@3.11"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "  sudo apt update && sudo apt install python3 python3-pip"
    fi
    
    exit 1
fi

# Check for PyYAML
if ! python3 -c "import yaml" 2>/dev/null; then
    echo "📦 Installing required Python dependencies..."
    python3 -m pip install --user PyYAML
fi

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Filter out the tier argument and pass remaining args
shift 2>/dev/null || true  # Remove the tier argument if present

# Run the installer
python3 "${SCRIPT_DIR}/installer.py" --tier "$TIER_ARG" "$@"