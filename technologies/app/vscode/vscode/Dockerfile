FROM ghcr.io/linuxserver/code-server:version-v3.9.0

COPY ressources/nginx.conf /etc/nginx/sites-enabled/nginx.conf
COPY ressources/entrypoint.sh /entrypoint.sh

EXPOSE 8443

ENTRYPOINT ["/entrypoint.sh"]