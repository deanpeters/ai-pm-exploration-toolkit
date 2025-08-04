# Workflow Tools - Docker Configurations

This directory contains Docker Compose configurations for the AI PM Toolkit's workflow automation tools.

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

## Troubleshooting

### Port Conflicts
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