
## Linux

Here we'll show you how to install Spark 3.3.2 for Linux.
We tested it on Ubuntu 20.04 (also WSL), but it should work
for other Linux distros as well


### Installing Java

Download OpenJDK 11 or Oracle JDK 11 (It's important that the version is 11 - spark requires 8 or 11)

We'll use [OpenJDK](https://jdk.java.net/archive/)

Download it (e.g. to `~/spark`):

```
wget https://download.java.net/java/GA/jdk11/9/GPL/openjdk-11.0.2_linux-x64_bin.tar.gz
```

Unpack it:

```bash
tar xzfv openjdk-11.0.2_linux-x64_bin.tar.gz
```

define `JAVA_HOME` and add it to `PATH`:

```bash
# original instructions
export JAVA_HOME="${HOME}/spark/jdk-11.0.2"
export PATH="${JAVA_HOME}/bin:${PATH}"



# actual instructions used following the video lectures
@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch/spark (main) $ pwd
/workspaces/data-engineering-zoomcamp-homework/05-batch/spark


export JAVA_HOME="${HOME}/05-batch/spark/jdk-11.0.2"
export PATH="${JAVA_HOME}/bin:${PATH}"


@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch/spark (main) $ echo ${PATH}
/home/codespace/05-batch/spark/jdk-11.0.2/bin:/usr/local/rvm/gems/ruby-3.4.7/bin:/usr/local/rvm/gems/ruby-3.4.7@global/bin:/usr/local/rvm/rubies/ruby-3.4.7/bin:/home/codespace/.vscode-remote/data/User/globalStorage/github.copilot-chat/debugCommand:/home/codespace/.vscode-remote/data/User/globalStorage/github.copilot-chat/copilotCli:/vscode/bin/linux-x64/c9d77990917f3102ada88be140d28b038d1dd7c7/bin/remote-cli:/home/codespace/.local/bin:/home/codespace/.dotnet:/home/codespace/nvm/current/bin:/home/codespace/.php/current/bin:/home/codespace/.python/current/bin:/home/codespace/java/current/bin:/home/codespace/.ruby/current/bin:/home/codespace/.local/bin:/usr/local/python/current/bin:/usr/local/py-utils/bin:/usr/local/jupyter:/usr/local/oryx:/usr/local/go/bin:/go/bin:/usr/local/sdkman/bin:/usr/local/sdkman/candidates/java/current/bin:/usr/local/sdkman/candidates/gradle/current/bin:/usr/local/sdkman/candidates/maven/current/bin:/usr/local/sdkman/candidates/ant/current/bin:/usr/local/rvm/gems/default/bin:/usr/local/rvm/gems/default@global/bin:/usr/local/rvm/rubies/default/bin:/usr/local/share/rbenv/bin:/usr/local/php/current/bin:/opt/conda/bin:/usr/local/nvs:/usr/local/share/nvm/versions/node/v24.11.1/bin:/usr/local/hugo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/share/dotnet:/home/codespace/.dotnet/tools:/usr/local/rvm/bin


@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch/spark (main) $ which java
/home/codespace/java/current/bin/java


@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch/spark (main) $ java --version
openjdk 25.0.1 2025-10-21 LTS
OpenJDK Runtime Environment Microsoft-12574222 (build 25.0.1+8-LTS)
OpenJDK 64-Bit Server VM Microsoft-12574222 (build 25.0.1+8-LTS, mixed mode, sharing)




# round 3
#  we also need to fix the path for JAVA
#  for Spark to pick up later in round 3 later
export JAVA_HOME="/workspaces/data-engineering-zoomcamp-homework/05-batch/spark/jdk-11.0.2"
export PATH="/usr/local/rvm/gems/ruby-3.4.7/bin:/usr/local/rvm/gems/ruby-3.4.7@global/bin:/usr/local/rvm/rubies/ruby-3.4.7/bin:/home/codespace/.vscode-remote/data/User/globalStorage/github.copilot-chat/debugCommand:/home/codespace/.vscode-remote/data/User/globalStorage/github.copilot-chat/copilotCli:/vscode/bin/linux-x64/c9d77990917f3102ada88be140d28b038d1dd7c7/bin/remote-cli:/home/codespace/.local/bin:/home/codespace/.dotnet:/home/codespace/nvm/current/bin:/home/codespace/.php/current/bin:/home/codespace/.python/current/bin:/home/codespace/java/current/bin:/home/codespace/.ruby/current/bin:/home/codespace/.local/bin:/usr/local/python/current/bin:/usr/local/py-utils/bin:/usr/local/jupyter:/usr/local/oryx:/usr/local/go/bin:/go/bin:/usr/local/sdkman/bin:/usr/local/sdkman/candidates/java/current/bin:/usr/local/sdkman/candidates/gradle/current/bin:/usr/local/sdkman/candidates/maven/current/bin:/usr/local/sdkman/candidates/ant/current/bin:/usr/local/rvm/gems/default/bin:/usr/local/rvm/gems/default@global/bin:/usr/local/rvm/rubies/default/bin:/usr/local/share/rbenv/bin:/usr/local/php/current/bin:/opt/conda/bin:/usr/local/nvs:/usr/local/share/nvm/versions/node/v24.11.1/bin:/usr/local/hugo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/share/dotnet:/home/codespace/.dotnet/tools:/usr/local/rvm/bin"
export PATH="${JAVA_HOME}/bin:${PATH}"

@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch/spark (main) $ java --version
openjdk 11.0.2 2019-01-15
OpenJDK Runtime Environment 18.9 (build 11.0.2+9)
OpenJDK 64-Bit Server VM 18.9 (build 11.0.2+9, mixed mode)
```

check that it works:

```bash
java --version
```

Output:

```
openjdk 11.0.2 2019-01-15
OpenJDK Runtime Environment 18.9 (build 11.0.2+9)
OpenJDK 64-Bit Server VM 18.9 (build 11.0.2+9, mixed mode)
```

Remove the archive:

```bash
rm openjdk-11.0.2_linux-x64_bin.tar.gz
```





### Installing Spark


Download Spark. Use 3.3.2 version:

```bash
wget https://archive.apache.org/dist/spark/spark-3.3.2/spark-3.3.2-bin-hadoop3.tgz
```

Unpack:

```bash
tar xzfv spark-3.3.2-bin-hadoop3.tgz
```

Remove the archive:

```bash
rm spark-3.3.2-bin-hadoop3.tgz
```

Add it to `PATH`:

```bash
# original instructions
export SPARK_HOME="${HOME}/spark/spark-3.3.2-bin-hadoop3"
export PATH="${SPARK_HOME}/bin:${PATH}"


# actual instructions used following the video lectures
@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch/spark (main) $ pwd
/workspaces/data-engineering-zoomcamp-homework/05-batch/spark

# round 1 - with issues for Spark
# not sure why OpenJDK was fine earlier
export SPARK_HOME="${HOME}/05-batch/spark/spark-3.3.2-bin-hadoop3"
export PATH="${SPARK_HOME}/bin:${PATH}"




@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch/spark (main) $ echo ${PATH}
/home/codespace/05-batch/spark/spark-3.3.2-bin-hadoop3/bin:/home/codespace/05-batch/spark/jdk-11.0.2/bin:/usr/local/rvm/gems/ruby-3.4.7/bin:/usr/local/rvm/gems/ruby-3.4.7@global/bin:/usr/local/rvm/rubies/ruby-3.4.7/bin:/home/codespace/.vscode-remote/data/User/globalStorage/github.copilot-chat/debugCommand:/home/codespace/.vscode-remote/data/User/globalStorage/github.copilot-chat/copilotCli:/vscode/bin/linux-x64/c9d77990917f3102ada88be140d28b038d1dd7c7/bin/remote-cli:/home/codespace/.local/bin:/home/codespace/.dotnet:/home/codespace/nvm/current/bin:/home/codespace/.php/current/bin:/home/codespace/.python/current/bin:/home/codespace/java/current/bin:/home/codespace/.ruby/current/bin:/home/codespace/.local/bin:/usr/local/python/current/bin:/usr/local/py-utils/bin:/usr/local/jupyter:/usr/local/oryx:/usr/local/go/bin:/go/bin:/usr/local/sdkman/bin:/usr/local/sdkman/candidates/java/current/bin:/usr/local/sdkman/candidates/gradle/current/bin:/usr/local/sdkman/candidates/maven/current/bin:/usr/local/sdkman/candidates/ant/current/bin:/usr/local/rvm/gems/default/bin:/usr/local/rvm/gems/default@global/bin:/usr/local/rvm/rubies/default/bin:/usr/local/share/rbenv/bin:/usr/local/php/current/bin:/opt/conda/bin:/usr/local/nvs:/usr/local/share/nvm/versions/node/v24.11.1/bin:/usr/local/hugo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/share/dotnet:/home/codespace/.dotnet/tools:/usr/local/rvm/bin

@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch/spark (main) $ spark-shell
bash: spark-shell: command not found

@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch/spark (main) $ ls -l "${SPARK_HOME}/bin/spark-shell"
ls: cannot access '/home/codespace/05-batch/spark/spark-3.3.2-bin-hadoop3/bin/spark-shell': No such file or directory









# round 2
export SPARK_HOME="/workspaces/data-engineering-zoomcamp-homework/05-batch/spark/spark-3.3.2-bin-hadoop3"
export PATH="/home/codespace/05-batch/spark/jdk-11.0.2/bin:/usr/local/rvm/gems/ruby-3.4.7/bin:/usr/local/rvm/gems/ruby-3.4.7@global/bin:/usr/local/rvm/rubies/ruby-3.4.7/bin:/home/codespace/.vscode-remote/data/User/globalStorage/github.copilot-chat/debugCommand:/home/codespace/.vscode-remote/data/User/globalStorage/github.copilot-chat/copilotCli:/vscode/bin/linux-x64/c9d77990917f3102ada88be140d28b038d1dd7c7/bin/remote-cli:/home/codespace/.local/bin:/home/codespace/.dotnet:/home/codespace/nvm/current/bin:/home/codespace/.php/current/bin:/home/codespace/.python/current/bin:/home/codespace/java/current/bin:/home/codespace/.ruby/current/bin:/home/codespace/.local/bin:/usr/local/python/current/bin:/usr/local/py-utils/bin:/usr/local/jupyter:/usr/local/oryx:/usr/local/go/bin:/go/bin:/usr/local/sdkman/bin:/usr/local/sdkman/candidates/java/current/bin:/usr/local/sdkman/candidates/gradle/current/bin:/usr/local/sdkman/candidates/maven/current/bin:/usr/local/sdkman/candidates/ant/current/bin:/usr/local/rvm/gems/default/bin:/usr/local/rvm/gems/default@global/bin:/usr/local/rvm/rubies/default/bin:/usr/local/share/rbenv/bin:/usr/local/php/current/bin:/opt/conda/bin:/usr/local/nvs:/usr/local/share/nvm/versions/node/v24.11.1/bin:/usr/local/hugo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/share/dotnet:/home/codespace/.dotnet/tools:/usr/local/rvm/bin"
export PATH="${SPARK_HOME}/bin:${PATH}"

@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch/spark (main) $ echo ${PATH}
/workspaces/data-engineering-zoomcamp-homework/05-batch/spark/spark-3.3.2-bin-hadoop3/bin:/home/codespace/05-batch/spark/jdk-11.0.2/bin:/usr/local/rvm/gems/ruby-3.4.7/bin:/usr/local/rvm/gems/ruby-3.4.7@global/bin:/usr/local/rvm/rubies/ruby-3.4.7/bin:/home/codespace/.vscode-remote/data/User/globalStorage/github.copilot-chat/debugCommand:/home/codespace/.vscode-remote/data/User/globalStorage/github.copilot-chat/copilotCli:/vscode/bin/linux-x64/c9d77990917f3102ada88be140d28b038d1dd7c7/bin/remote-cli:/home/codespace/.local/bin:/home/codespace/.dotnet:/home/codespace/nvm/current/bin:/home/codespace/.php/current/bin:/home/codespace/.python/current/bin:/home/codespace/java/current/bin:/home/codespace/.ruby/current/bin:/home/codespace/.local/bin:/usr/local/python/current/bin:/usr/local/py-utils/bin:/usr/local/jupyter:/usr/local/oryx:/usr/local/go/bin:/go/bin:/usr/local/sdkman/bin:/usr/local/sdkman/candidates/java/current/bin:/usr/local/sdkman/candidates/gradle/current/bin:/usr/local/sdkman/candidates/maven/current/bin:/usr/local/sdkman/candidates/ant/current/bin:/usr/local/rvm/gems/default/bin:/usr/local/rvm/gems/default@global/bin:/usr/local/rvm/rubies/default/bin:/usr/local/share/rbenv/bin:/usr/local/php/current/bin:/opt/conda/bin:/usr/local/nvs:/usr/local/share/nvm/versions/node/v24.11.1/bin:/usr/local/hugo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/share/dotnet:/home/codespace/.dotnet/tools:/usr/local/rvm/bin


@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch/spark (main) $ ls -l "${SPARK_HOME}/bin/spark-shell"
-rwxr-xr-x 1 codespace codespace 3122 Feb 10  2023 /workspaces/data-engineering-zoomcamp-homework/05-batch/spark/spark-3.3.2-bin-hadoop3/bin/spark-shell


@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch/spark (main) $ spark-shell
/workspaces/data-engineering-zoomcamp-homework/05-batch/spark/spark-3.3.2-bin-hadoop3/bin/spark-class: line 71: /home/codespace/05-batch/spark/jdk-11.0.2/bin/java: No such file or directory
/workspaces/data-engineering-zoomcamp-homework/05-batch/spark/spark-3.3.2-bin-hadoop3/bin/spark-class: line 96: CMD: bad array subscript


@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch/spark (main) $ chmod +x "${SPARK_HOME}/bin/spark-shell"


@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch/spark (main) $ ls -l "${SPARK_HOME}/bin/spark-shell"
-rwxr-xr-x 1 codespace codespace 3122 Feb 10  2023 /workspaces/data-engineering-zoomcamp-homework/05-batch/spark/spark-3.3.2-bin-hadoop3/bin/spark-shell


@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch/spark (main) $ spark-shell
/workspaces/data-engineering-zoomcamp-homework/05-batch/spark/spark-3.3.2-bin-hadoop3/bin/spark-class: line 71: /home/codespace/05-batch/spark/jdk-11.0.2/bin/java: No such file or directory
/workspaces/data-engineering-zoomcamp-homework/05-batch/spark/spark-3.3.2-bin-hadoop3/bin/spark-class: line 96: CMD: bad array subscript








# round 3
# (continue from Java round 3)
export SPARK_HOME="/workspaces/data-engineering-zoomcamp-homework/05-batch/spark/spark-3.3.2-bin-hadoop3"
export PATH="${SPARK_HOME}/bin:${PATH}"

@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch/spark (main) $ echo ${PATH}
/workspaces/data-engineering-zoomcamp-homework/05-batch/spark/spark-3.3.2-bin-hadoop3/bin:/workspaces/data-engineering-zoomcamp-homework/05-batch/spark/jdk-11.0.2/bin:/usr/local/rvm/gems/ruby-3.4.7/bin:/usr/local/rvm/gems/ruby-3.4.7@global/bin:/usr/local/rvm/rubies/ruby-3.4.7/bin:/home/codespace/.vscode-remote/data/User/globalStorage/github.copilot-chat/debugCommand:/home/codespace/.vscode-remote/data/User/globalStorage/github.copilot-chat/copilotCli:/vscode/bin/linux-x64/c9d77990917f3102ada88be140d28b038d1dd7c7/bin/remote-cli:/home/codespace/.local/bin:/home/codespace/.dotnet:/home/codespace/nvm/current/bin:/home/codespace/.php/current/bin:/home/codespace/.python/current/bin:/home/codespace/java/current/bin:/home/codespace/.ruby/current/bin:/home/codespace/.local/bin:/usr/local/python/current/bin:/usr/local/py-utils/bin:/usr/local/jupyter:/usr/local/oryx:/usr/local/go/bin:/go/bin:/usr/local/sdkman/bin:/usr/local/sdkman/candidates/java/current/bin:/usr/local/sdkman/candidates/gradle/current/bin:/usr/local/sdkman/candidates/maven/current/bin:/usr/local/sdkman/candidates/ant/current/bin:/usr/local/rvm/gems/default/bin:/usr/local/rvm/gems/default@global/bin:/usr/local/rvm/rubies/default/bin:/usr/local/share/rbenv/bin:/usr/local/php/current/bin:/opt/conda/bin:/usr/local/nvs:/usr/local/share/nvm/versions/node/v24.11.1/bin:/usr/local/hugo/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/share/dotnet:/home/codespace/.dotnet/tools:/usr/local/rvm/bin


@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch/spark (main) $ ls -l "${SPARK_HOME}/bin/spark-shell"
-rwxr-xr-x 1 codespace codespace 3122 Feb 10  2023 /workspaces/data-engineering-zoomcamp-homework/05-batch/spark/spark-3.3.2-bin-hadoop3/bin/spark-shell



```

### Testing Spark

Execute `spark-shell` and run the following:

```scala
val data = 1 to 10000
val distData = sc.parallelize(data)
distData.filter(_ < 10).collect()
```


```bash
@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch/spark (main) $ spark-shell
26/01/24 09:28:09 WARN Utils: Your hostname, codespaces-870bd8 resolves to a loopback address: 127.0.0.1; using 10.0.14.153 instead (on interface eth0)
26/01/24 09:28:09 WARN Utils: Set SPARK_LOCAL_IP if you need to bind to another address
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
26/01/24 09:28:16 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Spark context Web UI available at http://f9883e21-d377-4ad7-8178-aa68a242d7f0.internal.cloudapp.net:4040
Spark context available as 'sc' (master = local[*], app id = local-1769246898396).
Spark session available as 'spark'.
Welcome to
      ____              __
     / __/__  ___ _____/ /__
    _\ \/ _ \/ _ `/ __/  '_/
   /___/ .__/\_,_/_/ /_/\_\   version 3.3.2
      /_/
         
Using Scala version 2.12.15 (OpenJDK 64-Bit Server VM, Java 11.0.2)
Type in expressions to have them evaluated.
Type :help for more information.




scala> val data = 1 to 10000
data: scala.collection.immutable.Range.Inclusive = Range 1 to 10000


scala> data
res0: scala.collection.immutable.Range.Inclusive = Range 1 to 10000


# turn range of numbers into RDD
scala> val distData = sc.parallelize(data)
distData: org.apache.spark.rdd.RDD[Int] = ParallelCollectionRDD[0] at parallelize at <console>:24


scala> distData.filter(_ < 10).collect()
res1: Array[Int] = Array(1, 2, 3, 4, 5, 6, 7, 8, 9)


scala> :quit
```


### Add PATH variables to .bashrc

```bash
nano ~/.bashrc

# Add these lines to ~/.bashrc
export JAVA_HOME="/workspaces/data-engineering-zoomcamp-homework/05-batch/spark/jdk-11.0.2"
export SPARK_HOME="/workspaces/data-engineering-zoomcamp-homework/05-batch/spark/spark-3.3.2-bin-hadoop3"
export PATH="${JAVA_HOME}/bin:${SPARK_HOME}/bin:${PATH}"


# save and exit from the ~/.bashrc file
# refresh ~/.bashrc
source ~/.bashrc



@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch/spark (main) $ which java
/workspaces/data-engineering-zoomcamp-homework/05-batch/spark/jdk-11.0.2/bin/java


@kaiquanmah0 ➜ /workspaces/data-engineering-zoomcamp-homework/05-batch/spark (main) $ which pyspark
/workspaces/data-engineering-zoomcamp-homework/05-batch/spark/spark-3.3.2-bin-hadoop3/bin/pyspark
```

### PySpark

It's the same for all platforms. Go to [pyspark.md](pyspark.md). 
