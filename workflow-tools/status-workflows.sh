#!/bin/bash
# AI PM Toolkit - Workflow Tools Status Script
# Wrapper for the comprehensive orchestration script

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Call the comprehensive orchestration script
exec "$SCRIPT_DIR/orchestrate-workflows.sh" status