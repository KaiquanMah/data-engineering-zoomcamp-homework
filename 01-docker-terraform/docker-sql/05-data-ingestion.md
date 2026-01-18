# NY Taxi Dataset and Data Ingestion

**[↑ Up](README.md)** | **[← Previous](04-postgres-docker.md)** | **[Next →](06-ingestion-script.md)**

We will now create a Jupyter Notebook `notebook.ipynb` file which we will use to read a CSV file and export it to Postgres.

## Setting up Jupyter

Install Jupyter:

```bash
uv add --dev jupyter
```

* **Alternatively, install all the dev dependencies at 1 go**
```bash
uv sync --dev
```

Let's create a Jupyter notebook to explore the data:

```bash
uv run jupyter notebook



@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ uv sync --dev
Resolved 120 packages in 0.67ms
Audited 115 packages in 1ms


@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ uv run jupyter notebook
[I 2026-01-18 07:49:37.686 ServerApp] jupyter_lsp | extension was successfully linked.
[I 2026-01-18 07:49:37.689 ServerApp] jupyter_server_terminals | extension was successfully linked.
[W 2026-01-18 07:49:37.690 LabApp] 'allow_origin' has moved from NotebookApp to ServerApp. This config will be passed to ServerApp. Be sure to update your config before our next release.
[I 2026-01-18 07:49:37.692 ServerApp] jupyterlab | extension was successfully linked.
[I 2026-01-18 07:49:37.697 ServerApp] notebook | extension was successfully linked.
[I 2026-01-18 07:49:37.726 ServerApp] Writing Jupyter server cookie secret to /home/codespace/.local/share/jupyter/runtime/jupyter_cookie_secret
[I 2026-01-18 07:49:38.463 ServerApp] notebook_shim | extension was successfully linked.
[I 2026-01-18 07:49:38.498 ServerApp] notebook_shim | extension was successfully loaded.
[I 2026-01-18 07:49:38.500 ServerApp] jupyter_lsp | extension was successfully loaded.
[I 2026-01-18 07:49:38.501 ServerApp] jupyter_server_terminals | extension was successfully loaded.
[I 2026-01-18 07:49:38.511 LabApp] JupyterLab extension loaded from /workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/jupyterlab
[I 2026-01-18 07:49:38.511 LabApp] JupyterLab application directory is /workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/share/jupyter/lab
[I 2026-01-18 07:49:38.512 LabApp] Extension Manager is 'pypi'.
[I 2026-01-18 07:49:38.595 ServerApp] jupyterlab | extension was successfully loaded.
[I 2026-01-18 07:49:38.598 ServerApp] notebook | extension was successfully loaded.
[I 2026-01-18 07:49:38.599 ServerApp] Serving notebooks from local directory: /workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline
[I 2026-01-18 07:49:38.599 ServerApp] Jupyter Server 2.17.0 is running at:
[I 2026-01-18 07:49:38.599 ServerApp] http://localhost:8888/tree?token=93f8bad4c5a5d3a23cbf7ea8e521a38636f801d7102a0037
[I 2026-01-18 07:49:38.599 ServerApp]     http://127.0.0.1:8888/tree?token=93f8bad4c5a5d3a23cbf7ea8e521a38636f801d7102a0037
[I 2026-01-18 07:49:38.599 ServerApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 2026-01-18 07:49:38.611 ServerApp] 
    
    To access the server, open this file in a browser:
        file:///home/codespace/.local/share/jupyter/runtime/jpserver-31968-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/tree?token=93f8bad4c5a5d3a23cbf7ea8e521a38636f801d7102a0037
        http://127.0.0.1:8888/tree?token=93f8bad4c5a5d3a23cbf7ea8e521a38636f801d7102a0037
[I 2026-01-18 07:49:39.440 ServerApp] Skipped non-installed server(s): basedpyright, bash-language-server, dockerfile-language-server-nodejs, javascript-typescript-langserver, jedi-language-server, julia-language-server, pyrefly, pyright, python-language-server, python-lsp-server, r-languageserver, sql-language-server, texlab, typescript-language-server, unified-language-server, vscode-css-languageserver-bin, vscode-html-languageserver-bin, vscode-json-languageserver-bin, yaml-language-server
```








## The NYC Taxi Dataset

We will use data from the [NYC TLC Trip Record Data website](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page).

Specifically, we will use the [Yellow taxi trip records CSV file for January 2021](https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz).

This data used to be csv, but later they switched to parquet. We want to keep using CSV because we need to do a bit of extra pre-processing (for the purposes of learning it).

A dictionary to understand each field is available [here](https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf).

> Note: The CSV data is stored as gzipped files. Pandas can read them directly.

## Explore the Data

Create a new notebook and run:

```python
import pandas as pd

# Read a sample of the data
prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
df = pd.read_csv(prefix + 'yellow_tripdata_2021-01.csv.gz', nrows=100)

# Display first rows
df.head()

# Check data types
df.dtypes

# Check data shape
df.shape
```

### Handling Data Types

We have a warning:

```
/tmp/ipykernel_25483/2933316018.py:1: DtypeWarning: Columns (6) have mixed types. Specify dtype option on import or set low_memory=False.
```

So we need to specify the types:

```python
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

df = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    nrows=100,
    dtype=dtype,
    parse_dates=parse_dates
)
```

## Ingesting Data into Postgres

In the Jupyter notebook, we create code to:
1. Download the CSV file
2. Read it in chunks with pandas
3. Convert datetime columns
4. Insert data into PostgreSQL using SQLAlchemy


### Install SQLAlchemy

```bash
uv add sqlalchemy psycopg2-binary
```

### Create Database Connection

```python
from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
```

### Get DDL Schema

```python
print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))
```

Output:

```sql
CREATE TABLE yellow_taxi_data (
    "VendorID" BIGINT,
    tpep_pickup_datetime TIMESTAMP WITHOUT TIME ZONE,
    tpep_dropoff_datetime TIMESTAMP WITHOUT TIME ZONE,
    passenger_count BIGINT,
    trip_distance FLOAT(53),
    "RatecodeID" BIGINT,
    store_and_fwd_flag TEXT,
    "PULocationID" BIGINT,
    "DOLocationID" BIGINT,
    payment_type BIGINT,
    fare_amount FLOAT(53),
    extra FLOAT(53),
    mta_tax FLOAT(53),
    tip_amount FLOAT(53),
    tolls_amount FLOAT(53),
    improvement_surcharge FLOAT(53),
    total_amount FLOAT(53),
    congestion_surcharge FLOAT(53)
)
```

### Create the Table

```python
df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')
```

`head(n=0)` makes sure we only create the table, we don't add any data yet.

## Ingesting Data in Chunks

We don't want to insert all the data at once. Let's do it in batches and use an iterator for that:

```python
df_iter = pd.read_csv(
    ...
    iterator=True,
    chunksize=100000
)
```

### Iterate Over Chunks

```python
for df_chunk in df_iter:
    print(len(df_chunk))
```

### Inserting Data

```python
df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')
```

### Complete Ingestion Loop

```python
first = True

for df_chunk in df_iter:

    if first:
        # Create table schema (no data)
        df_chunk.head(0).to_sql(
            name="yellow_taxi_data",
            con=engine,
            if_exists="replace"
        )
        first = False
        print("Table created")

    # Insert chunk
    df_chunk.to_sql(
        name="yellow_taxi_data",
        con=engine,
        if_exists="append"
    )

    print("Inserted:", len(df_chunk))
```

### Alternative Approach (Without First Flag)

```python
first_chunk = next(df_iter)

first_chunk.head(0).to_sql(
    name="yellow_taxi_data",
    con=engine,
    if_exists="replace"
)

print("Table created")

first_chunk.to_sql(
    name="yellow_taxi_data",
    con=engine,
    if_exists="append"
)

print("Inserted first chunk:", len(first_chunk))

for df_chunk in df_iter:
    df_chunk.to_sql(
        name="yellow_taxi_data",
        con=engine,
        if_exists="append"
    )
    print("Inserted chunk:", len(df_chunk))
```

## Adding Progress Bar

Add `tqdm` to see progress:

```bash
uv add tqdm
```

Put it around the iterable:

```python
from tqdm.auto import tqdm

for df_chunk in tqdm(df_iter):
    ...
```

## Verify the Data

Connect to it using pgcli:

```bash
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

``bash
@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ uv run pgcli -h localhost -p 5432 -u root -d ny_taxi


Password for root: 
Using local time zone Etc/UTC (server uses Etc/UTC)
Use `set time zone <TZ>` to override, or set `use_local_timezone = False` in the config
Server: PostgreSQL 18.1 (Debian 18.1-1.pgdg13+2)
Version: 4.3.0
Home: http://pgcli.com



root@localhost:ny_taxi> \dt
+--------+------------------+-------+-------+
| Schema | Name             | Type  | Owner |
|--------+------------------+-------+-------|
| public | test             | table | root  |
| public | yellow_taxi_data | table | root  |
+--------+------------------+-------+-------+
SELECT 2
Time: 0.080s




root@localhost:ny_taxi> SELECT COUNT(1) FROM yellow_taxi_data;
+---------+
| count   |
|---------|
| 1369765 |
+---------+
SELECT 1
Time: 0.162s






root@localhost:ny_taxi> SELECT * FROM yellow_taxi_data LIMIT 10;
+-------+----------+----------------------+-----------------------+-----------------+---------------+------------+--------------------+------->
| index | VendorID | tpep_pickup_datetime | tpep_dropoff_datetime | passenger_count | trip_distance | RatecodeID | store_and_fwd_flag | PULoca>
|-------+----------+----------------------+-----------------------+-----------------+---------------+------------+--------------------+------->
| 0     | 1        | 2021-01-01 00:30:10  | 2021-01-01 00:36:12   | 1               | 2.1           | 1          | N                  | 142   >
| 1     | 1        | 2021-01-01 00:51:20  | 2021-01-01 00:52:19   | 1               | 0.2           | 1          | N                  | 238   >
| 2     | 1        | 2021-01-01 00:43:30  | 2021-01-01 01:11:06   | 1               | 14.7          | 1          | N                  | 132   >
| 3     | 1        | 2021-01-01 00:15:48  | 2021-01-01 00:31:01   | 0               | 10.6          | 1          | N                  | 138   >
| 4     | 2        | 2021-01-01 00:31:49  | 2021-01-01 00:48:21   | 1               | 4.94          | 1          | N                  | 68    >
| 5     | 1        | 2021-01-01 00:16:29  | 2021-01-01 00:24:30   | 1               | 1.6           | 1          | N                  | 224   >
| 6     | 1        | 2021-01-01 00:00:28  | 2021-01-01 00:17:28   | 1               | 4.1           | 1          | N                  | 95    >
| 7     | 1        | 2021-01-01 00:12:29  | 2021-01-01 00:30:34   | 1               | 5.7           | 1          | N                  | 90    >
| 8     | 1        | 2021-01-01 00:39:16  | 2021-01-01 01:00:13   | 1               | 9.1           | 1          | N                  | 97    >
| 9     | 1        | 2021-01-01 00:26:12  | 2021-01-01 00:39:46   | 2               | 2.7           | 1          | N                  | 263   >
+-------+----------+----------------------+-----------------------+-----------------+---------------+------------+--------------------+------->
SELECT 10

```



And explore the data.

**[↑ Up](README.md)** | **[← Previous](04-postgres-docker.md)** | **[Next →](06-ingestion-script.md)**
