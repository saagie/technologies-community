FROM grafana/grafana:8.2.4-ubuntu

USER root

RUN mkdir /opt/grafana && mkdir /opt/plugins && mkdir /app

RUN apt-get update

# Install Dependencies
RUN apt-get update \
  && apt-get install -y software-properties-common nginx cron wget libpq-dev python-dev openjdk-11-jdk ca-certificates-java postgresql postgresql-contrib \
  && add-apt-repository ppa:deadsnakes/ppa \
  && apt-get update \
  && apt-get install -y python3.9 pip \
  && rm /etc/nginx/sites-enabled/default

ADD code/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Fix certificate issues
RUN update-ca-certificates -f;

# Hadoop command-line
RUN cd / \
    && mkdir hadoop \
    && cd hadoop \
    && wget https://archive.apache.org/dist/hadoop/common/hadoop-2.6.5/hadoop-2.6.5.tar.gz \
    && tar xvf hadoop-2.6.5.tar.gz \
    && rm hadoop-2.6.5.tar.gz \
    && rm -rf hadoop-2.6.5/etc/hadoop \
    && ln -s /etc/hadoop/conf hadoop-2.6.5/etc/hadoop;

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/
ENV HADOOP_HOME=/hadoop/hadoop-2.6.5
ENV HADOOP_CONF_DIR=/hadoop/hadoop-2.6.5/etc/hadoop
ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/hadoop/hadoop-2.6.5/lib/native:/usr/lib/jvm/java-11-openjdk-amd64/lib"
ENV CLASSPATH="/etc/hadoop/conf:/hadoop/hadoop-2.6.5/share/hadoop/common/lib/*:/hadoop/hadoop-2.6.5/share/hadoop/common/*:/hadoop/hadoop-2.6.5/share/hadoop/hdfs:/hadoop/hadoop-2.6.5/share/hadoop/hdfs/lib/*:/hadoop/hadoop-2.6.5/share/hadoop/hdfs/*:/hadoop/hadoop-2.6.5/share/hadoop/yarn/lib/*:/hadoop/hadoop-2.6.5/share/hadoop/yarn/*:/hadoop/hadoop-2.6.5/share/hadoop/mapreduce/lib/*:/hadoop/hadoop-2.6.5/share/hadoop/mapreduce/*"
ENV PATH "/hadoop/hadoop-2.6.5/bin:${PATH}"

# Configure PostgreSQL
# check for default search text language (now english, swithc to french?)
RUN chown postgres:postgres /run/postgresql/ \
  && chmod 777 /run/postgresql \
  && mkdir /var/lib/postgresql/data \
  && chown postgres:postgres /var/lib/postgresql/data \
  && chmod 777 /var/lib/postgresql/data

USER postgres
RUN /usr/lib/postgresql/12/bin/initdb -D /var/lib/postgresql/data

USER root
RUN echo "export PATH=$PATH:/usr/lib/postgresql/12/bin" >> /etc/profile && . /etc/profile
ENV CRON_DAYS=1

ADD infra.sql infra.sql
ADD server.conf /etc/nginx/sites-enabled/grafana.conf
ADD grafana.ini /etc/grafana/grafana.ini

ADD grafana/provisioning /etc/grafana/provisioning
ADD grafana/dashboards /var/lib/grafana/dashboards

ENV GF_PATHS_DATA /opt/grafana
ENV GF_PATHS_PLUGINS /opt/plugins

ADD code /app

EXPOSE 80
ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT ["bash", "/entrypoint.sh"]