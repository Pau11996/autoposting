# syntax=docker/dockerfile:1
FROM python:3.10-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install dependencies first for better layer caching
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy application code
COPY autoposting_app ./autoposting_app
COPY main.py ./

# Create data directory for persistent state (mount a volume on /app/data)
RUN mkdir -p /app/data
ENV DB_PATH=/app/data/autoposting.db

# Default command; pass CLI flags like --offline or --post at runtime
CMD ["python", "main.py"]
