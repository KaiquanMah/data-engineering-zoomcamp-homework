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

### Actual pgadmin connection experience
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



**[↑ Up](README.md)** | **[← Previous](06-ingestion-script.md)** | **[Next →](08-dockerizing-ingestion.md)**
