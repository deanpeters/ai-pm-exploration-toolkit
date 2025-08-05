#!/bin/bash
# AI PM Toolkit - Workflow Tools Status Check

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}📊 AI PM Toolkit - Workflow Tools Status${NC}"
echo "========================================"

# Function to check service status
check_service() {
    local name=$1
    local port=$2
    local url="http://localhost:${port}"
    
    if curl -f -s "$url" >/dev/null 2>&1; then
        echo -e "${GREEN}✅ ${name} - Running${NC} (${url})"
    else
        echo -e "${RED}❌ ${name} - Not responding${NC} (${url})"
    fi
}

# Check each service
check_service "n8n" "5678"
check_service "Langflow" "7860"  
check_service "ToolJet" "8082"
check_service "Typebot Builder" "3001"
check_service "Jupyter Lab" "8888"

echo
echo -e "${BLUE}🐳 Docker Container Status:${NC}"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep -E "(aipm|n8n|tooljet|typebot|langflow|jupyter)"

echo
echo -e "${YELLOW}💡 Quick actions:${NC}"
echo "   • Start all: aipm_workflows"
echo "   • Stop all: aipm_workflows_stop" 
echo "   • Restart: aipm_workflows_restart"
echo "   • Fix issues: aipm_workflows_fix"