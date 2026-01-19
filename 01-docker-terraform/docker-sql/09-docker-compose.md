# Docker Compose

**[↑ Up](README.md)** | **[← Previous](08-dockerizing-ingestion.md)** | **[Next →](10-sql-refresher.md)**

`docker-compose` allows us to launch multiple containers using a single configuration file, so that we don't have to run multiple complex `docker run` commands separately.

Docker compose makes use of YAML files. Here's the `docker-compose.yaml` file:

```yaml
services:
  pgdatabase:
    image: postgres:18
    environment:
      POSTGRES_USER: "root"
      POSTGRES_PASSWORD: "root"
      POSTGRES_DB: "ny_taxi"
    volumes:
      - "ny_taxi_postgres_data:/var/lib/postgresql"
    ports:
      - "5432:5432"

  pgadmin:
    image: dpage/pgadmin4
    environment:
      PGADMIN_DEFAULT_EMAIL: "admin@admin.com"
      PGADMIN_DEFAULT_PASSWORD: "root"
    volumes:
      - "pgadmin_data:/var/lib/pgadmin"
    ports:
      - "8085:80"



volumes:
  ny_taxi_postgres_data:
  pgadmin_data:
```

### Explanation

* **We don't have to specify a network because `docker-compose` takes care of it**: every single container (or "service", as the file states) will run within the same network and will be able to find each other according to their names (`pgdatabase` and `pgadmin` in this example).
* All other details from the `docker run` commands (environment variables, volumes and ports) are mentioned accordingly in the file following YAML syntax.

### Kai 2026.01.19 Fix
* To implement the fixes found in [07-pgadmin.md](07-pgadmin.md) **regarding pgAdmin CSRF and cookie protection settings, additional environment variables have been added under the `pgadmin` service** in the `docker-compose.yaml` file above. **These settings are useful when running pgAdmin in certain environments like GitHub Codespaces.**
```yaml
      # ADD THESE FOR CODESPACES to work:
      PGADMIN_CONFIG_ENHANCED_COOKIE_PROTECTION: "False"
      PGADMIN_CONFIG_WTF_CSRF_ENABLED: "False"
      PGADMIN_CONFIG_WTF_CSRF_SSL_STRICT: "False"
      PGADMIN_CONFIG_WTF_CSRF_TIME_LIMIT: "None"
      PGADMIN_CONFIG_PROXY_X_FOR_COUNT: 1
      PGADMIN_CONFIG_PROXY_X_PROTO_COUNT: 1
      PGADMIN_CONFIG_PROXY_X_HOST_COUNT: 1
      PGADMIN_CONFIG_PROXY_X_PORT_COUNT: 1
      PGADMIN_CONFIG_PROXY_X_PREFIX_COUNT: 1
```






## Start Services with Docker Compose

We can now run Docker compose by running the following command from the same directory where `docker-compose.yaml` is found. Make sure that all previous containers aren't running anymore:

```bash
docker-compose up
```


```bash
@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework (main) $ cd 01-docker-terraform/docker-sql/pipeline




@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ docker-compose up
[+] Running 5/5
 ✔ Network pipeline_default               Created                                                                                                                                                                       0.1s 
 ✔ Volume pipeline_ny_taxi_postgres_data  Created                                                                                                                                                                       0.0s 
 ✔ Volume pipeline_pgadmin_data           Created                                                                                                                                                                       0.0s 
 ✔ Container pipeline-pgadmin-1           Created                                                                                                                                                                       0.1s 
 ✔ Container pipeline-pgdatabase-1        Created                                                                                                                                                                       0.1s 
Attaching to pgadmin-1, pgdatabase-1
pgadmin-1  | email config is {'CHECK_EMAIL_DELIVERABILITY': False, 'ALLOW_SPECIAL_EMAIL_DOMAINS': [], 'GLOBALLY_DELIVERABLE': True}
pgdatabase-1  | The files belonging to this database system will be owned by user "postgres".
pgdatabase-1  | This user must also own the server process.
pgdatabase-1  | 
pgdatabase-1  | The database cluster will be initialized with locale "en_US.utf8".
pgdatabase-1  | The default database encoding has accordingly been set to "UTF8".
pgdatabase-1  | The default text search configuration will be set to "english".
pgdatabase-1  | 
pgdatabase-1  | Data page checksums are enabled.
pgdatabase-1  | 
pgdatabase-1  | fixing permissions on existing directory /var/lib/postgresql/18/docker ... ok
pgdatabase-1  | creating subdirectories ... ok
pgdatabase-1  | selecting dynamic shared memory implementation ... posix
pgdatabase-1  | selecting default "max_connections" ... 100
pgdatabase-1  | selecting default "shared_buffers" ... 128MB
pgdatabase-1  | selecting default time zone ... Etc/UTC
pgdatabase-1  | creating configuration files ... ok
pgdatabase-1  | running bootstrap script ... ok
pgdatabase-1  | performing post-bootstrap initialization ... ok
pgdatabase-1  | syncing data to disk ... ok
pgdatabase-1  | 
pgdatabase-1  | 
pgdatabase-1  | Success. You can now start the database server using:
pgdatabase-1  | 
pgdatabase-1  |     pg_ctl -D /var/lib/postgresql/18/docker -l logfile start
pgdatabase-1  | 
pgdatabase-1  | initdb: warning: enabling "trust" authentication for local connections
pgdatabase-1  | initdb: hint: You can change this by editing pg_hba.conf or using the option -A, or --auth-local and --auth-host, the next time you run initdb.
pgdatabase-1  | waiting for server to start....2026-01-19 06:18:21.507 UTC [50] LOG:  starting PostgreSQL 18.1 (Debian 18.1-1.pgdg13+2) on x86_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit
pgdatabase-1  | 2026-01-19 06:18:21.509 UTC [50] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
pgdatabase-1  | 2026-01-19 06:18:21.518 UTC [56] LOG:  database system was shut down at 2026-01-19 06:18:20 UTC
pgdatabase-1  | 2026-01-19 06:18:21.523 UTC [50] LOG:  database system is ready to accept connections
pgdatabase-1  |  done
pgdatabase-1  | server started
pgdatabase-1  | CREATE DATABASE
pgdatabase-1  | 
pgdatabase-1  | 
pgdatabase-1  | /usr/local/bin/docker-entrypoint.sh: ignoring /docker-entrypoint-initdb.d/*
pgdatabase-1  | 
pgdatabase-1  | waiting for server to shut down...2026-01-19 06:18:22.914 UTC [50] LOG:  received fast shutdown request
pgdatabase-1  | .2026-01-19 06:18:22.921 UTC [50] LOG:  aborting any active transactions
pgdatabase-1  | 2026-01-19 06:18:22.930 UTC [50] LOG:  background worker "logical replication launcher" (PID 59) exited with exit code 1
pgdatabase-1  | 2026-01-19 06:18:22.932 UTC [54] LOG:  shutting down
pgdatabase-1  | 2026-01-19 06:18:22.933 UTC [54] LOG:  checkpoint starting: shutdown immediate
pgdatabase-1  | 2026-01-19 06:18:23.108 UTC [54] LOG:  checkpoint complete: wrote 943 buffers (5.8%), wrote 3 SLRU buffers; 0 WAL file(s) added, 0 removed, 0 recycled; write=0.033 s, sync=0.133 s, total=0.176 s; sync files=303, longest=0.119 s, average=0.001 s; distance=4352 kB, estimate=4352 kB; lsn=0/1B9FBA0, redo lsn=0/1B9FBA0
pgdatabase-1  | 2026-01-19 06:18:23.138 UTC [50] LOG:  database system is shut down
pgdatabase-1  |  done
pgdatabase-1  | server stopped
pgdatabase-1  | 
pgdatabase-1  | PostgreSQL init process complete; ready for start up.
pgdatabase-1  | 
pgdatabase-1  | 2026-01-19 06:18:23.290 UTC [1] LOG:  starting PostgreSQL 18.1 (Debian 18.1-1.pgdg13+2) on x86_64-pc-linux-gnu, compiled by gcc (Debian 14.2.0-19) 14.2.0, 64-bit
pgdatabase-1  | 2026-01-19 06:18:23.292 UTC [1] LOG:  listening on IPv4 address "0.0.0.0", port 5432
pgdatabase-1  | 2026-01-19 06:18:23.292 UTC [1] LOG:  listening on IPv6 address "::", port 5432
pgdatabase-1  | 2026-01-19 06:18:23.296 UTC [1] LOG:  listening on Unix socket "/var/run/postgresql/.s.PGSQL.5432"
pgdatabase-1  | 2026-01-19 06:18:23.307 UTC [72] LOG:  database system was shut down at 2026-01-19 06:18:23 UTC
pgdatabase-1  | 2026-01-19 06:18:23.315 UTC [1] LOG:  database system is ready to accept connections
pgadmin-1     | /venv/lib/python3.14/site-packages/sshtunnel.py:1040: SyntaxWarning: 'return' in a 'finally' block
pgadmin-1     |   return (ssh_host,
pgadmin-1     | NOTE: Configuring authentication for SERVER mode.
pgadmin-1     | 
pgadmin-1     | pgAdmin 4 - Application Initialisation
pgadmin-1     | ======================================
pgadmin-1     | 
pgadmin-1     | postfix/postlog: starting the Postfix mail system
pgadmin-1     | [2026-01-19 06:18:53 +0000] [1] [INFO] Starting gunicorn 23.0.0
pgadmin-1     | [2026-01-19 06:18:53 +0000] [1] [INFO] Listening at: http://[::]:80 (1)
pgadmin-1     | [2026-01-19 06:18:53 +0000] [1] [INFO] Using worker: gthread
pgadmin-1     | [2026-01-19 06:18:53 +0000] [132] [INFO] Booting worker with pid: 132
pgadmin-1     | /venv/lib/python3.14/site-packages/sshtunnel.py:1040: SyntaxWarning: 'return' in a 'finally' block
pgadmin-1     |   return (ssh_host,








@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework (main) $ docker ps -a
CONTAINER ID   IMAGE              COMMAND                  CREATED              STATUS                   PORTS                                              NAMES
4bef699eea32   dpage/pgadmin4     "/entrypoint.sh"         About a minute ago   Up About a minute        443/tcp, 0.0.0.0:8085->80/tcp, [::]:8085->80/tcp   pipeline-pgadmin-1
cdbf87253bb0   postgres:18        "docker-entrypoint.s…"   About a minute ago   Up About a minute        0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp        pipeline-pgdatabase-1
7b2a1362595a   taxi_ingest:v001   "python ingest_data.…"   2 hours ago          Exited (0) 2 hours ago                                                      romantic_mcnulty
6482c3442e3a   postgres:18        "docker-entrypoint.s…"   3 hours ago          Exited (0) 2 hours ago                                                      pgdatabase
637e46346ecd   taxi_ingest:v001   "python ingest_data.…"   3 hours ago          Exited (1) 3 hours ago                                                      jovial_kalam
c0313a85bdaf   taxi_ingest:v001   "python ingest_data.…"   3 hours ago          Exited (2) 3 hours ago                                                      compassionate_hugle
3bea62ff222d   taxi_ingest:v001   "python ingest_data.…"   3 hours ago          Exited (2) 3 hours ago                                                      vigilant_clarke
c77909d96a6c   dpage/pgadmin4     "/entrypoint.sh"         3 hours ago          Exited (0) 2 hours ago                                                      pgadmin
```


### Detached Mode

If you want to **run the containers again in the background rather than in the foreground (thus freeing up your terminal)**, you can run them in detached mode:

```bash
docker-compose up -d
```

## Stop Services

You will have to press `Ctrl+C` in order to shut down the containers when running in foreground mode. The proper way of shutting them down is with this command:

```bash
docker-compose down
```

## Other Useful Commands

```bash
# View logs
docker-compose logs

# Stop and remove volumes
docker-compose down -v
```

## Benefits of Docker Compose

- **Single command to start all services**
- **Automatic network creation**
- Easy configuration management
- Declarative infrastructure

## Running the Ingestion Script with Docker Compose

If you want to re-run the dockerized ingest script when you run Postgres and pgAdmin with `docker-compose`, you will have to find the name of the virtual network that Docker compose created for the containers.

```bash
# check the network link:
docker network ls

# it's pipeline_default (or similar based on directory name)
# now run the script:
docker run -it \
  --network=pipeline_default \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-pass=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips
```

```bash
@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework (main) $ docker network ls
NETWORK ID     NAME               DRIVER    SCOPE
0ad5357d8002   bridge             bridge    local
80910d3c31e4   host               host      local
d63d0532dd37   none               null      local
a4dabf2880a5   pg-network         bridge    local
e4446493a9e8   pipeline_default   bridge    local



@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework (main) $ docker run -it \
  --network=pipeline_default \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-pass=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips
14it [02:28, 10.63s/it]




@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ docker-compose down
[+] Running 3/3
 ✔ Container pipeline-pgdatabase-1  Removed                                                                                                 0.1s 
 ✔ Container pipeline-pgadmin-1     Removed                                                                                                 0.1s 
 ✔ Network pipeline_default         Removed    
```

* Kai remarks
  * Create default network - created (at the start) and deleted (at the end) automatically by Docker Compose
    * **If we do not specify the network in the `docker-compose.yaml file`**, the default network created by Docker Compose will be named based on the directory name with `_default` suffix.
    * In this case, since the directory is named `pipeline`, the network created is `pipeline_default`.
    * **However in this new network, there is no data in the DB yet, as it is in a different network from the previous one where we ingested data (`pg-network`).**
  * Reuse existing network - `pg-network`
    * Add `networks` section to the `docker-compose.yaml` file and reuse our existing `pg-network`
    * In `yaml file`, update the services to use this custom `pg-network`
    * After you login, you can see our ingested data from following instructions in `08-dockerizing-ingestion.md`



**[↑ Up](README.md)** | **[← Previous](08-dockerizing-ingestion.md)** | **[Next →](10-sql-refresher.md)**
