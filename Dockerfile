# Dockerfile for Gaming Analytics Pipeline
FROM python:3.12-slim

LABEL maintainer="gaming-analytics-pipeline"
LABEL version="1.0.0"
LABEL description="Gaming analytics pipeline with Prefect, SQLMesh, and dlt"

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock README.md ./

# Install dependencies
RUN uv sync --frozen --no-dev

# Copy application code
COPY src/ /app/src/
COPY main.py /app/

# Create directories
RUN mkdir -p /app/data /app/logs

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

EXPOSE 4200

ENV PYTHONPATH=/app/src

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:4200/api/health || exit 1

# Default command
CMD ["uv", "run", "python", "/app/main.py"]
