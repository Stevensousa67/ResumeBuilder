# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13.0
FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_ENV=production
ENV DEBUG=False

WORKDIR /app/ResumeBuilder

ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --no-cache-dir -r requirements.txt

COPY ResumeBuilder/ .

ENV GEMINI_API_KEY=dummy-key \
    SECRET_KEY=dummy-secret \
    SUPABASE_HOST=localhost \
    SUPABASE_PORT=5432 \
    SUPABASE_DB_NAME=postgres \
    SUPABASE_USER=postgres \
    SUPABASE_PASSWORD=postgres \
    ALLOWED_HOSTS=localhost
RUN python manage.py collectstatic --noinput

USER appuser
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--threads", "2", "--timeout", "90", "--log-level", "info", "ResumeBuilder.wsgi:application"]