#!/bin/bash

# Start Nginx for Saagie
echo "
Default user password is neo4j / neo4j
"
SAAGIE_BASE_PATH="${SAAGIE_BASE_PATH}"
NEO4J_BASE_PATH="${NEO4J_BASE_PATH}"
NEO4J_HTTPS_BASE_PATH="${NEO4J_HTTPS_BASE_PATH}"

echo "SAAGIE_BASE_PATH = $SAAGIE_BASE_PATH"
echo "NEO4J_BASE_PATH = $NEO4J_BASE_PATH"
echo "NEO4J_HTTPS_BASE_PATH = $NEO4J_HTTPS_BASE_PATH"

echo "############################################"
echo "Starting Nginx for Saagie"
echo "############################################"
sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/nginx/sites-enabled/nginx.conf
sed -i 's:NEO4J_BASE_PATH:'"$NEO4J_BASE_PATH"':g' /etc/nginx/sites-enabled/nginx.conf
sed -i 's:NEO4J_HTTPS_BASE_PATH:'"$NEO4J_HTTPS_BASE_PATH"':g' /etc/nginx/sites-enabled/nginx.conf
nginx
