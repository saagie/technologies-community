FROM ghcr.io/linuxserver/code-server:version-v3.9.0

COPY resources/nginx.conf /etc/nginx/sites-enabled/nginx.conf
COPY resources/entrypoint.sh /entrypoint.sh

EXPOSE 8443

ENTRYPOINT ["/entrypoint.sh"]