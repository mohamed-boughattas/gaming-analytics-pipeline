# Gaming Analytics Pipeline

[![CI](https://github.com/mohamed-boughattas/gaming-analytics-pipeline/actions/workflows/ci.yml/badge.svg?logo=githubactions)](https://github.com/mohamed-boughattas/gaming-analytics-pipeline/actions/workflows/ci.yml)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3120)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?logo=mit&logoColor=white)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-orange.svg?logo=ruff&logoColor=white)](https://github.com/astral-sh/ruff)
[![SQL Linting: sqlfluff](https://img.shields.io/badge/SQL%20linting-sqlfluff-blue?logo=sql)](https://sqlfluff.com/)
[![Type checking: ty](https://img.shields.io/badge/type%20checking-ty-blue?logo=python)](https://github.com/astral-sh/ty)
[![dlt](https://img.shields.io/badge/dlt-data%20loading-blue?logo=dlt)](https://dlthub.com/)
[![Soda](https://img.shields.io/badge/Soda%20Quality-green?logo=soda)](https://soda.io/)
[![SQLMesh](https://img.shields.io/badge/SQLMesh-transform-purple?logo=sqlmesh)](https://sqlmesh.com/)
[![Marimo](https://img.shields.io/badge/Marimo-dashboard-teal?logo=marimo)](https://marimo.io/)
[![DuckDB](https://img.shields.io/badge/DuckDB-database-yellow?logo=duckdb&logoColor=black)](https://duckdb.org/)


A modern data engineering pipeline for collecting, processing, and analyzing gaming data from the RAWG API.

## 🎯 Overview

This pipeline provides end-to-end data engineering capabilities for gaming analytics:

- **Data Ingestion**: Extract data from RAWG API using dlt
- **Data Orchestration**: Manage workflows with Prefect
- **Data Quality**: Validate data with Soda Core + SQLMesh tests
- **Data Transformation**: Transform data with SQLMesh
- **Data Visualization**: Present insights with Marimo and Evidence dashboards

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Gaming Analytics Pipeline                            │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐                                                          │
│  │   RAWG API   │ ◄── Source                                               │
│  └──────┬───────┘                                                          │
│         │                                                                   │
│         ▼                                                                   │
│  ┌──────────────┐     ┌──────────────┐                                    │
│  │     dlt      │ ◄── │   Prefect     │ ◄── Orchestration                 │
│  │  (Ingestion) │     │   (Tasks)     │                                    │
│  │  Incremental │     └──────────────┘                                    │
│  └──────┬───────┘                                                          │
│         │                                                                   │
│         ▼                                                                   │
│  ┌──────────────────────────────────┐                                     │
│  │         DuckDB                   │ ◄── Local DuckDB storage             │
│  │   ┌───────┐  ┌───────┐         │                                     │
│  │   │  raw  │─▶│ marts │         │                                     │
│  │   └───────┘  └───────┘         │                                     │
│  └──────────────┬──────────────────┘                                     │
│                 │                                                           │
│         ┌───────┴───────┐                                                  │
│         │               │                                                  │
│         ▼               ▼                                                  │
│  ┌──────────────┐ ┌──────────────┐                                        │
│  │   SQLMesh    │ │    Soda      │ ◄── Quality (Defense in Depth)        │
│  │ (Transform)  │ │  (Checks)    │                                        │
│  └──────────────┘ └──────────────┘                                        │
│                 │                                                           │
│         ┌───────┴───────┐                                                  │
│         │               │                                                  │
│         ▼               ▼                                                  │
│  ┌──────────────┐ ┌──────────────┐                                       │
│  │    Marimo     │ │   Evidence    │ ◄── Visualization (Dual Audience)   │
│  │   :2718       │ │    :3000     │                                       │
│  │  Python       │ │  Markdown    │                                       │
│  └──────────────┘ └──────────────┘                                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘

Data Flow: RAWG API → dlt → DuckDB → SQLMesh → Soda → Marimo/Evidence
Quality Gate: Soda Core + SQLMesh Tests
```

## 📈 Data Lineage

For detailed documentation of data flow and transformations, see [docs/data-flow.md](docs/data-flow.md).

## 🛠️ Why This Stack?

This project demonstrates a modern data engineering stack with intentional tool selection:

| Layer                | Tool        | Why Chosen                                                      | Alternative            |
| -------------------- | ----------- | --------------------------------------------------------------- | ---------------------- |
| **Ingestion**        | dlt         | Code-defined sources, **incremental loading**, automatic schema | Fivetran, Airbyte      |
| **Storage**          | DuckDB      | Local analytics DB, zero config, fast                           | PostgreSQL, ClickHouse |
| **Transformation**   | SQLMesh     | Virtual environments, built-in testing, no Jinja                | dbt                    |
| **Quality**          | Soda Core   | Declarative contracts, CI integration                        | Great Expectations     |
| **Orchestration**    | Prefect 3.x | Python-native, great DX, modern UI                              | Airflow, Dagster       |
| **Dashboard (Tech)** | Marimo      | Reactive Python notebooks, interactive                          | Streamlit, Jupyter     |
| **Dashboard (Biz)**  | Evidence    | Markdown-first BI, static HTML output                           | Rill, Metabase         |
| **Package Manager**  | uv          | 10-100x faster than pip, lockfile                               | pip, Poetry            |
| **Build Tool**       | Just        | Modern Make alternative, better errors                          | Make                   |

This stack demonstrates **modern data engineering practices** while keeping the project accessible and reproducible.

## ⚖️ Architectural Trade-offs

| Decision           | Choice               | Rationale                                          | Alternative Considered          |
| ------------------ | -------------------- | -------------------------------------------------- | ------------------------------- |
| **Database**       | DuckDB               | Embedded analytics DB, zero config, fast queries   | PostgreSQL, ClickHouse          |
| **Ingestion**      | dlt with incremental | Checkpoint-based, resumable, no duplicates         | Full reload (wastes API calls)  |
| **Transformation** | SQLMesh              | Virtual envs for dev/prod parity, built-in tests   | dbt (popular, separate testing) |
| **Quality**        | Soda + SQLMesh       | Defense in depth: contracts + transformation tests | Single tool (less coverage)     |
| **Orchestration**  | Prefect 3.x          | Python-native, task retries with backoff           | Airflow (heavier, Java-centric) |
| **Dashboards**     | Marimo + Evidence    | Dual audience: technical + business users          | Single tool (limited audience)  |

## 🔧 Technical Challenges & Solutions

### 1. Incremental Data Loading
**Challenge**: RAWG API has rate limits; failed requests waste API credits.

**Solution**: dlt's incremental loading with checkpoint persistence
- Pipeline resumes from last checkpoint on failure
- Only fetches changed records (using `updated` field)
- Write disposition: `merge` prevents duplicates

### 2. DuckDB File Locking
**Challenge**: DuckDB has file-level locking, preventing concurrent reads/writes.

**Solution**:
- Marimo connects with `read_only=True` for concurrent reads
- Pipeline writes run sequentially (Prefect handles orchestration)
- No concurrent write contention in practice for this use case

### 3. Data Quality at Scale
**Challenge**: Ensuring integrity across raw → staging → marts layers.

**Solution**: Defense-in-depth with layered quality gates
- **Raw**: Soda contracts (schema, completeness, domain)
- **Transformation**: SQLMesh tests (business logic)
- **Marts**: Referential integrity, freshness checks

### 4. Modern Tooling
**Challenge**: Showcasing modern alternatives to legacy tools.

**Solution**:
- `uv` instead of `pip` (10-100x faster)
- `Just` instead of `Make` (cleaner syntax)
- `dlt` instead of custom scripts (battle-tested)

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager

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
   uv run python main.py
   ```

## 📁 Project Structure

```text
gaming-analytics-pipeline/
├── src/gaming_pipeline/           # Main application package
│   ├── config/                    # Configuration management (Pydantic Settings)
│   │   ├── __init__.py
│   │   └── settings.py            # Environment-based configuration
│   ├── extract/                   # Data extraction layer
│   │   ├── __init__.py
│   │   └── dlt_source.py          # dlt source for RAWG API
│   ├── load/                      # Data loading layer
│   │   ├── __init__.py
│   │   └── pipeline.py            # dlt pipeline for DuckDB
│   ├── orchestrate/               # Workflow orchestration
│   │   ├── __init__.py
│   │   ├── flows.py               # Prefect 3.x flows
│   │   └── tasks.py               # Prefect tasks
│   ├── quality/                   # Data quality layer
│   │   ├── __init__.py
│   │   ├── checks.py              # Soda Core + SQLMesh checks
│   │   └── checks/                # Soda contract YAML files
│
├── marimo/                        # Marimo reactive dashboard
│   └── gaming_analytics.py        # Interactive visualizations
│
├── evidence/                      # Evidence markdown-first BI dashboard
│
├── tests/                        # Test suite
│   ├── test_config.py             # Config tests
│   ├── test_extract.py            # Extractor tests
│   ├── test_load.py               # Pipeline tests
│   ├── test_orchestrate.py        # Prefect orchestration tests
│   ├── test_quality.py            # Quality checks tests
│   ├── test_transform.py          # Transformation tests
│   └── conftest.py                # Pytest fixtures
│
├── docs/                          # Documentation
│   ├── adr/                       # Architecture Decision Records
│   └── data-flow.md              # Data flow documentation
│
├── data/                          # DuckDB database files (gitignored)
├── logs/                          # Application logs (gitignored)
├── htmlcov/                       # Test coverage reports (gitignored)
│
├── .github/workflows/             # CI pipelines
│   └── ci.yml                     # Lint and test
│
├── .env.example                   # Environment configuration template
├── .gitignore                     # Git ignore patterns
├── .sqlfluff                      # SQL linter configuration
├── LICENSE                        # MIT License
├── README.md                      # Project documentation
├── main.py                        # Pipeline entry point
├── pyproject.toml                 # Project dependencies & tool config
├── uv.lock                        # Dependency lock file
├── justfile                       # Development commands
└── sqlmesh/                       # SQLMesh project
    └── sqlmesh.yaml              # SQLMesh configuration
```

## 🔧 Configuration

### Environment Variables

| Variable          | Description             | Required |
| ----------------- | ----------------------- | -------- |
| `RAWG_API_KEY`    | RAWG API key            | Yes      |
| `DB_PATH`         | Path to DuckDB database | No       |
| `PREFECT_API_URL` | Prefect API URL         | No       |

### API Keys

Get your API keys:

- **RAWG**: [https://rawg.io/apidocs](https://rawg.io/apidocs)

## 📊 Data Model

### Raw Layer

- `raw.games`: Raw game data from RAWG (dlt normalizes nested JSON into child tables linked via `_dlt_id`)
- `raw.games__genres`: Genre links for each game (id, name, slug via `_dlt_root_id`)
- `raw.games__platforms`: Platform links for each game (platform__id, platform__name, platform__slug via `_dlt_root_id`)
- `raw.genres`: Genre information
- `raw.platforms`: Platform information

### Staging Layer

- `staging.stg_games`: Staging games data with type casting and null handling (exposes `_dlt_id` for joining child tables)
- `staging.stg_genres`: Staging genres data with type casting and null handling
- `staging.stg_platforms`: Staging platforms data with type casting and null handling

### Mart Layer

- `marts.fct_games`: Enriched game data with rating categories, engagement scores, and release year/month extraction
- `marts.fct_genres`: Aggregated genre statistics using JOINs to `raw.games__genres`
- `marts.fct_platforms`: Aggregated platform statistics using JOINs to `raw.games__platforms`

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
5. **Visualize**: View insights in Marimo dashboard

## 📈 Monitoring

### Data Quality

View Soda Core results:

```bash
just soda-scan
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

**Note**: Use `--host 0.0.0.0` (not `localhost`) for network access and `--no-token` to disable cloud auth prompts.

Access at <http://localhost:2718>

## 🔒 Security

This project uses automated security scanning to ensure code and dependency safety:

### Security Tools

- **[Ruff S Rules](https://docs.astral.sh/ruff/rules/#flake8-bandit-s)**: Code-level security linting
  - Integrated into Ruff's existing workflow
  - Identifies common security issues (SQL injection, hardcoded secrets, etc.)
  - Configured in `pyproject.toml` under `[tool.ruff.lint]`

- **[sqlfluff](https://sqlfluff.com/)**: SQL linting
  - Identifies SQL anti-patterns and syntax errors
  - Enforces consistent SQL style
  - Configured for DuckDB dialect in `.sqlfluff`

### Running Security Checks

```bash
# Run Ruff security rules
just lint-security
```

### Security Reports

- Ruff security issues are shown in CI logs
- Transitive dependency CVEs are managed by upstream package maintainers

### Best Practices

- Keep dependencies updated regularly
- Review security reports from CI
- Report vulnerabilities responsibly through security advisories
- Never commit secrets to repository (use environment variables)

## 🐛 Troubleshooting

### Common Issues

**Issue**: API rate limiting

- **Solution**: Add delays between requests or upgrade API plan

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
sqlfluff lint sqlmesh/
```

### Adding New Features

1. Add new extraction logic in `src/gaming_pipeline/extract/`
2. Create new SQLMesh models in `sqlmesh/models/staging/` or `sqlmesh/models/marts/`
3. Add Soda quality checks in `src/gaming_pipeline/quality/checks/`
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
- [Marimo](https://marimo.io/) for interactive data exploration
- [Evidence](https://evidence.dev/) for markdown-first BI dashboards

## 📞 Support

For issues and questions:

- Open an issue on GitHub
- Check the documentation
- Review existing issues

