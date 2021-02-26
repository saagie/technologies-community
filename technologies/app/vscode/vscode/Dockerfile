FROM ghcr.io/linuxserver/code-server:version-v3.9.0

USER root

RUN apt-get update \
  && apt-get install -y nginx \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/

COPY ressources/nginx.conf /etc/nginx/sites-enabled/nginx.conf
COPY ressources/entrypoint.sh /entrypoint.sh
COPY ressources/init_vscode.sh /init_vscode.sh

EXPOSE 8443

ENTRYPOINT ["/entrypoint.sh"]