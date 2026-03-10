# Gaming Analytics Pipeline

[![CI/CD](https://github.com/mohamed-boughattas/gaming-analytics-pipeline/actions/workflows/ci.yml/badge.svg?logo=githubactions)](https://github.com/mohamed-boughattas/gaming-analytics-pipeline/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/mohamed-boughattas/gaming-analytics-pipeline/branch/main/graph/badge.svg?logo=codecov)](https://codecov.io/gh/mohamed-boughattas/gaming-analytics-pipeline)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg?logo=python)](https://www.python.org/downloads/release/python-3120)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-orange.svg?logo=github)](https://github.com/astral-sh/ruff)
[![SQL Linting: sqlfluff](https://img.shields.io/badge/SQL%20linting-sqlfluff-blue?logo=github)](https://sqlfluff.com/)
[![Type checking: ty](https://img.shields.io/badge/type%20checking-ty-blue.svg?logo=github)](https://github.com/astral-sh/ty)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Security: Ruff S](https://img.shields.io/badge/Security-Ruff%20S-blue?logo=github)](https://github.com/astral-sh/ruff)
[![Security: detect-secrets](https://img.shields.io/badge/Security-detect--secrets-green?logo=github)](https://github.com/Yelp/detect-secrets)
[![dlt](https://img.shields.io/badge/dlt-data%20loading-blue?logo=github)](https://dlthub.com/)
[![Prefect](https://img.shields.io/badge/Prefect-3.x-orange?logo=prefect)](https://prefect.io/)
[![Soda](https://img.shields.io/badge/Soda%20Quality-green?logo=github)](https://soda.io/)
[![SQLMesh](https://img.shields.io/badge/SQLMesh-transform-purple?logo=github)](https://sqlmesh.com/)
[![Marimo](https://img.shields.io/badge/Marimo-dashboard-teal?logo=github)](https://marimo.io/)
[![Rill](https://img.shields.io/badge/Rill-BI%20as%20code-purple?logo=github)](https://rilldata.com/)
[![DuckDB](https://img.shields.io/badge/DuckDB-database-yellow?logo=duckdb)](https://duckdb.org/)
[![Docker](https://img.shields.io/badge/Docker-containerized-blue?logo=docker)](https://www.docker.com/)

A modern data engineering pipeline for collecting, processing, and analyzing gaming data from the RAWG API.

## 🎯 Overview

This pipeline provides end-to-end data engineering capabilities for gaming analytics:

- **Data Ingestion**: Extract data from RAWG API using dlt
- **Data Orchestration**: Manage workflows with Prefect 3.x
- **Data Quality**: Validate data with Soda Core + SQLMesh tests
- **Data Transformation**: Transform data with SQLMesh
- **Data Visualization**: Present insights with Marimo and Rill dashboards

## 🏗️ Architecture

```text
┌─────────────┐      ┌─────────────┐
│   RAWG API  │      │  Sources    │
└──────┬──────┘      └──────┬──────┘
       │                    │
       └─────────┬──────────┘
                 │
         ┌───────▼────────┐
         │  dlt Ingestion │
         └───────┬────────┘
                 │
         ┌───────▼────────┐
         │  DuckDB/      │
         │  MotherDuck   │
         └───────┬────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
┌───▼────┐  ┌──▼────┐  ┌──▼────────┐
│Prefect  │  │Soda    │  │Marimo     │
│3.x     │  │Core    │  │Dashboard   │
└────────┘  └─────────┘  └───────────┘
                              │
                         ┌────▼────┐
                         │Rill      │
                         │Dashboard │
                         └──────────┘
```

## 📈 Data Lineage

For detailed documentation of data flow and transformations, see [docs/data-flow.md](docs/data-flow.md).

## 📊 Dashboard Screenshots

### Marimo Dashboard

![Marimo Dashboard](docs/images/dashboard.png)

Reactive notebook-style dashboard for interactive data exploration

### Rill Dashboard

![Rill Dashboard](docs/images/rill.png)

BI-as-code dashboard for production-ready analytics

> **Note**: Replace placeholder screenshots above with actual screenshots of your dashboards.

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- Docker (optional, for containerized deployment)

### Installation

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd gaming-analytics-pipeline
   ```

2. **Install dependencies**:

   ```bash
   uv sync
   ```

3. **Configure environment variables**:

   ```bash
   cp .env.example .env
   # Edit .env with your API key
   ```

4. **Run the pipeline**:

   ```bash
   python main.py
   ```

### Demo Mode (No API Key Required)

Try the project without a RAWG API key using sample data:

```bash
make demo
```

This seeds the database with sample games and allows you to explore the dashboards without API access.

### Using Docker

All services can run in Docker containers. The entire stack is containerized:

1. **Build and start all services**:

   ```bash
   docker compose up -d --build
   ```

2. **Check container health status**:

   ```bash
   docker compose ps
   ```

3. **Access services**:
   - **Prefect UI**: <http://localhost:4200>
   - **Marimo Dashboard**: <http://localhost:2718>
   - **Rill Dashboard**: <http://localhost:9009>

4. **View logs**:

   ```bash
   docker compose logs -f
   ```

5. **Stop all services**:

   ```bash
   docker compose down
   ```

For detailed Docker setup instructions, see [DOCKER_SETUP.md](DOCKER_SETUP.md).

## 📁 Project Structure

```text
gaming-analytics-pipeline/
├── src/gaming_pipeline/           # Main application package
│   ├── config/                    # Configuration management (Pydantic Settings)
│   │   ├── __init__.py
│   │   └── settings.py            # Environment-based configuration
│   ├── extract/                   # Data extraction layer
│   │   ├── __init__.py
│   │   ├── base.py                # Base extractor interface
│   │   └── rawg.py                # RAWG API extractor with retry logic
│   ├── load/                      # Data loading layer
│   │   ├── __init__.py
│   │   └── pipeline.py            # dlt pipeline for DuckDB
│   ├── orchestrate/               # Workflow orchestration
│   │   ├── __init__.py
│   │   ├── flows.py               # Prefect 3.x flows
│   │   └── tasks.py               # Prefect tasks
│   ├── quality/                   # Data quality layer
│   │   ├── __init__.py
│   │   ├── checks.py              # Soda Core integration
│   │   ├── configuration.py       # Soda configuration
│   │   └── checks/                # Soda check files
│   │       ├── staging.yml        # Staging layer checks
│   │       └── marts.yml          # Mart layer checks
│   ├── transform/                 # SQLMesh transformations
│   │   ├── staging/               # Staging models (type casting, null handling)
│   │   │   ├── stg_games.sql
│   │   │   ├── stg_genres.sql
│   │   │   └── stg_platforms.sql
│   │   └── marts/                 # Mart models (business logic, aggregations)
│   │       ├── games.sql          # Rating categories, engagement scores
│   │       ├── genres.sql
│   │       └── platforms.sql
│   ├── __init__.py
│   └── logging_config.py          # Structured logging setup
│
├── scripts/                       # Utility scripts
│   ├── __init__.py
│   └── seed_sample_data.py        # Demo data generator (no API key needed)
│
├── tests/                         # Test suite
│   ├── test_extract.py            # Extractor tests
│   ├── test_load.py               # Pipeline tests
│   ├── test_orchestrate.py        # Orchestration tests (integration)
│   ├── test_transform.py          # Transformation tests
│   ├── sqlmesh/                   # SQLMesh native tests
│   │   ├── README.md
│   │   ├── test_no_null_game_names.sql
│   │   ├── test_rating_ranges.sql
│   │   └── test_engagement_score_positive.sql
│   └── conftest.py                # Pytest fixtures
│
├── marimo/                     # Marimo reactive dashboard
│   └── gaming_analytics.py        # Interactive visualizations
│
├── rill/                       # Rill BI-as-code dashboard
│   ├── rill.yaml                  # Rill configuration
│   ├── connectors/                # Data connectors
│   ├── sources/                   # Data sources
│   └── dashboards/                # Dashboard definitions
│   ├── gaming_overview.yaml
│   ├── games_analytics.yaml
│   ├── genre_performance.yaml
│   └── platform_analytics.yaml
│
├── docs/                          # Documentation
│   ├── adr/                       # Architecture Decision Records
│   │   ├── 001-choose-duckdb-over-postgresql.md
│   │   ├── 002-choose-prefect-over-airflow.md
│   │   └── 003-choose-sqlmesh-over-dbt.md
│   ├── images/                    # Dashboard screenshots
│   │   └── README.md
│   ├── data-flow.md               # Data lineage (Mermaid diagrams)
│   └── data-retention.md          # Data retention policies
│
├── data/                          # DuckDB database files (gitignored)
├── logs/                          # Application logs (gitignored)
├── htmlcov/                       # Test coverage reports (gitignored)
│
├── .github/workflows/             # CI/CD pipelines
│   └── ci.yml                     # Lint, test, build, security scan
│
├── .env.example                   # Environment configuration template
├── .gitignore                     # Git ignore patterns
├── .pre-commit-config.yaml        # Pre-commit hooks
├── .sqlfluff                      # SQL linter configuration
├── LICENSE                        # MIT License
├── README.md                      # Project documentation
├── DOCKER_SETUP.md                # Docker setup guide
├── CONTRIBUTING.md                # Contribution guidelines
├── main.py                        # CLI entry point (Click)
├── compose.yaml                   # Docker Compose (3 services)
├── Dockerfile                     # Prefect pipeline container
├── Dockerfile.marimo              # Marimo dashboard container
├── Dockerfile.rill                # Rill dashboard container
├── pyproject.toml                 # Project dependencies & tool config
├── uv.lock                        # Dependency lock file
├── Makefile                       # Development commands
└── sqlmesh.yaml                   # SQLMesh configuration
```

## 🔧 Configuration

### Environment Variables

| Variable           | Description                 | Required |
| ------------------ | --------------------------- | -------- |
| `RAWG_API_KEY`     | RAWG API key                | Yes      |
| `DATABASE_PATH`    | Path to DuckDB database     | No       |
| `PREFECT_API_URL`  | Prefect API URL             | No       |

### API Keys

Get your API keys:

- **RAWG**: [https://rawg.io/apidocs](https://rawg.io/apidocs)

## 📊 Data Model

### Staging Layer

- `stg_games`: Staging games data with type casting and null handling
- `stg_genres`: Staging genres data with type casting and null handling
- `stg_platforms`: Staging platforms data with type casting and null handling

- `rawg_games`: Raw game data from RAWG
- `rawg_genres`: Genre information
- `rawg_platforms`: Platform information

### Mart Layer

- `marts_games`: Enriched game data with metrics
- `marts_genres`: Aggregated genre statistics
- `marts_platforms`: Platform analytics

## 🧪 Testing

Run all tests:

```bash
pytest tests/ -v
```

Run with coverage:

```bash
pytest tests/ --cov=src --cov-report=html
```

Run specific test file:

```bash
pytest tests/test_extract.py -v
```

## 🔄 Workflow

The pipeline runs in the following order:

1. **Extract**: Fetch data from RAWG API
2. **Load**: Store data in DuckDB using dlt
3. **Transform**: Apply SQLMesh transformations
4. **Quality**: Validate data with Soda Core + SQLMesh tests
5. **Visualize**: View insights in Marimo or Rill dashboards

## 📈 Monitoring

### Prefect UI

Monitor pipeline execution:

```bash
prefect server start
```

Visit <http://localhost:4200>

### Data Quality

View Soda Core results:

```bash
python -m src.gaming_pipeline.quality.checks
```

### Marimo Dashboard Overview

Interactive dashboard for data exploration:

```bash
marimo edit marimo/gaming_analytics.py --no-token
```

Or run dashboard server:

```bash
marimo edit marimo/gaming_analytics.py --headless --host 0.0.0.0 --port 2718 --no-token
```

**Note**: Use `--host 0.0.0.0` (not `localhost`) for Docker compatibility and `--no-token` to disable cloud auth prompts.

Access at <http://localhost:2718>

### Rill Dashboard Overview

BI-as-code analytics dashboard:

```bash
rill start ./rill --port 9009
```

Or use Makefile:

```bash
make rill
```

Access at <http://localhost:9009>

## 🔒 Security

This project uses automated security scanning to ensure code and dependency safety:

### Security Tools

- **[Ruff S Rules](https://docs.astral.sh/ruff/rules/#flake8-bandit-s)**: Code-level security linting
  - Integrated into Ruff's existing workflow
  - Identifies common security issues (SQL injection, hardcoded secrets, etc.)
  - Configured in `pyproject.toml` under `[tool.ruff.lint]`

- **[uv audit](https://docs.astral.sh/uv/guides/integration/dependency-bots/)**: Built-in dependency vulnerability scanner
  - Checks Python dependencies for known vulnerabilities
  - Audits against PyPI and GitHub Advisory Database
  - Runs in CI/CD pipeline with `uv audit --preview-features audit`

- **[Gitleaks](https://github.com/gitleaks/gitleaks)**: Secrets detection
  - Scans code for accidentally committed secrets (API keys, tokens, passwords)
  - Runs as pre-commit hook and in CI/CD
  - Configured in `.pre-commit-config.yaml`

- **[sqlfluff](https://sqlfluff.com/)**: SQL linting
  - Identifies SQL anti-patterns and syntax errors
  - Enforces consistent SQL style
  - Configured for DuckDB dialect in `.sqlfluff`

### Running Security Checks

```bash
# Run all security checks
make security

# Run Ruff security rules
make security

# Run uv audit (dependency scanner)
uv audit --preview-features audit

# Run gitleaks (secrets detection)
uv run gitleaks detect --no-git
```

### Security Reports

- Ruff security issues are shown in CI logs and pre-commit
- uv audit vulnerabilities are shown in CI logs
- Gitleaks secrets detection runs in pre-commit and CI
- Transitive dependency CVEs are managed by upstream package maintainers

### Best Practices

- Keep dependencies updated regularly
- Review security reports from CI/CD
- Report vulnerabilities responsibly through security advisories
- Never commit secrets to repository (use environment variables)

## 🐛 Troubleshooting

### Common Issues

**Issue**: API rate limiting

- **Solution**: Add delays between requests or upgrade API plan

**Issue**: Docker container fails to start

- **Solution**: Check health status with `docker compose ps` and view logs with `docker compose logs <service>`

**Issue**: Cannot access dashboard from outside container

- **Solution**: Ensure port mappings in `compose.yaml` are correct and services bind to `0.0.0.0`

## 🤝 Contributing

1. Fork repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Development

### Code Style

We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting, [ty](https://github.com/astral-sh/ty) for type checking, and [sqlfluff](https://sqlfluff.com/) for SQL linting:

```bash
# Lint Python code
ruff check src/ tests/

# Format code
ruff format src/ tests/

# Type checking
ty check src/

# Lint SQL files
sqlfluff lint evidence/
```

All these checks are available via pre-commit hooks:

```bash
pre-commit run --all-files
```

### Adding New Features

1. Add new extraction logic in `src/gaming_pipeline/extract/`
2. Create new transformations in `src/gaming_pipeline/transform/`
3. Add data quality checks in `src/gaming_pipeline/quality/`
4. Write tests in `tests/`
5. Update documentation

## 📄 License

This project is licensed under MIT License.

## 🙏 Acknowledgments

- [RAWG API](https://rawg.io/) for game data
- [dlt](https://dlthub.com/) for data ingestion
- [Prefect](https://www.prefect.io/) for orchestration
- [Soda Core](https://www.soda.io/) for data quality
- [SQLMesh](https://sqlmesh.com/) for transformations
- [Marimo](https://marimo.io/) for visualization
- [Rill](https://rilldata.com/) for BI-as-code dashboards

## 📞 Support

For issues and questions:

- Open an issue on GitHub
- Check the documentation
- Review existing issues

---

Built with ❤️ for gaming analytics
