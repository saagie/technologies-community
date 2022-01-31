#!/bin/bash
echo "Set Proxy"

echo "
- INFO: 'PASSWORD' variable is optional and allow you to set a password to access your VsCode

INFO: If you hae any request don't hesitate to create an issue in this repository: https://github.com/saagie/technologies-community
"

export PROXY_DOMAIN=$SAAGIE_BASE_PATH

echo "SAAGIE_BASE_PATH"
echo $SAAGIE_BASE_PATH
echo "PROXY_DOMAIN"
echo $PROXY_DOMAIN

# /init

sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/nginx/sites-enabled/nginx.conf
nginx && /init