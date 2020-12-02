FROM amancevice/superset:0.38.0

USER root

RUN apt-get update \
  && apt-get install -y nginx \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/ \
  && rm /etc/nginx/sites-enabled/default

COPY server.conf /etc/nginx/sites-enabled/superset.conf

RUN superset db upgrade \
    && superset fab create-user \
      --role Admin \
      --username admin \
      --firstname admin \
      --lastname admin \
      --email user@example.com \
      --password admin \
    && superset init

EXPOSE 80
ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

