# Module 1 Homework: Docker & SQL

In this homework we'll prepare the environment and practice
Docker and SQL

When submitting your homework, you will also need to include
a link to your GitHub repository or other public code-hosting
site.

This repository should contain the code for solving the homework.

When your solution has SQL or shell commands and not code
(e.g. python files) file format, include them directly in
the README file of your repository.


## Question 1. Understanding Docker images

Run docker with the `python:3.13` image. Use an entrypoint `bash` to interact with the container.

What's the version of `pip` in the image?

- 25.3
- 24.3.1
- 24.2.1
- 23.3.1

* Workings
```bash
# docker exec -it <container_id> bash
docker run -it python:3.13 bash
pip --version



@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework (main) $ docker run -it python:3.13 bash
Unable to find image 'python:3.13' locally
3.13: Pulling from library/python
2ca1bfae7ba8: Pull complete 
82e18c5e1c15: Pull complete 
be442a7e0d6f: Pull complete 
26d823e3848f: Pull complete 
ca4b54413202: Pull complete 
b6513238a015: Pull complete 
9b57076d00d4: Pull complete 
Digest: sha256:02865b3929f3910fc2d6ebbf745bf00504d316478dacaea7d9e230e134411bcb
Status: Downloaded newer image for python:3.13
root@59ec6bea23fe:/# pip --version
pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)
```

* Answer: 25.3



## Question 2. Understanding Docker networking and docker-compose

Given the following `docker-compose.yaml`, what is the `hostname` and `port` that pgadmin should use to connect to the postgres database?

```yaml
services:
  db:
    container_name: postgres
    image: postgres:17-alpine
    environment:
      POSTGRES_USER: 'postgres'
      POSTGRES_PASSWORD: 'postgres'
      POSTGRES_DB: 'ny_taxi'
    ports:
      - '5433:5432'
    volumes:
      - vol-pgdata:/var/lib/postgresql/data

  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4:latest
    environment:
      PGADMIN_DEFAULT_EMAIL: "pgadmin@pgadmin.com"
      PGADMIN_DEFAULT_PASSWORD: "pgadmin"
    ports:
      - "8080:80"
    volumes:
      - vol-pgadmin_data:/var/lib/pgadmin

volumes:
  vol-pgdata:
    name: vol-pgdata
  vol-pgadmin_data:
    name: vol-pgadmin_data
```

If multiple answers are correct, select any
- postgres:5433
- localhost:5432
- db:5433
- postgres:5432
- db:5432

Answer
- db:5432
  - Service name: db (this is what other services use to connect)
  - **Internal container port: 5432 (where PostgreSQL actually listens inside the container)**
  - **Host port mapping: 5433:5432 (for external access from your machine**, not for inter-container communication)
  - Since both db and pgadmin services are in the **same docker-compose network, pgadmin should use the internal container port 5432 (not the mapped host port 5433)**
  - localhost - pgadmin's own local container, NOT postgres 'db' container




## Prepare the Data

Download the green taxi trips data for November 2025:

```bash
wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet
```

You will also need the dataset with zones:

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv
```

### Kai - Steps to ingest the parquet and CSV with containerised ingestion
* Please refer to the steps in `01-docker-terraform\docker-sql\pipeline-homework\README.md`


## Question 3. Counting short trips

For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a `trip_distance` of less than or equal to 1 mile?

- 7,853
- 8,007
- 8,254
- 8,421


```sql
-- check 1 record
SELECT *
FROM green_taxi_trips
LIMIT 1;
"VendorID"	"lpep_pickup_datetime"	"lpep_dropoff_datetime"	"store_and_fwd_flag"	"RatecodeID"	"PULocationID"	"DOLocationID"	"passenger_count"	"trip_distance"	"fare_amount"	"extra"	"mta_tax"	"tip_amount"	"tolls_amount"	"ehail_fee"	"improvement_surcharge"	"total_amount"	"payment_type"	"trip_type"	"congestion_surcharge"	"cbd_congestion_fee"
2	"2025-11-01 00:34:48"	"2025-11-01 00:41:39"	"N"	1	74	42	1	0.74	7.2	1	0.5	1.94	0		1	11.64	1	1	0	0






-- count distinct dates with records
SELECT COUNT(DISTINCT DATE(lpep_pickup_datetime)) AS distinct_dates
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2025-11-01 00:00:00'
      AND lpep_pickup_datetime < '2025-12-01 00:00:00';
"distinct_dates"
30



-- check dates with records
SELECT DISTINCT DATE(lpep_pickup_datetime) AS pickup_date,
COUNT(*) AS trip_count
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2025-11-01 00:00:00'
      AND lpep_pickup_datetime < '2025-12-01 00:00:00'
GROUP BY pickup_date
ORDER BY pickup_date;
"pickup_date"	"trip_count"
"2025-11-01"	1465
"2025-11-02"	1295
"2025-11-03"	1642
"2025-11-04"	1470
"2025-11-05"	1804
"2025-11-06"	1862
"2025-11-07"	1645
"2025-11-08"	1398
"2025-11-09"	1228
"2025-11-10"	1729
"2025-11-11"	1590
"2025-11-12"	1686
"2025-11-13"	1821
"2025-11-14"	1726
"2025-11-15"	1431
"2025-11-16"	1391
"2025-11-17"	1764
"2025-11-18"	1773
"2025-11-19"	1810
"2025-11-20"	1932
"2025-11-21"	1810
"2025-11-22"	1330
"2025-11-23"	1280
"2025-11-24"	1724
"2025-11-25"	1861
"2025-11-26"	1506
"2025-11-27"	1035
"2025-11-28"	1178
"2025-11-29"	1307
"2025-11-30"	1398



-- check count of trips which had a `trip_distance` of less than or equal to 1 mile
SELECT COUNT(*) AS trip_count
FROM green_taxi_trips
WHERE lpep_pickup_datetime >= '2025-11-01 00:00:00'
      AND lpep_pickup_datetime < '2025-12-01 00:00:00'
      AND trip_distance <=1.0;
"trip_count"
8007
```

* Answer: 8,007 trips




## Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance? Only consider trips with `trip_distance` less than 100 miles (to exclude data errors).

Use the pick up time for your calculations.

- 2025-11-14
- 2025-11-20
- 2025-11-23
- 2025-11-25

```sql
-- date with longest trip distance
WITH max_dist AS (
SELECT MAX(trip_distance) as max_trip_distance
FROM green_taxi_trips
WHERE trip_distance <100
)

SELECT DATE(lpep_pickup_datetime) AS pickup_date,
trip_distance
FROM green_taxi_trips
WHERE trip_distance = (SELECT max_trip_distance FROM max_dist);
"pickup_date"	"trip_distance"
"2025-11-14"	88.03
```

* Answer: 2025-11-14




## Question 5. Biggest pickup zone

Which was the pickup zone with the largest `total_amount` (sum of all trips) on November 18th, 2025?

- East Harlem North
- East Harlem South
- Morningside Heights
- Forest Hills

```sql
-- taxi_zone_lookup
SELECT *
FROM taxi_zone_lookup
LIMIT 10;
"LocationID"	"Borough"	"Zone"	"service_zone"
1	"EWR"	"Newark Airport"	"EWR"
2	"Queens"	"Jamaica Bay"	"Boro Zone"
3	"Bronx"	"Allerton/Pelham Gardens"	"Boro Zone"
4	"Manhattan"	"Alphabet City"	"Yellow Zone"
5	"Staten Island"	"Arden Heights"	"Boro Zone"
6	"Staten Island"	"Arrochar/Fort Wadsworth"	"Boro Zone"
7	"Queens"	"Astoria"	"Boro Zone"
8	"Queens"	"Astoria Park"	"Boro Zone"
9	"Queens"	"Auburndale"	"Boro Zone"
10	"Queens"	"Baisley Park"	"Boro Zone"




-- pickup zone `PULocationID` with highest total_amount on 18 November 2025
-- REMEMBER TO USE quotes around "CaseSensitive" COLNAMES
--    if they were UPPERCASE OR CaseSensitive when defining the table schema
--    otw postgrs will convert to lowercase
WITH max_amount AS (
SELECT MAX(total_amount) as max_total_amount
FROM green_taxi_trips
WHERE DATE(lpep_pickup_datetime) = '2025-11-18'
)

SELECT taxi_zone_lookup.*,
       green_taxi_trips.total_amount
FROM green_taxi_trips
JOIN taxi_zone_lookup ON green_taxi_trips."PULocationID" = taxi_zone_lookup."LocationID"
WHERE green_taxi_trips.total_amount = (SELECT max_total_amount FROM max_amount);
"LocationID"	"Borough"	"Zone"	"service_zone"	"total_amount"
92	"Queens"	"Flushing"	"Boro Zone"	351
92	"Queens"	"Flushing"	"Boro Zone"	351
-- not sure why the pick up zone is not in the 4 options available



-- if we see above, there seems to be 2 records with the MAX(total_amount) on the same date
--    SO MAYBE WE NEED TO SUM ALL the `total_amount`
--    instead of `total_amount` already being the SUM (which was my assumption above)
SELECT 
    taxi_zone_lookup."Zone",
    SUM(green_taxi_trips.total_amount) as total_zone_amount
FROM green_taxi_trips
JOIN taxi_zone_lookup ON green_taxi_trips."PULocationID" = taxi_zone_lookup."LocationID"
WHERE DATE(green_taxi_trips.lpep_pickup_datetime) = '2025-11-18'
GROUP BY taxi_zone_lookup."Zone"
ORDER BY total_zone_amount DESC
LIMIT 1;
"Zone"	"total_zone_amount"
"East Harlem North"	9281.919999999991
```
* Answer: East Harlem North






## Question 6. Largest tip

For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the **largest tip**?

Note: it's `tip` , not `trip`. We need the name of the zone, not the ID.

- JFK Airport
- Yorkville West
- East Harlem North
- LaGuardia Airport

```sql
SELECT *
FROM taxi_zone_lookup
WHERE "Zone" = 'East Harlem North';
"LocationID"	"Borough"	"Zone"	"service_zone"
74	"Manhattan"	"East Harlem North"	"Boro Zone"



SELECT 
    taxi_zone_lookup."Zone" as drop_off_zone,
    SUM(green_taxi_trips.tip_amount) as total_zone_tip
FROM green_taxi_trips
JOIN taxi_zone_lookup ON green_taxi_trips."DOLocationID" = taxi_zone_lookup."LocationID"
WHERE lpep_pickup_datetime >= '2025-11-01 00:00:00'
      AND lpep_pickup_datetime < '2025-12-01 00:00:00'
      AND taxi_zone_lookup."Zone" = 'East Harlem North'
GROUP BY drop_off_zone
ORDER BY total_zone_tip DESC
LIMIT 10;
"drop_off_zone"	"total_zone_tip"
"East Harlem North"	2978.3300000000017


SELECT 
    taxi_zone_lookup."Zone" as drop_off_zone,
    tip_amount
FROM green_taxi_trips
JOIN taxi_zone_lookup ON green_taxi_trips."DOLocationID" = taxi_zone_lookup."LocationID"
WHERE lpep_pickup_datetime >= '2025-11-01 00:00:00'
      AND lpep_pickup_datetime < '2025-12-01 00:00:00'
      AND taxi_zone_lookup."Zone" = 'East Harlem North'
ORDER BY tip_amount DESC
LIMIT 10;
"drop_off_zone"	"tip_amount"
"East Harlem North"	45
"East Harlem North"	40
"East Harlem North"	26
"East Harlem North"	18
"East Harlem North"	16
"East Harlem North"	12.5
"East Harlem North"	11.25
"East Harlem North"	10.55
"East Harlem North"	8.54
"East Harlem North"	7.86
```

* Answer: East Harlem North




## Terraform

In this section homework we'll prepare the environment by creating resources in GCP with Terraform.

In your VM on GCP/Laptop/GitHub Codespace install Terraform.
Copy the files from the course repo
[here](../../../01-docker-terraform/terraform/terraform) to your VM/Laptop/GitHub Codespace.

Modify the files as necessary to create a GCP Bucket and Big Query Dataset.


## Question 7. Terraform Workflow

Which of the following sequences, respectively, describes the workflow for:
1. Downloading the provider plugins and setting up backend,
2. Generating proposed changes and auto-executing the plan
3. Remove all resources managed by terraform`

Answers:
- terraform import, terraform apply -y, terraform destroy
- teraform init, terraform plan -auto-apply, terraform rm
- terraform init, terraform run -auto-approve, terraform destroy
- terraform init, terraform apply -auto-approve, terraform destroy
- terraform import, terraform apply -y, terraform rm


## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw1


## Learning in Public

We encourage everyone to share what they learned. This is called "learning in public".

### Why learn in public?

- Accountability: Sharing your progress creates commitment and motivation to continue
- Feedback: The community can provide valuable suggestions and corrections
- Networking: You'll connect with like-minded people and potential collaborators
- Documentation: Your posts become a learning journal you can reference later
- Opportunities: Employers and clients often discover talent through public learning

You can read more about the benefits [here](https://alexeyondata.substack.com/p/benefits-of-learning-in-public-and).

Don't worry about being perfect. Everyone starts somewhere, and people love following genuine learning journeys!

### Example post for LinkedIn

```
🚀 Week 1 of Data Engineering Zoomcamp by @DataTalksClub complete!

Just finished Module 1 - Docker & Terraform. Learned how to:

✅ Containerize applications with Docker and Docker Compose
✅ Set up PostgreSQL databases and write SQL queries
✅ Build data pipelines to ingest NYC taxi data
✅ Provision cloud infrastructure with Terraform

Here's my homework solution: <LINK>

Following along with this amazing free course - who else is learning data engineering?

You can sign up here: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```

### Example post for Twitter/X


```
🐳 Module 1 of Data Engineering Zoomcamp done!

- Docker containers
- Postgres & SQL
- Terraform & GCP
- NYC taxi data pipeline

My solution: <LINK>

Free course by @DataTalksClub: https://github.com/DataTalksClub/data-engineering-zoomcamp/
```


### Useful PostgreSQL (psql / pgcli) Commands When Running Postgres in Docker
-- Help & Navigation
\?                     -- Show all available commands
\h                     -- Show SQL syntax and help
\q                     -- Quit psql / pgcli
quit                   -- Quit pgcli
\c database_name       -- Connect to a different database
\conninfo              -- Show current connection info
\l                     -- List all databases

-- Schema & Object Inspection
\dn                    -- List schemas
\dt                    -- List tables
\d table_name          -- Describe a table
\d+ table_name         -- Detailed table info
\dv                    -- List views
\dm                    -- List materialized views
\di                    -- List indexes
\ds                    -- List sequences
\df                    -- List functions
\sf function_name      -- Show function definition
\dx                    -- List extensions
\db                    -- List tablespaces
\dT                    -- List data types
\dD                    -- List domains
\dE                    -- List foreign tables
\dF                    -- List text search configurations

-- Roles & Permissions
\du                    -- List roles
\dp                    -- List table privileges
\ddp                   -- List default privileges

-- Query & Output Utilities
\timing                -- Toggle query execution time
\x                     -- Toggle expanded output
\pset key value        -- Set output options
\T format              -- Change table output format
\o filename            -- Send query output to a file
\pager command         -- Pipe output through a pager
\log-file filename     -- Log query results to a file

-- Data Import / Export
\copy table_name TO 'file.csv' CSV HEADER
\copy table_name FROM 'file.csv' CSV HEADER

-- Working with Files & Shell
\i filename.sql        -- Execute SQL from a file
\e                    -- Open query in external editor
\! command             -- Run a shell command

-- Named Queries (pgcli)
\n                     -- List or execute named queries
\ns name query         -- Save a named query
\np name               -- Print a named query
\nd name               -- Delete a named query

-- Misc
\echo text             -- Print text to stdout
\qecho text            -- Print text to query output
\v on|off              -- Toggle verbose errors
\watch 2               -- Re-run last query every 2 seconds
\#                     -- Refresh auto-completion
\refresh               -- Refresh auto-completion