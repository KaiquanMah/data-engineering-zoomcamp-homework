# from base docker image
FROM python:3.13.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code
ENV PATH="/code/.venv/bin:$PATH"

# install libraries
# 1. individual libraries
# RUN pip install pandas pyarrow
# 2. from a toml file
COPY pyproject.toml .python-version uv.lock ./
RUN uv sync --locked

# copy the files we want
# 03-dockerizing-pipeline
# COPY pipeline.py .
# 08-dockerizing-ingestion
COPY ingest_data.py .


# when container runs
# what to do 1st
# 03-dockerizing-pipeline
# ENTRYPOINT ["python", "pipeline.py"]
# 08-dockerizing-ingestion
ENTRYPOINT ["python", "ingest_data.py"]