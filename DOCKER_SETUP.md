# Docker Setup Guide

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
| **evidence-dashboard** | 3000 | `curl -f http://localhost:3000`            | Evidence SQL dashboard    |

## Volume Mounts

All services share `./data` directory for the DuckDB database file.

### Development Mode

- **Marimo**: `./marimo` and `./src` are mounted for hot-reload
- **Evidence**: `./evidence/pages` and `./evidence/sources` are mounted for hot-reload

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
gaming_analytics_evidence healthy
```

## Access URLs

- **Prefect UI**: <http://localhost:4200>
- **Marimo Dashboard**: <http://localhost:2718>
- **Evidence Dashboard**: <http://localhost:3000>

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
# Check health endpoint manually
curl http://localhost:4200/api/health
curl http://localhost:2718/
curl http://localhost:3000
```

### Permission issues

If you encounter permission issues with the `./data` directory:

```bash
# Fix permissions
sudo chown -R $(id -u):$(id -g) ./data
```
