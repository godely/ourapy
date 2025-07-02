# Base stage for installing dependencies
FROM python:3.10-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user and group
RUN groupadd -r appuser && useradd -r -g appuser -d /home/appuser -s /sbin/nologin -c "Docker image user" appuser
RUN mkdir /home/appuser && chown appuser:appuser /home/appuser

# Create working directory
WORKDIR /app

# Upgrade pip
RUN python -m pip install --upgrade pip

# Copy requirement files
COPY requirements.txt requirements-dev.txt ./

# Install dependencies
# Install production dependencies first, then development dependencies
# This helps with Docker layer caching if only dev dependencies change
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt

# Application stage
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create a non-root user and group (must match builder stage if copying files with --chown)
RUN groupadd -r appuser && useradd -r -g appuser -d /home/appuser -s /bin/bash -c "Docker image user" appuser
RUN mkdir /home/appuser && chown appuser:appuser /home/appuser

# Create working directory
WORKDIR /app

# Copy installed dependencies from builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
COPY --from=builder /app/ /app/

# Copy application code and necessary files
# Ensure these paths are correct based on your project structure after reorganization
COPY src/ ./src/
COPY tests/ ./tests/
COPY config/ ./config/
COPY setup.py .
COPY openapi_spec.json .
# Copy other root files if necessary, e.g., README.md, LICENSE, etc.
# COPY README.md .
# COPY LICENSE .

# Ensure correct ownership of application files
RUN chown -R appuser:appuser /app /home/appuser

# Switch to non-root user
USER appuser

# Expose port if your application is a web service (e.g., example.py runs a Flask app)
# EXPOSE 5000

# Default command to run tests
# This makes the container runnable and immediately useful for a developer
CMD ["pytest", "tests/"]
