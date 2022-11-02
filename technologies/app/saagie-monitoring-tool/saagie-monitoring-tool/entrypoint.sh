#!/bin/bash

if [[ -z ${SAAGIE_SUPERVISION_LOGIN} || -z ${SAAGIE_SUPERVISION_PASSWORD} || -z ${SAAGIE_URL} || -z ${SAAGIE_REALM} || -z {$SAAGIE_PLATFORM_ID} || -z ${MONITORING_OPT} ]]; then
  echo "ERROR : Missing environment variables. In order to work, this app needs the following environment variables set : "
  echo "- SAAGIE_SUPERVISION_LOGIN"
  echo "- SAAGIE_SUPERVISION_PASSWORD"
  echo "- SAAGIE_URL"
  echo "- SAAGIE_REALM"
  echo "- SAAGIE_PLATFORM_ID"
  echo "- MONITORING_OPT"
  exit 1
fi

echo \#!/bin/bash
{
  echo export SAAGIE_SUPERVISION_LOGIN=$SAAGIE_SUPERVISION_LOGIN
  echo export SAAGIE_SUPERVISION_PASSWORD=$SAAGIE_SUPERVISION_PASSWORD
  echo export SAAGIE_URL=$SAAGIE_URL
  echo export SAAGIE_REALM=$SAAGIE_REALM
  echo export SAAGIE_PLATFORM_ID=$SAAGIE_PLATFORM_ID
  echo export MONITORING_OPT=$MONITORING_OPT
  echo export IP_HDFS=$IP_HDFS
  echo export HADOOP_HOME=/hadoop/hadoop-2.6.5
  echo python3 /app/__main__.py
} >> /app/script.sh

chmod +x /app/script.sh
PG_DATA_DIR=/var/lib/postgresql/data

if [ "$(ls -A $PG_DATA_DIR)" ]; then
  echo "PG Database already exists, skipping init"
  su postgres -c "export PATH=$PATH:/usr/lib/postgresql/12/bin && pg_ctl start -D ${PG_DATA_DIR}" > /dev/null
else
  echo "Initializing PG database"
  chown postgres:postgres $PG_DATA_DIR
  chmod 777 $PG_DATA_DIR

  {
    su postgres -c "/usr/lib/postgresql/12/bin/initdb -D $PG_DATA_DIR"
    su postgres -c "export PATH=$PATH:/usr/lib/postgresql/12/bin && pg_ctl start -D $PG_DATA_DIR"
    su postgres -c 'psql --command "CREATE USER supervision_pg_user"'
    su postgres -c 'psql --command "CREATE DATABASE supervision_pg_db ENCODING \"UTF8\" TEMPLATE template0"'
    su postgres -c 'psql --command "GRANT ALL PRIVILEGES ON DATABASE supervision_pg_db to supervision_pg_user"'
    su postgres -c 'psql -U supervision_pg_user -d supervision_pg_db -f infra.sql'
  } > /dev/null
fi


sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/grafana/grafana.ini
sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/nginx/sites-enabled/grafana.conf

cp /var/lib/grafana/tmp-dashboards/saagie*.json /var/lib/grafana/dashboards/

if [ "$MONITORING_OPT" == "SAAGIE_AND_DATALAKE" ]; then
   cp /var/lib/grafana/tmp-dashboards/datalake*.json /var/lib/grafana/dashboards/
fi


echo "0 * * * * /app/script.sh >> /tmp/log_cron.log 2>&1" > mycron \
&& crontab mycron \
&& rm mycron \
&& service cron start

echo "Job's starting" >> /tmp/log_cron.log

tail -f /tmp/log_cron.log &

/app/script.sh &
nginx && /run.sh
