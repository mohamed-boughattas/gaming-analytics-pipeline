# Dockerfile for Gaming Analytics Pipeline
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install uv package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock ./
COPY README.md ./
COPY .env.example ./

# Install dependencies
RUN uv pip install --system --upgrade pip setuptools wheel
RUN uv pip install --system -e .

# Copy application code
COPY src/ /app/src/
COPY main.py /app/

# Create data directory
RUN mkdir -p /app/data

# Create logs directory
RUN mkdir -p /app/logs

# Expose port for Prefect UI (if needed)
EXPOSE 4200

# Set environment variables
ENV PYTHONPATH=/app/src

# Default command runs the CLI
CMD ["python", "/app/main.py"]
