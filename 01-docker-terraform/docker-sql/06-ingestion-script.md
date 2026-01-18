# Creating the Data Ingestion Script

**[↑ Up](README.md)** | **[← Previous](05-data-ingestion.md)** | **[Next →](07-pgadmin.md)**

Now let's convert the notebook to a Python script.

## Convert Notebook to Script

```bash
uv run jupyter nbconvert --to=script notebook.ipynb
mv notebook.py ingest_data.py
```
* KAI - my notebook was created in jupyterlab with the required name in the pipeline folder path
```bash
01-docker-terraform/docker-sql/pipeline/05-data-ingestion-workings.ipynb
```



## The Complete Ingestion Script

See the `pipeline/` directory for the complete script with click integration. Here's the core structure:

```python
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

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
```

## Click Integration

The script uses `click` for command-line argument parsing:

```python
import click

@click.command()
@click.option('--user', default='root', help='PostgreSQL user')
@click.option('--password', default='root', help='PostgreSQL password')
@click.option('--host', default='localhost', help='PostgreSQL host')
@click.option('--port', default=5432, type=int, help='PostgreSQL port')
@click.option('--db', default='ny_taxi', help='PostgreSQL database name')
@click.option('--table', default='yellow_taxi_data', help='Target table name')
def ingest_data(user, password, host, port, db, table):
    # Ingestion logic here
    pass
```

## Running the Script

The script reads data in chunks (100,000 rows at a time) to handle large files efficiently without running out of memory.

Example usage:

```bash
uv run python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table=yellow_taxi_trips
```

* actual run
```bash
@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ uv run python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table=yellow_taxi_trips
Usage: ingest_data.py [OPTIONS]
Try 'ingest_data.py --help' for help.

Error: No such option: --user (Possible options: --pg-user, --year)





# start docker img if u restarted ur VM
cd 01-docker-terraform/docker-sql/pipeline

docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18


uv run python ingest_data.py \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=yellow_taxi_trips
```

* run1 - docker with postgres DB is still initialising, so it is not accepting connections yet
```bash
@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ uv run python ingest_data.py   --pg-user=root   --pg-pass=root   --pg-host=localhost   --pg-port=5432   --pg-db=ny_taxi   --target-table=yellow_taxi_trips
0it [00:00, ?it/s]
Traceback (most recent call last):
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ~~~~~~~~~~~~~~~~~~~~~^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 3309, in raw_connection
    return self.pool.connect()
           ~~~~~~~~~~~~~~~~~^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/pool/base.py", line 447, in connect
    return _ConnectionFairy._checkout(self)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
    rec = pool._do_get()
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
    with util.safe_reraise():
         ~~~~~~~~~~~~~~~~~^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
    return self._create_connection()
           ~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
    return _ConnectionRecord(self)
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
    self.__connect()
    ~~~~~~~~~~~~~~^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
    with util.safe_reraise():
         ~~~~~~~~~~~~~~~~~^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/engine/create.py", line 661, in connect
    return dialect.connect(*cargs, **cparams)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/engine/default.py", line 630, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
           ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/psycopg2/__init__.py", line 122, in connect
    conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
psycopg2.OperationalError: connection to server at "localhost" (::1), port 5432 failed: FATAL:  the database system is not yet accepting connections
DETAIL:  Consistent recovery state has not been yet reached.





The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/ingest_data.py", line 77, in <module>
    run()
    ~~~^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/click/core.py", line 1485, in __call__
    return self.main(*args, **kwargs)
           ~~~~~~~~~^^^^^^^^^^^^^^^^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/click/core.py", line 1406, in main
    rv = self.invoke(ctx)
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/click/core.py", line 1269, in invoke
    return ctx.invoke(self.callback, **ctx.params)
           ~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/click/core.py", line 824, in invoke
    return callback(*args, **kwargs)
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/ingest_data.py", line 63, in run
    df_chunk.head(0).to_sql(
    ~~~~~~~~~~~~~~~~~~~~~~~^
        name=target_table,
        ^^^^^^^^^^^^^^^^^^
        con=engine,
        ^^^^^^^^^^^
        if_exists='replace'
        ^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/pandas/util/_decorators.py", line 333, in wrapper
    return func(*args, **kwargs)
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/pandas/core/generic.py", line 3109, in to_sql
    return sql.to_sql(
           ~~~~~~~~~~^
        self,
        ^^^^^
    ...<8 lines>...
        method=method,
        ^^^^^^^^^^^^^^
    )
    ^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/pandas/io/sql.py", line 843, in to_sql
    with pandasSQL_builder(con, schema=schema, need_transaction=True) as pandas_sql:
         ~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/pandas/io/sql.py", line 908, in pandasSQL_builder
    return SQLDatabase(con, schema, need_transaction)
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/pandas/io/sql.py", line 1648, in __init__
    con = self.exit_stack.enter_context(con.connect())
                                        ~~~~~~~~~~~^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 3285, in connect
    return self._connection_cls(self)
           ~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 145, in __init__
    Connection._handle_dbapi_exception_noconnection(
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^
        err, dialect, engine
        ^^^^^^^^^^^^^^^^^^^^
    )
    ^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 2448, in _handle_dbapi_exception_noconnection
    raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 143, in __init__
    self._dbapi_connection = engine.raw_connection()
                             ~~~~~~~~~~~~~~~~~~~~~^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/engine/base.py", line 3309, in raw_connection
    return self.pool.connect()
           ~~~~~~~~~~~~~~~~~^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/pool/base.py", line 447, in connect
    return _ConnectionFairy._checkout(self)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/pool/base.py", line 1264, in _checkout
    fairy = _ConnectionRecord.checkout(pool)
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/pool/base.py", line 711, in checkout
    rec = pool._do_get()
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/pool/impl.py", line 177, in _do_get
    with util.safe_reraise():
         ~~~~~~~~~~~~~~~~~^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/pool/impl.py", line 175, in _do_get
    return self._create_connection()
           ~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/pool/base.py", line 388, in _create_connection
    return _ConnectionRecord(self)
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/pool/base.py", line 673, in __init__
    self.__connect()
    ~~~~~~~~~~~~~~^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/pool/base.py", line 899, in __connect
    with util.safe_reraise():
         ~~~~~~~~~~~~~~~~~^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/util/langhelpers.py", line 224, in __exit__
    raise exc_value.with_traceback(exc_tb)
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/pool/base.py", line 895, in __connect
    self.dbapi_connection = connection = pool._invoke_creator(self)
                                         ~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/engine/create.py", line 661, in connect
    return dialect.connect(*cargs, **cparams)
           ~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/sqlalchemy/engine/default.py", line 630, in connect
    return self.loaded_dbapi.connect(*cargs, **cparams)  # type: ignore[no-any-return]  # NOQA: E501
           ~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^
  File "/workspaces/data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline/.venv/lib/python3.13/site-packages/psycopg2/__init__.py", line 122, in connect
    conn = _connect(dsn, connection_factory=connection_factory, **kwasync)
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) connection to server at "localhost" (::1), port 5432 failed: FATAL:  the database system is not yet accepting connections
DETAIL:  Consistent recovery state has not been yet reached.

(Background on this error at: https://sqlalche.me/e/20/e3q8  )
```

* run2 - rerun cmd after Docker img containing postgres DB has fully initialised
```bash
uv run python ingest_data.py \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=yellow_taxi_trips

14it [01:59,  8.55s/it]
```





**[↑ Up](README.md)** | **[← Previous](05-data-ingestion.md)** | **[Next →](07-pgadmin.md)**
