#!/bin/bash
# AI PM Toolkit - Workflow Tools Fix Script
# Handles common issues and provides troubleshooting

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔧 AI PM Toolkit - Workflow Tools Troubleshooter${NC}"
echo "=============================================="

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

# Interactive menu
show_menu() {
    echo
    echo -e "${BLUE}🛠  What would you like to fix?${NC}"
    echo "1. Kill port conflicts"
    echo "2. Clean Docker resources"
    echo "3. Check Docker health"
    echo "4. Recreate Docker network"
    echo "5. Check system resources"
    echo "6. Full nuclear reset (all of the above)"
    echo "7. Exit"
    echo
    read -p "Choose option (1-7): " choice
    
    case $choice in
        1) kill_port_conflicts ;;
        2) clean_docker ;;
        3) check_docker ;;
        4) fix_network ;;
        5) check_resources ;;
        6) 
            echo -e "${RED}☢️  FULL NUCLEAR RESET${NC}"
            read -p "This will stop all containers and clean everything. Continue? (y/N): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                kill_port_conflicts
                clean_docker
                fix_network
                check_docker
                echo -e "${GREEN}✅ Nuclear reset complete${NC}"
            fi
            ;;
        7) echo "Exiting..."; exit 0 ;;
        *) echo "Invalid option"; show_menu ;;
    esac
}

# Main execution
main() {
    check_docker
    show_menu
    
    echo
    echo -e "${BLUE}🚀 Ready to try starting workflows again?${NC}"
    read -p "Start workflow tools now? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ./start-workflows.sh
    fi
}

main "$@"