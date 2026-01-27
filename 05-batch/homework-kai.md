# Module 5 Homework
* For the notebook with more workings, please refer to `05-batch/code/homework-kai.ipynb`


In this homework we'll put what we learned about Spark in practice.

For this homework we will be using the Yellow 2024-10 data from the official website: 

```bash
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-10.parquet
```


## Question 1: Install Spark and PySpark

- Install Spark
- Run PySpark
- Create a local spark session
- Execute spark.version.

What's the output?

> [!NOTE]
> To install PySpark follow this [guide](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/05-batch/setup/pyspark.md)

```python
spark.version
'3.3.2'


spark
SparkSession - in-memory
SparkContext
Spark UI - `http://3bf809a4-aad5-48c7-b237-0316d51fa8a7.internal.cloudapp.net:4040/`, `https://expert-waddle-v6w4g64w564wc7wv-4040.app.github.dev/jobs/`
Version v3.3.2
Master local[*]
AppName test
```

Answer: spark v3.3.2


## Question 2: Yellow October 2024

Read the October 2024 Yellow into a Spark Dataframe.

Repartition the Dataframe to 4 partitions and save it to parquet.

What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.

- 6MB
- 25MB
- 75MB
- 100MB


```bash
!ls -lh data/pq/yellow/2024/10/
total 100M
-rw-r--r-- 1 codespace codespace   0 Jan 27 02:43 _SUCCESS
-rw-r--r-- 1 codespace codespace 25M Jan 27 02:43 part-00000-468d7f16-8a9f-4ca9-bff6-3ed89f438424-c000.snappy.parquet
-rw-r--r-- 1 codespace codespace 25M Jan 27 02:43 part-00001-468d7f16-8a9f-4ca9-bff6-3ed89f438424-c000.snappy.parquet
-rw-r--r-- 1 codespace codespace 25M Jan 27 02:43 part-00002-468d7f16-8a9f-4ca9-bff6-3ed89f438424-c000.snappy.parquet
-rw-r--r-- 1 codespace codespace 25M Jan 27 02:43 part-00003-468d7f16-8a9f-4ca9-bff6-3ed89f438424-c000.snappy.parquet
```

answer: 25MB



## Question 3: Count records 

How many taxi trips were there on the 15th of October?

Consider only trips that **started on** the 15th of October.

- 85,567
- 105,567
- 125,567
- 145,567

```python
df_yellow_20241015 = df_yellow_w_date.filter(df_yellow_w_date.pickup_date == '2024-10-15')
df_yellow_20241015.show(10)

+--------+-------------------+-------------------+---------------+-------------+----------+------------------+------------+------------+------------+-----------+-----+-------+----------+------------+---------------------+------------+--------------------+-----------+-----------+------------+
|VendorID|    pickup_datetime|   dropoff_datetime|passenger_count|trip_distance|RatecodeID|store_and_fwd_flag|PULocationID|DOLocationID|payment_type|fare_amount|extra|mta_tax|tip_amount|tolls_amount|improvement_surcharge|total_amount|congestion_surcharge|Airport_fee|pickup_date|dropoff_date|
+--------+-------------------+-------------------+---------------+-------------+----------+------------------+------------+------------+------------+-----------+-----+-------+----------+------------+---------------------+------------+--------------------+-----------+-----------+------------+
|       2|2024-10-15 00:43:57|2024-10-15 00:45:14|              1|         0.29|         5|                 N|         138|         223|           1|       65.0|  5.0|    0.0|       0.0|         0.0|                  1.0|       72.75|                 0.0|       1.75| 2024-10-15|  2024-10-15|
|       2|2024-10-15 15:17:23|2024-10-15 15:56:18|              1|          5.0|         1|                 N|          43|         114|           1|       35.2|  0.0|    0.5|       9.8|         0.0|                  1.0|        49.0|                 2.5|        0.0| 2024-10-15|  2024-10-15|
|       2|2024-10-15 19:31:57|2024-10-15 19:52:52|              1|         8.92|         1|                 N|         138|         229|           1|       37.3|  7.5|    0.5|     11.15|        6.94|                  1.0|       68.64|                 2.5|       1.75| 2024-10-15|  2024-10-15|
|       2|2024-10-15 17:47:22|2024-10-15 18:57:21|              1|        18.49|         2|                 N|         132|         231|           1|       70.0|  5.0|    0.5|     19.75|         0.0|                  1.0|       100.5|                 2.5|       1.75| 2024-10-15|  2024-10-15|
|       1|2024-10-15 09:56:09|2024-10-15 10:06:58|              1|          1.6|         1|                 N|         161|         140|           1|       11.4|  2.5|    0.5|      3.05|         0.0|                  1.0|       18.45|                 2.5|        0.0| 2024-10-15|  2024-10-15|
|       1|2024-10-15 11:14:55|2024-10-15 11:24:51|              1|          0.8|         1|                 N|         141|         162|           2|       10.0|  2.5|    0.5|       0.0|         0.0|                  1.0|        14.0|                 2.5|        0.0| 2024-10-15|  2024-10-15|
|       2|2024-10-15 08:26:44|2024-10-15 08:59:44|              1|          3.1|         1|                 N|         137|         143|           1|       28.2|  0.0|    0.5|       1.0|         0.0|                  1.0|        33.2|                 2.5|        0.0| 2024-10-15|  2024-10-15|
|       2|2024-10-15 15:10:55|2024-10-15 15:25:45|              1|         1.23|         1|                 N|          43|         163|           1|       13.5|  0.0|    0.5|      2.62|         0.0|                  1.0|       20.12|                 2.5|        0.0| 2024-10-15|  2024-10-15|
|       1|2024-10-15 07:31:45|2024-10-15 07:55:42|              1|          4.9|         1|                 N|         158|         238|           1|       24.7|  2.5|    0.5|       7.2|         0.0|                  1.0|        35.9|                 2.5|        0.0| 2024-10-15|  2024-10-15|
|       2|2024-10-15 16:06:34|2024-10-15 16:08:27|              1|         0.21|         1|                 N|         236|         236|           4|       -4.4| -2.5|   -0.5|       0.0|         0.0|                 -1.0|       -10.9|                -2.5|        0.0| 2024-10-15|  2024-10-15|
+--------+-------------------+-------------------+---------------+-------------+----------+------------------+------------+------------+------------+-----------+-----+-------+----------+------------+---------------------+------------+--------------------+-----------+-----------+------------+
only showing top 10 rows





df_yellow_20241015.count()
128893

```

Answer: 125,567 (closest to 128,893 which we got from the filtered df count)




## Question 4: Longest trip

What is the length of the longest trip in the dataset in hours?

- 122
- 142
- 162
- 182


```python
df_yellow_w_date.show(10)
+--------+-------------------+-------------------+---------------+-------------+----------+------------------+------------+------------+------------+-----------+-----+-------+----------+------------+---------------------+------------+--------------------+-----------+-----------+------------+
|VendorID|    pickup_datetime|   dropoff_datetime|passenger_count|trip_distance|RatecodeID|store_and_fwd_flag|PULocationID|DOLocationID|payment_type|fare_amount|extra|mta_tax|tip_amount|tolls_amount|improvement_surcharge|total_amount|congestion_surcharge|Airport_fee|pickup_date|dropoff_date|
+--------+-------------------+-------------------+---------------+-------------+----------+------------------+------------+------------+------------+-----------+-----+-------+----------+------------+---------------------+------------+--------------------+-----------+-----------+------------+
|       2|2024-10-12 04:16:59|2024-10-12 04:24:37|              2|         2.07|         1|                 N|         125|         100|           1|       10.7|  1.0|    0.5|       2.0|         0.0|                  1.0|        17.7|                 2.5|        0.0| 2024-10-12|  2024-10-12|
|       2|2024-10-11 23:59:07|2024-10-12 00:24:29|              1|         6.04|         1|                 N|          79|         238|           1|       29.6|  1.0|    0.5|       3.0|         0.0|                  1.0|        37.6|                 2.5|        0.0| 2024-10-11|  2024-10-12|
|       2|2024-10-10 14:08:03|2024-10-10 14:26:53|              1|         1.12|         1|                 N|         230|         141|           1|       16.3|  0.0|    0.5|      4.06|         0.0|                  1.0|       24.36|                 2.5|        0.0| 2024-10-10|  2024-10-10|
|       2|2024-10-03 22:22:07|2024-10-03 22:26:50|              1|         1.51|         1|                 N|         229|         263|           1|        8.6|  1.0|    0.5|      2.72|         0.0|                  1.0|       16.32|                 2.5|        0.0| 2024-10-03|  2024-10-03|
|       1|2024-10-05 23:46:46|2024-10-06 00:29:08|              2|          8.2|         1|                 N|         148|         188|           1|       42.2|  3.5|    0.5|      11.8|         0.0|                  1.0|        59.0|                 2.5|        0.0| 2024-10-05|  2024-10-06|
|       2|2024-10-15 00:43:57|2024-10-15 00:45:14|              1|         0.29|         5|                 N|         138|         223|           1|       65.0|  5.0|    0.0|       0.0|         0.0|                  1.0|       72.75|                 0.0|       1.75| 2024-10-15|  2024-10-15|
|       2|2024-10-14 23:42:49|2024-10-14 23:42:56|              1|         0.01|         2|                 N|          68|          68|           4|       70.0|  0.0|    0.5|       0.0|         0.0|                  1.0|        74.0|                 2.5|        0.0| 2024-10-14|  2024-10-14|
|       2|2024-10-12 22:25:19|2024-10-12 22:48:40|              4|         3.83|         1|                 N|         237|         114|           1|       22.6|  1.0|    0.5|       5.0|         0.0|                  1.0|        32.6|                 2.5|        0.0| 2024-10-12|  2024-10-12|
|       1|2024-10-12 17:26:36|2024-10-12 18:35:15|              1|         18.0|         2|                 N|         132|         186|           1|       70.0| 4.25|    0.5|     16.55|        6.94|                  1.0|       99.24|                 2.5|       1.75| 2024-10-12|  2024-10-12|
|       1|2024-10-10 14:09:32|2024-10-10 14:18:16|              1|          0.9|         1|                 Y|          68|          90|           1|        7.9|  2.5|    0.5|      2.35|         0.0|                  1.0|       14.25|                 2.5|        0.0| 2024-10-10|  2024-10-10|
+--------+-------------------+-------------------+---------------+-------------+----------+------------------+------------+------------+------------+-----------+-----+-------+----------+------------+---------------------+------------+--------------------+-----------+-----------+------------+
only showing top 10 rows






# find diff of dropoff_datetime - pickup_datetime
# get the full hh-mm-ss time interval
df_yellow_w_date.withColumn('duration', df_yellow_w_date.dropoff_datetime - df_yellow_w_date.pickup_datetime).show(10)
+--------+-------------------+-------------------+---------------+-------------+----------+------------------+------------+------------+------------+-----------+-----+-------+----------+------------+---------------------+------------+--------------------+-----------+-----------+------------+--------------------+
|VendorID|    pickup_datetime|   dropoff_datetime|passenger_count|trip_distance|RatecodeID|store_and_fwd_flag|PULocationID|DOLocationID|payment_type|fare_amount|extra|mta_tax|tip_amount|tolls_amount|improvement_surcharge|total_amount|congestion_surcharge|Airport_fee|pickup_date|dropoff_date|            duration|
+--------+-------------------+-------------------+---------------+-------------+----------+------------------+------------+------------+------------+-----------+-----+-------+----------+------------+---------------------+------------+--------------------+-----------+-----------+------------+--------------------+
|       2|2024-10-12 04:16:59|2024-10-12 04:24:37|              2|         2.07|         1|                 N|         125|         100|           1|       10.7|  1.0|    0.5|       2.0|         0.0|                  1.0|        17.7|                 2.5|        0.0| 2024-10-12|  2024-10-12|INTERVAL '0 00:07...|
|       2|2024-10-11 23:59:07|2024-10-12 00:24:29|              1|         6.04|         1|                 N|          79|         238|           1|       29.6|  1.0|    0.5|       3.0|         0.0|                  1.0|        37.6|                 2.5|        0.0| 2024-10-11|  2024-10-12|INTERVAL '0 00:25...|
|       2|2024-10-10 14:08:03|2024-10-10 14:26:53|              1|         1.12|         1|                 N|         230|         141|           1|       16.3|  0.0|    0.5|      4.06|         0.0|                  1.0|       24.36|                 2.5|        0.0| 2024-10-10|  2024-10-10|INTERVAL '0 00:18...|
|       2|2024-10-03 22:22:07|2024-10-03 22:26:50|              1|         1.51|         1|                 N|         229|         263|           1|        8.6|  1.0|    0.5|      2.72|         0.0|                  1.0|       16.32|                 2.5|        0.0| 2024-10-03|  2024-10-03|INTERVAL '0 00:04...|
|       1|2024-10-05 23:46:46|2024-10-06 00:29:08|              2|          8.2|         1|                 N|         148|         188|           1|       42.2|  3.5|    0.5|      11.8|         0.0|                  1.0|        59.0|                 2.5|        0.0| 2024-10-05|  2024-10-06|INTERVAL '0 00:42...|
|       2|2024-10-15 00:43:57|2024-10-15 00:45:14|              1|         0.29|         5|                 N|         138|         223|           1|       65.0|  5.0|    0.0|       0.0|         0.0|                  1.0|       72.75|                 0.0|       1.75| 2024-10-15|  2024-10-15|INTERVAL '0 00:01...|
|       2|2024-10-14 23:42:49|2024-10-14 23:42:56|              1|         0.01|         2|                 N|          68|          68|           4|       70.0|  0.0|    0.5|       0.0|         0.0|                  1.0|        74.0|                 2.5|        0.0| 2024-10-14|  2024-10-14|INTERVAL '0 00:00...|
|       2|2024-10-12 22:25:19|2024-10-12 22:48:40|              4|         3.83|         1|                 N|         237|         114|           1|       22.6|  1.0|    0.5|       5.0|         0.0|                  1.0|        32.6|                 2.5|        0.0| 2024-10-12|  2024-10-12|INTERVAL '0 00:23...|
|       1|2024-10-12 17:26:36|2024-10-12 18:35:15|              1|         18.0|         2|                 N|         132|         186|           1|       70.0| 4.25|    0.5|     16.55|        6.94|                  1.0|       99.24|                 2.5|       1.75| 2024-10-12|  2024-10-12|INTERVAL '0 01:08...|
|       1|2024-10-10 14:09:32|2024-10-10 14:18:16|              1|          0.9|         1|                 Y|          68|          90|           1|        7.9|  2.5|    0.5|      2.35|         0.0|                  1.0|       14.25|                 2.5|        0.0| 2024-10-10|  2024-10-10|INTERVAL '0 00:08...|
+--------+-------------------+-------------------+---------------+-------------+----------+------------------+------------+------------+------------+-----------+-----+-------+----------+------------+---------------------+------------+--------------------+-----------+-----------+------------+--------------------+
only showing top 10 rows









# find diff of dropoff_datetime - pickup_datetime
# convert to hours (divide by 60 seconds, 60 minutes)
df_yellow_w_date.withColumn('duration_hours', (df_yellow_w_date.dropoff_datetime - df_yellow_w_date.pickup_datetime).cast('int') / 60/60).show(10)
+--------+-------------------+-------------------+---------------+-------------+----------+------------------+------------+------------+------------+-----------+-----+-------+----------+------------+---------------------+------------+--------------------+-----------+-----------+------------+--------------------+
|VendorID|    pickup_datetime|   dropoff_datetime|passenger_count|trip_distance|RatecodeID|store_and_fwd_flag|PULocationID|DOLocationID|payment_type|fare_amount|extra|mta_tax|tip_amount|tolls_amount|improvement_surcharge|total_amount|congestion_surcharge|Airport_fee|pickup_date|dropoff_date|      duration_hours|
+--------+-------------------+-------------------+---------------+-------------+----------+------------------+------------+------------+------------+-----------+-----+-------+----------+------------+---------------------+------------+--------------------+-----------+-----------+------------+--------------------+
|       2|2024-10-12 04:16:59|2024-10-12 04:24:37|              2|         2.07|         1|                 N|         125|         100|           1|       10.7|  1.0|    0.5|       2.0|         0.0|                  1.0|        17.7|                 2.5|        0.0| 2024-10-12|  2024-10-12| 0.12722222222222224|
|       2|2024-10-11 23:59:07|2024-10-12 00:24:29|              1|         6.04|         1|                 N|          79|         238|           1|       29.6|  1.0|    0.5|       3.0|         0.0|                  1.0|        37.6|                 2.5|        0.0| 2024-10-11|  2024-10-12|  0.4227777777777778|
|       2|2024-10-10 14:08:03|2024-10-10 14:26:53|              1|         1.12|         1|                 N|         230|         141|           1|       16.3|  0.0|    0.5|      4.06|         0.0|                  1.0|       24.36|                 2.5|        0.0| 2024-10-10|  2024-10-10|  0.3138888888888889|
|       2|2024-10-03 22:22:07|2024-10-03 22:26:50|              1|         1.51|         1|                 N|         229|         263|           1|        8.6|  1.0|    0.5|      2.72|         0.0|                  1.0|       16.32|                 2.5|        0.0| 2024-10-03|  2024-10-03| 0.07861111111111112|
|       1|2024-10-05 23:46:46|2024-10-06 00:29:08|              2|          8.2|         1|                 N|         148|         188|           1|       42.2|  3.5|    0.5|      11.8|         0.0|                  1.0|        59.0|                 2.5|        0.0| 2024-10-05|  2024-10-06|  0.7061111111111111|
|       2|2024-10-15 00:43:57|2024-10-15 00:45:14|              1|         0.29|         5|                 N|         138|         223|           1|       65.0|  5.0|    0.0|       0.0|         0.0|                  1.0|       72.75|                 0.0|       1.75| 2024-10-15|  2024-10-15| 0.02138888888888889|
|       2|2024-10-14 23:42:49|2024-10-14 23:42:56|              1|         0.01|         2|                 N|          68|          68|           4|       70.0|  0.0|    0.5|       0.0|         0.0|                  1.0|        74.0|                 2.5|        0.0| 2024-10-14|  2024-10-14|0.001944444444444...|
|       2|2024-10-12 22:25:19|2024-10-12 22:48:40|              4|         3.83|         1|                 N|         237|         114|           1|       22.6|  1.0|    0.5|       5.0|         0.0|                  1.0|        32.6|                 2.5|        0.0| 2024-10-12|  2024-10-12|  0.3891666666666667|
|       1|2024-10-12 17:26:36|2024-10-12 18:35:15|              1|         18.0|         2|                 N|         132|         186|           1|       70.0| 4.25|    0.5|     16.55|        6.94|                  1.0|       99.24|                 2.5|       1.75| 2024-10-12|  2024-10-12|  1.1441666666666668|
|       1|2024-10-10 14:09:32|2024-10-10 14:18:16|              1|          0.9|         1|                 Y|          68|          90|           1|        7.9|  2.5|    0.5|      2.35|         0.0|                  1.0|       14.25|                 2.5|        0.0| 2024-10-10|  2024-10-10| 0.14555555555555555|
+--------+-------------------+-------------------+---------------+-------------+----------+------------------+------------+------------+------------+-----------+-----+-------+----------+------------+---------------------+------------+--------------------+-----------+-----------+------------+--------------------+
only showing top 10 rows






# find max duration_hours
df_yellow_w_date.withColumn('duration_hours', (df_yellow_w_date.dropoff_datetime - df_yellow_w_date.pickup_datetime).cast('int') / 60/60).agg({'duration_hours': 'max'}).show()
+-------------------+
|max(duration_hours)|
+-------------------+
|  162.6177777777778|
+-------------------+
```



Answer: 162 hours



## Question 5: User Interface

Spark’s User Interface which shows the application's dashboard runs on which local port?

- 80
- 443
- 4040
- 8080

```bash
http://3bf809a4-aad5-48c7-b237-0316d51fa8a7.internal.cloudapp.net:4040/
```

Answer: 4040


## Question 6: Least frequent pickup location zone

Load the zone lookup data into a temp view in Spark:

```bash
wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
```

Using the zone lookup data and the Yellow October 2024 data, what is the name of the LEAST frequent pickup location Zone?

- Governor's Island/Ellis Island/Liberty Island
- Arden Heights
- Rikers Island
- Jamaica Bay

```python
# pwd
# /workspaces/data-engineering-zoomcamp-homework/05-batch/code

# lookup CSV location
# /workspaces/data-engineering-zoomcamp-homework/05-batch/code/taxi_zone_lookup.csv

# sort in descending order
df_yellow_w_date.groupBy('PULocationID').count().orderBy('count', ascending=False).show()
+------------+------+
|PULocationID| count|
+------------+------+
|         132|194113|
|         237|191011|
|         161|177568|
|         236|167231|
|         162|132055|
|         230|127529|
|         142|124801|
|         186|121396|
|         138|118708|
|         170|110194|
|         163|108517|
|         234|104874|
|          68|103753|
|         239|102386|
|          48| 91864|
|         164| 86562|
|         249| 86242|
|         141| 84690|
|          79| 84429|
|         107| 75192|
+------------+------+
only showing top 20 rows




# read taxi_zone_lookup CSV
df_zonelookup = spark.read \
                 .option("header", "true") \
                 .option("samplingRatio", 0.01) \
                 .option("inferSchema", True) \
                 .csv('taxi_zone_lookup.csv')
df_zonelookup.show(10)
+----------+-------------+--------------------+------------+
|LocationID|      Borough|                Zone|service_zone|
+----------+-------------+--------------------+------------+
|         1|          EWR|      Newark Airport|         EWR|
|         2|       Queens|         Jamaica Bay|   Boro Zone|
|         3|        Bronx|Allerton/Pelham G...|   Boro Zone|
|         4|    Manhattan|       Alphabet City| Yellow Zone|
|         5|Staten Island|       Arden Heights|   Boro Zone|
|         6|Staten Island|Arrochar/Fort Wad...|   Boro Zone|
|         7|       Queens|             Astoria|   Boro Zone|
|         8|       Queens|        Astoria Park|   Boro Zone|
|         9|       Queens|          Auburndale|   Boro Zone|
|        10|       Queens|        Baisley Park|   Boro Zone|
+----------+-------------+--------------------+------------+
only showing top 10 rows





# merge df_yellow_w_date with taxi_zone_lookup on PULocationID and LocationID respectively
df_yellow_pickuplocationid_count.schema
StructType([StructField('PULocationID', IntegerType(), True), StructField('count', LongType(), False)])

df_zonelookup.schema
StructType([StructField('LocationID', IntegerType(), True), StructField('Borough', StringType(), True), StructField('Zone', StringType(), True), StructField('service_zone', StringType(), True)])

df_yellow_pickuplocationwithname_count = df_yellow_pickuplocationid_count.join(df_zonelookup,   # df1.join(df2
                                         df_yellow_pickuplocationid_count.PULocationID == df_zonelookup.LocationID,   # joining key
                                         'left')
df_yellow_pickuplocationwithname_count.show(10)

+------------+------+----------+---------+--------------------+------------+
|PULocationID| count|LocationID|  Borough|                Zone|service_zone|
+------------+------+----------+---------+--------------------+------------+
|         132|194113|       132|   Queens|         JFK Airport|    Airports|
|         237|191011|       237|Manhattan|Upper East Side S...| Yellow Zone|
|         161|177568|       161|Manhattan|      Midtown Center| Yellow Zone|
|         236|167231|       236|Manhattan|Upper East Side N...| Yellow Zone|
|         162|132055|       162|Manhattan|        Midtown East| Yellow Zone|
|         230|127529|       230|Manhattan|Times Sq/Theatre ...| Yellow Zone|
|         142|124801|       142|Manhattan| Lincoln Square East| Yellow Zone|
|         186|121396|       186|Manhattan|Penn Station/Madi...| Yellow Zone|
|         138|118708|       138|   Queens|   LaGuardia Airport|    Airports|
|         170|110194|       170|Manhattan|         Murray Hill| Yellow Zone|
+------------+------+----------+---------+--------------------+------------+
only showing top 10 rows










# NOW sort in ascending order for count
df_yellow_pickuplocationwithname_count.orderBy('count', ascending=True).show(10)
+------------+-----+----------+-------------+--------------------+------------+
|PULocationID|count|LocationID|      Borough|                Zone|service_zone|
+------------+-----+----------+-------------+--------------------+------------+
|         105|    1|       105|    Manhattan|Governor's Island...| Yellow Zone|
|         199|    2|       199|        Bronx|       Rikers Island|   Boro Zone|
|           5|    2|         5|Staten Island|       Arden Heights|   Boro Zone|
|         111|    3|       111|     Brooklyn| Green-Wood Cemetery|   Boro Zone|
|           2|    3|         2|       Queens|         Jamaica Bay|   Boro Zone|
|          44|    4|        44|Staten Island|Charleston/Totten...|   Boro Zone|
|          84|    4|        84|Staten Island|Eltingville/Annad...|   Boro Zone|
|         204|    4|       204|Staten Island|   Rossville/Woodrow|   Boro Zone|
|         245|    4|       245|Staten Island|       West Brighton|   Boro Zone|
|         187|    4|       187|Staten Island|       Port Richmond|   Boro Zone|
+------------+-----+----------+-------------+--------------------+------------+
only showing top 10 rows


```

Answer: Governor's Island/Ellis Island/Liberty Island




## Submitting the solutions

- Form for submitting: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw5
- Deadline: See the website
