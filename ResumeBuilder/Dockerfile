# Stage 1: Builder
FROM python:3.13-slim AS builder

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --user -r requirements.txt

# Stage 2: Production
FROM python:3.13-slim

RUN useradd -m appuser && \
    mkdir /app && \
    chown -R appuser:appuser /app

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:${PATH}"

COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local
COPY --chown=appuser:appuser . .

USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "ResumeBuilder.wsgi:application"]
