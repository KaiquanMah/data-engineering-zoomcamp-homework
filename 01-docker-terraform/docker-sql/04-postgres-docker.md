# Running PostgreSQL with Docker

**[↑ Up](README.md)** | **[← Previous](03-dockerizing-pipeline.md)** | **[Next →](05-data-ingestion.md)**

Now we want to do real data engineering. Let's use a Postgres database for that.

You can run a containerized version of Postgres that doesn't require any installation steps. You only need to provide a few _environment variables_ to it as well as a _volume_ for storing data.

## Running PostgreSQL in a Container

Create a folder anywhere you'd like for Postgres to store data in. We will use the example folder `ny_taxi_postgres_data`. Here's how to run the container:

```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```

### Explanation of Parameters

* `-e` sets environment variables (user, password, database name)
* `-v ny_taxi_postgres_data:/var/lib/postgresql` creates a **named volume**
  * Docker manages this volume automatically
  * Data persists even after container is removed
  * Volume is stored in Docker's internal storage
* `-p 5432:5432` maps port 5432 from container to host
* `postgres:18` uses PostgreSQL version 18 (latest as of Dec 2025)

### Alternative Approach - Bind Mount

First create the directory, then map it:

```bash
mkdir ny_taxi_postgres_data

docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```

### Named Volume vs Bind Mount

* **Named volume** (`name:/path`): Managed by Docker, easier
* **Bind mount** (`/host/path:/container/path`): Direct mapping to host filesystem, more control


### Actual tryout
```bash
# volumes tt docker knows abt
# Docker's internal database of volumes
# → If ny_taxi_postgres_data exists → Docker uses that volume.
# → If it doesn't exist → Docker automatically creates a new volume with this name.
@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework (main) $ docker volume ls
DRIVER    VOLUME NAME
local     ny_taxi_postgres_data

```

* Physical storage location (hidden from you)
*   → Docker stores the actual data in its private storage area on the host:
```bash
# Typical location on Linux:
# On macOS/Windows (inside Docker VM):
/var/lib/docker/volumes/ny_taxi_postgres_data/_data/


@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework (main) $ docker volume inspect ny_taxi_postgres_data
[
    {
        "CreatedAt": "2026-01-18T07:27:23Z",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/ny_taxi_postgres_data/_data",
        "Name": "ny_taxi_postgres_data",
        "Options": null,
        "Scope": "local"
    }
]


@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework (main) $ cd /var/lib/docker/volumes/
bash: cd: /var/lib/docker/volumes/: Permission denied
```




## Connecting to PostgreSQL

Once the container is running, we can log into our database with [pgcli](https://www.pgcli.com/).

Install pgcli:

```bash
uv add --dev pgcli



@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework (main) $ cd 01-docker-terraform/docker-sql/pipeline/
@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ uv add --dev pgcli
Resolved 120 packages in 0.63ms
Audited 115 packages in 51ms
```

The `--dev` flag marks this as a **development dependency (not needed in production)**. It will be added to the `[dependency-groups]` section of `pyproject.toml` instead of the main `dependencies` section.




Now use it to connect to Postgres:

```bash
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

* `uv run` executes a command in the context of the virtual environment
* `-h` is the host. Since we're running locally we can use `localhost`.
* `-p` is the port.
* `-u` is the username.
* `-d` is the database name.
* The password is not provided; it will be requested after running the command.

When prompted, enter the password: `root`

```bash
@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ uv run pgcli -h localhost -p 5432 -u root -d ny_taxi

Password for root: 
Using local time zone Etc/UTC (server uses Etc/UTC)
Use `set time zone <TZ>` to override, or set `use_local_timezone = False` in the config
Server: PostgreSQL 18.1 (Debian 18.1-1.pgdg13+2)
Version: 4.3.0
Home: http://pgcli.com


root@localhost:ny_taxi>
```


## Basic SQL Commands

Try some SQL commands:

```sql
-- List tables
\dt

root@localhost:ny_taxi> \dt
+--------+------+------+-------+
| Schema | Name | Type | Owner |
|--------+------+------+-------|
+--------+------+------+-------+
SELECT 0
Time: 0.009s







-- Create a test table
CREATE TABLE test (id INTEGER, name VARCHAR(50));

-- Insert data
INSERT INTO test VALUES (1, 'Hello Docker');

-- Query data
SELECT * FROM test;



root@localhost:ny_taxi> \dt
+--------+------+-------+-------+
| Schema | Name | Type  | Owner |
|--------+------+-------+-------|
| public | test | table | root  |
+--------+------+-------+-------+
SELECT 1
Time: 0.004s

root@localhost:ny_taxi> SELECT * FROM test;
+----+--------------+
| id | name         |
|----+--------------|
| 1  | Hello Docker |
+----+--------------+
SELECT 1
Time: 0.005s











-- Exit
\q
```

**[↑ Up](README.md)** | **[← Previous](03-dockerizing-pipeline.md)** | **[Next →](05-data-ingestion.md)**
