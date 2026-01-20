# Homework Data Ingestion

Containerized solution to ingest NYC green taxi and zone lookup data into PostgreSQL.

## Files
- `green_tripdata_2025-11.parquet` → `green_taxi_trips` table
- `taxi_zone_lookup.csv` → `taxi_zone_lookup` table

## Usage (Run in GitHub Codespace)

```bash
# 1. Navigate to this folder
cd 01-docker-terraform/docker-sql/pipeline-homework

# 2. Download data files
wget -P data/ https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet
wget -P data/ https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv

# 3. Start Postgres, pgAdmin, and run ingestion
docker compose up --build

# 4. Verify in pgAdmin (http://localhost:8085)
# Email: admin@admin.com | Password: root
# Register server: host=pgdatabase, port=5432, user=root, password=root
```

* 2026.01.20
```bash
@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline-homework (main) $ docker compose down
[+] Running 3/3
 ✔ Container pipeline-homework-ingest-1      Removed                                                                                                                                                                           0.0s 
 ✔ Container pipeline-homework-pgadmin-1     Removed                                                                                                                                                                           0.0s 
 ✔ Container pipeline-homework-pgdatabase-1  Removed                                                                                                                                                                           0.0s 




@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline-homework (main) $ docker compose up --build
[+] Building 2.5s (17/17) FINISHED                                                                                                                                                                                                  
 => [internal] load local bake definitions                                                                                                                                                                                     0.0s
 => => reading from stdin 663B                                                                                                                                                                                                 0.0s
 => [internal] load build definition from Dockerfile                                                                                                                                                                           0.0s
 => => transferring dockerfile: 356B                                                                                                                                                                                           0.0s
 => [internal] load metadata for docker.io/library/python:3.13-slim                                                                                                                                                            1.4s
 => [internal] load metadata for ghcr.io/astral-sh/uv:latest                                                                                                                                                                   0.8s
 => [auth] library/python:pull token for registry-1.docker.io                                                                                                                                                                  0.0s
 => [auth] astral-sh/uv:pull token for ghcr.io                                                                                                                                                                                 0.0s
 => [internal] load .dockerignore                                                                                                                                                                                              0.0s
 => => transferring context: 2B                                                                                                                                                                                                0.0s
 => FROM ghcr.io/astral-sh/uv:latest@sha256:9a23023be68b2ed09750ae636228e903a54a05ea56ed03a934d00fe9fbeded4b                                                                                                                   0.0s
 => [internal] load build context                                                                                                                                                                                              0.0s
 => => transferring context: 2.95kB                                                                                                                                                                                            0.0s
 => [stage-0 1/6] FROM docker.io/library/python:3.13-slim@sha256:51e1a0a317fdb6e170dc791bbeae63fac5272c82f43958ef74a34e170c6f8b18                                                                                              0.0s
 => CACHED [stage-0 2/6] COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/                                                                                                                                                     0.0s
 => CACHED [stage-0 3/6] WORKDIR /app                                                                                                                                                                                          0.0s
 => CACHED [stage-0 4/6] COPY pyproject.toml ./                                                                                                                                                                                0.0s
 => CACHED [stage-0 5/6] RUN uv sync                                                                                                                                                                                           0.0s
 => [stage-0 6/6] COPY ingest_homework.py .                                                                                                                                                                                    0.0s
 => exporting to image                                                                                                                                                                                                         0.8s
 => => exporting layers                                                                                                                                                                                                        0.8s
 => => writing image sha256:a569791d526e0ad7e37f52922d4fe564c02360fff48647f5c2030767004eba3b                                                                                                                                   0.0s
 => => naming to docker.io/library/pipeline-homework-ingest                                                                                                                                                                    0.0s
 => resolving provenance for metadata file                                                                                                                                                                                     0.0s
[+] Running 4/4
 ✔ pipeline-homework-ingest                  Built                                                                                                                                                                             0.0s 
 ✔ Container pipeline-homework-pgdatabase-1  Created                                                                                                                                                                           0.0s 
 ✔ Container pipeline-homework-ingest-1      Created                                                                                                                                                                           0.1s 
 ✔ Container pipeline-homework-pgadmin-1     Created                                                                                                                                                                           0.1s 


Attaching to ingest-1, pgadmin-1, pgdatabase-1


pgdatabase-1  | 
pgdatabase-1  | PostgreSQL Database directory appears to contain a database; Skipping initialization
pgdatabase-1  | 
pgdatabase-1  | 2026-01-20 01:56:33.879 UTC [1] LOG:  starting PostgreSQL 18.1 (Debian 18.1-1.pgdg13+2) on x86_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit
pgdatabase-1  | 2026-01-20 01:56:33.879 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
pgdatabase-1  | 2026-01-20 01:56:33.880 UTC [1] LOG:  listening on IPv6 address "::", port 5432
pgdatabase-1  | 2026-01-20 01:56:33.885 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
pgdatabase-1  | 2026-01-20 01:56:33.896 UTC [31] LOG:  database system was shut down at 2026-01-20 01:55:40 UTC
pgdatabase-1  | 2026-01-20 01:56:33.923 UTC [1] LOG:  database system is ready to accept connections





pgadmin-1     | postfix/postlog: starting the Postfix mail system
pgadmin-1     | [2026-01-20 01:56:53 +0000] [1] [INFO] Starting gunicorn 23.0.0
pgadmin-1     | [2026-01-20 01:56:53 +0000] [1] [INFO] Listening at: http://[::]:80 (1)
pgadmin-1     | [2026-01-20 01:56:53 +0000] [1] [INFO] Using worker: gthread
pgadmin-1     | [2026-01-20 01:56:53 +0000] [96] [INFO] Booting worker with pid: 96





ingest-1      | Connecting to PostgreSQL at pgdatabase:5432/ny_taxi
ingest-1      | PostgreSQL is ready!
ingest-1      | Reading parquet file: /data/green_tripdata_2025-11.parquet
ingest-1      | Loaded 46912 rows from parquet
ingest-1      | Ingesting into table: green_taxi_trips
ingest-1      | Successfully ingested 46912 rows into green_taxi_trips


ingest-1      | Reading CSV file: /data/taxi_zone_lookup.csv
ingest-1      | Loaded 265 rows from CSV
ingest-1      | Ingesting into table: taxi_zone_lookup
ingest-1      | Successfully ingested 265 rows into taxi_zone_lookup


ingest-1      | Ingestion complete!
ingest-1 exited with code 0


pgadmin-1     | /venv/lib/python3.14/site-packages/sshtunnel.py:1040: SyntaxWarning: 'return' in a 'finally' block
pgadmin-1     |   return (ssh_host,
```





## Re-running Ingestion

```bash
# If you need to re-ingest data
docker compose up --build ingest
```

## Cleanup

```bash
docker compose down -v  # removes containers and volumes
```




# To have the old lesson docker AND new homework docker use the same volume
* Issue - when we ran the new homework docker-compose above, the old data in the lesson pipeline's Postgres disappeared. Why?
  * 1. Volume Names Are Project-Scoped
    * Even though both docker-compose files define the same volume name ny_taxi_postgres_data, Docker Compose prefixes volume names with the project name (folder name by default):
    *  | Folder	| Actual Volume Name |
       |--------|--------------------|
       |pipeline/	|pipeline_ny_taxi_postgres_data|
       |pipeline-homework/	|pipeline-homework_ny_taxi_postgres_data|
    * They are two completely separate volumes!
* How to Share Data Between Both Compose Files
  * If you want both pipeline and pipeline-homework to use the same database, you have two options:
  * Option A: Use External Named Volume (Recommended)
    * Update both docker-compose files to reference an external volume:
  *Option B: Use One Compose File
    * Run both pipelines against the same Postgres container by only using one docker-compose up at a time and connecting to the same network.


* In BOTH docker-compose.yaml files
```yaml
volumes:
  ny_taxi_postgres_data:
    external: true
    name: shared_ny_taxi_data  # Shared across pipeline and pipeline-homework
  pgadmin_data:
    external: true
    name: shared_pgadmin_data  # Shared across pipeline and pipeline-homework

```
* Run in github codespace terminal
```bash
# 1. Stop any running containers
docker compose down  # (run in both folders if needed)

# 2. Create the shared volume (run once)
docker volume create shared_ny_taxi_data
docker volume create shared_pgadmin_data

# 3. Create the shared network (if not exists)
docker network create pg-network

# 4. Pull latest changes
cd /workspaces/data-engineering-zoomcamp-homework
git pull

# 5. Run pipeline-homework (ingests green_taxi_trips + taxi_zone_lookup)
cd 01-docker-terraform/docker-sql/pipeline-homework
docker compose up --build
# ctrl+C to stop
# then
docker compose down




# 6. (Optional) Run pipeline (ingests yellow_taxi_trips)
cd ../pipeline
# approach 1 - docker compose down old container, then docker compose up new container
# otherwise if we do not docker compose down above
# we will get an error from running approach 1 below
# due to a PORT CONFLICT
#     pgdatabase uses port 5432 in both containers
#     pgadmin uses port 8085 in both containers
# @kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ docker compose up --build
# [+] Running 2/2
#  ✔ Container pipeline-pgadmin-1     Created                                                                                                                                                                  0.0s 
#  ✔ Container pipeline-pgdatabase-1  Created                                                                                                                                                                  0.0s 
# Attaching to pgadmin-1, pgdatabase-1
# Error response from daemon: failed to set up container networking: driver failed programming external connectivity on endpoint pipeline-pgadmin-1 (d9ccd1ae7bdd635ee769934af91df8a8d945fc26f649424733d7e5530d786ef1): Bind for 0.0.0.0:8085 failed: port is already allocated
docker compose up --build

# approach 2 - run only the ingestion container
docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-pass=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips
# 14it [02:36, 11.20s/it]
```
