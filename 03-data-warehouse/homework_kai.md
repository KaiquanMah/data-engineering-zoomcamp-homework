## [DRAFT] Module 3 Homework

ATTENTION: At the end of the submission form, you will be required to include a link to your GitHub repository or other public code-hosting site. 
This repository should contain your code for solving the homework. If your solution includes code that is not in file format (such as SQL queries or 
shell commands), please include these directly in the README file of your repository.

<b><u>Important Note:</b></u> <p> For this homework we will be using the Yellow Taxi Trip Records for **January 2024 - June 2024 NOT the entire year of data** 
Parquet Files from the New York
City Taxi Data found here: </br> https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page </br>
If you are using orchestration such as Kestra, Mage, Airflow or Prefect etc. do not load the data into Big Query using the orchestrator.</br> 
Stop with loading the files into a bucket. </br></br>

**Load Script:** You can manually download the parquet files and upload them to your GCS Bucket or you can use the linked script [here](./load_yellow_taxi_data.py):<br>
You will simply need to generate a Service Account with GCS Admin Priveleges or be authenticated with the Google SDK and update the bucket name in the script to the name of your bucket<br>
Nothing is fool proof so make sure that all 6 files show in your GCS Bucket before beginning.</br><br>

<u>NOTE:</u> You will need to use the PARQUET option files when creating an External Table</br>

<b>BIG QUERY SETUP:</b></br>
Create an external table using the Yellow Taxi Trip Records. </br>
Create a (regular/materialized) table in BQ using the Yellow Taxi Trip Records (do not partition or cluster this table). </br>
</p>



## Kai 2026.01.22 Setup Environment and Ingest Data into GCS
* bring 2025 cohort homework's .py file into `03-data-warehouse/load_yellow_taxi_data.py` to laod data into GCS
  * update `BUCKET_NAME`, `CREDENTIALS_FILE`
* create `pyproject.toml` for week 3's homework
* setup environment
```bash
@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework (main) $ python --version
Python 3.12.1



@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/03-data-warehouse (main) $ # Create a virtual environment in the current directory
python -m venv .venv
# Activate the virtual environment
source .venv/bin/activate



(.venv) @kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/03-data-warehouse (main) $ # Install uv if you don't have it
pip install uv

# Install dependencies from pyproject.toml
uv pip install -e .
Collecting uv
  Obtaining dependency information for uv from https://files.pythonhosted.org/packages/38/16/a07593a040fe6403c36f3b0a99b309f295cbfe19a1074dbadb671d5d4ef7/uv-0.9.26-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata
  Downloading uv-0.9.26-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
Downloading uv-0.9.26-py3-none-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (23.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 23.3/23.3 MB 21.5 MB/s eta 0:00:00
Installing collected packages: uv
Successfully installed uv-0.9.26

[notice] A new release of pip is available: 23.2.1 -> 25.3
[notice] To update, run: pip install --upgrade pip
warning: Failed to parse `pyproject.toml` during settings discovery:
  TOML parse error at line 8, column 5
    |
  8 |     google,
    |     ^^^^^^
  string values must be quoted, expected literal string

error: Failed to parse metadata from built wheel
  Caused by: Invalid `pyproject.toml`
  Caused by: TOML parse error at line 8, column 5
  |
8 |     google,
  |     ^^^^^^
string values must be quoted, expected literal string
(.venv) @kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/03-data-warehouse (main) $ uv pip install -e .
  × No solution found when resolving dependencies:
  ╰─▶ Because the current Python version (3.12.1) does not satisfy Python>=3.13 and data-warehouse==0.1.0 depends on Python>=3.13, we can conclude
      that data-warehouse==0.1.0 cannot be used.
      And because only data-warehouse==0.1.0 is available and you require data-warehouse, we can conclude that your requirements are unsatisfiable.





(.venv) @kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/03-data-warehouse (main) $ uv pip install -e .
Resolved 22 packages in 1.29s
      Built data-warehouse @ file:///workspaces/data-engineering-zoomcamp-homework/03-data-warehouse
Prepared 14 packages in 892ms
Uninstalled 1 package in 0.69ms
░░░░░░░░░░░░░░░░░░░░ [0/18] Installing wheels...                                                                                                       warning: Failed to hardlink files; falling back to full copy. This may lead to degraded performance.
         If the cache and target directories are on different filesystems, hardlinking may not be supported.
         If this is intentional, set `export UV_LINK_MODE=copy` or use `--link-mode=copy` to suppress this warning.
Installed 18 packages in 1.03s
 + certifi==2026.1.4
 + charset-normalizer==3.4.4
 ~ data-warehouse==0.1.0 (from file:///workspaces/data-engineering-zoomcamp-homework/03-data-warehouse)
 + google-api-core==2.29.0
 + google-auth==2.47.0
 + google-cloud-core==2.5.0
 + google-cloud-storage==3.8.0
 + google-crc32c==1.8.0
 + google-resumable-media==2.8.0
 + googleapis-common-protos==1.72.0
 + idna==3.11
 + proto-plus==1.27.0
 + protobuf==6.33.4
 + pyasn1==0.6.2
 + pyasn1-modules==0.4.2
 + requests==2.32.5
 + rsa==4.9.1
 + urllib3==2.6.3



 # Check that google-cloud-storage is installed
pip list | grep google-cloud-storage
google-cloud-storage     3.8.0
[notice] A new release of pip is available: 23.2.1 -> 25.3
[notice] To update, run: pip install --upgrade pip



# Or check the installed packages
pip freeze
beautifulsoup4==4.14.3
certifi==2026.1.4
charset-normalizer==3.4.4
-e git+https://github.com/KaiquanMah/data-engineering-zoomcamp-homework@0b21b5952cc1cc6f39f02c4bde72ec23e9526014#egg=data_warehouse&subdirectory=03-data-warehouse
google==3.0.0
google-api-core==2.29.0
google-auth==2.47.0
google-cloud-core==2.5.0
google-cloud-storage==3.8.0
google-crc32c==1.8.0
google-resumable-media==2.8.0
googleapis-common-protos==1.72.0
idna==3.11
proto-plus==1.27.0
protobuf==6.33.4
pyasn1==0.6.2
pyasn1_modules==0.4.2
requests==2.32.5
rsa==4.9.1
soupsieve==2.8.3
typing_extensions==4.15.0
urllib3==2.6.3
uv==0.9.26
```

* run the `load_yellow_taxi_data.py` script to download NYC yellow taxi data from Jan 2024 to Jun 2024, then upload to GCS
```bash
(.venv) @kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/03-data-warehouse (main) $ python load_yellow_taxi_data.py
Bucket 'kai-kestra' exists and belongs to your project. Proceeding...
Downloading https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet...
Downloading https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-02.parquet...
Downloading https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-03.parquet...
Downloading https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-04.parquet...
Downloaded: ./yellow_tripdata_2024-02.parquet
Downloading https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-05.parquet...
Downloaded: ./yellow_tripdata_2024-01.parquet
Downloading https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-06.parquet...
Downloaded: ./yellow_tripdata_2024-03.parquet
Downloaded: ./yellow_tripdata_2024-04.parquet
Downloaded: ./yellow_tripdata_2024-05.parquet
Downloaded: ./yellow_tripdata_2024-06.parquet


Bucket 'kai-kestra' exists and belongs to your project. Proceeding...
Uploading ./yellow_tripdata_2024-03.parquet to kai-kestra (Attempt 1)...
Bucket 'kai-kestra' exists and belongs to your project. Proceeding...
Uploading ./yellow_tripdata_2024-01.parquet to kai-kestra (Attempt 1)...
Bucket 'kai-kestra' exists and belongs to your project. Proceeding...
Uploading ./yellow_tripdata_2024-04.parquet to kai-kestra (Attempt 1)...
Bucket 'kai-kestra' exists and belongs to your project. Proceeding...
Uploading ./yellow_tripdata_2024-02.parquet to kai-kestra (Attempt 1)...
Uploaded: gs://kai-kestra/yellow_tripdata_2024-01.parquet
Uploaded: gs://kai-kestra/yellow_tripdata_2024-02.parquet
Verification successful for yellow_tripdata_2024-01.parquet
Verification successful for yellow_tripdata_2024-02.parquet
Bucket 'kai-kestra' exists and belongs to your project. Proceeding...
Uploading ./yellow_tripdata_2024-05.parquet to kai-kestra (Attempt 1)...
Bucket 'kai-kestra' exists and belongs to your project. Proceeding...
Uploading ./yellow_tripdata_2024-06.parquet to kai-kestra (Attempt 1)...
Uploaded: gs://kai-kestra/yellow_tripdata_2024-03.parquet
Uploaded: gs://kai-kestra/yellow_tripdata_2024-04.parquet
Verification successful for yellow_tripdata_2024-03.parquet
Verification successful for yellow_tripdata_2024-04.parquet
Uploaded: gs://kai-kestra/yellow_tripdata_2024-06.parquet
Verification successful for yellow_tripdata_2024-06.parquet
Uploaded: gs://kai-kestra/yellow_tripdata_2024-05.parquet
Verification successful for yellow_tripdata_2024-05.parquet
All files processed and verified.




# deactivate venv after finishing ingestion
(.venv) @kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/03-data-warehouse (main) $ deactivate
```


## Kai 2026.01.22 - Create 1 external table using the Yellow Taxi Trip Records
* https://console.cloud.google.com/bigquery
  * zoomcamp dataset >> create table
    * create table from: Google Cloud Storage
    * uri pattern: `kai-kestra/yellow_tripdata_2024-0*.parquet` (Reading - https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage#wildcard-support)
    * file format: Parquet
    * table: `yellow_tripdata_external_2024_01to06`
    * table type: External table
    * Schema: Auto detect

## Kai 2026.01.22 - Create 1 (regular/materialized) table in BQ using the Yellow Taxi Trip Records (NOT partitioned or clustered)
* https://console.cloud.google.com/bigquery
  * zoomcamp dataset >> create table
    * create table from: Google Cloud Storage
    * uri pattern: `kai-kestra/yellow_tripdata_2024-0*.parquet` (Reading - https://docs.cloud.google.com/bigquery/docs/external-data-cloud-storage#wildcard-support)
    * file format: Parquet
    * table: `yellow_tripdata_regular_2024_01to06`
    * table type: Native table
    * Schema: Source file defines the schema
    * Partitioning settings: No partitioning
    * Clustering settings: <No selection>



## Question 1:
What is count of records for the 2024 Yellow Taxi Data?
- 65,623
- 840,402
- 20,332,093
- 85,431,289


* `yellow_tripdata_regular_2024_01to06` Storage info

|Information|Value|
|---|---|
|Number of rows|20,332,093|
|Total logical bytes|2.72 GB|
|Active logical bytes|2.72 GB|
|Long-term logical bytes|0 B|
|Current physical bytes|0 B|
|Total physical bytes|0 B|
|Active physical bytes|0 B|
|Long-term physical bytes|0 B|
|Time travel physical bytes|0 B|


Answer: 20,332,093





## Question 2:
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.</br> 
What is the **estimated amount** of data that will be read when this query is executed on the External Table and the Table?

- 18.82 MB for the External Table and 47.60 MB for the Materialized Table
- 0 MB for the External Table and 155.12 MB for the Materialized Table
- 2.14 GB for the External Table and 0MB for the Materialized Table
- 0 MB for the External Table and 0MB for the Materialized Table

Working
```sql
-- q2
SELECT COUNT(1)
FROM (
      SELECT DISTINCT PULocationID
      FROM zoomcamp.yellow_tripdata_regular_2024_01to06
);

SELECT COUNT(1)
FROM (
      SELECT DISTINCT PULocationID
      FROM zoomcamp.yellow_tripdata_external_2024_01to06
);
```

Answer
* Option 2. 0 MB for the External Table (`This query will process 0 B when run.`) and 155.12 MB for the Materialized Table (`This query will process 155.12 MB when run.`)
* **For the External Table, a dry run of a federated query** that uses an external table **might report a lower bound of 0 bytes of data, even if rows are returned.** This happens because external tables are federated queries where BigQuery merely **references the external storage rather than owning the storage for the rows**. The **actual data scanning occurs at the external storage level (like Google Cloud Storage),** and BigQuery's estimation system doesn't account for this external scanning in the same way it does for native tables.
* For the **Materialized Table, BigQuery charges based on the logical (uncompressed) size** of just the **columns read** for all files that need to be read. When you execute a COUNT(DISTINCT PULocationID) query on a materialized table, BigQuery must **scan the entire column to compute the distinct values**, resulting in 155.12 MB of data being scanned according to the estimation.
* The key difference is that external tables are reference-based queries to external storage systems, while materialized tables store data directly within BigQuery's managed storage system, leading to fundamentally **different billing and data scanning estimation behaviours.**



## Question 3:
Write a query to **retrieve the PULocationID from the table (not the external table) in BigQuery**. Now write a query to retrieve the **PULocationID and DOLocationID on the same table**. Why are the estimated number of Bytes different?
- BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.
- BigQuery duplicates data across multiple storage partitions, so selecting two columns instead of one requires scanning the table twice, doubling the estimated bytes processed.
- BigQuery automatically caches the first queried column, so adding a second column increases processing time but does not affect the estimated bytes scanned.
- When selecting multiple columns, BigQuery performs an implicit join operation between them, increasing the estimated bytes processed

```sql
-- q3
-- This query will process 155.12 MB when run.
SELECT PULocationID
FROM zoomcamp.yellow_tripdata_regular_2024_01to06;

-- This query will process 310.24 MB when run.
SELECT PULocationID, DOLocationID
FROM zoomcamp.yellow_tripdata_regular_2024_01to06;
```

Answer: Option 1. BigQuery is a **columnar database, and it only scans the specific columns requested in the query**. **Querying two columns** (PULocationID, DOLocationID) requires **reading more data than querying one column** (PULocationID), leading to a higher estimated number of bytes processed.




## Question 4:
How many records have a fare_amount of 0?
- 128,210
- 546,578
- 20,188,016
- 8,333

```sql
-- q4
-- This query will process 155.12 MB when run.
SELECT COUNT(1) AS CNT
FROM zoomcamp.yellow_tripdata_regular_2024_01to06
WHERE fare_amount = 0;
-- [{
--   "CNT": "8333"
-- }]

-- This query will process 155.12 MB when run.
SELECT COUNT(1) AS CNT
FROM zoomcamp.yellow_tripdata_regular_2024_01to06
WHERE fare_amount IS NULL;
-- [{
--   "CNT": "0"
-- }]
```

Answer: 8,333




## Question 5:
What is the best strategy to make an optimized table in Big Query if your query will always **filter** based on `tpep_dropoff_datetime` and **order** the results by `VendorID` (Create a new table with this strategy)
- Partition by tpep_dropoff_datetime and Cluster on VendorID
- Cluster on by tpep_dropoff_datetime and Cluster on VendorID
- Cluster on tpep_dropoff_datetime Partition by VendorID
- Partition by tpep_dropoff_datetime and Partition by VendorID

Answer
* Option 1. Partition by tpep_dropoff_datetime and Cluster on VendorID
* Partiton on your filtering column
* Cluster on your ordering column

```sql
-- q5
CREATE OR REPLACE TABLE zoomcamp.yellow_tripdata_partitioned_clustered_2024_01to06
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID
AS
(
SELECT *
FROM zoomcamp.yellow_tripdata_regular_2024_01to06
);

-- Duration        6 sec
-- Bytes processed 2.72 GB
-- Bytes billed    2.72 GB
-- Slot milliseconds 308868
```





## Question 6:
Write a query to retrieve the distinct VendorIDs between `tpep_dropoff_datetime`
`2024-03-01` and `2024-03-15` (inclusive)</br>

Use the `materialized table` you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the `partitioned table` you created for question 5 and note the estimated bytes processed. What are these values? </br>

Choose the answer which most closely matches.</br> 

- 12.47 MB for non-partitioned table and 326.42 MB for the partitioned table
- 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table
- 5.87 MB for non-partitioned table and 0 MB for the partitioned table
- 310.31 MB for non-partitioned table and 285.64 MB for the partitioned table

```sql
-- q6
-- This query will process 310.24 MB when run.
SELECT VendorID
FROM zoomcamp.yellow_tripdata_regular_2024_01to06
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' and '2024-03-15';

-- This query will process 26.84 MB when run.
SELECT VendorID
FROM zoomcamp.yellow_tripdata_partitioned_clustered_2024_01to06
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' and '2024-03-15';
```

Answer: Option 2. 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table



## Question 7: 
Where is the data stored in the External Table you created?

- Big Query
- Container Registry
- GCP Bucket
- Big Table

Answer: GCP Bucket


## Question 8:
It is best practice in Big Query to always cluster your data:
- True
- False

Answer: False

Reasoning
* When Clustering is Beneficial:
  * Large tables (typically 1GB+)
  * Queries frequently filter on specific columns (WHERE clauses)
  * Queries often aggregate by certain dimensions (GROUP BY)
  * Tables have predictable access patterns that align with clustering keys
* **When Clustering May Not Be Appropriate:**
  * **Small tables where the overhead outweighs benefits**
  * Tables with **random query patterns that don't align with any specific columns**
  * **Frequently updated** tables with random update patterns (clustering degrades over time)
  * **Time-series data where partitioning alone may be sufficient**
  * When you need **more than 4 clustering columns (BigQuery limit)**



## (Bonus: Not worth points) Question 9:
No Points: Write a `SELECT count(*)` query FROM the materialized table you created. How many bytes does it estimate will be read? Why?


```sql
-- q9
-- from 'external table' pointing to GCS parquet files
-- copy/materialise the data into a materialised table
CREATE OR REPLACE TABLE zoomcamp.yellow_tripdata_materialized_2024_01to06
AS
(
SELECT *
FROM zoomcamp.yellow_tripdata_external_2024_01to06
);

-- Duration        7 sec
-- Bytes processed 2.72 GB
-- Bytes billed    2.72 GB
-- Slot milliseconds 139368



-- This query will process 0 B when run.
--      0B because count of records is in table's metadata
--      no need to read any records/data
SELECT COUNT(*)
FROM zoomcamp.yellow_tripdata_materialized_2024_01to06;
-- This query will process 0 B when run.
SELECT COUNT(1)
FROM zoomcamp.yellow_tripdata_materialized_2024_01to06;

-- This would scan ALL data (full table scan)
--      when counting on a specific col
--      cuz we counts only non-NULL values in that specific column
-- This query will process 155.12 MB when run.
SELECT COUNT(PULocationID)
FROM zoomcamp.yellow_tripdata_materialized_2024_01to06;
```




## Submitting the solutions

Form for submitting: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw3

## Solution

Solution: https://www.youtube.com/watch?v=wpLmImIUlPg
