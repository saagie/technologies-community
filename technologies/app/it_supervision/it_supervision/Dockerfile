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
RUN apk add postgresql --no-cache \
    mkdir /run/postgresql \ 
    chown postgres:postgres /run/postgresql/ \
    mkdir /var/lib/postgresql/data \
    chmod 0700 /var/lib/postgresql/data \
    initdb -D /var/lib/postgresql/data \
    echo "host all all 0.0.0.0/0 md5" >> /var/lib/postgresql/data/pg_hba.conf \
    echo "listen_addresses='*'" >> /var/lib/postgresql/data/postgresql.conf

ENV GF_PATHS_DATA /opt/grafana
ENV GF_PATHS_PLUGINS /opt/plugins

EXPOSE 80
ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

