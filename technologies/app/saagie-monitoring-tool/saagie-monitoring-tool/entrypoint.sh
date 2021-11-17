#!/bin/bash

echo \#!/bin/bash
{
  echo export SAAGIE_SUPERVISION_LOGIN=$SAAGIE_SUPERVISION_LOGIN
  echo export SAAGIE_SUPERVISION_PASSWORD=$SAAGIE_SUPERVISION_PASSWORD
  echo export SAAGIE_URL=$SAAGIE_URL
  echo export SAAGIE_REALM=$SAAGIE_REALM
  echo export SAAGIE_PLATFORM_ID=$SAAGIE_PLATFORM_ID
  echo export MONITORING_OPT=$MONITORING_OPT
  echo export IP_HDFS=$IP_HDFS
  echo export IP_HDFS=$IP_HDFS
  echo export HADOOP_HOME=/hadoop/hadoop-2.6.5
  echo python3 /app/__main__.py
} >> /app/script.sh

chmod +x /app/script.sh

su postgres -c 'source /etc/profile && pg_ctl start -D /var/lib/postgresql/data'
su postgres -c 'psql --command "CREATE USER supervision_pg_user"'
su postgres -c 'psql --command "CREATE DATABASE supervision_pg_db ENCODING \"UTF8\" TEMPLATE template0"'
su postgres -c 'psql --command "GRANT ALL PRIVILEGES ON DATABASE supervision_pg_db to supervision_pg_user"'
su postgres -c 'psql -U supervision_pg_user -d supervision_pg_db -f infra.sql'

sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/grafana/grafana.ini
sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/nginx/sites-enabled/grafana.conf

echo "0 0 */$CRON_DAYS * * /app/script.sh >> /tmp/log_cron.log 2>&1" > mycron \
&& crontab mycron \
&& rm mycron \
&& service cron start

echo "Job's starting" >> /tmp/log_cron.log

tail -f /tmp/log_cron.log &
nginx && /run.sh
