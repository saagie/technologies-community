#!/usr/bin/with-contenv bash

if [ -n "${VSCODE_PASSWORD}" ] || [ -n "${VSCODE_HASHED_PASSWORD}" ]; then
  AUTH="password"
else
  AUTH="none"
  echo "starting with no password"
fi

if [ -z ${SAAGIE_BASE_PATH+x} ]; then
  PROXY_DOMAIN_ARG=""
else
  PROXY_DOMAIN_ARG="--proxy-domain=${SAAGIE_BASE_PATH}"
fi

exec \
	s6-setuidgid abc \
		/usr/local/bin/code-server \
			--bind-addr 0.0.0.0:8443 \
			--user-data-dir /config/data \
			--extensions-dir /config/extensions \
			--disable-telemetry \
			--auth "${AUTH}" \
			--proxy-domain=${SAAGIE_BASE_PATH}
			/config/workspace