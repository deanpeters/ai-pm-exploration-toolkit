#!/bin/bash
# AI PM Toolkit - Workflow Tools Fix Script
# Interactive troubleshooting and repair interface

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 AI PM Toolkit - Workflow Tools Fix${NC}"
echo "========================================"

cd "$SCRIPT_DIR"

# Function to kill processes on common ports
kill_port_conflicts() {
    echo -e "${YELLOW}🔫 Checking for port conflicts...${NC}"
    
    for port in 5678 7860 8082 3001 8888; do
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            echo -e "${YELLOW}⚠️  Port $port is in use${NC}"
            read -p "Kill process on port $port? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                sudo lsof -ti:$port | xargs kill 2>/dev/null || echo "Failed to kill process"
                echo -e "${GREEN}✅ Cleared port $port${NC}"
            fi
        fi
    done
}

# Function to clean Docker resources
clean_docker() {
    echo -e "${YELLOW}🧹 Cleaning Docker resources...${NC}"
    
    # Stop any running workflow containers
    docker stop $(docker ps -q --filter "label=ai-pm-toolkit.service") 2>/dev/null || echo "No toolkit containers running"
    
    # Remove stopped containers
    docker container prune -f
    
    # Clean up unused networks
    docker network prune -f
    
    # Clean up unused volumes (optional)
    read -p "Remove unused Docker volumes? This will delete data (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        docker volume prune -f
        echo -e "${GREEN}✅ Docker volumes cleaned${NC}"
    fi
    
    echo -e "${GREEN}✅ Docker cleanup complete${NC}"
}

# Function to check Docker health
check_docker() {
    echo -e "${YELLOW}🏥 Checking Docker health...${NC}"
    
    if ! docker info >/dev/null 2>&1; then
        echo -e "${RED}❌ Docker is not running${NC}"
        echo "Please start Docker Desktop and try again"
        return 1
    fi
    
    # Check Docker resources
    echo "Docker version: $(docker --version)"
    echo "Available disk space:"
    df -h $(docker info --format '{{.DockerRootDir}}') 2>/dev/null || echo "Could not check Docker disk usage"
    
    echo -e "${GREEN}✅ Docker is healthy${NC}"
}

# Function to recreate network
fix_network() {
    echo -e "${YELLOW}🔗 Fixing Docker network...${NC}"
    
    # Remove existing network
    docker network rm aipm_workflow_network 2>/dev/null || echo "Network doesn't exist"
    
    # Create new network
    docker network create aipm_workflow_network
    
    echo -e "${GREEN}✅ Docker network recreated${NC}"
}

# Function to check system resources
check_resources() {
    echo -e "${YELLOW}💻 Checking system resources...${NC}"
    
    # Check available RAM
    if command -v free >/dev/null 2>&1; then
        free -h
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "Memory usage:"
        vm_stat | head -10
    fi
    
    # Check disk space
    echo "Disk usage:"
    df -h . | tail -1
    
    # Check CPU load
    if command -v uptime >/dev/null 2>&1; then
        uptime
    fi
}

# Comprehensive auto-fix function
auto_fix() {
    echo -e "${BLUE}🔧 Running comprehensive auto-fix...${NC}"
    
    check_docker || return 1
    
    # Kill port conflicts automatically
    echo -e "${YELLOW}🔫 Checking for port conflicts...${NC}"
    for port in 5678 7860 8082 8083 8084 8085; do
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            echo -e "${YELLOW}⚠️  Port $port is in use - killing process${NC}"
            lsof -ti:$port | xargs kill 2>/dev/null || true
            sleep 1
        fi
    done
    
    # Stop existing containers
    echo -e "${YELLOW}🛑 Stopping existing workflow containers...${NC}"
    "$SCRIPT_DIR/orchestrate-workflows.sh" stop >/dev/null 2>&1 || true
    
    # Clean Docker resources
    echo -e "${YELLOW}🧹 Cleaning Docker resources...${NC}"
    docker container prune -f >/dev/null 2>&1 || true
    docker network prune -f >/dev/null 2>&1 || true
    
    # Recreate network
    echo -e "${YELLOW}🔗 Recreating network...${NC}"
    "$SCRIPT_DIR/manage-network.sh" remove >/dev/null 2>&1 || true
    "$SCRIPT_DIR/manage-network.sh" create || return 1
    
    echo -e "${GREEN}✅ Auto-fix complete${NC}"
    return 0
}

# Interactive menu
show_menu() {
    echo
    echo -e "${BLUE}🛠  What would you like to fix?${NC}"
    echo "1. 🚀 Auto-fix everything (recommended)"
    echo "2. Kill port conflicts"
    echo "3. Clean Docker resources"
    echo "4. Check Docker health"
    echo "5. Recreate Docker network"
    echo "6. Check system resources"
    echo "7. ☢️  Nuclear cleanup (remove all data)"
    echo "8. Exit"
    echo
    read -p "Choose option (1-8): " choice
    
    case $choice in
        1) 
            auto_fix
            if [ $? -eq 0 ]; then
                echo
                echo -e "${BLUE}🚀 Ready to start workflows?${NC}"
                read -p "Start workflow tools now? (y/N): " -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    "$SCRIPT_DIR/orchestrate-workflows.sh" start
                fi
            fi
            ;;
        2) kill_port_conflicts ;;
        3) clean_docker ;;
        4) check_docker ;;
        5) fix_network ;;
        6) check_resources ;;
        7) 
            echo -e "${RED}☢️  NUCLEAR CLEANUP${NC}"
            echo "This will remove all containers, networks, and volumes"
            read -p "Continue? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                "$SCRIPT_DIR/orchestrate-workflows.sh" cleanup
            fi
            ;;
        8) echo "Exiting..."; exit 0 ;;
        *) echo "Invalid option"; show_menu ;;
    esac
}

# Main execution
main() {
    local mode="${1:-interactive}"
    
    case "$mode" in
        auto|--auto)
            auto_fix
            ;;
        interactive|*)
            check_docker
            show_menu
            ;;
    esac
}

main "$@"