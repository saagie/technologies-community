#!/bin/bash
set -eo pipefail

sed -i 's:PASSWORD:'"$PASSWORD_AIRBYTE"':g' /etc/nginx/auth.htpasswd
sed -i 's:LOGIN:'"$LOGIN_AIRBYTE"':g' /etc/nginx/auth.htpasswd
sed -i 's|AIRBYTE_PATH|'"$URL_AIRBYTE"'|g' /etc/nginx/conf.d/default.conf


nginx -g "daemon off;"