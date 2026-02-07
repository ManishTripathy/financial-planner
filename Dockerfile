# Financial Backend
# Runs the Adaptive Financial Planner on Agent Field

FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first for better caching
COPY pyproject.toml ./

# Install Python dependencies
# We install in editable mode or just install the package
RUN pip install --upgrade pip && \
    pip install -e .

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -s /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser

# Default port
EXPOSE 8002

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8002/ || exit 1

# Run the API server
CMD ["uvicorn", "financial_backend.api:app", "--host", "0.0.0.0", "--port", "8002"]
