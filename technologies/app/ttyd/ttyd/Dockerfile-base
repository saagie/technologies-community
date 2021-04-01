FROM tsl0922/ttyd:latest

RUN apt-get update \
    && apt-get install -y \
    wget \
    vim \
    default-jdk \
    libcurl3 \
    libevent-dev \
    libsvn1 \
    libsasl2-modules \
    libcurl4-nss-dev \
    bzip2 \
    software-properties-common \
    ftp

ENV JAVA_HOME "/usr/lib/jvm/java-8-openjdk-amd64"

# Hadoop
RUN mkdir app \
    && cd app \
    && wget https://archive.cloudera.com/cdh5/cdh/5/hadoop-2.6.0-cdh5.13.0.tar.gz \
    && tar xvf hadoop-2.6.0-cdh5.13.0.tar.gz \
    && rm hadoop-2.6.0-cdh5.13.0.tar.gz \
    && rm -rf hadoop-2.6.0-cdh5.13.0/etc/hadoop/ \
    && ln -s /etc/hadoop/conf hadoop-2.6.0-cdh5.13.0/etc/hadoop

ENV PATH "/app/hadoop-2.6.0-cdh5.13.0/bin:${PATH}"

# Hive
RUN cd app \
    && wget https://archive.cloudera.com/cdh5/cdh/5/hive-1.1.0-cdh5.13.0.tar.gz \
    && tar xvf hive-1.1.0-cdh5.13.0.tar.gz \
    && rm hive-1.1.0-cdh5.13.0.tar.gz \
    && rm -rf hive-1.1.0-cdh5.13.0/conf \
    && ln -s /etc/hive/conf hive-1.1.0-cdh5.13.0/conf

ENV PATH "/app/hive-1.1.0-cdh5.13.0/bin:${PATH}"

# Sqoop
RUN cd app \
    && wget https://archive.cloudera.com/cdh5/cdh/5/sqoop-1.4.6-cdh5.13.0.tar.gz \
    && tar xvf sqoop-1.4.6-cdh5.13.0.tar.gz \
    && rm -rf sqoop-1.4.6-cdh5.13.0.tar.gz \
    && cd sqoop-1.4.6-cdh5.13.0 \
    && mv conf/sqoop-env-template.sh conf/sqoop-env.sh \
    && echo 'export HADOOP_COMMON_HOME=/app/hadoop-2.6.0-cdh5.13.0' >> conf/sqoop-env.sh \
    && echo 'export HADOOP_MAPRED_HOME=/app/hadoop-2.6.0-cdh5.13.0' >> conf/sqoop-env.sh \
    && echo 'export HIVE_HOME=/app/hive-1.1.0-cdh5.13.0' >> conf/sqoop-env.sh \
    && echo 'export HBASE_HOME=/app/hive-1.1.0-cdh5.13.0/lib' >> conf/sqoop-env.sh \
    && echo 'export ACCUMULO_HOME=/app/hive-1.1.0-cdh5.13.0/hcatalog' >> conf/sqoop-env.sh

# Add connectors
COPY ./assets/ /app/sqoop-1.4.6-cdh5.13.0/lib

ENV PATH "/app/sqoop-1.4.6-cdh5.13.0/bin:${PATH}"

ENV HADOOP_USER_NAME "hdfs"

# Python (Vanilla)
RUN add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt install -y python3.7 \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && apt-get install -y python3-pip \
    && ln -s /usr/bin/pip3 /usr/bin/pip \
    && pip install pyspark==2.3.3

# Spark (local only)
RUN cd app \
    && wget http://apache.mirror.anlx.net/spark/spark-2.3.4/spark-2.3.4-bin-hadoop2.6.tgz \
    && tar -xvzf spark-2.3.4-bin-hadoop2.6.tgz \
    && cp spark-2.3.4-bin-hadoop2.6/conf/spark-env.sh.template spark-2.3.4-bin-hadoop2.6/conf/spark-env.sh \
    && echo 'export HADOOP_CONF_DIR=/etc/hadoop/conf/' >> spark-2.3.4-bin-hadoop2.6/conf/spark-env.sh \
    && rm spark-2.3.4-bin-hadoop2.6.tgz

ENV PATH "/app/spark-2.3.4-bin-hadoop2.6/bin:${PATH}"
ENV PYSPARK_PYTHON "python3"

# Auto refresh every hour
#CMD ["bash", "-r", "3600"]
CMD ["ttyd", "bash"]
