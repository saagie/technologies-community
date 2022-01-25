#!/bin/bash

# Start Nginx for Saagie
echo "
Default user password is neo4j / neo4j
"
SAAGIE_BASE_PATH="${SAAGIE_BASE_PATH}/browser/"
echo "SAAGIE_BASE_PATH = $SAAGIE_BASE_PATH"

echo "############################################"
echo "Starting Nginx for Saagie"
echo "############################################"
sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/nginx/sites-enabled/nginx.conf
nginx