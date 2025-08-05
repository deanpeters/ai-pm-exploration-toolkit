#!/bin/bash
# AI PM Toolkit - Workflow Tools Stop Script

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo -e "${BLUE}🛑 AI PM Toolkit - Stopping Workflow Tools${NC}"
echo "========================================"

cd "$SCRIPT_DIR"

# Stop all Docker Compose services
echo -e "${YELLOW}🔄 Stopping Docker Compose services...${NC}"
docker-compose -f docker-compose.n8n.yml down 2>/dev/null || echo "n8n not running"
docker-compose -f docker-compose.tooljet.yml down 2>/dev/null || echo "ToolJet not running"
docker-compose -f docker-compose.typebot.yml down 2>/dev/null || echo "Typebot not running"
docker-compose -f docker-compose.penpot.yml down 2>/dev/null || echo "Penpot not running"

# Stop Langflow container if running
echo -e "${YELLOW}🔄 Stopping Langflow container...${NC}"
docker stop aipm-langflow 2>/dev/null && docker rm aipm-langflow 2>/dev/null || echo "Langflow not running"

echo -e "${GREEN}✅ All workflow tools stopped${NC}"
echo
echo -e "${YELLOW}💡 To completely reset (remove data):${NC}"
echo "   aipm_workflows_reset"