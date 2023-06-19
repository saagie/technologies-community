FROM tsl0922/ttyd:1.7.3

RUN apt-get update \
    && apt-get install -y \
    wget \
    vim \
    default-jdk \
    curl \
    libevent-dev \
    libsvn1 \
    libsasl2-modules \
    libcurl4-nss-dev \
    bzip2 \
    software-properties-common \
    ftp \
    mysql-client \
    jq

ENV JAVA_HOME "/usr/lib/jvm/java-11-openjdk-amd64"
WORKDIR /

# Hadoop
RUN mkdir app \
    && cd app \
    && wget -q https://archive.apache.org/dist/hadoop/common/hadoop-2.6.0/hadoop-2.6.0.tar.gz \
    && tar xvf hadoop-2.6.0.tar.gz \
    && rm hadoop-2.6.0.tar.gz \
    && rm -rf hadoop-2.6.0/etc/hadoop/conf \ 
    && ln -s /etc/hadoop/conf hadoop-2.6.0/etc/hadoop

ENV PATH "/app/hadoop-2.6.0/bin:${PATH}"

# Hive
RUN cd app \
    && wget -q https://archive.apache.org/dist/hive/hive-1.1.0/apache-hive-1.1.0-bin.tar.gz \
    && tar xvf apache-hive-1.1.0-bin.tar.gz \
    && rm apache-hive-1.1.0-bin.tar.gz \
    && rm -rf hive-1.1.0-bin/conf \
    && ln -s /etc/hive/conf apache-hive-1.1.0-bin/conf

ENV PATH "/app/apache-hive-1.1.0-bin/bin:${PATH}"

# Sqoop
RUN cd app \
    && wget -q https://archive.apache.org/dist/sqoop/1.4.6/sqoop-1.4.6.tar.gz \
    && tar xvf sqoop-1.4.6.tar.gz \
    && rm -rf sqoop-1.4.6.tar.gz \
    && cd sqoop-1.4.6 \
    && mv conf/sqoop-env-template.sh conf/sqoop-env.sh \
    && echo 'export HADOOP_COMMON_HOME=/app/hadoop-2.6.0' >> conf/sqoop-env.sh \
    && echo 'export HADOOP_MAPRED_HOME=/app/hadoop-2.6.0' >> conf/sqoop-env.sh \
    && echo 'export HIVE_HOME=/app/hive-1.1.0' >> conf/sqoop-env.sh \
    && echo 'export HBASE_HOME=/app/hive-1.1.0/lib' >> conf/sqoop-env.sh \
    && echo 'export ACCUMULO_HOME=/app/hive-1.1.0/hcatalog' >> conf/sqoop-env.sh

# Add connectors
COPY ./assets/ /app/sqoop-1.4.6/lib

ENV PATH "/app/sqoop-1.4.6/bin:${PATH}"

# Python
RUN add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get update \
    && apt install -y python3.11 \
    && ln -s /usr/bin/python3.11 /usr/bin/python \
    && rm /usr/bin/python3 \
    && ln -s /usr/bin/python3.11 /usr/bin/python3 \
    && apt install python3.11 python3.11-distutils \
    && curl -sS https://bootstrap.pypa.io/get-pip.py | python3.11


# Spark (local only)
RUN cd app \
    && wget -q https://dlcdn.apache.org/spark/spark-3.4.0/spark-3.4.0-bin-hadoop3.tgz \
    && tar -xvzf spark-3.4.0-bin-hadoop3.tgz \
    && cp spark-3.4.0-bin-hadoop3/conf/spark-env.sh.template spark-3.4.0-bin-hadoop3/conf/spark-env.sh \
    && echo 'export HADOOP_CONF_DIR=/etc/hadoop/conf/' >> spark-3.4.0-bin-hadoop3/conf/spark-env.sh \
    && rm spark-3.4.0-bin-hadoop3.tgz

ENV PATH "/app/spark-3.4.0-bin-hadoop3/bin:${PATH}"
ENV PYSPARK_PYTHON "python3"

# Auto refresh every hour
CMD ["ttyd", "bash"]
