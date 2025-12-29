# Dockerfile for Thirsty's Game Studio Agent System
# Multi-stage build for optimized production image

# Build stage
FROM python:3.12-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt requirements-dev.txt ./
COPY setup.py pyproject.toml README.md ./

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

# Production stage
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Set environment variables
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Copy application code
COPY agent/ ./agent/
COPY setup.py pyproject.toml README.md ./

# Install the package
RUN pip install -e .

# Create output directory
RUN mkdir -p /app/output

# Set volume for output
VOLUME ["/app/output"]

# Default command
ENTRYPOINT ["python", "-m", "agent.runner"]
CMD ["--output-dir", "/app/output"]

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import agent; print('healthy')" || exit 1

# Labels
LABEL maintainer="Thirsty's Game Studio"
LABEL description="Multi-agent orchestration system for game development"
LABEL version="0.1.0"
