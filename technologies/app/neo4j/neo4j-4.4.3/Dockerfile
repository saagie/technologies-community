FROM neo4j:4.4.3-community

# INSTALLATION DES PREREQUIS
RUN apt-get update && apt-get install -y  \
    nginx \
    openssl \
    git \
    && rm /etc/nginx/sites-enabled/default

COPY ressources/nginx.conf /etc/nginx/sites-enabled/nginx.conf
COPY ressources/saagie_entrypoint.sh /saagie_entrypoint.sh

# set EXTENSION_SCRIPT env var to tell Neo4j to run this script at init
ENV EXTENSION_SCRIPT=/saagie_entrypoint.sh

# Bolt connector port 7687
# HTTP Connector port 7474
# HTTPS Connector port 7473
# Redirected port 80
EXPOSE 7687 80

VOLUME ["/data", "/logs", "/var/lib/neo4j/import", "/plugins"]