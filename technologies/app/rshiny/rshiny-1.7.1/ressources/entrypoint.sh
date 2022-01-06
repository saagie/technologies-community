#!/bin/bash

set -xeuo pipefail

echo "SAAGIE_BASE_PATH = SAAGIE_BASE_PATH"
echo "Setting SHINY_GIT_BRANCH to $SHINY_GIT_BRANCH..."
SHINY_GIT_BRANCH=${DASH_GIT_BRANCH:-master}
echo "cloning repo from DASH_GIT_URL_REPOSITORY: $DASH_GIT_URL_REPOSITORY"


git clone $DASH_GIT_URL_REPOSITORY --branch $SHINY_GIT_BRANCH --single-branch --depth 1 app

sudo sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/nginx/sites-enabled/shiny.conf
nginx && Rscript -e 'library(shiny); runApp("app", 3838)'

