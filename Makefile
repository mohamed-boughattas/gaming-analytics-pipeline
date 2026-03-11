.PHONY: help install test test-fast lint format lint-full lint-yaml lint-precommit lint-security clean docker-up docker-down docker-build docker-logs docker-ps demo run marimo db-reset sqlmesh-plan sqlmesh-apply sqlmesh-test version pre-commit-install

# Default target
help:
	@echo "Gaming Analytics Pipeline - Available Commands:"
	@echo ""
	@echo "Setup:"
	@echo "  make install              - Install dependencies with uv"
	@echo "  make demo                 - Run demo with sample data (no API key needed)"
	@echo "  make pre-commit-install   - Install pre-commit hooks"
	@echo ""
	@echo "Development:"
	@echo "  make test                - Run tests with coverage"
	@echo "  make test-fast           - Run tests without coverage (faster)"
	@echo "  make lint                - Run linters (ruff)"
	@echo "  make format              - Format code"
	@echo "  make lint-full           - Run full CI locally"
	@echo "  make lint-yaml           - Lint YAML files"
	@echo "  make lint-precommit      - Run pre-commit hooks"
	@echo "  make lint-security       - Run security checks"
	@echo ""
	@echo "Pipeline:"
	@echo "  make run                 - Run daily pipeline"
	@echo "  make sqlmesh-plan        - Create SQLMesh plan"
	@echo "  make sqlmesh-apply       - Apply SQLMesh plan"
	@echo "  make sqlmesh-test        - Run SQLMesh tests"
	@echo ""
	@echo "Dashboards:"
	@echo "  make marimo              - Start Marimo dashboard"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up           - Start Docker containers"
	@echo "  make docker-down         - Stop Docker containers"
	@echo "  make docker-build        - Build Docker images"
	@echo "  make docker-ps           - Show running containers"
	@echo "  make docker-logs         - View container logs"
	@echo ""
	@echo "Other:"
	@echo "  make db-reset            - Reset database (deletes all data)"
	@echo "  make version             - Show version information"
	@echo "  make clean               - Clean generated files"

# Setup
install:
	uv sync

pre-commit-install:
	uv run pre-commit install

demo:
	@echo "Seeding database with sample data..."
	uv run python main.py seed
	@echo "Demo mode: Sample data seeded successfully!"

# Development
test:
	@echo "Running tests with coverage..."
	uv run pytest tests/ -v --cov=src --cov-report=term-missing

test-fast:
	@echo "Running tests (fast mode - no coverage)..."
	uv run pytest tests/ -v --no-cov

lint:
	@echo "Running linters..."
	uv run ruff check src/ tests/

format:
	@echo "Formatting code..."
	uv run ruff format src/ tests/

lint-full:
	@echo "Running full CI locally (format + lint + type check + sqlmesh + yaml)..."
	@echo ""
	@echo ">>> Checking code format..."
	@uv run ruff format --check src/ tests/
	@echo ">>> Running linters..."
	@uv run ruff check src/ tests/
	@echo ">>> Running type checker..."
	@uv run ty check src/
	@echo ">>> Running SQLMesh lint..."
	@cd sqlmesh && uv run sqlmesh lint
	@echo ">>> Running YAML lint..."
	@make lint-yaml
	@echo ""
	@echo "✅ All CI checks passed!"

lint-yaml:
	@echo "Linting YAML files..."
	@uv run yamllint . -d .yamllint

lint-precommit:
	@echo "Running pre-commit hooks..."
	uv run pre-commit run --all-files

lint-security:
	@echo "Running security checks..."
	@echo ">>> Running ruff security rules..."
	@uv run ruff check src/ tests/ --select S
	@echo ">>> Running uv audit..."
	@uv audit --preview-features audit
	@echo ""
	@echo "✅ Security checks passed!"

# Pipeline
run:
	uv run python main.py run

# SQLMesh
sqlmesh-plan:
	cd sqlmesh && uv run sqlmesh plan

sqlmesh-apply:
	cd sqlmesh && uv run sqlmesh plan --auto-apply

sqlmesh-test:
	@echo "Running SQLMesh tests..."
	@cd sqlmesh && uv run sqlmesh test --verbose
	@echo "SQLMesh tests completed (silent success = all tests passed)"

# Dashboards
marimo:
	uv run marimo edit marimo/gaming_analytics.py --headless --host 0.0.0.0 --port 2718 --no-token

# Docker
docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-build:
	docker compose build

docker-ps:
	docker compose ps

docker-logs:
	docker compose logs -f

# Database
db-reset:
	@echo "⚠️  This will delete the DuckDB database and all data!"
	@echo "Type 'yes' to confirm or anything else to cancel:"
	@read -r confirm && [ "$$confirm" = "yes" ] || exit 0
	@rm -f data/*.duckdb data/*.db
	@echo "Database reset complete."

# Other
version:
	@uv run python main.py version

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage 2>/dev/null || true
