#!/usr/bin/env python
# coding: utf-8
"""
Homework Ingestion Script
Ingests green taxi parquet and zone lookup CSV into PostgreSQL
"""

import os
import time
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError


def wait_for_postgres(engine, max_retries=30, delay=2):
    """Wait for PostgreSQL to be ready."""
    for i in range(max_retries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("PostgreSQL is ready!")
            return True
        except OperationalError:
            print(f"Waiting for PostgreSQL... ({i+1}/{max_retries})")
            time.sleep(delay)
    raise Exception("PostgreSQL not available after maximum retries")


def ingest_parquet(engine, filepath, table_name):
    """Ingest parquet file into PostgreSQL."""
    print(f"Reading parquet file: {filepath}")
    df = pd.read_parquet(filepath)
    print(f"Loaded {len(df)} rows from parquet")
    
    print(f"Ingesting into table: {table_name}")
    df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    print(f"Successfully ingested {len(df)} rows into {table_name}")


def ingest_csv(engine, filepath, table_name):
    """Ingest CSV file into PostgreSQL."""
    print(f"Reading CSV file: {filepath}")
    df = pd.read_csv(filepath)
    print(f"Loaded {len(df)} rows from CSV")
    
    print(f"Ingesting into table: {table_name}")
    df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    print(f"Successfully ingested {len(df)} rows into {table_name}")


def main():
    # PostgreSQL connection from environment variables
    pg_user = os.getenv('PG_USER', 'root')
    pg_pass = os.getenv('PG_PASS', 'root')
    pg_host = os.getenv('PG_HOST', 'pgdatabase')
    pg_port = os.getenv('PG_PORT', '5432')
    pg_db = os.getenv('PG_DB', 'ny_taxi')
    
    # Data directory (mounted from host)
    data_dir = os.getenv('DATA_DIR', '/data')
    
    # File paths
    parquet_file = os.path.join(data_dir, 'green_tripdata_2025-11.parquet')
    csv_file = os.path.join(data_dir, 'taxi_zone_lookup.csv')
    
    # Create engine
    conn_string = f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}'
    print(f"Connecting to PostgreSQL at {pg_host}:{pg_port}/{pg_db}")
    engine = create_engine(conn_string)
    
    # Wait for PostgreSQL
    wait_for_postgres(engine)
    
    # Ingest files
    if os.path.exists(parquet_file):
        ingest_parquet(engine, parquet_file, 'green_taxi_trips')
    else:
        print(f"WARNING: Parquet file not found: {parquet_file}")
    
    if os.path.exists(csv_file):
        ingest_csv(engine, csv_file, 'taxi_zone_lookup')
    else:
        print(f"WARNING: CSV file not found: {csv_file}")
    
    print("Ingestion complete!")


if __name__ == '__main__':
    main()
