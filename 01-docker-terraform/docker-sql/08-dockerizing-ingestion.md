# Dockerizing the Ingestion Script

**[↑ Up](README.md)** | **[← Previous](07-pgadmin.md)** | **[Next →](09-docker-compose.md)**

Now let's containerize the ingestion script so we can run it in Docker.

## The Dockerfile

The `pipeline/Dockerfile` shows how to containerize the ingestion script:

```dockerfile
FROM python:3.13.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code
ENV PATH="/code/.venv/bin:$PATH"

COPY pyproject.toml .python-version uv.lock ./
RUN uv sync --locked

COPY ingest_data.py .

ENTRYPOINT ["python", "ingest_data.py"]
```

### Explanation

- `FROM python:3.13.11-slim`: Start with **slim Python 3.13 image for smaller size**
- `COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/`: **Copy uv binary from official uv image**
- `WORKDIR /code`: Set **working directory inside container**
- `ENV PATH="/code/.venv/bin:$PATH"`: **Add virtual environment** to PATH
- `COPY pyproject.toml .python-version uv.lock ./`: **Copy dependency files first (better caching)**
- `RUN uv sync --locked`: **Install all dependencies** from lock file (ensures reproducible builds)
- `COPY ingest_data.py .`: **Copy ingestion script**
- `ENTRYPOINT ["python", "ingest_data.py"]`: **Set entry point to run** the ingestion script








## Build the Docker Image

```bash
cd 01-docker-terraform/docker-sql/pipeline/
docker build -t taxi_ingest:v001 .





@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ docker build -t taxi_ingest:v001 .
[+] Building 1.9s (15/15) FINISHED                                                                                                docker:default
 => [internal] load build definition from Dockerfile                                                                                        0.1s
 => => transferring dockerfile: 651B                                                                                                        0.0s
 => [internal] load metadata for ghcr.io/astral-sh/uv:latest                                                                                1.1s
 => [internal] load metadata for docker.io/library/python:3.13.11-slim                                                                      1.7s
 => [auth] astral-sh/uv:pull token for ghcr.io                                                                                              0.0s
 => [auth] library/python:pull token for registry-1.docker.io                                                                               0.0s
 => [internal] load .dockerignore                                                                                                           0.0s
 => => transferring context: 2B                                                                                                             0.0s
 => FROM ghcr.io/astral-sh/uv:latest@sha256:9a23023be68b2ed09750ae636228e903a54a05ea56ed03a934d00fe9fbeded4b                                0.0s
 => [internal] load build context                                                                                                           0.1s
 => => transferring context: 2.89kB                                                                                                         0.1s
 => [stage-0 1/6] FROM docker.io/library/python:3.13.11-slim@sha256:51e1a0a317fdb6e170dc791bbeae63fac5272c82f43958ef74a34e170c6f8b18        0.0s
 => CACHED [stage-0 2/6] COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/                                                                  0.0s
 => CACHED [stage-0 3/6] WORKDIR /code                                                                                                      0.0s
 => CACHED [stage-0 4/6] COPY pyproject.toml .python-version uv.lock ./                                                                     0.0s
 => CACHED [stage-0 5/6] RUN uv sync --locked                                                                                               0.0s
 => CACHED [stage-0 6/6] COPY ingest_data.py .                                                                                              0.0s
 => exporting to image                                                                                                                      0.0s
 => => exporting layers                                                                                                                     0.0s
 => => writing image sha256:25252d83c5196bd5fcff6b5b82cde24626cc5556b8088f97ada621292c39f27c                                                0.0s
 => => naming to docker.io/library/taxi_ingest:v001                                                                                         0.0s
```





## Run the Containerized Ingestion

```bash
docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table=yellow_taxi_trips











@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ docker ps
CONTAINER ID   IMAGE            COMMAND                  CREATED          STATUS          PORTS                                              NAMES
6482c3442e3a   postgres:18      "docker-entrypoint.s…"   28 seconds ago   Up 28 seconds   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp        pgdatabase
c77909d96a6c   dpage/pgadmin4   "/entrypoint.sh"         51 minutes ago   Up 51 minutes   443/tcp, 0.0.0.0:8085->80/tcp, [::]:8085->80/tcp   pgadmin

@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table=yellow_taxi_trips
Usage: ingest_data.py [OPTIONS]
Try 'ingest_data.py --help' for help.

Error: No such option: --user (Possible options: --pg-user, --year)







# updated params following ingest.py script's 'click' params
@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-pass=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips
14it [02:18,  9.89s/it]


```

### Important Notes

* We need to provide the network for Docker to find the Postgres container. It goes before the name of the image.
* Since Postgres is running on a separate container, the host argument will have to point to the container name of Postgres (`pgdatabase`).
* You can drop the table in pgAdmin beforehand if you want, but the script will automatically replace the pre-existing table.

**[↑ Up](README.md)** | **[← Previous](07-pgadmin.md)** | **[Next →](09-docker-compose.md)**
