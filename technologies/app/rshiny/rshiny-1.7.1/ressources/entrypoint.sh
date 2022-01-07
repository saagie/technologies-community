#!/bin/bash

set -xeuo pipefail

echo "SAAGIE_BASE_PATH = $SAAGIE_BASE_PATH"
SHINY_GIT_BRANCH=${SHINY_GIT_BRANCH:-master}
echo "Setting SHINY_GIT_BRANCH to $SHINY_GIT_BRANCH..."
echo "cloning repo from SHINY_GIT_URL_REPOSITORY: $SHINY_GIT_URL_REPOSITORY"


git clone $SHINY_GIT_URL_REPOSITORY --branch $SHINY_GIT_BRANCH --single-branch --depth 1 app

sudo sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/nginx/sites-enabled/nginx.conf
nginx && Rscript -e 'library(methods); library(shiny); runApp("app", 3838)'

