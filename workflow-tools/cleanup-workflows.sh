#!/bin/bash
# AI PM Toolkit - Nuclear Docker Cleanup Script
# Wrapper for the comprehensive orchestration script with user confirmation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${RED}☢️ AI PM Toolkit - Nuclear Docker Cleanup${NC}"
echo "========================================"
echo -e "${YELLOW}⚠️  This will stop and remove ALL AIPM workflow containers, networks, and volumes${NC}"
echo

read -p "Continue with nuclear cleanup? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cleanup cancelled"
    exit 0
fi

# Call the comprehensive orchestration script
exec "$SCRIPT_DIR/orchestrate-workflows.sh" cleanup