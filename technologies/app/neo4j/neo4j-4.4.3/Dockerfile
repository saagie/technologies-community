FROM neo4j:4.4.3-community

# INSTALLATION DES PREREQUIS
RUN apt-get update && apt-get install -y  \
    nginx \
    openssl \
    git \
    && rm /etc/nginx/sites-enabled/default



COPY ressources/nginx.conf /etc/nginx/sites-enabled/nginx.conf
COPY ressources/entrypoint.sh /entrypoint.sh

EXPOSE 80
ENTRYPOINT ["/entrypoint.sh"]