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

# Type checking
typecheck:
    @echo "Running type checker..."
    uv run ty check src/

# Lint YAML files
lint-yaml:
    @echo "Linting YAML files..."
    uv run yamllint . -d .yamllint

# Run security checks
lint-security:
    @echo "Running security checks..."
    uv run ruff check src/ tests/ --select S

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
    @just lint-security
    @just typecheck
    @just sqlmesh-lint
    @just lint-yaml

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
    cd evidence && eval "$(fnm env)" && fnm use 22 && npm run dev

# ============================================================================
# Database
# ============================================================================

# Reset database and SQLMesh state (WARNING: deletes all data)
db-reset:
    @echo "⚠️  This will delete the DuckDB database and all data!"
    @echo "Type 'yes' to confirm or anything else to cancel:"
    @read -r confirm && [ "$$confirm" = "yes" ] || exit 0
    rm -f data/*.duckdb data/*.db
    rm -rf sqlmesh/.cache/
    @echo "Database and SQLMesh state reset complete."

# ============================================================================
# Data Quality
# ============================================================================

# Run Soda quality checks
soda-scan:
    @echo "Running Soda quality scans..."
    uv run python -m gaming_pipeline.quality

# ============================================================================
# Other
# ============================================================================

# Show version
version:
    @uv run python -c "from importlib.metadata import version; print(version('gaming_analytics_pipeline'))"

# Clean generated files
clean:
    rm -rf __pycache__ .pytest_cache .ruff_cache htmlcov .coverage
    find . -type f -name "*.pyc" -delete 2>/dev/null || true


