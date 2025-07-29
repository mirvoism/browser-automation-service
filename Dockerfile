# Multi-stage Docker build for AI Browser Automation
FROM mcr.microsoft.com/playwright/python:v1.41.0-jammy as base

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    unzip \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements*.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-macstudio.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 automation && \
    chown -R automation:automation /app
USER automation

# Set environment variables
ENV PYTHONPATH=/app
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import browser_use; print('OK')" || exit 1

# Default command
CMD ["python", "examples/google_search.py"]
