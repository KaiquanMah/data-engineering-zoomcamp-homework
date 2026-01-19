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

## Re-running Ingestion

```bash
# If you need to re-ingest data
docker compose up --build ingest
```

## Cleanup

```bash
docker compose down -v  # removes containers and volumes
```
