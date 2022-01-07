FROM rocker/shiny:4.1.2

# Install R packages required by your Shiny app
# RUN R -e 'install.packages(c("DT", "magrittr"), repos="http://cloud.r-project.org")'

# INSTALLATION DES PRERREQUIS
RUN apt-get update && apt-get install -y  \
    nginx \
    openssl \
    git \
    && rm /etc/nginx/sites-enabled/default

COPY ressources/nginx.conf /etc/nginx/sites-enabled/nginx.conf
COPY ressources/entrypoint.sh /entrypoint.sh

EXPOSE 80
ENTRYPOINT ["/entrypoint.sh"]