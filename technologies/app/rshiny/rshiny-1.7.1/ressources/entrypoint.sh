#!/bin/bash

set -xeuo pipefail

echo "
- 'SHINY_GIT_URL_REPOSITORY' variable is mandatory and should be set to the name of the git repository containning your RShiny app source code (e.g.:https://github.com/saagie/demo-r-shiny.git).
- 'SHINY_GIT_BRANCH' is optional and defaulted to master, it indicates a specific branch to checkout.
"

if [[ -z "${SHINY_GIT_URL_REPOSITORY}" ]]; then
  echo "ERROR : Variable SHINY_GIT_URL_REPOSITORY must be set before running the app. 
  See https://docs.saagie.io/user/latest/tutorials/projects-module/projects/envar/index.html#projects-create-envar-project for more information"
  exit 1
fi

echo "SAAGIE_BASE_PATH = $SAAGIE_BASE_PATH"
SHINY_GIT_BRANCH=${SHINY_GIT_BRANCH:-master}
echo "Setting SHINY_GIT_BRANCH to $SHINY_GIT_BRANCH"
echo "cloning repo from SHINY_GIT_URL_REPOSITORY: $SHINY_GIT_URL_REPOSITORY"

git clone $SHINY_GIT_URL_REPOSITORY --branch $SHINY_GIT_BRANCH --single-branch --depth 1 app

sudo sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/nginx/sites-enabled/nginx.conf
nginx && Rscript -e 'library(methods); library(shiny); runApp("app", 3838)'

