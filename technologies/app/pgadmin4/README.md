# PGadmin4

![Docker Image Size (tag)](https://img.shields.io/docker/image-size/saagie/vscode-server/3.9.3?label=v3.9.3%20image%20size&style=for-the-badge)

## Description
pgAdmin 4 is a complete rewrite of pgAdmin, built using Python and Javascript/jQuery. A desktop runtime written in NWjs allows it to run standalone for individual users, or the web application code may be deployed directly on a web server for use by one or more users through their web browser. The software has the look and feels of a desktop application whatever the runtime environment is, and vastly improves on pgAdmin III with updated user interface elements, multi-user/web deployment options, dashboards, and a more modern design.


## How to run image in local

```
docker run -p81:80 -e PGADMIN_DEFAULT_EMAIL=user@my_mail.com \
                    -e PGADMIN_DEFAULT_PASSWORD=password \
                    -e SAAGIE_BASE_PATH="/baseurl" \
                    saagie/pgadmin4
```


PGADMIN_DEFAULT_EMAIL : Default user for PGadmin
PGADMIN_DEFAULT_PASSWORD : Default password for PGadmin
SAAGIE_BASE_PATH : Base URL

For Saagie deploiement, uncheck checkbox "Use rewrite url".

