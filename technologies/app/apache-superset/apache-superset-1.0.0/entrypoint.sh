#!/bin/bash
sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/nginx/sites-enabled/superset.conf
/rewrite_base_path.sh

nginx&

# Init superset DB and creates Admin user at first startup
/init_superset.sh

# Start gunicorn
# Recommended settings for gunicorn are already applied 
# https://superset.apache.org/docs/installation/configuring-superset#running-on-a-wsgi-http-server
gunicorn "superset.app:create_app()"