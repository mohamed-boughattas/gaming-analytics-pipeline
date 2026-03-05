# Gaming Analytics Pipeline

[![CI/CD](https://github.com/mohamed-boughattas/gaming-analytics-pipeline/actions/workflows/ci.yml/badge.svg)](https://github.com/mohamed-boughattas/gaming-analytics-pipeline/actions/workflows/ci.yml)
[![Coverage](https://codecov.io/gh/mohamed-boughattas/gaming-analytics-pipeline/branch/main/graph/badge.svg)](https://codecov.io/gh/mohamed-boughattas/gaming-analytics-pipeline)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-orange.svg)](https://github.com/astral-sh/ruff)
[![Type checking: ty](https://img.shields.io/badge/type%20checking-ty-blue.svg)](https://github.com/astral-sh/ty)
[![Pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Security: bandit](https://img.shields.io/badge/Security-bandit-blue)](https://bandit.readthedocs.io/)
[![Security: pip-audit](https://img.shields.io/badge/Security-pip--audit-green)](https://pypi.org/project/pip-audit/)
[![dlt](https://img.shields.io/badge/dlt-data%20loading-blue)](https://dlthub.com/)
[![Prefect](https://img.shields.io/badge/Prefect-3.x-orange)](https://prefect.io/)
[![Soda](https://img.shields.io/badge/Soda%20Quality-green)](https://soda.io/)
[![SQLMesh](https://img.shields.io/badge/SQLMesh-transform-purple)](https://sqlmesh.com/)
[![Marimo](https://img.shields.io/badge/Marimo-dashboard-teal)](https://marimo.io/)
[![DuckDB](https://img.shields.io/badge/DuckDB-database-yellow)](https://duckdb.org/)

A modern data engineering pipeline for collecting, processing, and analyzing gaming data from the RAWG API.

## 🎯 Overview

This pipeline provides end-to-end data engineering capabilities for gaming analytics:

- **Data Ingestion**: Extract data from RAWG API using dlt
- **Data Orchestration**: Manage workflows with Prefect 3.x
- **Data Quality**: Validate data with Soda Core
- **Data Transformation**: Transform data with SQLMesh
- **Data Visualization**: Present insights with Marimo

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
```

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

### Using Docker

1. **Build and run with Docker Compose**:

   ```bash
   docker compose up -d
   ```

2. **Access services**:
   - Prefect UI: <http://localhost:4200>
   - Marimo Dashboard: <http://localhost:8000>

## 📁 Project Structure

```text
gaming-analytics-pipeline/
├── src/gaming_pipeline/
│   ├── config/           # Configuration management
│   ├── extract/          # Data extraction (RAWG)
│   ├── load/             # Data loading with dlt
│   ├── orchestrate/      # Prefect workflows
│   ├── quality/          # Soda Core checks
│   └── transform/        # SQLMesh transformations
├── tests/                # Pytest tests
├── data/                 # DuckDB database files
├── dashboard/            # Marimo dashboard
├── docs/                 # Documentation (ADR, data lineage, etc.)
├── logs/                 # Application logs
├── htmlcov/              # Test coverage reports
├── .github/workflows/    # CI/CD pipelines
├── .env.example          # Environment configuration template
├── .gitignore            # Git ignore patterns
├── .pre-commit-config.yaml # Pre-commit hooks
├── LICENSE               # MIT License
├── README.md             # Project documentation
├── CONTRIBUTING.md       # Contribution guidelines
├── main.py               # Main entry point
├── compose.yaml          # Docker Compose configuration
├── Dockerfile            # Pipeline container
├── Dockerfile.dashboard  # Dashboard container
├── pyproject.toml        # Project dependencies
├── uv.lock               # Dependency lock file
├── Makefile              # Development commands
└── sqlmesh.yaml          # SQLMesh configuration
```

## 🔧 Configuration

### Environment Variables

| Variable           | Description                 | Required |
| ------------------ | --------------------------- | -------- |
| `RAWG_API_KEY`     | RAWG API key                | Yes      |
| `DATABASE_PATH`    | Path to DuckDB database     | No       |
| `MOTHERDUCK_TOKEN` | MotherDuck token (optional) | No       |
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
4. **Quality**: Validate data with Soda Core
5. **Visualize**: Update Marimo dashboard

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

### Marimo Dashboard

Interactive dashboard for data exploration:

```bash
marimo edit dashboard/gaming_analytics.py
```

Or run the dashboard server:

```bash
marimo edit dashboard/gaming_analytics.py --headless --port 8000
```

Access at <http://localhost:8000>

## 🔒 Security

This project uses automated security scanning to ensure code and dependency safety:

### Security Tools

- **[Bandit](https://bandit.readthedocs.io/)**: Code-level security linter
  - Identifies common security issues in Python code
  - Runs as non-blocking check in CI/CD pipeline
  - Configuration: `.bandit`

- **[pip-audit](https://pypi.org/project/pip-audit/)**: Dependency vulnerability scanner
  - Checks Python dependencies for known vulnerabilities
  - Audits against PyPI and GitHub Advisory Database
  - Runs in CI/CD pipeline

### Running Security Checks

```bash
# Run all security checks
make security

# Run only bandit
make bandit

# Run only pip-audit
make pip-audit
```

### Security Reports

- Bandit reports are available as artifacts in CI/CD
- Pip-audit vulnerabilities are shown in CI logs
- Transitive dependency CVEs are managed by upstream package maintainers

### Best Practices

- Keep dependencies updated regularly
- Review security reports from CI/CD
- Report vulnerabilities responsibly through security advisories

## 🐛 Troubleshooting

### Common Issues

**Issue**: API rate limiting

- **Solution**: Add delays between requests or upgrade API plan

**Issue**: DuckDB database locked

- **Solution**: Ensure no other processes are using the database

**Issue**: Docker container fails to start

- **Solution**: Check environment variables in `.env` file

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 Development

### Code Style

We use [Ruff](https://github.com/astral-sh/ruff) for linting and formatting, and [ty](https://github.com/astral-sh/ty) for type checking:

```bash
# Lint code
ruff check src/ tests/

# Format code
ruff format src/ tests/

# Type checking
ty check src/
```

### Adding New Features

1. Add new extraction logic in `src/gaming_pipeline/extract/`
2. Create new transformations in `src/gaming_pipeline/transform/`
3. Add data quality checks in `src/gaming_pipeline/quality/`
4. Write tests in `tests/`
5. Update documentation

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- [RAWG API](https://rawg.io/) for game data
- [dlt](https://dlthub.com/) for data ingestion
- [Prefect](https://www.prefect.io/) for orchestration
- [Soda Core](https://www.soda.io/) for data quality
- [SQLMesh](https://sqlmesh.com/) for transformations
- [Marimo](https://marimo.io/) for visualization

## 📞 Support

For issues and questions:

- Open an issue on GitHub
- Check the documentation
- Review existing issues

---

Built with ❤️ for gaming analytics
