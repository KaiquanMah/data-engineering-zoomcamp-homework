# pgAdmin - Database Management Tool

**[↑ Up](README.md)** | **[← Previous](06-ingestion-script.md)** | **[Next →](08-dockerizing-ingestion.md)**

`pgcli` is a handy tool but it's cumbersome to use for complex queries and database management. [`pgAdmin` is a web-based tool](https://www.pgadmin.org/) that makes it more convenient to access and manage our databases.

It's possible to run pgAdmin as a container along with the Postgres container, but both containers will have to be in the **same _virtual network_ so that they can find each other.**

## Run pgAdmin Container

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  dpage/pgadmin4
```

The `-v pgadmin_data:/var/lib/pgadmin` volume mapping saves pgAdmin settings (server connections, preferences) so you don't have to reconfigure it every time you restart the container.

### Parameters Explained

* The container needs 2 environment variables: a login email and a password. We use `admin@admin.com` and `root` in this example.
* pgAdmin is a web app and its default port is 80; we map it to 8085 in our localhost to avoid any possible conflicts.
* The actual image name is `dpage/pgadmin4`.

**Note:** This won't work yet because pgAdmin can't see the PostgreSQL container. They need to be on the same Docker network!






## Docker Networks

Let's create a virtual Docker network called `pg-network`:

```bash
docker network create pg-network


@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework (main) $ docker network create pg-network
930ce7e5330d0c2b1c09d18237cb32d07c8ba4b395a89a71d575f41232e257ea
```

> You can remove the network later with the command `docker network rm pg-network`. You can look at the existing networks with `docker network ls`.

```bash
@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework (main) $ docker network ls
NETWORK ID     NAME         DRIVER    SCOPE
fa27f6eb3e7d   bridge       bridge    local
80910d3c31e4   host         host      local
d63d0532dd37   none         null      local
930ce7e5330d   pg-network   bridge    local
```




### Run Containers on the Same Network

Stop both containers and re-run them with the network configuration:

```bash
cd 01-docker-terraform/docker-sql/pipeline/
docker stop pgadmin pgdatabase
docker rm pgadmin pgdatabase


# Run PostgreSQL on the network
# added network - same network for both docker containers
#       name - to identify DB or pgadmin
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  --network=pg-network \
  --name pgdatabase \
  postgres:18

# In another terminal, run pgAdmin on the same network
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

* Check where volumes are persisted, for docker containers to store information across sessions
```bash
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


@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework (main) $ docker volume inspect pgadmin_data
[
    {
        "CreatedAt": "2026-01-18T10:37:43Z",
        "Driver": "local",
        "Labels": null,
        "Mountpoint": "/var/lib/docker/volumes/pgadmin_data/_data",
        "Name": "pgadmin_data",
        "Options": null,
        "Scope": "local"
    }
]
```

* Just like with the Postgres container, we specify a network and a name for pgAdmin.
* The container names (`pgdatabase` and `pgadmin`) allow the containers to find each other within the network.





## Connect pgAdmin to PostgreSQL

You should now be able to load pgAdmin on a web browser by browsing to `http://localhost:8085`. Use the same email and password you used for running the container to log in.

1. Open browser and go to `http://localhost:8085`
2. Login with email: `admin@admin.com`, password: `root`
3. Right-click "Servers" → Register → Server
4. Configure:
   - **General tab**: Name: `Local Docker`
   - **Connection tab**:
     - Host: `pgdatabase` (the container name)
     - Port: `5432`
     - Username: `root`
     - Password: `root`
5. Save

Now you can explore the database using the pgAdmin interface!

### Actual pgadmin connection experience - 2026.01.18 Multiple tries - still with white screen issue after login
* Webpage loads
* Logged in
* Browser shows a white screen
  * Even in incognito mode
  * Even in a different browser

* Debug
  * ✅ Login succeeds (302 redirect after POST /authenticate/login)
  * ✅ Browser page loads (200 for /browser/)
  * ✅ All JS/CSS files load properly
  * ❌ API calls fail with 401 Unauthorized - This is why you get a white screen
    * GitHub Codespaces uses a reverse proxy setup where:
      * The port number (8085) is embedded in the hostname
      * pgAdmin doesn't know it's behind a proxy
      * Session cookies are set for the wrong domain/path
      * Authentication headers get stripped or don't match
  * ```bash
    GET /browser/ HTTP/1.1" 200 2933  # ✅ Page loads
    GET /preferences/get_all HTTP/1.1" 401 130  # ❌ Session missing
    GET /misc/bgprocess/ HTTP/1.1" 401 130  # ❌ Session missing  
    GET /browser/check_corrupted_db_file HTTP/1.1" 401 130  # ❌ Session missing
    ```

* stop pgadmin container, and run pgadmin container using more information in the code below
```bash
docker stop pgadmin
docker rm pgadmin


docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -e SCRIPT_NAME="/" \
  -e PGADMIN_CONFIG_SERVER_MODE=True \
  -e PGADMIN_CONFIG_SESSION_COOKIE_DOMAIN='".app.github.dev"' \
  -e PGADMIN_CONFIG_SESSION_COOKIE_SECURE=True \
  -e PGADMIN_CONFIG_SESSION_COOKIE_SAMESITE='"None"' \
  -e PGADMIN_CONFIG_UPGRADE_CHECK_ENABLED=False \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```
|Environment Variable|Purpose|
|--------------------|-------|
|SCRIPT_NAME="/"| Tells pgAdmin it's at the root path behind proxy|
|PGADMIN_CONFIG_SERVER_MODE=True| Enables proper reverse proxy handling, otherwise pgAdmin defaults to standalone mode|
|PGADMIN_CONFIG_SESSION_COOKIE_DOMAIN='".app.github.dev"'| Sets cookie domain for GitHub's infrastructure. Otherwise session cookies cant send back to the server and we see 401 errors on API calls after login. pgAdmin evaluates environment variables starting with PGADMIN_CONFIG_ as Python expressions, so the value needs to be wrapped in '' quotes within the environment variable|
|PGADMIN_CONFIG_SESSION_COOKIE_SECURE=True| Required for HTTPS connections|
|PGADMIN_CONFIG_SESSION_COOKIE_SAMESITE='"None"'| Allows cookies across different contexts|
|PGADMIN_CONFIG_UPGRADE_CHECK_ENABLED=False| Prevents unnecessary HTTP calls that can fail in container environments. Improves startup speed and reduces network errors|



### Actual pgadmin connection experience - 2026.01.19 Fix
* Issue - After login, the session cookie is not being maintained due to GitHub Codespaces' reverse proxy
```bash
"POST /authenticate/login HTTP/1.1" 302 205  ← Login succeeds
"GET /browser/ HTTP/1.1" 200 2933             ← Page loads
"GET /preferences/get_all HTTP/1.1" 401       ← ❌ Session lost!
"GET /browser/check_corrupted_db_file HTTP/1.1" 401  ← ❌ Unauthorized
```
* Terminal 1 - remove 2 old containers AND old pgadmin_data volume
```bash
@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ docker rm -f pgadmin pgdatabase
pgadmin
pgdatabase
@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ docker volume rm pgadmin_data
Error response from daemon: remove pgadmin_data: volume is in use - [d851705cf81d6dde2fc0a6a82faa1240b399538d898bbc02a936fb9aeb8d8454]

# Find container using and having a 'resource lock' on the pgadmin_data volume
@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ docker ps -a --filter volume=pgadmin_data
CONTAINER ID   IMAGE            COMMAND            CREATED        STATUS                    PORTS     NAMES
d851705cf81d   dpage/pgadmin4   "/entrypoint.sh"   16 hours ago   Exited (0) 16 hours ago             fervent_booth
# Force remove ALL stopped containers
@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ docker container prune -f
Deleted Containers:
d851705cf81d6dde2fc0a6a82faa1240b399538d898bbc02a936fb9aeb8d8454

Total reclaimed space: 464B
# Now remove the volume
@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ docker volume rm pgadmin_data
pgadmin_data


# Terminal 1 - rerun postgres container
@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pgdatabase \
  postgres:13
Unable to find image 'postgres:13' locally
13: Pulling from library/postgres
d7ecded7702a: Pull complete 
80e8d95fdf53: Pull complete 
fcfd49225910: Pull complete 
947bdcac0ea3: Pull complete 
097f34b018c0: Pull complete 
4d2c7a7b3dba: Pull complete 
8cb000c698bc: Pull complete 
ba168ff08d42: Pull complete 
bad194149a82: Pull complete 
5f1cded65589: Pull complete 
7d0650bb210f: Pull complete 
23a39b1003e9: Pull complete 
21f7a31efcb7: Pull complete 
ae52c8ce1a35: Pull complete 
Digest: sha256:4689940c683801b4ab839ab3b0a0a3555a5fe425371422310944e89eca7d8068
Status: Downloaded newer image for postgres:13
The files belonging to this database system will be owned by user "postgres".
This user must also own the server process.

The database cluster will be initialized with locale "en_US.utf8".
The default database encoding has accordingly been set to "UTF8".
The default text search configuration will be set to "english".

Data page checksums are disabled.

initdb: error: directory "/var/lib/postgresql/data" exists but is not empty
If you want to create a new database system, either remove or empty
the directory "/var/lib/postgresql/data" or run initdb
with an argument other than "/var/lib/postgresql/data".
```
* Terminal 2 - Rerun pgadmin container with additional environment variables to disable enhanced cookie protection and CSRF protection
```bash
@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework (main) $ docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -e PGADMIN_CONFIG_ENHANCED_COOKIE_PROTECTION="False" \
  -e PGADMIN_CONFIG_WTF_CSRF_ENABLED="False" \
  -e PGADMIN_CONFIG_WTF_CSRF_SSL_STRICT="False" \
  -e PGADMIN_CONFIG_WTF_CSRF_TIME_LIMIT="None" \
  -e PGADMIN_CONFIG_PROXY_X_FOR_COUNT=1 \
  -e PGADMIN_CONFIG_PROXY_X_PROTO_COUNT=1 \
  -e PGADMIN_CONFIG_PROXY_X_HOST_COUNT=1 \
  -e PGADMIN_CONFIG_PROXY_X_PORT_COUNT=1 \
  -e PGADMIN_CONFIG_PROXY_X_PREFIX_COUNT=1 \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4




email config is {'CHECK_EMAIL_DELIVERABILITY': False, 'ALLOW_SPECIAL_EMAIL_DOMAINS': [], 'GLOBALLY_DELIVERABLE': True}
NOTE: Configuring authentication for SERVER mode.

/venv/lib/python3.14/site-packages/sshtunnel.py:1040: SyntaxWarning: 'return' in a 'finally' block
  return (ssh_host,
pgAdmin 4 - Application Initialisation
======================================

postfix/postfix-script: starting the Postfix mail system
[2026-01-19 02:59:34 +0000] [1] [INFO] Starting gunicorn 23.0.0
[2026-01-19 02:59:34 +0000] [1] [INFO] Listening at: http://[::]:80 (1)
[2026-01-19 02:59:34 +0000] [1] [INFO] Using worker: gthread
[2026-01-19 02:59:34 +0000] [133] [INFO] Booting worker with pid: 133


/venv/lib/python3.14/site-packages/sshtunnel.py:1040: SyntaxWarning: 'return' in a 'finally' block
  return (ssh_host,
180.129.75.2 - - [19/Jan/2026:03:01:09 +0000] "GET / HTTP/1.1" 302 213 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:09 +0000] "GET /login?next=/ HTTP/1.1" 200 2495 "-" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:09 +0000] "GET /tools/translations.js?ver=91100 HTTP/1.1" 200 321 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/login?next=/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:09 +0000] "GET /browser/js/endpoints.js?ver=91100 HTTP/1.1" 200 16662 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/login?next=/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:18 +0000] "POST /authenticate/login HTTP/1.1" 302 205 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/login?next=/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:18 +0000] "GET /browser/ HTTP/1.1" 200 2933 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/login?next=/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:19 +0000] "GET /browser/browser.css?ver=91100 HTTP/1.1" 200 4180 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:19 +0000] "GET /browser/js/messages.js?ver=91100 HTTP/1.1" 200 883 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:19 +0000] "GET /tools/translations.js?ver=91100 HTTP/1.1" 200 321 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:19 +0000] "GET /browser/js/utils.js?ver=91100 HTTP/1.1" 200 2025 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:19 +0000] "GET /user_management/current_user.js?ver=91100 HTTP/1.1" 200 475 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:19 +0000] "GET /browser/server/supported_servers.js?ver=91100 HTTP/1.1" 200 291 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:19 +0000] "GET /browser/js/endpoints.js?ver=91100 HTTP/1.1" 200 3738 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:20 +0000] "GET /browser/check_corrupted_db_file HTTP/1.1" 200 61 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:20 +0000] "GET /misc/bgprocess/ HTTP/1.1" 200 2 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:20 +0000] "GET /preferences/get_all HTTP/1.1" 200 11809 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:20 +0000] "GET /settings/get_tree_state/ HTTP/1.1" 200 0 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:21 +0000] "GET /browser/nodes/ HTTP/1.1" 200 273 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:21 +0000] "POST /browser/master_password HTTP/1.1" 200 166 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:21 +0000] "GET /sqleditor/new_connection_dialog HTTP/1.1" 200 130 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:21 +0000] "GET /static/js/generated/fonts/fa-solid-900..woff2 HTTP/1.1" 200 0 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/static/js/generated/style.css?ver=91100" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:21 +0000] "GET /sqleditor/new_connection_dialog HTTP/1.1" 200 130 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:21 +0000] "GET /sqleditor/new_connection_dialog HTTP/1.1" 200 130 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:21 +0000] "GET /sqleditor/new_connection_dialog HTTP/1.1" 200 130 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:21 +0000] "GET /settings/object_explorer_filter HTTP/1.1" 200 95 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:21 +0000] "GET /browser/server_group/static/img/server_group.svg?ver=91100 HTTP/1.1" 200 0 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/browser.css?ver=91100" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:21 +0000] "GET /static/js/generated/fonts/fa-regular-400..woff2 HTTP/1.1" 200 0 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/static/js/generated/style.css?ver=91100" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:22 +0000] "GET /misc/upgrade_check?trigger_update_check=false HTTP/1.1" 200 77 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:51 +0000] "POST /settings/save_tree_state/ HTTP/1.1" 200 63 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:01:51 +0000] "GET /settings/get_tree_state/ HTTP/1.1" 200 2 "https://expert-waddle-v6w4g64w564wc7wv-8085.app.github.dev/browser/" "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0"
180.129.75.2 - - [19/Jan/2026:03:06:20 +0000] "POST /misc/cleanup HTTP/1.1" 200 0 "https://e
```
* Then in codespace >> ports >> 8085 >> public >> copy URL and open in new browser tab
* Login >> Now pgadmin loads properly after login


|Environment Variable|Purpose|
|--------------------|-------|
|PGADMIN_CONFIG_ENHANCED_COOKIE_PROTECTION="False"| **Disables enhanced cookie protection which can interfere with reverse proxy setups**. GitHub Codespaces uses a complex reverse proxy setup with domain names like expert-waddle-v6w4g64w564wc7wv-<portNumber>.app.github.dev. Enhanced cookie protection blocks cookies when the domain doesn't match exactly. Without this, session cookies were being rejected → API calls failed with 401 errors|
|PGADMIN_CONFIG_WTF_CSRF_ENABLED="False"| Disables CSRF protection which can block requests in certain proxy scenarios. Your browser sends: `Origin: https://expert-waddle-...-8085.app.github.dev`. pgAdmin expects: `Origin: http://localhost:80`|
|PGADMIN_CONFIG_WTF_CSRF_SSL_STRICT="False"| Disables strict SSL checking for CSRF tokens. External (you → proxy): HTTPS on port 443. Internal (proxy → container): HTTP on port 80. pgAdmin sees HTTP but CSRF expects HTTPS → Fails|
|PGADMIN_CONFIG_WTF_CSRF_TIME_LIMIT="None"| Disables time limit on CSRF tokens to prevent expiration issues|
|PGADMIN_CONFIG_PROXY_X_FOR_COUNT=1| Configures pgAdmin to trust 1st proxy layer's headers in the X-Forwarded-For header. Otherwise GitHub Codespaces has multiple proxy layers between browser and container. pgAdmin needs to understand: The **real client IP from X-Forwarded-For header** (not the proxy IP), that the connection is actually **HTTPS (not HTTP) from X-Forwarded-Proto header**, and the **correct hostname from X-Forwarded-Host header** being used |
|PGADMIN_CONFIG_PROXY_X_PROTO_COUNT=1| Configures pgAdmin to trust 1st proxy layer's headers in the X-Forwarded-Proto header|
|PGADMIN_CONFIG_PROXY_X_HOST_COUNT=1| Configures pgAdmin to trust 1st proxy layer's headers in the X-Forwarded-Host header|
|PGADMIN_CONFIG_PROXY_X_PORT_COUNT=1| Configures pgAdmin to trust 1st proxy layer's headers in the **X-Forwarded-Port header (get original port)**|
|PGADMIN_CONFIG_PROXY_X_PREFIX_COUNT=1| Configures pgAdmin to trust 1st proxy layer's headers in the **X-Forwarded-Prefix header (get URL prefix path)**|

* Logs after fix
```bash
"GET /browser/check_corrupted_db_file HTTP/1.1" 200 61  // ✅ Success!
"GET /misc/bgprocess/ HTTP/1.1" 200 2                    // ✅ Success!
"GET /preferences/get_all HTTP/1.1" 200 11809            // ✅ Success!
```
* Why GitHub Codespaces Specifically Causes This Issue
The Proxy Chain Problem:
```bash
Browser → GitHub Edge (HTTPS) → Codespace Proxy → Docker Container (HTTP)
```
* Protocol Switch: HTTPS (external) → HTTP (internal container)
* Domain Mismatch: *.app.github.dev vs container's internal hostname
* Header Modification: Proxy adds/changes headers that security features check

|Security Feature|What it expects|What proxy provides|Result|
|----------------|---------------|-------------------|------|
|Session cookies|Same domain|Different domain|❌ Rejected|
|CSRF tokens|Same protocol/domain|HTTPS → HTTP, different domain|❌ Blocked|
|IP validation|Real client IP|Proxy IP|❌ Failures|


**[↑ Up](README.md)** | **[← Previous](06-ingestion-script.md)** | **[Next →](08-dockerizing-ingestion.md)**
