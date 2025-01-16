#!/bin/bash
set -euo pipefail

if compgen -G "*.zip*" > /dev/null;
then
    echo "Zip file detected ... unzipping ..."
    unzip -q *.zip
fi

if test -f main_script;
then sh ./main_script;
else exec "$@"
fi;
