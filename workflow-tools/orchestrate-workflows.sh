#!/bin/bash
# AI PM Toolkit - Single Workflow Orchestration Script
# Non-interactive, robust orchestration of all workflow tools

set -eo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TIMEOUT=120
MAX_RETRIES=3
NETWORK_NAME="aipm_workflow_network"

# Service definitions (service_name:compose_file:port:health_path)
SERVICES=(
    "n8n:docker-compose.n8n.yml:5678:/"
    "tooljet:docker-compose.tooljet.yml:8082:/"
    "typebot:docker-compose.typebot.yml:8083:/"
    "penpot:docker-compose.penpot.yml:8085:/"
)

# Service tiers
TIER1_SERVICES=("n8n")                    # Essential - always started
TIER2_SERVICES=("tooljet")                # Advanced - on-demand
TIER3_SERVICES=("typebot" "penpot")       # Optional - on-demand

# Logging function
log() {
    local level="$1"
    shift
    local message="$*"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    case "$level" in
        INFO)  echo -e "${BLUE}[${timestamp}] INFO:${NC} $message" ;;
        WARN)  echo -e "${YELLOW}[${timestamp}] WARN:${NC} $message" ;;
        ERROR) echo -e "${RED}[${timestamp}] ERROR:${NC} $message" ;;
        SUCCESS) echo -e "${GREEN}[${timestamp}] SUCCESS:${NC} $message" ;;
        *) echo -e "[${timestamp}] $level: $message" ;;
    esac
}

# Check if Docker is running
check_docker() {
    log INFO "Checking Docker availability..."
    
    if ! command -v docker >/dev/null 2>&1; then
        log ERROR "Docker is not installed"
        return 1
    fi
    
    if ! docker info >/dev/null 2>&1; then
        log ERROR "Docker daemon is not running"
        return 1
    fi
    
    log SUCCESS "Docker is available and running"
    return 0
}

# Handle port conflicts automatically
handle_port_conflict() {
    local port="$1"
    local service_name="$2"
    
    log WARN "Port $port conflict detected for $service_name"
    
    # Get process using the port
    local pid
    if pid=$(lsof -ti:$port 2>/dev/null); then
        local process_name=$(ps -p $pid -o comm= 2>/dev/null || echo "unknown")
        log WARN "Port $port is used by process $pid ($process_name)"
        
        # Only kill if it's not a Docker container we care about
        if ! docker ps --format "{{.Names}}" | grep -q "aipm-"; then
            log INFO "Killing conflicting process $pid on port $port"
            kill $pid 2>/dev/null || true
            sleep 2
            return 0
        else
            log INFO "Port used by AIPM container - will handle during cleanup"
            return 0
        fi
    fi
    
    return 1
}

# Wait for service health check
wait_for_service_health() {
    local service_name="$1"
    local container_name="aipm-$service_name"
    local max_wait="$2"
    local count=0
    
    log INFO "Waiting for $service_name health check (max ${max_wait}s)..."
    
    while [ $count -lt $max_wait ]; do
        # Check if container is healthy
        local health_status
        health_status=$(docker inspect "$container_name" --format='{{.State.Health.Status}}' 2>/dev/null || echo "no-health-check")
        
        case "$health_status" in
            "healthy")
                log SUCCESS "$service_name is healthy"
                return 0
                ;;
            "unhealthy")
                log ERROR "$service_name is unhealthy"
                return 1
                ;;
            "starting")
                if [ $((count % 10)) -eq 0 ]; then
                    log INFO "$service_name is starting... (${count}s elapsed)"
                fi
                ;;
            "no-health-check")
                # Fallback to container running check
                if docker ps --format "{{.Names}}" | grep -q "^${container_name}$"; then
                    log SUCCESS "$service_name is running (no health check available)"
                    return 0
                fi
                ;;
        esac
        
        sleep 1
        count=$((count + 1))
    done
    
    log ERROR "$service_name failed to become healthy within ${max_wait}s"
    return 1
}

# Wait for HTTP endpoint
wait_for_http() {
    local port="$1"
    local path="$2"
    local service_name="$3"
    local max_wait="$4"
    local count=0
    
    log INFO "Waiting for $service_name HTTP endpoint on port $port (max ${max_wait}s)..."
    
    while [ $count -lt $max_wait ]; do
        if curl -sf "http://localhost:${port}${path}" >/dev/null 2>&1; then
            log SUCCESS "$service_name is responding at http://localhost:$port"
            return 0
        fi
        
        if [ $((count % 10)) -eq 0 ] && [ $count -gt 0 ]; then
            log INFO "Still waiting for $service_name... (${count}s elapsed)"
        fi
        
        sleep 1
        count=$((count + 1))
    done
    
    log ERROR "$service_name failed to respond within ${max_wait}s"
    return 1
}

# Cleanup existing containers
cleanup_existing() {
    log INFO "Cleaning up existing AIPM containers..."
    
    # Stop and remove containers
    local containers
    containers=$(docker ps -a --format "{{.Names}}" | grep "^aipm-" || true)
    
    if [ -n "$containers" ]; then
        echo "$containers" | while read -r container; do
            log INFO "Stopping and removing container: $container"
            docker stop "$container" >/dev/null 2>&1 || true
            docker rm "$container" >/dev/null 2>&1 || true
        done
        log SUCCESS "Existing containers cleaned up"
    else
        log INFO "No existing AIPM containers found"
    fi
}

# Setup network
setup_network() {
    log INFO "Setting up Docker network..."
    "$SCRIPT_DIR/manage-network.sh" ensure
}

# Get service info by name
get_service_info() {
    local search_name="$1"
    for service_line in "${SERVICES[@]}"; do
        IFS=':' read -r name compose_file port health_path <<< "$service_line"
        if [ "$name" = "$search_name" ]; then
            echo "$compose_file:$port:$health_path"
            return 0
        fi
    done
    return 1
}

# Start a service with retries
start_service() {
    local service_name="$1"
    local compose_file="$2"
    local port="$3"
    local health_path="$4"
    local attempt=1
    
    log INFO "Starting $service_name (attempt $attempt/$MAX_RETRIES)..."
    
    while [ $attempt -le $MAX_RETRIES ]; do
        # Check for port conflicts
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            handle_port_conflict "$port" "$service_name"
        fi
        
        # Start the service
        if docker compose -f "$compose_file" up -d --wait --wait-timeout $TIMEOUT; then
            log SUCCESS "$service_name containers started"
            
            # Wait for health check
            if wait_for_service_health "$service_name" $TIMEOUT; then
                # Also check HTTP endpoint if health check passes
                if wait_for_http "$port" "$health_path" "$service_name" 30; then
                    log SUCCESS "$service_name is fully operational"
                    return 0
                fi
            fi
        fi
        
        log WARN "$service_name startup attempt $attempt failed"
        
        # Stop containers before retry
        docker compose -f "$compose_file" down >/dev/null 2>&1 || true
        
        attempt=$((attempt + 1))
        if [ $attempt -le $MAX_RETRIES ]; then
            log INFO "Retrying $service_name startup in 5 seconds..."
            sleep 5
        fi
    done
    
    log ERROR "$service_name failed to start after $MAX_RETRIES attempts"
    return 1
}

# Stop all services
stop_all() {
    log INFO "Stopping all workflow services..."
    
    cd "$SCRIPT_DIR"
    
    for service_line in "${SERVICES[@]}"; do
        IFS=':' read -r service compose_file port health_path <<< "$service_line"
        log INFO "Stopping $service..."
        docker compose -f "$compose_file" down --remove-orphans >/dev/null 2>&1 || true
    done
    
    # Stop any standalone containers
    docker stop aipm-langflow >/dev/null 2>&1 && docker rm aipm-langflow >/dev/null 2>&1 || true
    
    # Clean up orphaned containers
    cleanup_existing
    
    log SUCCESS "All services stopped"
}

# Start a specific service by name
start_specific_service() {
    local target_service="$1"
    
    log INFO "Starting $target_service..."
    
    cd "$SCRIPT_DIR"
    
    local service_info
    if service_info=$(get_service_info "$target_service"); then
        IFS=':' read -r compose_file port health_path <<< "$service_info"
        
        if start_service "$target_service" "$compose_file" "$port" "$health_path"; then
            log SUCCESS "$target_service is ready at http://localhost:$port"
            return 0
        else
            log ERROR "$target_service failed to start"
            return 1
        fi
    else
        log ERROR "Service $target_service not found"
        return 1
    fi
}

# Start all essential services
start_all() {
    log INFO "Starting essential workflow services..."
    
    cd "$SCRIPT_DIR"
    
    local started_services=()
    local failed_services=()
    
    # Start Tier 1 services (essential)
    for service in "${TIER1_SERVICES[@]}"; do
        local service_info
        if service_info=$(get_service_info "$service"); then
            IFS=':' read -r compose_file port health_path <<< "$service_info"
            
            if start_service "$service" "$compose_file" "$port" "$health_path"; then
                started_services+=("$service (http://localhost:$port)")
            else
                failed_services+=("$service")
            fi
        else
            log ERROR "Service $service not found in configuration"
            failed_services+=("$service")
        fi
    done
    
    # Try to start Langflow if available
    if docker images --format "{{.Repository}}" | grep -q "langflow"; then
        log INFO "Starting Langflow..."
        if docker run -d --name aipm-langflow \
            --network "$NETWORK_NAME" \
            -p 7860:7860 \
            --label "ai-pm-toolkit.service=langflow" \
            langflow/langflow:latest >/dev/null 2>&1; then
            
            if wait_for_http "7860" "/" "Langflow" 60; then
                started_services+=("Langflow (http://localhost:7860)")
            else
                failed_services+=("Langflow")
                docker stop aipm-langflow >/dev/null 2>&1 && docker rm aipm-langflow >/dev/null 2>&1 || true
            fi
        else
            log WARN "Langflow container failed to start"
        fi
    fi
    
    # Report results
    log INFO "=== STARTUP SUMMARY ==="
    
    if [ ${#started_services[@]} -gt 0 ]; then
        log SUCCESS "Successfully started services:"
        for service in "${started_services[@]}"; do
            echo "   ✅ $service"
        done
    fi
    
    if [ ${#failed_services[@]} -gt 0 ]; then
        log ERROR "Failed to start services:"
        for service in "${failed_services[@]}"; do
            echo "   ❌ $service"
        done
        log INFO "Check logs with: docker compose -f <service-file>.yml logs"
    fi
    
    log INFO "=== QUICK ACCESS ==="
    echo "   • n8n Workflows: http://localhost:5678"
    echo "   • ToolJet Dashboards: http://localhost:8082"
    echo "   • Langflow AI: http://localhost:7860 (if started)"
    echo ""
    log INFO "Run 'aipm_workflows_status' to check service health"
    echo
    log INFO "=== AVAILABLE SERVICES ==="
    echo "   • Start ToolJet: aipm_workflows tooljet"
    echo "   • Start Typebot: aipm_workflows typebot"  
    echo "   • Start Penpot: aipm_workflows penpot"
    echo "   • Start all services: aipm_workflows all"
}

# Show status
show_status() {
    log INFO "Checking workflow services status..."
    
    cd "$SCRIPT_DIR"
    
    # Check network
    if "$SCRIPT_DIR/manage-network.sh" exists >/dev/null 2>&1; then
        log SUCCESS "Network: $NETWORK_NAME is available"
    else
        log ERROR "Network: $NETWORK_NAME is missing"
    fi
    
    # Check services
    for service_line in "${SERVICES[@]}"; do
        IFS=':' read -r service compose_file port health_path <<< "$service_line"
        
        local container_name="aipm-$service"
        
        if docker ps --format "{{.Names}}" | grep -q "^${container_name}$"; then
            local health_status
            health_status=$(docker inspect "$container_name" --format='{{.State.Health.Status}}' 2>/dev/null || echo "no-health-check")
            
            case "$health_status" in
                "healthy") log SUCCESS "$service: Running and healthy (http://localhost:$port)" ;;
                "unhealthy") log ERROR "$service: Running but unhealthy" ;;
                "starting") log WARN "$service: Starting up..." ;;
                *) log INFO "$service: Running (http://localhost:$port)" ;;
            esac
        else
            log ERROR "$service: Not running"
        fi
    done
    
    # Check Langflow
    if docker ps --format "{{.Names}}" | grep -q "^aipm-langflow$"; then
        log SUCCESS "Langflow: Running (http://localhost:7860)"
    else
        log WARN "Langflow: Not running"
    fi
}

# Main execution
main() {
    local command="${1:-start}"
    
    echo -e "${BLUE}🚀 AI PM Toolkit - Workflow Orchestration${NC}"
    echo "=================================================="
    
    case "$command" in
        start)
            check_docker || exit 1
            setup_network || exit 1
            cleanup_existing
            start_all
            ;;
        stop)
            check_docker || exit 1
            stop_all
            ;;
        restart)
            check_docker || exit 1
            stop_all
            sleep 3
            setup_network || exit 1
            cleanup_existing
            start_all
            ;;
        status)
            check_docker || exit 1
            show_status
            ;;
        cleanup)
            check_docker || exit 1
            stop_all
            "$SCRIPT_DIR/manage-network.sh" remove || true
            log SUCCESS "Complete cleanup finished"
            ;;
        tooljet|typebot|penpot)
            check_docker || exit 1
            setup_network || exit 1
            start_specific_service "$command"
            ;;
        all)
            check_docker || exit 1
            setup_network || exit 1
            cleanup_existing
            
            # Start all services
            local all_services=("${TIER1_SERVICES[@]}" "${TIER2_SERVICES[@]}" "${TIER3_SERVICES[@]}")
            for service in "${all_services[@]}"; do
                start_specific_service "$service"
            done
            ;;
        help|*)
            echo "Usage: $0 {start|stop|restart|status|cleanup|SERVICE|all|help}"
            echo ""
            echo "Commands:"
            echo "  start    - Start essential services (n8n)"
            echo "  stop     - Stop all workflow services"
            echo "  restart  - Stop and start essential services"
            echo "  status   - Show service status"
            echo "  cleanup  - Complete cleanup (removes all containers and network)"
            echo "  all      - Start all available services"
            echo ""
            echo "Individual Services:"
            echo "  tooljet  - Start ToolJet low-code platform"
            echo "  typebot  - Start Typebot conversational forms"
            echo "  penpot   - Start Penpot design platform"
            echo ""
            echo "Examples:"
            echo "  $0 start         # Start n8n (essential)"
            echo "  $0 tooljet       # Start just ToolJet"
            echo "  $0 all           # Start everything"
            echo "  $0 status        # Check what's running"
            ;;
    esac
}

# Run main function
main "$@"