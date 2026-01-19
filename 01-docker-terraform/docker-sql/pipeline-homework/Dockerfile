FROM python:3.13-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency files first (better caching)
COPY pyproject.toml ./
RUN uv sync

# Copy ingestion script
COPY ingest_homework.py .

# Run ingestion on startup
CMD ["python", "ingest_homework.py"]
