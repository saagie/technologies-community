#!/bin/bash
sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/nginx/sites-enabled/superset.conf

nginx && gunicorn "superset.app:create_app()"
