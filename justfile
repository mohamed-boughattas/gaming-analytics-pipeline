# Gaming Analytics Pipeline - Just Commands
# Modern build tool alternative to Makefile
# Run with: just <command>

# Show available commands
default:
    @just --list

# ============================================================================
# Setup
# ============================================================================

# Install dependencies
install:
    uv sync

# ============================================================================
# Development
# ============================================================================

# Run linters (ruff)
lint:
    @echo "Running linters..."
    uv run ruff check src/ tests/

# Format code (ruff)
format:
    @echo "Formatting code..."
    uv run ruff format src/ tests/

# Run tests (no coverage — fast)
test:
    @echo "Running tests..."
    uv run pytest tests/ -v --no-cov

# Run tests with coverage
test-cov:
    @echo "Running tests with coverage..."
    uv run pytest tests/ -v --cov=src --cov-report=term-missing

# Run full CI locally
lint-full:
    @echo "Running full CI locally..."
    @just format
    @just lint
    @just typecheck
    @just sqlmesh-lint
    @just lint-yaml

# Lint YAML files
lint-yaml:
    @echo "Linting YAML files..."
    uv run yamllint . -d .yamllint

# Run security checks
lint-security:
    @echo "Running security checks..."
    uv run ruff check src/ tests/ --select S

# Type checking
typecheck:
    @echo "Running type checker..."
    uv run ty check src/

# ============================================================================
# Pipeline
# ============================================================================

# Run daily pipeline
run:
    uv run python main.py

# Create SQLMesh plan (dev)
sqlmesh-plan:
    cd sqlmesh && uv run sqlmesh plan

# Apply SQLMesh plan
sqlmesh-apply:
    cd sqlmesh && uv run sqlmesh plan --auto-apply

# Run SQLMesh tests
sqlmesh-test:
    @echo "Running SQLMesh tests..."
    cd sqlmesh && uv run sqlmesh test --verbose

# Run SQLMesh linting
sqlmesh-lint:
    @echo "Running SQLMesh lint..."
    cd sqlmesh && uv run sqlmesh lint

# ============================================================================
# Dashboards
# ============================================================================

# Start Marimo dashboard
marimo:
    uv run marimo edit marimo/gaming_analytics.py --headless --host 0.0.0.0 --port 2718 --no-token

# Start Evidence dashboard (Node 22 required)
evidence:
    cd evidence && fnm use 22 && npm run dev

# ============================================================================
# Database
# ============================================================================

# Reset database (WARNING: deletes all data)
db-reset:
    @echo "⚠️  This will delete the DuckDB database and all data!"
    @echo "Type 'yes' to confirm or anything else to cancel:"
    @read -r confirm && [ "$$confirm" = "yes" ] || exit 0
    rm -f data/*.duckdb data/*.db
    @echo "Database reset complete."

# ============================================================================
# Data Quality
# ============================================================================

# Run Soda quality checks
soda-scan:
    @echo "Running Soda quality scans..."
    uv run python -m gaming_pipeline.quality.checks

# Run unified quality validation
quality-check:
    @echo "Running unified quality validation..."
    uv run python -c "from gaming_pipeline.quality.checks import run_quality_checks; import json; print(json.dumps(run_quality_checks('marts'), indent=2))"

# ============================================================================
# Other
# ============================================================================

# Show version
version:
    @uv run python -c "from importlib.metadata import version; print(version('gaming_analytics_pipeline'))"

# Clean generated files
clean:
    find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
    find . -type f -name "*.pyc" -delete 2>/dev/null || true
    find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
    find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
    rm -rf htmlcov/ .coverage 2>/dev/null || true

# Demo mode (no API key required)
demo: seed sqlmesh-apply

# Seed sample data (demo mode without API key)
seed:
    uv run python -m gaming_pipeline.demo.seed_database


