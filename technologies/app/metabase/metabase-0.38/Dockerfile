FROM metabase/metabase:v0.38.1

USER root

#Installing Nginx
RUN apk update \
    && apk add nginx \
    && rm /etc/nginx/conf.d/default.conf \
    && mkdir -p /run/nginx

COPY server.conf /etc/nginx/conf.d/metabase.conf

#Installing Impala Driver
RUN mkdir /app/plugins && chmod 777 /app/plugins
COPY assets/impala.metabase-driver.jar /app/plugins/impala.metabase-driver.jar
COPY assets/ImpalaJDBC41.jar /app/plugins/ImpalaJDBC41.jar

ENV MB_DB_TYPE h2
ENV MB_DB_FILE /metabase-data
ENV MB_PLUGINS_DIR /app/plugins

EXPOSE 80
ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]