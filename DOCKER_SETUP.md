# Docker Setup Guide

This guide covers running the Gaming Analytics Pipeline using Docker.

## Prerequisites

- Docker Engine 20.10+
- Docker Compose v2+
- At least 4GB RAM available

## Quick Start

```bash
# Start all services in background
docker compose up -d --build

# View logs
docker compose logs -f

# Check container health status
docker compose ps

# Stop all services
docker compose down
```

## Services

| Service                | Port | Healthcheck                                | Description               |
| ---------------------- | ---- | ------------------------------------------ | ------------------------- |
| **gaming-pipeline**    | 4200 | `curl -f http://localhost:4200/api/health` | Prefect server            |
| **marimo-dashboard**   | 2718 | `curl -f http://localhost:2718/`           | Marimo notebook dashboard |

## Configuration

### Environment Variables

Create a `.env` file:

```bash
# Required
RAWG_API_KEY=your_api_key_here

# Optional - defaults shown
DATABASE_PATH=data/gaming_analytics.duckdb
PREFECT_API_URL=http://localhost:4200/api
```

### Volume Mounts

All services share:
- `./data` - DuckDB database file
- Environment variables from `.env`

### Development Mode

- **Marimo**: `./marimo` and `./src` are mounted for hot-reload

## Health Status

Check if all containers are healthy:

```bash
docker compose ps
```

 Expected output (all services should show `healthy`):

 ```text
 NAME                       STATUS
 gaming_analytics_pipeline healthy
 gaming_analytics_marimo    healthy
 ```

## Access URLs

| Service            | URL                        | Description           |
| ------------------ | -------------------------- | --------------------- |
| Prefect UI         | <http://localhost:4200>    | Workflow orchestration |
| Marimo Dashboard   | <http://localhost:2718>    | Interactive dashboard |

## Running the Pipeline

### Option 1: Inside Container

```bash
# Run daily pipeline
docker compose exec gaming-pipeline python main.py run

# Run full load
docker compose exec gaming-pipeline python main.py full-load

# Check status
docker compose exec gaming-pipeline python main.py status
```

### Option 2: Outside Container

The pipeline can also be run directly on the host:

```bash
# Install dependencies
make install

# Run pipeline
make run
```

## Data Persistence

- Database is stored in `./data/gaming_analytics.duckdb`
- This file is shared across all containers and the host
- To reset: `rm data/gaming_analytics.duckdb`

## Troubleshooting

### Container won't start

```bash
# Check logs
docker compose logs <service-name>

# Rebuild specific service
docker compose up -d --build <service-name>
```

### Healthcheck failing

 ```bash
 # Check health endpoints manually
 curl http://localhost:4200/api/health
 curl http://localhost:2718/
 ```

### Permission issues

```bash
# Fix data directory permissions
chmod -R 777 data/
```

### Out of memory

```bash
# Limit Docker memory in Docker Desktop preferences
# Or reduce pipeline page_size in main.py
```

## Production Considerations

For production deployment:

1. **Security**
   - Use Docker secrets for API keys
   - Enable HTTPS/TLS
   - Run containers as non-root user

2. **Monitoring**
   - Add healthcheck endpoints
   - Set up logging aggregation
   - Configure resource limits

3. **Backup**
   - Regular database backups
   - Volume snapshots

4. **Scaling**
   - Use Docker Swarm or Kubernetes
   - Separate services to different hosts
   - Add caching layer (Redis)

## Building Images Manually

```bash
# Build all images
docker compose build

# Build specific service
docker build -t gaming-pipeline:latest .
```
