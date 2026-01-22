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


## Question 1:
What is count of records for the 2024 Yellow Taxi Data?
- 65,623
- 840,402
- 20,332,093
- 85,431,289


## Question 2:
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.</br> 
What is the **estimated amount** of data that will be read when this query is executed on the External Table and the Table?

- 18.82 MB for the External Table and 47.60 MB for the Materialized Table
- 0 MB for the External Table and 155.12 MB for the Materialized Table
- 2.14 GB for the External Table and 0MB for the Materialized Table
- 0 MB for the External Table and 0MB for the Materialized Table

## Question 3:
Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?
- BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires 
reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.
- BigQuery duplicates data across multiple storage partitions, so selecting two columns instead of one requires scanning the table twice, 
doubling the estimated bytes processed.
- BigQuery automatically caches the first queried column, so adding a second column increases processing time but does not affect the estimated bytes scanned.
- When selecting multiple columns, BigQuery performs an implicit join operation between them, increasing the estimated bytes processed

## Question 4:
How many records have a fare_amount of 0?
- 128,210
- 546,578
- 20,188,016
- 8,333

## Question 5:
What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)
- Partition by tpep_dropoff_datetime and Cluster on VendorID
- Cluster on by tpep_dropoff_datetime and Cluster on VendorID
- Cluster on tpep_dropoff_datetime Partition by VendorID
- Partition by tpep_dropoff_datetime and Partition by VendorID


## Question 6:
Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime
2024-03-01 and 2024-03-15 (inclusive)</br>

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values? </br>

Choose the answer which most closely matches.</br> 

- 12.47 MB for non-partitioned table and 326.42 MB for the partitioned table
- 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table
- 5.87 MB for non-partitioned table and 0 MB for the partitioned table
- 310.31 MB for non-partitioned table and 285.64 MB for the partitioned table


## Question 7: 
Where is the data stored in the External Table you created?

- Big Query
- Container Registry
- GCP Bucket
- Big Table

## Question 8:
It is best practice in Big Query to always cluster your data:
- True
- False


## (Bonus: Not worth points) Question 9:
No Points: Write a `SELECT count(*)` query FROM the materialized table you created. How many bytes does it estimate will be read? Why?


## Submitting the solutions

Form for submitting: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw3

## Solution

Solution: https://www.youtube.com/watch?v=wpLmImIUlPg
