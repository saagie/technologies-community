FROM metabase/metabase:v0.38.1

USER root

RUN apk update \
    && apk add nginx \
    && rm /etc/nginx/conf.d/default.conf \
    && mkdir -p /run/nginx

COPY server.conf /etc/nginx/conf.d/metabase.conf

ENV MB_DB_TYPE h2
ENV MB_DB_FILE /metabase-data

EXPOSE 80
ADD entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]