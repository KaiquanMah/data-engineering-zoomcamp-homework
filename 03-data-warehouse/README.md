# Data Warehouse and BigQuery

- [Slides](https://docs.google.com/presentation/d/1a3ZoBAXFk8-EhUsd7rAZd-5p_HpltkzSeujjRGB2TAI/edit?usp=sharing)  
- [Big Query basic SQL](big_query.sql)

# Videos

## Data Warehouse

- Data Warehouse and BigQuery

[![](https://markdown-videos-api.jorgenkh.no/youtube/jrHljAoD6nM)](https://youtu.be/jrHljAoD6nM&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=34)

- [Slides](https://docs.google.com/presentation/d/1a3ZoBAXFk8-EhUsd7rAZd-5p_HpltkzSeujjRGB2TAI/)

| Topic | OLTP | OLAP |
| --- | --- | --- |
| Purpose | Control and run essential **business operations in real time** | Plan, **solve problems, support decisions, discover hidden insights** |
| Data updates | Short, **fast updates initiated by user** | Data **periodically refreshed with scheduled, long-running batch jobs** |
| Database design | **Normalized databases** for efficiency | **Denormalized** databases for analysis |
| **Space requirements** | Generally small if historical data is archived | Generally **large due to aggregating large datasets** |
| **Backup and recovery** | **Regular backups** required to ensure business continuity and meet **legal and governance requirements** | Lost data can be **reloaded** from OLTP database **as needed** in lieu of regular backups |
| **Productivity** | Increases productivity of **end users** | Increases productivity of **business managers, data analysts, and executives** |
| **Data view** | Lists **day-to-day business transactions** | **Multi-dimensional view** of enterprise data |
| **User examples** | Customer-facing personnel, clerks, online shoppers | Knowledge workers such as data analysts, business analysts, and executives|


* What is a data warehouse
  * OLAP solution
  * Used for reporting and data analysis 

* BigQuery
  * **Serverless** data warehouse - There are **no servers to manage** or database **software to install**
  * Software as well as infrastructure including 
    * **scalability and high-availability**
  * Built-in features like 
    * ML
    * geospatial analysis
    * business intelligence
  * BigQuery maximizes flexibility by separating the compute engine that analyzes your data from your storage
  * eg partiton on `creation_date`
  * within each partition, cluster on `field2 / OS`

* BigQuery Partition
  * **Time-unit** column
  * **Ingestion time** (_PARTITIONTIME)
  * **Integer range** partitioning
  * When using **Time unit or ingestion time**
    * Daily (Default)
    * Hourly
    * Monthly or yearly
  * Number of partitions limit is 4000

* BigQuery Clustering
  * **Columns you specify** are used to **colocate related data**
  * **Order of the column** is **important**
  * The order of the specified columns determines the sort order of the data.
  * Clustering improves
    * **Filter** queries
    * **Aggregate** queries
  * Table with data size < 1 GB, don’t show significant improvement with partitioning and clustering
  * You can specify **up to four clustering columns**
  * Clustering columns must be **top-level, non-repeated columns**
    * INT64
    * NUMERIC
    * BIGNUMERIC
    * DATE
    * DATETIME
    * TIMESTAMP
    * GEOGRAPHY
    * STRING
    * BOOL

| Partitioning | Clustering |
| --- | --- |
| **Cost benefit upfront** | Cost **unknown** |
| You need partition-level management. |You **need more granularity** than partitioning alone allows | 
| **Filter or aggregate on single column** | Your queries commonly use filters or aggregation against **multiple specific columns** |
| NA | The **cardinality/combinations** of the number of values in a column or group of columns is **large** |

* Choose clustering over paritioning when
  * **Partitioning** results in a **SMALL AMOUNT of DATA PER PARTITION (approximately less than 1 GB)**
  * Partitioning results in a **TOO MANY/large number of PARTITIONS beyond the limits on partitioned tables**
  * Partitioning results in your **mutation operations MODIFYING the MAJORITY of PARTITIONS in the table FREQUENTLY** (for example, every few minutes)

 * Automatic reclustering
  * As data is added to a clustered table
    * the **newly inserted data can be written to blocks** that contain key ranges that **overlap** with the key ranges in **previously written blocks**
    * These **overlapping keys weaken the sort property of the table**
  * To maintain the performance characteristics of a clustered table
    * BigQuery performs **automatic re-clustering in the background** to restore the sort property of the table
    * For partitioned tables, **clustering is maintained for data within the scope of EACH PARTITION**

* BigQuery-Best Practice
  * Cost reduction
    * Avoid SELECT *
    * **Price your queries before running** them
    * Use **clustered or partitioned tables**
    * Use streaming inserts with caution
    * Materialize query results in stages
  * Query performance
    * **Filter on partitioned columns**
    * **Denormalizing** data
    * Use **nested or repeated columns**
    * Use external data sources appropriately
    * Don't use it???, in case u want a high query performance
    * **Reduce data before using a JOIN**
    * Do not treat WITH clauses as prepared statements
    * **Avoid oversharding tables**
    * **Avoid JavaScript user-defined functions**
    * Use **approximate aggregation functions (HyperLogLog++)**
    * **Order Last**, for query operations to maximize performance
    * Optimize your join patterns
      * As a best practice,
        * place the **table with the largest number of rows first**,
        * followed by the table with the **fewest rows**, and then
        * place the **remaining tables by decreasing size**




## :movie_camera: Partitioning and clustering

- Partitioning vs Clustering

[![](https://markdown-videos-api.jorgenkh.no/youtube/-CqXf7vhhDs)](https://youtu.be/-CqXf7vhhDs?si=p1sYQCAs8dAa7jIm&t=193&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=35)

## :movie_camera: Best practices

[![](https://markdown-videos-api.jorgenkh.no/youtube/k81mLJVX08w)](https://youtu.be/k81mLJVX08w&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=36)

## :movie_camera: Internals of BigQuery

[![](https://markdown-videos-api.jorgenkh.no/youtube/eduHi1inM4s)](https://youtu.be/eduHi1inM4s&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=37)

## Advanced topics

### :movie_camera: Machine Learning in Big Query

[![](https://markdown-videos-api.jorgenkh.no/youtube/B-WtpB0PuG4)](https://youtu.be/B-WtpB0PuG4&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=34)

* [SQL for ML in BigQuery](big_query_ml.sql)

**Important links**

- [BigQuery ML Tutorials](https://cloud.google.com/bigquery-ml/docs/tutorials)
- [BigQuery ML Reference Parameter](https://cloud.google.com/bigquery-ml/docs/analytics-reference-patterns)
- [Hyper Parameter tuning](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-create-glm)
- [Feature preprocessing](https://cloud.google.com/bigquery-ml/docs/reference/standard-sql/bigqueryml-syntax-preprocess-overview)

### :movie_camera: Deploying Machine Learning model from BigQuery

[![](https://markdown-videos-api.jorgenkh.no/youtube/BjARzEWaznU)](https://youtu.be/BjARzEWaznU&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb&index=39)

- [Steps to extract and deploy model with docker](extract_model.md)  



# Homework

* [2026 Homework](../cohorts/2026/03-data-warehouse/homework.md)


# Community notes

<details>
<summary>Did you take notes? You can share them here</summary>

* [Notes by Alvaro Navas](https://github.com/ziritrion/dataeng-zoomcamp/blob/main/notes/3_data_warehouse.md)
* [Isaac Kargar's blog post](https://kargarisaac.github.io/blog/data%20engineering/jupyter/2022/01/30/data-engineering-w3.html)
* [Marcos Torregrosa's blog post](https://www.n4gash.com/2023/data-engineering-zoomcamp-semana-3/) 
* [Notes by Victor Padilha](https://github.com/padilha/de-zoomcamp/tree/master/week3)
* [Notes from Xia He-Bleinagel](https://xiahe-bleinagel.com/2023/02/week-3-data-engineering-zoomcamp-notes-data-warehouse-and-bigquery/)
* [Bigger picture summary on Data Lakes, Data Warehouses, and tooling](https://medium.com/@verazabeida/zoomcamp-week-4-b8bde661bf98), by Vera
* [Notes by froukje](https://github.com/froukje/de-zoomcamp/blob/main/week_3_data_warehouse/notes/notes_week_03.md)
* [Notes by Alain Boisvert](https://github.com/boisalai/de-zoomcamp-2023/blob/main/week3.md)
* [Notes from Vincenzo Galante](https://binchentso.notion.site/Data-Talks-Club-Data-Engineering-Zoomcamp-8699af8e7ff94ec49e6f9bdec8eb69fd)
* [2024 videos transcript week3](https://drive.google.com/drive/folders/1quIiwWO-tJCruqvtlqe_Olw8nvYSmmDJ?usp=sharing) by Maria Fisher 
* [Notes by Linda](https://github.com/inner-outer-space/de-zoomcamp-2024/blob/main/3a-data-warehouse/readme.md)
* [Jonah Oliver's blog post](https://www.jonahboliver.com/blog/de-zc-w3)
* [2024 - steps to send data from Mage to GCS + creating external table](https://drive.google.com/file/d/1GIi6xnS4070a8MUlIg-ozITt485_-ePB/view?usp=drive_link) by Maria Fisher
* [2024 - mage dataloader script to load the parquet files from a remote URL and push it to Google bucket as parquet file](https://github.com/amohan601/dataengineering-zoomcamp2024/blob/main/week_3_data_warehouse/mage_scripts/green_taxi_2022_v2.py) by Anju Mohan
* [2024 - steps to send data from Mage to GCS + creating external table](https://drive.google.com/file/d/1GIi6xnS4070a8MUlIg-ozITt485_-ePB/view?usp=drive_link) by Maria Fisher 
* [Notes by HongWei](https://github.com/hwchua0209/data-engineering-zoomcamp-submission/blob/main/03-data-warehouse/README.md)
* [2025 Notes by Manuel Guerra](https://github.com/ManuelGuerra1987/data-engineering-zoomcamp-notes/blob/main/3_Data-Warehouse/README.md)
* [Notes from Horeb SEIDOU](https://spotted-hardhat-eea.notion.site/Week-3-Data-Warehouse-and-BigQuery-17c29780dc4a80c8a226f372543ae388)
* [2025 - Notes by Gabi Fonseca](https://github.com/fonsecagabriella/data_engineering/blob/main/03_data_warehouse/00_notes.md)
* [2025 Gitbook Notes Tinker0425](https://data-engineering-zoomcamp-2025-t.gitbook.io/tinker0425/module-3/introduction-to-module-3)
* [2025 Notes from Daniel Lachner](https://drive.google.com/file/d/105zjtLFi0sRqqFFgdMSCTzfcLPx2rfv4/view?usp=sharing)
* Add your notes here (above this line)

</details>