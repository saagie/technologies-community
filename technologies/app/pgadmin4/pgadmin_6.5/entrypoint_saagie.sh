#!/bin/sh

echo launching Nginx
sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/nginx/http.d/pgadmin.conf
#nginx -g 'pid /tmp/nginx.pid; daemon on;'


cat /etc/nginx/http.d/pgadmin.conf
nginx -g 'pid /tmp/nginx.pid; daemon on;' && /entrypoint.sh

