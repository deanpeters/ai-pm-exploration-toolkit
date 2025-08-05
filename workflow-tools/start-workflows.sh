#!/bin/bash
# AI PM Toolkit - Workflow Tools Startup Script
# Starts Docker containers and waits for them to be ready

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMEOUT=120  # 2 minutes timeout for each service

echo -e "${BLUE}🚀 AI PM Toolkit - Starting Workflow Tools${NC}"
echo "========================================"

# Function to check if a port is responding
wait_for_port() {
    local port=$1
    local service_name=$2
    local timeout=$3
    local count=0
    
    echo -e "${YELLOW}⏳ Waiting for ${service_name} on port ${port}...${NC}"
    
    while ! curl -f -s http://localhost:${port} >/dev/null 2>&1; do
        if [ $count -ge $timeout ]; then
            echo -e "${RED}❌ ${service_name} failed to start within ${timeout} seconds${NC}"
            return 1
        fi
        sleep 1
        count=$((count + 1))
        if [ $((count % 10)) -eq 0 ]; then
            echo -e "${YELLOW}   Still waiting... (${count}s elapsed)${NC}"
        fi
    done
    
    echo -e "${GREEN}✅ ${service_name} is ready at http://localhost:${port}${NC}"
    return 0
}

# Function to start a service
start_service() {
    local compose_file=$1
    local service_name=$2
    local port=$3
    local health_path=${4:-""}
    
    echo -e "${BLUE}🔄 Starting ${service_name}...${NC}"
    
    cd "$SCRIPT_DIR"
    
    # Check if already running
    if curl -f -s http://localhost:${port}${health_path} >/dev/null 2>&1; then
        echo -e "${GREEN}✅ ${service_name} is already running${NC}"
        return 0
    fi
    
    # Start the service
    docker-compose -f "$compose_file" up -d
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}❌ Failed to start ${service_name}${NC}"
        return 1
    fi
    
    # Wait for service to be ready
    wait_for_port "$port" "$service_name" "$TIMEOUT"
}

# Function to create network if it doesn't exist
ensure_network() {
    if ! docker network ls | grep -q aipm_workflow_network; then
        echo -e "${YELLOW}🔗 Creating Docker network...${NC}"
        docker network create aipm_workflow_network
    fi
}

# Function to check Docker is running
check_docker() {
    if ! docker info >/dev/null 2>&1; then
        echo -e "${RED}❌ Docker is not running. Please start Docker and try again.${NC}"
        exit 1
    fi
}

# Function to handle port conflicts
handle_port_conflict() {
    local port=$1
    local service_name=$2
    
    echo -e "${YELLOW}⚠️  Port ${port} conflict detected for ${service_name}${NC}"
    echo "Options:"
    echo "1. Kill process using port ${port}: sudo lsof -ti:${port} | xargs kill"
    echo "2. Use different port by editing docker-compose files"
    echo "3. Stop conflicting Docker containers: docker ps"
    
    read -p "Kill process on port ${port}? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}🔫 Killing process on port ${port}...${NC}"
        sudo lsof -ti:${port} | xargs kill 2>/dev/null || echo "No process found or permission denied"
        sleep 2
        return 0
    fi
    return 1
}

# Main execution
main() {
    check_docker
    ensure_network
    
    # Track which services started successfully
    declare -a started_services=()
    declare -a failed_services=()
    
    echo -e "${BLUE}🎯 Starting essential workflow tools...${NC}"
    echo
    
    # Start n8n (Tier 1 - Essential)
    if start_service "docker-compose.n8n.yml" "n8n" "5678" || handle_port_conflict "5678" "n8n" && start_service "docker-compose.n8n.yml" "n8n" "5678"; then
        started_services+=("n8n (http://localhost:5678)")
    else
        failed_services+=("n8n")
    fi
    
    # Start ToolJet (Tier 2 - Advanced) 
    echo
    if start_service "docker-compose.tooljet.yml" "ToolJet" "8082" || handle_port_conflict "8082" "ToolJet" && start_service "docker-compose.tooljet.yml" "ToolJet" "8082"; then
        started_services+=("ToolJet (http://localhost:8082)")
    else
        failed_services+=("ToolJet")
    fi
    
    # Check if Langflow should be started (if installed)
    if docker images | grep -q langflow; then
        echo
        echo -e "${BLUE}🔄 Starting Langflow...${NC}"
        if docker run -d --name aipm-langflow -p 7860:7860 langflow/langflow:latest >/dev/null 2>&1; then
            if wait_for_port "7860" "Langflow" "$TIMEOUT"; then
                started_services+=("Langflow (http://localhost:7860)")
            else
                failed_services+=("Langflow")
            fi
        else
            echo -e "${YELLOW}ℹ️  Langflow not available or port conflict${NC}"
        fi
    fi
    
    # Summary
    echo
    echo -e "${BLUE}📊 Startup Summary${NC}"
    echo "=================="
    
    if [ ${#started_services[@]} -gt 0 ]; then
        echo -e "${GREEN}✅ Successfully started:${NC}"
        for service in "${started_services[@]}"; do
            echo "   • $service"
        done
    fi
    
    if [ ${#failed_services[@]} -gt 0 ]; then
        echo -e "${RED}❌ Failed to start:${NC}"
        for service in "${failed_services[@]}"; do
            echo "   • $service"
        done
    fi
    
    echo
    echo -e "${BLUE}🎉 Workflow tools startup complete!${NC}"
    echo
    echo -e "${YELLOW}💡 Quick tips:${NC}"
    echo "   • Run 'aipm_workflows_status' to check service health"
    echo "   • Run 'aipm_workflows_stop' to stop all services"
    echo "   • Run 'aipm_workflows_restart' to restart failed services"
    echo "   • Check logs: docker-compose -f [compose-file] logs"
}

# Run main function
main "$@"