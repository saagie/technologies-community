FROM amancevice/superset:0.38.0

USER root

RUN apt-get update \
  && apt-get install -y nginx \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/ \
  && rm /etc/nginx/sites-enabled/default

ADD superset_config.py /etc/superset/superset_config.py
ADD server.conf /etc/nginx/sites-enabled/superset.conf
ADD entrypoint.sh /entrypoint.sh
ADD init_superset.sh /init_superset.sh

EXPOSE 80
ENTRYPOINT ["/entrypoint.sh"]

