# Stage 1: Builder
FROM python:3.13-slim AS builder

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=ResumeBuilder.settings \
    STATIC_ROOT=/app/staticfiles

# Install system dependencies required for build
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc python3-dev libpq-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy and install requirements first for layer caching
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --user -r requirements.txt

# Copy application code
COPY . .

# Collect static files with proper paths
RUN mkdir -p /app/staticfiles && \
    python manage.py collectstatic --noinput && \
    ls -la /app/staticfiles  # Debug: Verify staticfiles contents

# Stage 2: Production
FROM python:3.13-slim

# Create app user and directories with proper permissions
RUN useradd -m appuser && \
    mkdir -p /app/staticfiles && \
    chown -R appuser:appuser /app

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:${PATH}" \
    DJANGO_SETTINGS_MODULE=ResumeBuilder.settings \
    STATIC_ROOT=/app/staticfiles

# Copy dependencies from builder
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser . .

# Copy collected static files
COPY --from=builder --chown=appuser:appuser /app/staticfiles /app/staticfiles
RUN ls -la /app/staticfiles  # Debug: Verify copied files

USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "ResumeBuilder.wsgi:application"]