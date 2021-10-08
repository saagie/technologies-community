#!/bin/bash

su postgres -c 'source /etc/profile && pg_ctl start -D /var/lib/postgresql/data'
su postgres -c 'psql --command "CREATE USER supervision_pg_user"'
su postgres -c 'psql --command "CREATE DATABASE supervision_pg_db"'
su postgres -c 'psql --command "GRANT ALL PRIVILEGES ON DATABASE supervision_pg_db to supervision_pg_user"'
su postgres -c 'psql -U supervision_pg_user --command $(cat infra.sql)'


if [[ -z "${GRAFANA_ADMIN_PASSWORD}" ]]; then
  echo "ERROR : Grafana admin password must be set through GRAFANA_ADMIN_PASSWORD environment variable. Exiting."
  exit 1
else
  sed -i 's:GRAFANA_ADMIN_PASSWORD:'"$GRAFANA_ADMIN_PASSWORD"':g' /etc/grafana/grafana.ini
fi

sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/grafana/grafana.ini
sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/nginx/sites-enabled/grafana.conf

nginx && /run.sh