FROM saagie/spark:2.4-jre-8-1.44.0

USER root

RUN apt-get update \
  && apt-get install -y nginx \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/

COPY server.conf /etc/nginx/sites-enabled/spark-history.conf
RUN rm /etc/nginx/sites-enabled/default

ENV SPARK_NO_DAEMONIZE TRUE
EXPOSE 80

ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
