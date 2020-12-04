#!/bin/bash
sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/nginx/sites-enabled/superset.conf

nginx&

# Init superset db and admin user at first startup
/init_superset.sh&

#Start gunicorn
export SUPERSET_UPDATE_PERMS=0 #FIXME SUPERSET_UPDATE_PERMS does not work
gunicorn "superset.app:create_app()"