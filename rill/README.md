# Rill Dashboard

Real-time analytics dashboard for the Gaming Analytics Pipeline.

## What is Rill?

[Rill](https://www.rill.dev/) is a real-time business intelligence tool with native DuckDB support. It provides:

- Sub-second dashboard performance
- SQL + YAML configuration (no Node.js required)
- Single binary deployment
- Native DuckDB connector

## Quick Start

### Install Rill CLI

```bash
curl -s https://cdn.rilldata.com/install.sh | bash
```

### Run Locally

```bash
# From project root
make rill

# Or directly
rill start ./rill --port 9009
```

Open <http://localhost:9009>

### Run with Docker

```bash
# Start all services
docker compose up -d

# Or just Rill
docker compose up rill-dashboard
```

Open <http://localhost:9009>

## Project Structure

```text
rill/
├── rill.yaml                    # Project configuration (DuckDB connection)
├── sources/
│   ├── games.yaml               # Games model from marts.games
│   ├── genres.yaml              # Genres model from marts.genres
│   └── platforms.yaml           # Platforms model from marts.platforms
├── dashboards/
│   └── gaming_overview.yaml     # Main dashboard with KPIs
└── README.md                    # This file
```

## Available Data

| Model     | Source Table    | Key Metrics                                           |
| --------- | --------------- | ----------------------------------------------------- |
| games     | marts.games     | rating, metacritic, engagement_score, rating_category |
| genres    | marts.genres    | total_games, avg_rating, excellent_pct                |
| platforms | marts.platforms | total_games, avg_rating, year_start                   |

## Comparison with Other Dashboards

| Feature       | Rill      | Marimo     | Evidence       |
| ------------- | --------- | ---------- | -------------- |
| Port          | 9009      | 2718       | 3000           |
| Tech          | Go binary | Python     | Node.js        |
| Config        | YAML      | Python     | Markdown + SQL |
| Real-time     | Yes       | No         | No             |
| DuckDB Native | Yes       | Via Python | Via connector  |

## Resources

- [Rill Documentation](https://docs.rill.dev/)
- [Rill DuckDB Connector](https://docs.rill.dev/connectors/duckdb)
- [Rill Dashboard Reference](https://docs.rill.dev/reference/project-files/dashboards)
