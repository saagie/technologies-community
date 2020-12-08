#!/bin/bash
sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/nginx/sites-enabled/superset.conf

nginx&

# Init superset DB and creates Admin user at first startup
/init_superset.sh

# Start gunicorn
gunicorn "superset.app:create_app()"