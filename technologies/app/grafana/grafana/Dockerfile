FROM grafana/grafana:7.1.5-ubuntu

USER root

RUN mkdir /opt/grafana && mkdir /opt/plugins
# Nginx
RUN apt-get update \
  && apt-get install -y nginx \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/

COPY server.conf /etc/nginx/sites-enabled/grafana.conf
COPY grafana.ini /etc/grafana/grafana.ini
RUN rm /etc/nginx/sites-enabled/default

ENV GF_PATHS_DATA /opt/grafana
ENV GF_PATHS_PLUGINS /opt/plugins

EXPOSE 80
ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
