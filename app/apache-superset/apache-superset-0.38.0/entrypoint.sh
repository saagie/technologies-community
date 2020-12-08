#!/bin/bash
sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/nginx/sites-enabled/superset.conf

sed -i 's#/static/#'"$SAAGIE_BASE_PATH/static/"'#g' /usr/local/lib/python3.8/site-packages/superset/static/assets/*.js
sed -i 's#/superset/#'"$SAAGIE_BASE_PATH/superset/"'#g' /usr/local/lib/python3.8/site-packages/superset/static/assets/*.js
sed -i 's#/csstemplateasyncmodelview/#'"$SAAGIE_BASE_PATH/csstemplateasyncmodelview/"'#g' /usr/local/lib/python3.8/site-packages/superset/static/assets/*.js

# TODO fixme : redirections when saving a chart or a dashbaord

nginx&

# Init superset DB and creates Admin user at first startup
/init_superset.sh

# Start gunicorn
# Recommended settings for gunicorn are already applied 
# https://superset.apache.org/docs/installation/configuring-superset#running-on-a-wsgi-http-server
gunicorn "superset.app:create_app()"