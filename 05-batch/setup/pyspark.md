## After OpenJDK AND Spark setup, now create virtualenv AND install jupyter library inside

* Reference: https://datatalks.club/faq/data-engineering-zoomcamp.html#e269cf9e38
```bash
# Update and Upgrade Packages:
sudo apt update && sudo apt -y upgrade
...
Get:24 http://archive.ubuntu.com/ubuntu noble-backports/universe amd64 Packages [34.6 kB]
Reading package lists... Done                                                                                                                                      
W: GPG error: https://dl.yarnpkg.com/debian stable InRelease: The following signatures were invalid: EXPKEYSIG 23E7166788B63E1E Yarn Packaging <yarn@dan.cx>
E: The repository 'https://dl.yarnpkg.com/debian stable InRelease' is not signed.
N: Updating from such a repository can't be done securely, and is therefore disabled by default.
N: See apt-secure(8) manpage for repository creation and user configuration details.


# Install Python
sudo apt install python3-pip python3-dev
Reading package lists... Done
Building dependency tree... Done
Reading state information... Done
python3-pip is already the newest version (24.0+dfsg-1ubuntu1.3).
python3-dev is already the newest version (3.12.3-0ubuntu2.1).
0 upgraded, 0 newly installed, 0 to remove and 76 not upgraded.


# Install Python Virtualenv
sudo -H pip3 install --upgrade pip
sudo -H pip3 install virtualenv
Requirement already satisfied: pip in /usr/local/python/3.12.1/lib/python3.12/site-packages (25.3)
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
Collecting virtualenv
  Downloading virtualenv-20.36.1-py3-none-any.whl.metadata (4.7 kB)
Collecting distlib<1,>=0.3.7 (from virtualenv)
  Downloading distlib-0.4.0-py2.py3-none-any.whl.metadata (5.2 kB)
Collecting filelock<4,>=3.20.1 (from virtualenv)
  Downloading filelock-3.20.3-py3-none-any.whl.metadata (2.1 kB)
Collecting platformdirs<5,>=3.9.1 (from virtualenv)
  Downloading platformdirs-4.5.1-py3-none-any.whl.metadata (12 kB)
Downloading virtualenv-20.36.1-py3-none-any.whl (6.0 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.0/6.0 MB 55.6 MB/s  0:00:00
Downloading distlib-0.4.0-py2.py3-none-any.whl (469 kB)
Downloading filelock-3.20.3-py3-none-any.whl (16 kB)
Downloading platformdirs-4.5.1-py3-none-any.whl (18 kB)
Installing collected packages: distlib, platformdirs, filelock, virtualenv
Successfully installed distlib-0.4.0 filelock-3.20.3 platformdirs-4.5.1 virtualenv-20.36.1
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.





@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch (main) $ virtualenv jupyterenv
source jupyterenv/bin/activate

created virtual environment CPython3.12.1.final.0-64 in 853ms
  creator CPython3Posix(dest=/workspaces/data-engineering-zoomcamp-homework/05-batch/jupyterenv, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, via=copy, app_data_dir=/home/codespace/.local/share/virtualenv)
    added seed packages: pip==25.3
  activators BashActivator,CShellActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator





# actual
export PYTHONPATH="/workspaces/data-engineering-zoomcamp-homework/05-batch/spark/spark-3.3.2-bin-hadoop3/python:$PYTHONPATH"
export PYTHONPATH="/workspaces/data-engineering-zoomcamp-homework/05-batch/spark/spark-3.3.2-bin-hadoop3/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"




# install
(jupyterenv) @kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch (main) $ pip install jupyter
# Run Jupyter Notebook:
jupyter notebook
https://expert-waddle-v6w4g64w564wc7wv-8888.app.github.dev/tree?
```






## PySpark

This document assumes you already have python.

To run PySpark, we first need to add it to `PYTHONPATH`:

```bash
# instructions
export PYTHONPATH="${SPARK_HOME}/python/:$PYTHONPATH"
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"


# actual
export PYTHONPATH="/workspaces/data-engineering-zoomcamp-homework/05-batch/spark/spark-3.3.2-bin-hadoop3/python:$PYTHONPATH"
export PYTHONPATH="/workspaces/data-engineering-zoomcamp-homework/05-batch/spark/spark-3.3.2-bin-hadoop3/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"
```

Make sure that the version under `${SPARK_HOME}/python/lib/` matches the filename of py4j or you will
encounter `ModuleNotFoundError: No module named 'py4j'` while executing `import pyspark`.

For example, if the file under `${SPARK_HOME}/python/lib/` is `py4j-0.10.9.3-src.zip`, then the
`export PYTHONPATH` statement above should be changed to

```bash
export PYTHONPATH="${SPARK_HOME}/python/lib/py4j-0.10.9.3-src.zip:$PYTHONPATH"
```

On Windows, you may have to do path conversion from unix-style to windows-style:

```bash
SPARK_WIN=`cygpath -w ${SPARK_HOME}`

export PYTHONPATH="${SPARK_WIN}\\python\\"
export PYTHONPATH="${SPARK_WIN}\\python\\lib\\py4j-0.10.9-src.zip;$PYTHONPATH"
```

Now you can run Jupyter or IPython to test if things work. Go to some other directory, e.g. `~/tmp`.

Download a CSV file that we'll use for testing:

```bash
wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
```

Now let's run `ipython` (or `jupyter notebook`) and execute:

```python
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

df = spark.read \
    .option("header", "true") \
    .csv('taxi_zone_lookup.csv')

df.show()
```

Test that writing works as well:

```python
df.write.parquet('zones')
```

Note that the code workings above is used in `/workspaces/data-engineering-zoomcamp-homework/05-batch/code/03_test.ipynb`


### PySpark: Setting Spark up in Google Colab (Last Resort)
If you are struggling to set things up "locally" (meaning non-managed environments like your laptop, a VM, or Codespaces), you can follow this guide to use Spark in Google Colab:

Launch Spark on Google Colab and Connect to SparkUI - https://medium.com/gitconnected/launch-spark-on-google-colab-and-connect-to-sparkui-342cad19b304

Starter notebook:
GitHub Repository - Spark in Colab - https://github.com/aaalexlit/medium_articles/blob/main/Spark_in_Colab.ipynb

It’s advisable to spend some time setting up locally rather than using this solution immediately.



## Free up space in github codespace after setups and large file downloads
```bash
ls -la ~/.local/share/Trash/*
ls: cannot access '/home/codespace/.local/share/Trash/*': No such file or directory

ls -la ~/.local/share/ | grep Trash



df -h
Filesystem      Size  Used Avail Use% Mounted on
overlay          32G   29G  1.2G  96% /
tmpfs            64M     0   64M   0% /dev
shm              64M     0   64M   0% /dev/shm
/dev/root        29G   22G  7.6G  74% /vscode
/dev/sdc1        44G  2.9G   39G   7% /tmp
/dev/loop4       32G   29G  1.2G  96% /workspaces



du -sh * | sort -h
4.0K    LICENSE
16K     later
332K    [to revisit taxi_rides_ny - confusing lectures] 04-analytics-engineering
3.5M    02-workflow-orchestration
129M    yellow_tripdata_2020-12.csv
412M    03-data-warehouse
703M    01-docker-terraform
913M    05-batch


sudo apt-get clean
pip cache purge
docker system prune -f
docker volume prune -f

du -sh ~/.cache/* 2>/dev/null | sort -h
8.0K    /home/codespace/.cache/conda
12K     /home/codespace/.cache/Microsoft
4.6M    /home/codespace/.cache/pip
6.7M    /home/codespace/.cache/jedi
556M    /home/codespace/.cache/uv

du -sh ~/.npm/* 2>/dev/null | sort -h
16K     /home/codespace/.npm/_logs







df -h
Filesystem      Size  Used Avail Use% Mounted on
overlay          32G   29G  1.7G  95% /
tmpfs            64M     0   64M   0% /dev
shm              64M     0   64M   0% /dev/shm
/dev/root        29G   22G  7.6G  74% /vscode
/dev/sdc1        44G  3.9G   38G  10% /tmp
/dev/loop4       32G   29G  1.7G  95% /workspaces

du -sh * | sort -h
4.0K    LICENSE
16K     later
332K    [to revisit taxi_rides_ny - confusing lectures] 04-analytics-engineering
3.5M    02-workflow-orchestration
412M    03-data-warehouse
703M    01-docker-terraform
913M    05-batch




# then cd.. all the way up to /workspaces
@kaiquanmah0 ➜ /workspaces $

# Navigate to the trash directory
cd /workspaces/.Trash-1000

# Remove all files and folders in the trash (this is safe - these are already deleted files)
rm -rf files/* info/*

# Verify the trash is empty
ls files/ info/


rm -rf .Trash-1000

ls -la
total 20
drwxr-xrwx+ 5 codespace root      4096 Jan 25 09:26 .
drwxr-xr-x  1 root      root      4096 Jan 18 03:49 ..
drwxr-xr-x+ 4 codespace root      4096 Jan 18 03:49 .codespaces
drwxrwxrwx+ 2 codespace codespace 4096 Jan 18 03:50 .oryx
drwxrwxrwx+ 9 codespace root      4096 Jan 25 09:15 data-engineering-zoomcamp-homework



# last resort
#    go to the top of codespace
#    > rebuild codespace
#    full rebuild

df -h
Filesystem      Size  Used Avail Use% Mounted on
overlay          32G   12G   18G  40% /
tmpfs            64M     0   64M   0% /dev
shm              64M     0   64M   0% /dev/shm
/dev/root        29G   22G  7.6G  74% /vscode
/dev/sdc1        44G  4.2G   38G  10% /tmp
/dev/loop4       32G   12G   18G  40% /workspaces


du -sh * | sort -h
4.0K    LICENSE
16K     later
332K    [to revisit taxi_rides_ny - confusing lectures] 04-analytics-engineering
3.5M    02-workflow-orchestration
412M    03-data-warehouse
703M    01-docker-terraform
913M    05-batch
```


## Setup during every new codespace session
```bash
cd 05-batch/
source jupyterenv/bin/activate
export PYTHONPATH="/workspaces/data-engineering-zoomcamp-homework/05-batch/spark/spark-3.3.2-bin-hadoop3/python:$PYTHONPATH"
export PYTHONPATH="/workspaces/data-engineering-zoomcamp-homework/05-batch/spark/spark-3.3.2-bin-hadoop3/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH"

jupyter notebook
```


## URLs
* Port 8888 - Jupyter notebook UI - https://expert-waddle-v6w4g64w564wc7wv-8888.app.github.dev/tree/code
* Port 4040 - Spark cluster jobs monitoring UI - https://expert-waddle-v6w4g64w564wc7wv-4040.app.github.dev/jobs/

## Download dataset
* Which comes from https://github.com/DataTalksClub/nyc-tlc-data/releases
```bash
cd 05-batch/code/
chmod +x download_data.sh
./download_data.sh yellow 2020
```