#!/bin/bash
# AI PM Toolkit - Master Network Management
# Single source of truth for Docker network operations

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

NETWORK_NAME="aipm_workflow_network"

# Function to check if network exists
network_exists() {
    docker network ls --format "{{.Name}}" | grep -q "^${NETWORK_NAME}$"
}

# Function to create network
create_network() {
    if network_exists; then
        echo -e "${GREEN}✅ Network ${NETWORK_NAME} already exists${NC}"
        return 0
    fi
    
    echo -e "${YELLOW}🔗 Creating Docker network: ${NETWORK_NAME}${NC}"
    
    if docker network create \
        --driver bridge \
        --label "ai-pm-toolkit.network=main" \
        --label "ai-pm-toolkit.description=Main workflow network" \
        "${NETWORK_NAME}"; then
        echo -e "${GREEN}✅ Network ${NETWORK_NAME} created successfully${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to create network ${NETWORK_NAME}${NC}"
        return 1
    fi
}

# Function to remove network
remove_network() {
    if ! network_exists; then
        echo -e "${YELLOW}⚠️  Network ${NETWORK_NAME} does not exist${NC}"
        return 0
    fi
    
    echo -e "${YELLOW}🗑️  Removing Docker network: ${NETWORK_NAME}${NC}"
    
    # First disconnect any connected containers
    local connected_containers
    connected_containers=$(docker network inspect "${NETWORK_NAME}" --format '{{range .Containers}}{{.Name}} {{end}}' 2>/dev/null || echo "")
    
    if [ -n "$connected_containers" ]; then
        echo -e "${YELLOW}⚠️  Disconnecting containers: ${connected_containers}${NC}"
        for container in $connected_containers; do
            docker network disconnect "${NETWORK_NAME}" "$container" 2>/dev/null || true
        done
    fi
    
    if docker network rm "${NETWORK_NAME}"; then
        echo -e "${GREEN}✅ Network ${NETWORK_NAME} removed successfully${NC}"
        return 0
    else
        echo -e "${RED}❌ Failed to remove network ${NETWORK_NAME}${NC}"
        return 1
    fi
}

# Function to inspect network
inspect_network() {
    if ! network_exists; then
        echo -e "${RED}❌ Network ${NETWORK_NAME} does not exist${NC}"
        return 1
    fi
    
    echo -e "${BLUE}🔍 Network Information:${NC}"
    docker network inspect "${NETWORK_NAME}" --format '
Network: {{.Name}}
Driver: {{.Driver}}
Scope: {{.Scope}}
Created: {{.Created}}
Labels: {{range $key, $value := .Labels}}
  {{$key}}: {{$value}}{{end}}
Connected Containers:{{range .Containers}}
  - {{.Name}} ({{.IPv4Address}}){{end}}'
}

# Function to ensure network is ready
ensure_network() {
    if ! network_exists; then
        create_network
    else
        echo -e "${GREEN}✅ Network ${NETWORK_NAME} is ready${NC}"
    fi
}

# Main command handler
case "${1:-help}" in
    create)
        create_network
        ;;
    remove|rm)
        remove_network
        ;;
    inspect|info)
        inspect_network
        ;;
    ensure)
        ensure_network
        ;;
    exists)
        if network_exists; then
            echo -e "${GREEN}✅ Network exists${NC}"
            exit 0
        else
            echo -e "${RED}❌ Network does not exist${NC}"
            exit 1
        fi
        ;;
    help|*)
        echo -e "${BLUE}AI PM Toolkit - Network Management${NC}"
        echo "Usage: $0 {create|remove|inspect|ensure|exists|help}"
        echo ""
        echo "Commands:"
        echo "  create   - Create the workflow network"
        echo "  remove   - Remove the workflow network"
        echo "  inspect  - Show network information"
        echo "  ensure   - Create network if it doesn't exist"
        echo "  exists   - Check if network exists (exit code)"
        echo "  help     - Show this help message"
        ;;
esac