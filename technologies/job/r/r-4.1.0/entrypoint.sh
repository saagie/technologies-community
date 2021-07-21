#!/bin/bash

set -euo pipefail
if compgen -G "*.zip*" > /dev/null; then
    echo "Zip file detected ... unzipping ..."
    unzip -qo *.zip
fi
if test -f main_script; then
    echo "'main_script' detected ... executing ..."
    bash ./main_script
else
    exec "$@"
fi