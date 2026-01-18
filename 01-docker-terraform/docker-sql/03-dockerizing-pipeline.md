# Dockerizing the Pipeline

**[↑ Up](README.md)** | **[← Previous](02-virtual-environment.md)** | **[Next →](04-postgres-docker.md)**

Now let's containerize the script. Create the following `Dockerfile` file:

## 1. Simple Dockerfile with pip

```dockerfile
# base Docker image that we will build on
FROM python:3.13.11-slim

# set up our image by installing prerequisites; pandas in this case
RUN pip install pandas pyarrow

# set up the working directory inside the container
WORKDIR /app
# copy the script to the container. 1st name is source file, 2nd is destination
COPY pipeline.py pipeline.py

# define what to do first when the container runs
# in this example, we will just run the script
ENTRYPOINT ["python", "pipeline.py"]
```

**Explanation:**

- `FROM`: Base image (Python 3.13)
- `RUN`: Execute commands during build
- `WORKDIR`: Set working directory
- `COPY`: Copy files into the image
- `ENTRYPOINT`: Default command to run




### Build and Run

Let's **build the image:**

```bash
docker build -t test:pandas .
```

* The **image name** will be `test` and its **tag** will be `pandas`. 
* **If the tag isn't specified** it will **default to `latest`.**
* We can now run the container and pass an argument to it, so that our pipeline will receive it:

```bash
docker run -it --rm test:pandas some_number
```

You should get the same output you did when you ran the pipeline script by itself.

> Note: these instructions assume that `pipeline.py` and `Dockerfile` are in the same directory. The Docker commands should also be run from the same directory as these files.




## 2. Dockerfile with uv

What about uv? Let's use it instead of using pip:

```dockerfile
# Start with slim Python 3.13 image
FROM python:3.13.10-slim

# Copy uv binary from official uv docker image (multi-stage build pattern)
#      put in '/bin' folder in ur new docker img
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set working directory
WORKDIR /app

# Add virtual environment to PATH so we can use installed packages
ENV PATH="/app/.venv/bin:$PATH"

# Copy dependency files first (better layer caching)
COPY "pyproject.toml" "uv.lock" ".python-version" ./
# Install dependencies from lock file (ensures reproducible builds)
RUN uv sync --locked

# Copy application code
COPY pipeline.py pipeline.py

# Set entry point
ENTRYPOINT ["python", "pipeline.py"]
```



### Build docker img AND run docker container (from img)
```bash
@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework (main) $ cd 01-docker-terraform/docker-sql/pipeline/
@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ ls
Dockerfile  docker-compose.yaml  ingest_data.py  output_day_10.parquet  pipeline.py  pyproject.toml  uv.lock


@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ docker build -t test:pandas .
[+] Building 29.2s (15/15) FINISHED                                                                                                              docker:default
 => [internal] load build definition from Dockerfile                                                                                                       0.0s
 => => transferring dockerfile: 484B                                                                                                                       0.0s
 => [internal] load metadata for docker.io/library/python:3.13.11-slim                                                                                     2.5s
 => [internal] load metadata for ghcr.io/astral-sh/uv:latest                                                                                               2.1s
 => [auth] astral-sh/uv:pull token for ghcr.io                                                                                                             0.0s
 => [auth] library/python:pull token for registry-1.docker.io                                                                                              0.0s
 => [internal] load .dockerignore                                                                                                                          0.0s
 => => transferring context: 2B                                                                                                                            0.0s
 => FROM ghcr.io/astral-sh/uv:latest@sha256:9a23023be68b2ed09750ae636228e903a54a05ea56ed03a934d00fe9fbeded4b                                               6.0s
 => => resolve ghcr.io/astral-sh/uv:latest@sha256:9a23023be68b2ed09750ae636228e903a54a05ea56ed03a934d00fe9fbeded4b                                         0.0s
 => => sha256:02338ef4d522b073c9469e1656cfa160407cb7160023300bb8622c9757778b13 1.30kB / 1.30kB                                                             0.0s
 => => sha256:9a23023be68b2ed09750ae636228e903a54a05ea56ed03a934d00fe9fbeded4b 2.19kB / 2.19kB                                                             0.0s
 => => sha256:08a7428e3daeb4ff634fe06d3d9aec278579e88f770b5d141e5a408cb998f40a 669B / 669B                                                                 0.0s
 => => sha256:5b10ebfb4e369f07b34982c85caaab98838a61ebb54e54946271f61d7cf1f8a6 23.02MB / 23.02MB                                                           4.1s
 => => sha256:b3d2c6abdae87c43a56d2830b783d600de9274bb8791534edac6e02d23667aa3 98B / 98B                                                                   1.5s
 => => extracting sha256:5b10ebfb4e369f07b34982c85caaab98838a61ebb54e54946271f61d7cf1f8a6                                                                  0.5s
 => => extracting sha256:b3d2c6abdae87c43a56d2830b783d600de9274bb8791534edac6e02d23667aa3                                                                  0.0s
 => [internal] load build context                                                                                                                          0.0s
 => => transferring context: 245.34kB                                                                                                                      0.0s
 => [stage-0 1/6] FROM docker.io/library/python:3.13.11-slim@sha256:51e1a0a317fdb6e170dc791bbeae63fac5272c82f43958ef74a34e170c6f8b18                       6.4s
 => => resolve docker.io/library/python:3.13.11-slim@sha256:51e1a0a317fdb6e170dc791bbeae63fac5272c82f43958ef74a34e170c6f8b18                               0.0s
 => => sha256:8843ea38a07e15ac1b99c72108fbb492f737032986cc0b65ed351f84e5521879 1.29MB / 1.29MB                                                             0.9s
 => => sha256:0bee50492702eb5d822fbcbac8f545a25f5fe173ec8030f57691aefcc283bbc9 11.79MB / 11.79MB                                                           0.9s
 => => sha256:51e1a0a317fdb6e170dc791bbeae63fac5272c82f43958ef74a34e170c6f8b18 10.37kB / 10.37kB                                                           0.0s
 => => sha256:fbc43b66207d7e2966b5f06e86f2bc46aa4b10f34bf97784f3a10da80b1d6f0b 1.75kB / 1.75kB                                                             0.0s
 => => sha256:dd4049879a507d6f4bb579d2d94b591135b95daab37abb3df9c1d40b7d71ced0 5.53kB / 5.53kB                                                             0.0s
 => => sha256:119d43eec815e5f9a47da3a7d59454581b1e204b0c34db86f171b7ceb3336533 29.77MB / 29.77MB                                                           0.9s
 => => extracting sha256:119d43eec815e5f9a47da3a7d59454581b1e204b0c34db86f171b7ceb3336533                                                                  1.2s
 => => sha256:36b6de65fd8d6bd36071ea9efa7d078ebdc11ecc23d2426ec9c3e9f092ae824d 249B / 249B                                                                 1.2s
 => => extracting sha256:8843ea38a07e15ac1b99c72108fbb492f737032986cc0b65ed351f84e5521879                                                                  0.2s
 => => extracting sha256:0bee50492702eb5d822fbcbac8f545a25f5fe173ec8030f57691aefcc283bbc9                                                                  1.8s
 => => extracting sha256:36b6de65fd8d6bd36071ea9efa7d078ebdc11ecc23d2426ec9c3e9f092ae824d                                                                  0.0s
 => [stage-0 2/6] COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/                                                                                        0.7s
 => [stage-0 3/6] WORKDIR /code                                                                                                                            0.0s
 => [stage-0 4/6] COPY pyproject.toml .python-version uv.lock ./                                                                                           0.0s
 => [stage-0 5/6] RUN uv sync --locked                                                                                                                    12.5s
 => [stage-0 6/6] COPY pipeline.py .                                                                                                                    0.0s
 => exporting to image                                                                                                                                     6.8s
 => => exporting layers                                                                                                                                    6.8s
 => => writing image sha256:25252d83c5196bd5fcff6b5b82cde24626cc5556b8088f97ada621292c39f27c                                                               0.0s
 => => naming to docker.io/library/test:pandas                                                                                                             0.0s








@kaiquanmah0 ➜ .../data-engineering-zoomcamp-homework/01-docker-terraform/docker-sql/pipeline (main) $ docker run -it --rm test:pandas 8
arguments ['pipeline.py', '8']
Running pipeline for day 8
   A  B
0  1  3
1  2  4
```





**[↑ Up](README.md)** | **[← Previous](02-virtual-environment.md)** | **[Next →](04-postgres-docker.md)**
