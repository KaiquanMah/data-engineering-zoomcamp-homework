# Introduction to Docker

**[↑ Up](README.md)** | **[← Previous](README.md)** | **[Next →](02-virtual-environment.md)**

Docker is a _containerization software_ that allows us to isolate software in a similar way to virtual machines but in a much leaner way.

A Docker image is a _snapshot_ of a container that we can define to run our software, or in this case our data pipelines. By exporting our Docker images to Cloud providers such as Amazon Web Services or Google Cloud Platform we can run our containers there.

## Why Docker?

Docker provides the following advantages:

- Reproducibility: Same environment everywhere
- Isolation: Applications run independently
- Portability: Run anywhere Docker is installed

They are used in many situations:

- Integration tests: CI/CD pipelines
- Running pipelines on the cloud: AWS Batch, Kubernetes jobs
- Spark: Analytics engine for large-scale data processing
- Serverless: AWS Lambda, Google Functions

## Basic Docker Commands

Check Docker version:

```bash
docker --version

Docker version 28.5.1-1, build e180ab8ab82d22b7895a3e6e110cf6dd5c45f1d7
```


Run a simple container:

```bash
docker run hello-world



Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
17eec7bbc9d7: Pull complete 
Digest: sha256:05813aedc15fb7b4d732e1be879d3252c1c9c25d885824f6295cab4538cb85cd
Status: Downloaded newer image for hello-world:latest

Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (amd64)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

Run something more complex:

```bash
docker run ubuntu


Unable to find image 'ubuntu:latest' locally
latest: Pulling from library/ubuntu
a3629ac5b9f4: Pull complete 
Digest: sha256:7a398144c5a2fa7dbd9362e460779dc6659bd9b19df50f724250c62ca7812eb3
Status: Downloaded newer image for ubuntu:latest
```

Nothing happens. Need to run it in `-it` mode:

```bash
docker run -it ubuntu
```

We don't have `python` there so let's install it:

```bash
apt update && apt install python3
python3 -V



Python 3.12.3
root@9949608d4cc2:/# exit
exit
```







## Stateless Containers

Important: Docker containers are stateless - any changes done inside a container will NOT be saved when the container is killed and started again.

When you exit the container and use it again, the changes are gone:

```bash
docker run -it ubuntu
python3 -V


bash: python3: command not found
```

This is good, because it doesn't affect your host system. Let's say you do something crazy like this:

```bash
docker run -it ubuntu
rm -rf / # don't run it on your computer!
```

**Next time we run it, all the files are back.**






## Managing Containers

But, this is not _completely_ correct. 
The state is saved somewhere. We can see stopped containers:

```bash
docker ps -a


@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework (main) $ docker ps -a
CONTAINER ID   IMAGE         COMMAND       CREATED              STATUS                            PORTS     NAMES
4fdbed8ae01d   ubuntu        "/bin/bash"   About a minute ago   Exited (1) 1 second ago                     busy_goldberg
9f4560b17e08   ubuntu        "/bin/bash"   About a minute ago   Exited (127) About a minute ago             boring_colden
9949608d4cc2   ubuntu        "/bin/bash"   3 minutes ago        Exited (127) 2 minutes ago                  eager_euclid
2d337f7737b2   ubuntu        "/bin/bash"   3 minutes ago        Exited (0) 3 minutes ago                    lucid_kowalevski
a5d83b31aecc   hello-world   "/hello"      4 minutes ago        Exited (0) 4 minutes ago                    goofy_ardinghelli
```




We can restart one of them, but we won't do it, because it's not a good practice. 
```bash
@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework (main) $ docker ps -aq
4fdbed8ae01d
9f4560b17e08
9949608d4cc2
2d337f7737b2
a5d83b31aecc
```

They take space, so let's delete them:

```bash
docker rm `docker ps -aq`


@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework (main) $ docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```



Next time we run something, we add `--rm`:

```bash
docker run -it --rm ubuntu


@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework (main) $ docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```








## Different Base Images

There are other base images besides `hello-world` and `ubuntu`. For example, Python:

```bash
docker run -it --rm python:3.9.16
# add -slim to get a smaller version
```

This one starts `python`. If we want bash, we need to overwrite `entrypoint`:

```bash
docker run -it \
    --rm \
    --entrypoint=bash \
    python:3.9.16-slim
```






## Volumes

So, we know that with docker we can restore any container to its initial state in a reproducible manner. But what about data? A common way to do so is with _volumes_.

Let's create some data in `test`:

```bash
mkdir test
cd test
touch file1.txt file2.txt file3.txt
echo "Hello from host" > file1.txt
cd ..
```



Now let's create a simple script `test/list_files.py` that shows the files in the folder:

```python
from pathlib import Path

current_dir = Path.cwd()
current_file = Path(__file__).name

print(f"Files in {current_dir}:")

for filepath in current_dir.iterdir():
    if filepath.name == current_file:
        continue

    print(f"  - {filepath.name}")

    if filepath.is_file():
        content = filepath.read_text(encoding='utf-8')
        print(f"    Content: {content}")
```

Now let's map this to a Python container:

```bash
docker run -it \
    --rm \
    -v $(pwd)/test:/app/test \
    --entrypoint=bash \
    python:3.9.16-slim
```

Inside the container, run:

```bash
cd /app/test
ls -la
cat file1.txt
python list_files.py
```

```bash
root@eaa1a046257d:/# pwd
/
root@eaa1a046257d:/# ls
app  bin  boot  dev  etc  home  lib  lib64  media  mnt  opt  proc  root  run  sbin  srv  sys  tmp  usr  var


root@eaa1a046257d:/# cd app
root@eaa1a046257d:/app# pwd
/app
root@eaa1a046257d:/app# ls
test


root@eaa1a046257d:/app# cd test
root@eaa1a046257d:/app/test# pwd
/app/test
root@eaa1a046257d:/app/test# ls
file1.txt  file2.txt  file3.txt  list_files.py


root@eaa1a046257d:/app/test# ls -la
total 16
drwxrwxrwx+ 2 1000 1000 4096 Jan 18 04:00 .
drwxr-xr-x  3 root root 4096 Jan 18 04:01 ..
-rw-rw-rw-  1 1000 1000   16 Jan 18 04:00 file1.txt
-rw-rw-rw-  1 1000 1000    0 Jan 18 04:00 file2.txt
-rw-rw-rw-  1 1000 1000    0 Jan 18 04:00 file3.txt
-rw-rw-rw-  1 1000 1000  374 Jan 18 04:00 list_files.py


root@eaa1a046257d:/app/test# cat file1.txt
Hello from host


root@eaa1a046257d:/app/test# python list_files.py
Files in /app/test:
  - file1.txt
    Content: Hello from host

  - file2.txt
    Content: 
  - file3.txt
    Content: 
```




You'll see the files from your host machine are accessible in the container!

**[↑ Up](README.md)** | **[← Previous](README.md)** | **[Next →](02-virtual-environment.md)**
