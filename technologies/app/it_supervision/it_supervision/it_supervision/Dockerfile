FROM grafana/grafana:8.0.6-ubuntu

USER root

RUN mkdir /opt/grafana && mkdir /opt/plugins

# Install Ngins
RUN apt-get update \
  && apt-get install -y nginx \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/ \
  && rm /etc/nginx/sites-enabled/default

COPY server.conf /etc/nginx/sites-enabled/grafana.conf
COPY grafana.ini /etc/grafana/grafana.ini

# Install PostgreSQL
# check for default search text language (now english, swithc to french?)
RUN apt-get update \
  && apt-get install -y postgresql postgresql-contrib \
  && chown postgres:postgres /run/postgresql/ \
  && chmod 777 /run/postgresql \
  && mkdir /var/lib/postgresql/data \
  && chown postgres:postgres /var/lib/postgresql/data \
  && chmod 777 /var/lib/postgresql/data

ENV SUPERVISION_SAAGIE_PG_TABLE="SUPERVISION_SAAGIE_PG_TABLE" \
  SUPERVISION_SAAGIE_JOBS_PG_TABLE="SUPERVISION_SAAGIE_JOBS_PG_TABLE" \
  SUPERVISION_SAAGIE_JOBS_SNAPSHOT_PG_TABLE="SUPERVISION_SAAGIE_JOBS_SNAPSHOT_PG_TABLE" \
  SUPERVISION_DATALAKE_PG_TABLE="SUPERVISION_DATALAKE_PG_TABLE" \
  SUPERVISION_PG_DB="SUPERVISION_PG_DB" \
  SUPERVISION_PG_USER="supervision_pg_user" \
  SUPERVISION_PG_HOST="local_host"

COPY infra.sql infra.sql

RUN echo "export PATH=$PATH:/usr/lib/postgresql/12/bin" >> /etc/profile && . /etc/profile



USER postgres

RUN /usr/lib/postgresql/12/bin/initdb -D /var/lib/postgresql/data

USER root

ENV GF_PATHS_DATA /opt/grafana
ENV GF_PATHS_PLUGINS /opt/plugins

EXPOSE 80
ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT ["bash", "/entrypoint.sh"]