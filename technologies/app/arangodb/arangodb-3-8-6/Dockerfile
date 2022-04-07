FROM arangodb:3.8.6

# INSTALLATION DES PREREQUIS
RUN apk update && \
    apk add nginx openssl

COPY ressources/nginx.conf /etc/nginx/sites-enabled/nginx.conf
COPY ressources/saagie_entrypoint.sh /saagie_entrypoint.sh

EXPOSE 8529
# /
ENTRYPOINT ["/entrypoint.sh"]
CMD ["arangod"]