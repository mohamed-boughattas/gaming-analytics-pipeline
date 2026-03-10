.PHONY: help install test lint format clean docker-up docker-down demo run marimo rill db-reset sqlmesh-plan sqlmesh-apply sqlmesh-test version

# Default target
help:
	@echo "Gaming Analytics Pipeline - Available Commands:"
	@echo ""
	@echo "Setup:"
	@echo "  make install           - Install dependencies with uv"
	@echo "  make demo              - Run demo with sample data (no API key needed)"
	@echo ""
	@echo "Development:"
	@echo "  make test              - Run tests with coverage"
	@echo "  make lint              - Run linters (ruff)"
	@echo "  make format            - Format code"
	@echo ""
	@echo "Pipeline:"
	@echo "  make run               - Run daily pipeline"
	@echo "  make sqlmesh-plan      - Create SQLMesh plan"
	@echo "  make sqlmesh-apply     - Apply SQLMesh plan"
	@echo "  make sqlmesh-test      - Run SQLMesh tests"
	@echo ""
	@echo "Dashboards:"
	@echo "  make marimo            - Start Marimo dashboard locally"
	@echo "  make rill              - Start Rill dashboard locally"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-up         - Start Docker containers"
	@echo "  make docker-down       - Stop Docker containers"
	@echo ""
	@echo "Other:"
	@echo "  make db-reset          - Reset database (deletes all data)"
	@echo "  make version           - Show version information"
	@echo "  make clean             - Clean generated files"

# Setup
install:
	uv sync

demo:
	@echo "Seeding database with sample data..."
	uv run python main.py seed
	@echo "Demo mode: Sample data seeded successfully!"

# Development
test:
	@echo "Running tests with coverage..."
	uv run pytest tests/ -v --cov=src --cov-report=term-missing

lint:
	@echo "Running linters..."
	uv run ruff check src/ tests/

format:
	@echo "Formatting code..."
	uv run ruff format src/ tests/

# Pipeline
run:
	uv run python main.py run

# SQLMesh
sqlmesh-plan:
	cd sqlmesh && uv run sqlmesh plan

sqlmesh-apply:
	cd sqlmesh && uv run sqlmesh plan --auto-apply

sqlmesh-test:
	cd sqlmesh && uv run sqlmesh test

# Dashboards
marimo:
	uv run marimo edit marimo/gaming_analytics.py --headless --host 0.0.0.0 --port 2718 --no-token

rill:
	@echo "Starting Rill dashboard..."
	@echo "Note: Install Rill CLI first with: curl -s https://cdn.rilldata.com/install.sh | bash"
	rill start ./rill --port 9009

# Docker
docker-up:
	docker compose up -d

docker-down:
	docker compose down

# Database
db-reset:
	@echo "⚠️  This will delete duckdb database"
	@read -p ""
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
