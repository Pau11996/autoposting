# syntax=docker/dockerfile:1
FROM python:3.10-slim

# Add labels for better Fly.io integration
LABEL fly_launch_runtime="python"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8000 \
    LOG_LEVEL=INFO \
    LOG_FORMAT=json

WORKDIR /app

# Install dependencies first for better layer caching
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY autoposting_app ./autoposting_app
COPY api ./api
COPY main.py ./
COPY run_api.py ./

# Create data directory for persistent state (mount a volume on /app/data)
RUN mkdir -p /app/data
ENV DB_PATH=/app/data/autoposting.db

# Default to running the API server, but can be overridden
CMD ["python", "run_api.py"]
