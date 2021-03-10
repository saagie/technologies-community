#!/bin/bash
echo "SAAGIE_BASE_PATH"
echo $SAAGIE_BASE_PATH

# /init

sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/nginx/sites-enabled/nginx.conf
nginx && /init