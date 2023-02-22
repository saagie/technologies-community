FROM nginx:latest

RUN apt-get update && apt-get install -y nginx

ADD ressources/nginx.conf /etc/nginx/conf.d/default.conf
ADD ressources/auth.htpasswd /etc/nginx/auth.htpasswd
ADD ressources/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]