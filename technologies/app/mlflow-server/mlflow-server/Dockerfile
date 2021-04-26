FROM python:3.7.0

RUN mkdir /mlflow/

RUN apt-get update && \
    apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get clean;

RUN cd / \
    && mkdir app \
    && cd app \
    && wget https://archive.apache.org/dist/hadoop/common/hadoop-2.6.0/hadoop-2.6.0.tar.gz \
    && tar xvf hadoop-2.6.0.tar.gz \
    && rm hadoop-2.6.0.tar.gz \
    && rm -rf hadoop-2.6.0/etc/hadoop \
    && ln -s /etc/hadoop/conf hadoop-2.6.0/etc/hadoop;

ENV PATH "/app/hadoop-2.6.0/bin:${PATH}"

RUN apt-get update && \
    apt-get install ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f;

ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64/
ENV HADOOP_HOME=/app/hadoop-2.6.0
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop-2.6.0

RUN pip install --upgrade pip
RUN pip install git+https://github.com/saagie/mlflow.git@v1.13.1

RUN pip install SQLAlchemy mysqlclient pyarrow

EXPOSE 5000

CMD mlflow server \
    --backend-store-uri 'mysql://'${MYSQL_USER_LOGIN}':'${MYSQL_USER_PASSWORD}'@'${MYSQL_HOST}'/'${MYSQL_DB}  \
    --default-artifact-root $HDFS_URI'tmp/'\
    --host 0.0.0.0
