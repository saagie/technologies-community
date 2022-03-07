#!/bin/sh

if [[ -z "${SAAGIE_BASE_PATH}" ]]; then
  echo 'ERROR : $SAAGIE_BASE_PATH variable must be set before launch. Exiting.'
  exit 1
fi

echo "launching Nginx"
sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/nginx/http.d/pgadmin.conf
#nginx -g 'pid /tmp/nginx.pid; daemon on;'


cat /etc/nginx/http.d/pgadmin.conf
nginx -g 'pid /tmp/nginx.pid; daemon on;' && /entrypoint.sh

