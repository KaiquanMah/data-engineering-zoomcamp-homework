## Module 2 Homework

ATTENTION: At the end of the submission form, you will be required to include a link to your GitHub repository or other public code-hosting site. This repository should contain your code for solving the homework. If your solution includes code that is not in file format, please include these directly in the README file of your repository.

> In case you don't get one option exactly, select the closest one 

For the homework, we'll be working with the _green_ taxi dataset located here:

`https://github.com/DataTalksClub/nyc-tlc-data/releases/tag/green/download`

To get a `wget`-able link, use this prefix (note that the link itself gives 404):

`https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/`

### Assignment

So far in the course, we processed data for the year 2019 and 2020. Your task is to extend the existing flows to include data for the year 2021.

![homework datasets](../../../02-workflow-orchestration/images/homework.png)

As a hint, Kestra makes that process really easy:
1. You can leverage the backfill functionality in the [scheduled flow](../../../02-workflow-orchestration/flows/05_gcp_taxi_scheduled.yaml) to backfill the data for the year 2021. Just make sure to select the time period for which data exists i.e. from `2021-01-01` to `2021-07-31`. Also, make sure to do the same for both `yellow` and `green` taxi data (select the right service in the `taxi` input).
2. Alternatively, run the flow manually for each of the seven months of 2021 for both `yellow` and `green` taxi data. Challenge for you: find out how to loop over the combination of Year-Month and `taxi`-type using `ForEach` task which triggers the flow for each combination using a `Subflow` task.

### Quiz Questions

Complete the quiz shown below. It's a set of 6 multiple-choice questions to test your understanding of workflow orchestration, Kestra, and ETL pipelines.

1) Within the execution for `Yellow` Taxi data for the year `2020` and month `12`: what is the uncompressed file size (i.e. the output file `yellow_tripdata_2020-12.csv` of the `extract` task)?
- 128.3 MiB
- 134.5 MiB
- 364.7 MiB
- 692.6 MiB

```bash
wget -qO- https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2020-12.csv.gz | gunzip > yellow_tripdata_2020-12.csv


@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework (main) $ ls -la
total 131364
drwxrwxrwx+ 6 codespace root           4096 Jan 21 09:03 .
drwxr-xrwx+ 5 codespace root           4096 Jan 18 03:50 ..
drwxrwxrwx+ 8 codespace root           4096 Jan 21 08:56 .git
-rw-rw-rw-  1 codespace codespace       383 Jan 20 07:27 .gitignore
drwxrwxrwx+ 4 codespace root           4096 Jan 20 08:25 01-docker-terraform
drwxrwxrwx+ 4 codespace codespace      4096 Jan 21 08:54 02-workflow-orchestration
-rw-rw-rw-  1 codespace root           1211 Jan 18 03:50 LICENSE
drwxrwxrwx+ 6 codespace codespace      4096 Jan 20 13:56 later
-rw-rw-rw-  1 codespace codespace 134481400 Jan 21 09:03 yellow_tripdata_2020-12.csv
```

* Answer: 134.5 MiB



2) What is the rendered value of the variable `file` when the inputs `taxi` is set to `green`, `year` is set to `2020`, and `month` is set to `04` during execution?
- `{{inputs.taxi}}_tripdata_{{inputs.year}}-{{inputs.month}}.csv` 
- `green_tripdata_2020-04.csv`
- `green_tripdata_04_2020.csv`
- `green_tripdata_2020.csv`

Answer: `green_tripdata_2020-04.csv`



* Kai 20226.01.21 Notes
  * Load data using 09_gcp_taxi_scheduled.yaml using Triggers > Backfill
  * FAILED - Try to extract list of execution runs `https://kestra.io/docs/api-reference/open-source#get-/api/v1/-tenant-/executions`
    ```bash
    kaiqu@kai-aftershock MINGW64 ~/Downloads/data-engineering-zoomcamp-homework (main)
    $ curl -k -L "https://expert-waddle-v6w4g64w564wc7wv-8080.app.github.dev/api/v1/main/executions?namespace=zoomcamp&flowId=09_gcp_taxi_scheduled" -o executions.json
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0

    kaiqu@kai-aftershock MINGW64 ~/Downloads/data-engineering-zoomcamp-homework (main)
    $ curl -k -L "https://expert-waddle-v6w4g64w564wc7wv-8080.app.github.dev/api/v1/executions?namespace=zoomcamp&flowId=09_gcp_taxi_scheduled" -o executions.json
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0

    kaiqu@kai-aftershock MINGW64 ~/Downloads/data-engineering-zoomcamp-homework (main)
    $ curl -k -L "https://expert-waddle-v6w4g64w564wc7wv-8080.app.github.dev/api/v1/main/executions?namespace=zoomcamp&flowId=09_gcp_taxi_scheduled" \
    -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36" \
    -H "Accept: application/json" \
    -H "Accept-Language: en-US,en;q=0.9" \
    -H "Referer: https://expert-waddle-v6w4g64w564wc7wv-8080.app.github.dev/" \
    -o executions.json
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0

    kaiqu@kai-aftershock MINGW64 ~/Downloads/data-engineering-zoomcamp-homework (main)
    $ # Remove "/main/" from the path - CE doesn't have tenants!
    # Use /executions/search endpoint

    curl -k -L "https://expert-waddle-v6w4g64w564wc7wv-8080.app.github.dev/api/v1/executions/search?namespace=zoomcamp&flowId=09_gcp_taxi_scheduled&size=100" \ 
    -H "Accept: application/json" \
    -o executions.json
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0

    kaiqu@kai-aftershock MINGW64 ~/Downloads/data-engineering-zoomcamp-homework (main)
    $ curl -k -L -X POST "https://expert-waddle-v6w4g64w564wc7wv-8080.app.github.dev/api/v1/executions/search" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d '{
        "namespace": "zoomcamp",
        "flowId": "09_gcp_taxi_scheduled",
        "size": 100
    }' \
    -o executions.json
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    100    89    0     0  100    89      0    916 --:--:-- --:--:-- --:--:--   936

    kaiqu@kai-aftershock MINGW64 ~/Downloads/data-engineering-zoomcamp-homework (main)
    $ curl -k -L "https://expert-waddle-v6w4g64w564wc7wv-8080.app.github.dev/api/v1/executions/search?namespace=zoomcamp&flowId=09_gcp_taxi_scheduled&size=100"   -H "Accept: application/json"   -o executions.json
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0









    @kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/02-workflow-orchestration (main) $ curl http://expert-waddle-v6w4g64w564wc7wv-8080.app.github.dev/api/v1/main/executions?namespace=zoomcamp&flowId=09_gcp_taxi_scheduled
    [1] 14002
    @kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/02-workflow-orchestration (main) $ <html>
    <head><title>308 Permanent Redirect</title></head>
    <body>
    <center><h1>308 Permanent Redirect</h1></center>
    <hr><center>nginx</center>
    </body>
    </html>
    ^C
    [1]+  Done                    curl http://expert-waddle-v6w4g64w564wc7wv-8080.app.github.dev/api/v1/main/executions?namespace=zoomcamp
    @kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/02-workflow-orchestration (main) $ curl "http://localhost:8080/api/v1/executions/search?namespace=zoomcamp&flowId=09_gcp_taxi_scheduled&size=100" \
    -o executions.json
    % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                    Dload  Upload   Total   Spent    Left  Speed
    0     0    0     0    0     0      0      0 --:--:-- --:--:-- --:--:--     0
    @kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/02-workflow-orchestration (main) $ # In Codespace - see actual response
    curl -v "http://localhost:8080/api/v1/executions/search?namespace=zoomcamp&flowId=09_gcp_taxi_scheduled&size=100"
    * Host localhost:8080 was resolved.
    * IPv6: ::1
    * IPv4: 127.0.0.1
    *   Trying [::1]:8080...
    * Connected to localhost (::1) port 8080
    > GET /api/v1/executions/search?namespace=zoomcamp&flowId=09_gcp_taxi_scheduled&size=100 HTTP/1.1
    > Host: localhost:8080
    > User-Agent: curl/8.5.0
    > Accept: */*
    > 
    < HTTP/1.1 401 Unauthorized
    < WWW-Authenticate: Basic
    < content-length: 0
    < 
    * Connection #0 to host localhost left intact
    @kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/02-workflow-orchestration (main) $ curl "http://localhost:8080/api/v1/flows"
    ```
  * Download list execution runs by running a flow
| Id | Start date | End date | Duration | Namespace | Flow | Labels | State | Actions |
| ES98Ffb3 | Wed, Jan 21, 2026 5:26 PM | Wed, Jan 21, 2026 5:27 PM | 1m, 1.01s | zoomcamp | 09_gcp_taxi_scheduled | file:yellow_tripdata_2020-12.csvtaxi:yellow | SUCCESS | Details |
| 5n8KVHyz | Wed, Jan 21, 2026 5:25 PM | Wed, Jan 21, 2026 5:26 PM | 1m, 8.63s | zoomcamp | 09_gcp_taxi_scheduled | file:yellow_tripdata_2020-11.csvtaxi:yellow |  | SUCCESS | Details |
| 2gIESsbx | Wed, Jan 21, 2026 5:23 PM | Wed, Jan 21, 2026 5:25 PM | 1m, 17.36s | zoomcamp | 09_gcp_taxi_scheduled | file:yellow_tripdata_2020-10.csvtaxi:yellow |  | SUCCESS | Details |
| 44rznaUy | Wed, Jan 21, 2026 5:22 PM | Wed, Jan 21, 2026 5:23 PM | 1m, 2.64s | zoomcamp | 09_gcp_taxi_scheduled | file:yellow_tripdata_2020-09.csvtaxi:yellow |  | SUCCESS | Details |
| 60IHjoiZ | Wed, Jan 21, 2026 5:22 PM | Wed, Jan 21, 2026 5:22 PM | 29.31s | zoomcamp | 09_gcp_taxi_scheduled | file:green_tripdata_2021-07.csvtaxi:green |  | SUCCESS | Details |
| 1NtK7wZ3 | Wed, Jan 21, 2026 5:21 PM | Wed, Jan 21, 2026 5:22 PM | 50.71s | zoomcamp | 09_gcp_taxi_scheduled | file:yellow_tripdata_2020-08.csvtaxi:yellow |  | SUCCESS | Details |
| 6ZBpw8AQ | Wed, Jan 21, 2026 5:21 PM | Wed, Jan 21, 2026 5:22 PM | 17.83s | zoomcamp | 09_gcp_taxi_scheduled | file:green_tripdata_2021-06.csvtaxi:green |  | SUCCESS | Details |
| 6ytB6sSt | Wed, Jan 21, 2026 5:21 PM | Wed, Jan 21, 2026 5:21 PM | 18.36s | zoomcamp | 09_gcp_taxi_scheduled | file:green_tripdata_2021-05.csvtaxi:green |  | SUCCESS | Details |
| 7KH8Y5Gd | Wed, Jan 21, 2026 5:21 PM | Wed, Jan 21, 2026 5:21 PM | 18.34s | zoomcamp | 09_gcp_taxi_scheduled | file:green_tripdata_2021-04.csvtaxi:green |  | SUCCESS | Details |
| 31BzK9Y3 | Wed, Jan 21, 2026 5:20 PM | Wed, Jan 21, 2026 5:21 PM | 54.27s | zoomcamp | 09_gcp_taxi_scheduled | file:green_tripdata_2021-06.csvtaxi:green |  | SUCCESS | Details |
| 6BZp5Q6L | Wed, Jan 21, 2026 5:20 PM | Wed, Jan 21, 2026 5:21 PM | 19.68s | zoomcamp | 09_gcp_taxi_scheduled | file:green_tripdata_2021-03.csvtaxi:green |  | SUCCESS | Details |
| 2m5JO9Da | Wed, Jan 21, 2026 5:19 PM | Wed, Jan 21, 2026 5:20 PM | 56.51s | zoomcamp | 09_gcp_taxi_scheduled | file:green_tripdata_2021-02.csvtaxi:green |  | SUCCESS | Details |
| 2uHGZBE5 | Wed, Jan 21, 2026 5:19 PM | Wed, Jan 21, 2026 5:19 PM | 21.70s | zoomcamp | 09_gcp_taxi_scheduled | file:green_tripdata_2021-01.csvtaxi:green |  | SUCCESS | Details |
| 6tgdlXaZ | Wed, Jan 21, 2026 5:19 PM | Wed, Jan 21, 2026 5:20 PM | 1m, 35.24s | zoomcamp | 09_gcp_taxi_scheduled | file:yellow_tripdata_2020-06.csvtaxi:yellow |  | SUCCESS | Details |
| 7lapRxlP | Wed, Jan 21, 2026 5:19 PM | Wed, Jan 21, 2026 5:19 PM | 18.39s | zoomcamp | 09_gcp_taxi_scheduled | file:green_tripdata_2020-12.csvtaxi:green |  | SUCCESS | Details |
| 5hWohFVr | Wed, Jan 21, 2026 5:18 PM | Wed, Jan 21, 2026 5:19 PM | 25.04s | zoomcamp | 09_gcp_taxi_scheduled | file:yellow_tripdata_2020-05.csvtaxi:yellow |  | SUCCESS | Details |
| 6wnFX8SK | Wed, Jan 21, 2026 5:18 PM | Wed, Jan 21, 2026 5:19 PM | 21.73s | zoomcamp | 09_gcp_taxi_scheduled | file:green_tripdata_2020-11.csvtaxi:green |  | SUCCESS | Details |
| 4Sv7u8lD | Wed, Jan 21, 2026 5:18 PM | Wed, Jan 21, 2026 5:18 PM | 22.72s | zoomcamp | 09_gcp_taxi_scheduled | file:yellow_tripdata_2020-04.csvtaxi:yellow |  | SUCCESS | Details |
| 1ubEURxU | Wed, Jan 21, 2026 5:18 PM | Wed, Jan 21, 2026 5:18 PM | 18.55s | zoomcamp | 09_gcp_taxi_scheduled | file:green_tripdata_2020-10.csvtaxi:green |  | SUCCESS | Details |
| 4nppiEyd | Wed, Jan 21, 2026 5:17 PM | Wed, Jan 21, 2026 5:18 PM | 53.26s | zoomcamp | 09_gcp_taxi_scheduled | file:green_tripdata_2020-09.csvtaxi:green |  | SUCCESS | Details |
| 7AcUP93a | Wed, Jan 21, 2026 5:17 PM | Wed, Jan 21, 2026 5:17 PM | 18.12s | zoomcamp | 09_gcp_taxi_scheduled | file:green_tripdata_2020-08.csvtaxi:green |  | SUCCESS | Details |
| 37QhQDvZ | Wed, Jan 21, 2026 5:16 PM | Wed, Jan 21, 2026 5:17 PM | 18.41s | zoomcamp | 09_gcp_taxi_scheduled | file:green_tripdata_2020-07.csvtaxi:green |  | SUCCESS | Details |
| 78J21ylW | Wed, Jan 21, 2026 5:16 PM | Wed, Jan 21, 2026 5:16 PM | 20.44s | zoomcamp | 09_gcp_taxi_scheduled | file:green_tripdata_2020-06.csvtaxi:green |  | SUCCESS | Details |
| 5fNwZnn8 | Wed, Jan 21, 2026 5:16 PM | Wed, Jan 21, 2026 5:18 PM | 1m, 57.09s | zoomcamp | 09_gcp_taxi_scheduled | file:yellow_tripdata_2020-03.csvtaxi:yellow |  | SUCCESS | Details |
| 4VxDGrlF | Wed, Jan 21, 2026 5:16 PM | Wed, Jan 21, 2026 5:16 PM | 16.76s | zoomcamp | 09_gcp_taxi_scheduled | file:green_tripdata_2020-05.csvtaxi:green |  | SUCCESS | Details |
| 60IHjoiZ | Wed, Jan 21, 2026 5:22 PM | Wed, Jan 21, 2026 5:22 PM | 29.31s | zoomcamp | 09_gcp_taxi_scheduled | file:green_tripdata_2021-07.csvtaxi:green |  | SUCCESS | Details |
| 1NtK7wZ3 | Wed, Jan 21, 2026 5:21 PM | Wed, Jan 21, 2026 5:22 PM | 50.71s | zoomcamp | 09_gcp_taxi_scheduled | file:yellow_tripdata_2020-08.csvtaxi:yellow |  | SUCCESS | Details |
| 6ZBpw8AQ | Wed, Jan 21, 2026 5:21 PM | Wed, Jan 21, 2026 5:22 PM | 17.83s | zoomcamp | 09_gcp_taxi_scheduled | file:green_tripdata_2021-06.csvtaxi:green |  | SUCCESS | Details |


6wnFX8SK
Wed, Jan 21, 2026 5:18 PM
Wed, Jan 21, 2026 5:19 PM
21.73s
zoomcamp
09_gcp_taxi_scheduled
file:green_tripdata_2020-11.csvtaxi:green
4Sv7u8lD
Wed, Jan 21, 2026 5:18 PM
Wed, Jan 21, 2026 5:18 PM
22.72s
zoomcamp
09_gcp_taxi_scheduled
file:yellow_tripdata_2020-04.csvtaxi:yellow
1ubEURxU
Wed, Jan 21, 2026 5:18 PM
Wed, Jan 21, 2026 5:18 PM
18.55s
zoomcamp
09_gcp_taxi_scheduled
file:green_tripdata_2020-10.csvtaxi:green
4nppiEyd
Wed, Jan 21, 2026 5:17 PM
Wed, Jan 21, 2026 5:18 PM
53.26s
zoomcamp
09_gcp_taxi_scheduled
file:green_tripdata_2020-09.csvtaxi:green
7AcUP93a
Wed, Jan 21, 2026 5:17 PM
Wed, Jan 21, 2026 5:17 PM
18.12s
zoomcamp
09_gcp_taxi_scheduled
file:green_tripdata_2020-08.csvtaxi:green
37QhQDvZ
Wed, Jan 21, 2026 5:16 PM
Wed, Jan 21, 2026 5:17 PM
18.41s
zoomcamp
09_gcp_taxi_scheduled
file:green_tripdata_2020-07.csvtaxi:green
78J21ylW
Wed, Jan 21, 2026 5:16 PM
Wed, Jan 21, 2026 5:16 PM
20.44s
zoomcamp
09_gcp_taxi_scheduled
file:green_tripdata_2020-06.csvtaxi:green
5fNwZnn8
Wed, Jan 21, 2026 5:16 PM
Wed, Jan 21, 2026 5:18 PM
1m, 57.09s
zoomcamp
09_gcp_taxi_scheduled
file:yellow_tripdata_2020-03.csvtaxi:yellow
4VxDGrlF
Wed, Jan 21, 2026 5:16 PM
Wed, Jan 21, 2026 5:16 PM
16.76s
zoomcamp
09_gcp_taxi_scheduled
file:green_tripdata_2020-05.csvtaxi:green
5J5P3abd
Wed, Jan 21, 2026 5:16 PM
Wed, Jan 21, 2026 5:16 PM
16.54s
zoomcamp
09_gcp_taxi_scheduled
file:green_tripdata_2020-04.csvtaxi:green
5aEM6MmX
Wed, Jan 21, 2026 5:15 PM
Wed, Jan 21, 2026 5:15 PM
24.11s
zoomcamp
09_gcp_taxi_scheduled
file:green_tripdata_2020-03.csvtaxi:green
39WXmch9
Wed, Jan 21, 2026 5:15 PM
Wed, Jan 21, 2026 5:15 PM
32.60s
zoomcamp
09_gcp_taxi_scheduled
file:green_tripdata_2020-02.csvtaxi:green
7BTHyGOV
Wed, Jan 21, 2026 5:14 PM
Wed, Jan 21, 2026 5:15 PM
33.25s
zoomcamp
09_gcp_taxi_scheduled
file:green_tripdata_2020-01.csvtaxi:green
6ekGh9TT
Wed, Jan 21, 2026 5:13 PM
Wed, Jan 21, 2026 5:16 PM
3m, 22.39s
zoomcamp
09_gcp_taxi_scheduled
file:yellow_tripdata_2020-02.csvtaxi:yellow
48pUgMGQ
Wed, Jan 21, 2026 5:07 PM
Wed, Jan 21, 2026 5:10 PM
3m, 26.34s
zoomcamp
09_gcp_taxi_scheduled
file:yellow_tripdata_2020-01.csvtaxi:yellow
5C5Daq4A
Wed, Jan 21, 2026 5:06 PM
Wed, Jan 21, 2026 5:08 PM
1m, 58.13s
zoomcamp
09_gcp_taxi_scheduled
file:yellow_tripdata_2021-07.csvtaxi:yellow
3V9ToELD
Wed, Jan 21, 2026 5:04 PM
Wed, Jan 21, 2026 5:06 PM
1m, 52.49s
zoomcamp
09_gcp_taxi_scheduled
file:yellow_tripdata_2021-06.csvtaxi:yellow
64U8w6Ee
Wed, Jan 21, 2026 5:02 PM
Wed, Jan 21, 2026 5:04 PM
1m, 51.75s
zoomcamp
09_gcp_taxi_scheduled
file:yellow_tripdata_2021-05.csvtaxi:yellow
1wVN9HsT
Wed, Jan 21, 2026 5:00 PM
Wed, Jan 21, 2026 5:02 PM
1m, 33.27s
zoomcamp
09_gcp_taxi_scheduled
file:yellow_tripdata_2021-04.csvtaxi:yellow
4ohFMYBw
Wed, Jan 21, 2026 4:59 PM
Wed, Jan 21, 2026 5:00 PM
1m, 20.88s
zoomcamp
09_gcp_taxi_scheduled
file:yellow_tripdata_2021-03.csvtaxi:yellow
7N5ZgqyZ
Wed, Jan 21, 2026 4:58 PM
Wed, Jan 21, 2026 4:59 PM
59.08s
zoomcamp
09_gcp_taxi_scheduled
file:yellow_tripdata_2021-02.csvtaxi:yellow
60CvMDHc
Wed, Jan 21, 2026 4:57 PM
Wed, Jan 21, 2026 4:58 PM
1m, 7.57s
zoomcamp
09_gcp_taxi_scheduled
file:yellow_tripdata_2021-01.csvtaxi:yellow
IM8YEGxD
Wed, Jan 21, 2026 4:02 PM
Wed, Jan 21, 2026 4:06 PM
4m, 1.38s
zoomcamp
09_gcp_taxi_scheduled
file:yellow_tripdata_2019-02.csvtaxi:yellow
qCudMigM
Wed, Jan 21, 2026 3:58 PM
Wed, Jan 21, 2026 4:02 PM
4m, 2.78s
zoomcamp
09_gcp_taxi_scheduled
file:yellow_tripdata_2019-01.csvtaxi:yellow
2OGCtcHF
Wed, Jan 21, 2026 3:53 PM
Wed, Jan 21, 2026 3:58 PM
4m, 15.20s
zoomcamp
09_gcp_taxi_scheduled
file:yellow_tripdata_2019-03.csvtaxi:yellow
    ```


3) How many rows are there for the `Yellow` Taxi data for all CSV files in the year 2020?
- 13,537.299
- 24,648,499
- 18,324,219
- 29,430,127

4) How many rows are there for the `Green` Taxi data for all CSV files in the year 2020?
- 5,327,301
- 936,199
- 1,734,051
- 1,342,034

5) How many rows are there for the `Yellow` Taxi data for the March 2021 CSV file?
- 1,428,092
- 706,911
- 1,925,152
- 2,561,031

6) How would you configure the timezone to New York in a Schedule trigger?
- Add a `timezone` property set to `EST` in the `Schedule` trigger configuration  
- Add a `timezone` property set to `America/New_York` in the `Schedule` trigger configuration
- Add a `timezone` property set to `UTC-5` in the `Schedule` trigger configuration
- Add a `location` property set to `New_York` in the `Schedule` trigger configuration  

* Answer: Add a `timezone` property set to `America/New_York` in the `Schedule` trigger configuration
```bash
timezone        string
    Default     Etc/UTC
    Description The time zone identifier (i.e. the second column in the Wikipedia table https://en.wikipedia.org/wiki/List_of_tz_database_time_zones) to use for evaluating the cron expression. Default value is the server default zone ID.
```

## Submitting the solutions

* Form for submitting: https://courses.datatalks.club/de-zoomcamp-2026/homework/hw2
* Check the link above to see the due date

## Solution

Will be added after the due date
