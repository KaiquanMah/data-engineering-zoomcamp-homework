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


## URLs
* Port 8888 - Jupyter notebook UI - https://expert-waddle-v6w4g64w564wc7wv-8888.app.github.dev/tree/code
* Port 4040 - Spark cluster jobs monitoring UI - https://expert-waddle-v6w4g64w564wc7wv-4040.app.github.dev/jobs/