.PHONY: help install test lint typecheck format clean docker-build docker-up docker-down db-status pre-commit pre-commit-install demo all check-env sqlmesh-plan sqlmesh-apply sqlmesh-test dashboard docker-logs docker-restart docker-ps format-check seed-data docker-build-marimo docker-up-marimo

# Default target
help:
	@echo "Gaming Analytics Pipeline - Available Commands:"
	@echo ""
	@echo "Setup:"
	@echo "  make all              - Install dependencies, lint, and test"
	@echo "  make install          - Install dependencies with uv"
	@echo "  make check-env        - Check if .env file exists"
	@echo "  make pre-commit-install - Install pre-commit hooks"
	@echo ""
	@echo "Development:"
	@echo "  make test             - Run tests with coverage"
	@echo "  make lint             - Run linters (ruff)"
	@echo "  make typecheck        - Run type checking (ty)"
	@echo "  make format           - Format code"
	@echo "  make format-check     - Check if code is formatted"
	@echo "  make pre-commit       - Run pre-commit hooks"
	@echo "  make seed-data        - Seed database with sample data"
	@echo "  make dashboard        - Start Marimo dashboard locally"
	@echo ""
	@echo "Pipeline:"
	@echo "  make run              - Run daily pipeline (default: 50 pages, 10 max)"
	@echo "  make full-load        - Run full historical load"
	@echo "  make db-status        - Check database status"
	@echo "  make demo             - Run demo with small dataset"
	@echo "  make sqlmesh-plan     - Create SQLMesh plan"
	@echo "  make sqlmesh-apply    - Apply SQLMesh plan"
	@echo "  make sqlmesh-test     - Run SQLMesh tests"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build     - Build all Docker images"
	@echo "  make docker-up        - Start all Docker containers"
	@echo "  make docker-down      - Stop all Docker containers"
	@echo "  make docker-logs      - Show Docker container logs"
	@echo "  make docker-restart   - Restart Docker containers"
	@echo "  make docker-ps        - Show Docker container status"
	@echo "  make docker-build-marimo  - Build Marimo dashboard image"
	@echo "  make docker-up-marimo     - Start Marimo dashboard container"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean            - Clean generated files"

# Setup
all: install lint typecheck test

check-env:
	@test -f .env || (echo "Error: .env file not found. Copy .env.example to .env" && exit 1)

install:
	uv sync

pre-commit-install:
	uv run pre-commit install

# Development
test:
	uv run pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

lint:
	uv run ruff check src/ tests/

typecheck:
	uv run ty check src/

format:
	uv run ruff format src/ tests/

pre-commit:
	uv run pre-commit run --all-files

# Pipeline
run:
	uv run python main.py run --page-size 50 --max-pages 10

full-load:
	uv run python main.py full-load

db-status:
	uv run python main.py status

demo:
	uv run python main.py run --page-size 10 --max-pages 2

seed-data:
	uv run python scripts/seed_data.py

# SQLMesh
sqlmesh-plan:
	uv run sqlmesh plan

sqlmesh-apply:
	uv run sqlmesh plan --apply

sqlmesh-test:
	uv run sqlmesh test

# Dashboards
dashboard:
	uv run marimo edit dashboard/gaming_analytics.py

# Format check
format-check:
	uv run ruff format --check src/ tests/

# Docker
docker-build:
	docker compose build

docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f

docker-restart:
	docker compose restart

docker-ps:
	docker compose ps

docker-build-marimo:
	docker compose build marimo-dashboard

docker-up-marimo:
	docker compose up -d marimo-dashboard

# Cleanup
clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name ".coverage" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf htmlcov/ .coverage 2>/dev/null || true
