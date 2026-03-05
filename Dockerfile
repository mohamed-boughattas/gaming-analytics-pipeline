# Dockerfile for Gaming Analytics Pipeline
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy dependency files AND README (required for build metadata)
COPY pyproject.toml uv.lock README.md ./

# Install dependencies using uv sync --frozen (uses locked versions)
RUN uv sync --frozen --no-dev

# Copy application code
COPY src/ /app/src/
COPY main.py /app/
COPY .env.example ./

# Create data directory
RUN mkdir -p /app/data

# Create logs directory
RUN mkdir -p /app/logs

# Expose port for Prefect UI (if needed)
EXPOSE 4200

# Set environment variables
ENV PYTHONPATH=/app/src

# Default command runs the CLI (using uv to access venv)
CMD ["uv", "run", "python", "/app/main.py"]
