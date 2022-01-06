FROM rocker/shiny:4.1.2

# INSTALLATION DES PRERREQUIS
RUN apt-get update && apt-get install -y  \
    nginx \
    openssl

COPY ressources/nginx.conf /etc/nginx/sites-enabled/nginx.conf
COPY ressources/entrypoint.sh /entrypoint.sh

EXPOSE 80
ENTRYPOINT ["/entrypoint.sh"]