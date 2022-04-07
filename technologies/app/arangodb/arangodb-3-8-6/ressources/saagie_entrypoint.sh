#!/bin/bash

# Start Nginx for Saagie
echo "Starting arangoDB"

SAAGIE_BASE_PATH="${SAAGIE_BASE_PATH}"

echo "SAAGIE_BASE_PATH = $SAAGIE_BASE_PATH"

echo "############################################"
echo "Starting Nginx for Saagie"
echo "############################################"
sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/nginx/sites-enabled/nginx.conf
nginx && ./entrypoint.sh arangod
