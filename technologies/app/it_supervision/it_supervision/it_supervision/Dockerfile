FROM grafana/grafana:8.0.6-ubuntu

USER root

RUN mkdir /opt/grafana && mkdir /opt/plugins && mkdir /app

RUN apt-get update

# Install Ngins
RUN apt-get update \
  && apt-get install -y software-properties-common nginx cron wget libpq-dev python-dev \
  && add-apt-repository ppa:deadsnakes/ppa \
  && apt-get update \
  && apt-get install -y python3.7 pip \
  && rm /etc/nginx/sites-enabled/default

COPY server.conf /etc/nginx/sites-enabled/grafana.conf
COPY grafana.ini /etc/grafana/grafana.ini

# Hadoop command-line
RUN mkdir hadoop \
    && cd hadoop \
    && wget https://archive.apache.org/dist/hadoop/core/hadoop-2.6.0/hadoop-2.6.0.tar.gz \
    && tar xvf hadoop-2.6.0.tar.gz \
    && rm hadoop-2.6.0.tar.gz \
    && rm -rf hadoop-2.6.0/etc/hadoop/ \
    && ln -s /etc/hadoop/conf hadoop-2.6.0/etc/hadoop

ENV PATH "/hadoop/hadoop-2.6.0/bin:${PATH}"

# Install PostgreSQL
# check for default search text language (now english, swithc to french?)
RUN apt-get update \
  && apt-get install -y postgresql postgresql-contrib \
  && chown postgres:postgres /run/postgresql/ \
  && chmod 777 /run/postgresql \
  && mkdir /var/lib/postgresql/data \
  && chown postgres:postgres /var/lib/postgresql/data \
  && chmod 777 /var/lib/postgresql/data
  #&& apt-get clean \
  #&& rm -rf /var/lib/apt/lists/ 

ENV CRON_DAYS=1

USER postgres
RUN /usr/lib/postgresql/12/bin/initdb -D /var/lib/postgresql/data

USER root
COPY infra.sql infra.sql

ADD grafana/provisioning /etc/grafana/provisioning
ADD grafana/dashboards /var/lib/grafana/dashboards

ENV GF_PATHS_DATA /opt/grafana
ENV GF_PATHS_PLUGINS /opt/plugins

RUN echo "export PATH=$PATH:/usr/lib/postgresql/12/bin" >> /etc/profile && . /etc/profile
ADD code /app
RUN pip install -r /app/requirements.txt

EXPOSE 80
ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT ["bash", "/entrypoint.sh"]