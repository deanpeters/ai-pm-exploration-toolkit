# Workflow Tools - Docker Configurations

This directory contains Docker Compose configurations for the AI PM Toolkit's workflow automation tools.

## 🚀 Quick Start (Most Users)

**The easy way - just run this command:**
```bash
aipm_workflows
```
This will start all essential workflow tools and wait for them to be ready with health checks.

**Check if everything is running:**
```bash
aipm_workflows_status
```

**Having issues? Fix them automatically:**
```bash
aipm_workflows_fix
```

## Available Services

### Tier 1: n8n (Essential)
- **Service**: Visual workflow automation
- **URL**: http://localhost:5678
- **File**: `docker-compose.n8n.yml`
- **Resources**: Lightweight, single container

### Tier 2: ToolJet (Advanced)
- **Service**: Low-code application builder
- **URL**: http://localhost:8082
- **File**: `docker-compose.tooljet.yml`
- **Resources**: Multi-container with PostgreSQL database

### Tier 2: Typebot (Advanced)
- **Service**: Conversational form builder
- **Builder URL**: http://localhost:8083
- **Viewer URL**: http://localhost:8084
- **File**: `docker-compose.typebot.yml`
- **Resources**: Multi-container with PostgreSQL database

### Tier 3: Penpot (Expert)
- **Service**: Open-source design platform
- **URL**: http://localhost:8085
- **File**: `docker-compose.penpot.yml`
- **Resources**: Complex multi-container setup with PostgreSQL and Redis

## Network Architecture

All services use a shared Docker network `aipm_workflow_network` to enable inter-service communication when needed.

## Security Notes

⚠️ **Development Use Only**: These configurations are optimized for local development and PoL Probes. Default passwords and secrets are used for simplicity.

For production use:
- Change all default passwords
- Generate proper secret keys
- Configure proper authentication
- Use environment-specific secrets management

## Volume Management

Each service uses named Docker volumes for data persistence:
- `aipm_n8n_data` - n8n workflows and configurations
- `aipm_tooljet_postgres_data` - ToolJet database
- `aipm_typebot_postgres_data` - Typebot database  
- `aipm_penpot_postgres_data` - Penpot database
- `aipm_penpot_assets_data` - Penpot design assets

## Manual Operations

To manually start services:

```bash
# Start n8n
docker-compose -f docker-compose.n8n.yml up -d

# Start ToolJet
docker-compose -f docker-compose.tooljet.yml up -d

# Start Typebot
docker-compose -f docker-compose.typebot.yml up -d

# Start Penpot
docker-compose -f docker-compose.penpot.yml up -d
```

To stop services:

```bash
# Stop all services
docker-compose -f docker-compose.n8n.yml down
docker-compose -f docker-compose.tooljet.yml down
docker-compose -f docker-compose.typebot.yml down
docker-compose -f docker-compose.penpot.yml down
```

## 🚨 Common Issues & Solutions

### "The tools are never ready when I try to access them!"
**Problem:** You ran `aipm_workflows` but the URLs don't work.
**Solution:** The new `aipm_workflows` command actually starts the containers and waits for them to be ready. If it's still not working:

```bash
# Check what's actually running
aipm_workflows_status

# Fix common issues automatically  
aipm_workflows_fix

# Nuclear option - reset everything
aipm_workflows_stop
aipm_workflows_fix  # Choose option 6 for full reset
aipm_workflows
```

### Port Conflicts (Port already in use)
**Problem:** Error like "Port 5678 is already in use"
**Solution:** 
```bash
aipm_workflows_fix  # Choose option 1 to kill port conflicts
```

Or manually:
```bash
# See what's using the port
sudo lsof -i :5678

# Kill it
sudo lsof -ti:5678 | xargs kill
```

### Docker Not Responding
**Problem:** Docker containers won't start or behave weirdly
**Solution:**
```bash
aipm_workflows_fix  # Choose option 6 for nuclear reset
```

Or manually:
```bash
# Clean everything
docker system prune -f
docker volume prune -f
docker network create aipm_workflow_network

# Try again
aipm_workflows
```

### Containers Start But URLs Don't Work
**Problem:** Docker says containers are running but http://localhost:5678 doesn't load
**Solutions:**
1. **Wait longer** - Some tools take 30-60 seconds to fully initialize
2. **Check the logs**: `docker-compose -f docker-compose.n8n.yml logs`
3. **Restart the specific service**: `docker-compose -f docker-compose.n8n.yml restart`

## 🛠️ Advanced Management Commands

### Workflow Management
```bash
aipm_workflows              # Start all workflow tools (with health checks)
aipm_workflows_status       # Check which tools are running
aipm_workflows_stop         # Stop all workflow tools
aipm_workflows_restart      # Stop and restart all tools
aipm_workflows_fix          # Interactive troubleshooting menu
```

### Individual Service Control
```bash
# n8n workflow automation
docker-compose -f docker-compose.n8n.yml up -d
docker-compose -f docker-compose.n8n.yml logs
docker-compose -f docker-compose.n8n.yml restart

# ToolJet dashboard builder
docker-compose -f docker-compose.tooljet.yml up -d
docker-compose -f docker-compose.tooljet.yml logs

# Stop individual services
docker-compose -f docker-compose.n8n.yml down
```

## Legacy Troubleshooting

### Port Conflicts (Manual Method)
If ports are already in use, modify the port mappings in the compose files:
```yaml
ports:
  - "NEW_PORT:INTERNAL_PORT"
```

### Database Issues
If database containers fail to start:
1. Check Docker logs: `docker-compose logs [service-name]`
2. Remove volumes to reset: `docker volume rm [volume-name]`
3. Restart the service

### Network Issues
Create the shared network manually if needed:
```bash
docker network create aipm_workflow_network
```