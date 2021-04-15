#!/usr/bin/env bash
sed -i 's:SAAGIE_BASE_PATH:'"$SAAGIE_BASE_PATH"':g' /etc/nginx/conf.d/server.conf

[[ -z "${SPARK_HISTORY_EVENT_LOG_DIR}" ]] && logDirectory='hdfs://cluster/tmp/spark-events' || logDirectory="${SPARK_HISTORY_EVENT_LOG_DIR}"
export SPARK_HISTORY_OPTS='-Dspark.ui.proxyBase='"$SAAGIE_BASE_PATH"' -Dspark.history.fs.logDirectory='"$logDirectory"
nginx && /opt/spark/sbin/start-history-server.sh

