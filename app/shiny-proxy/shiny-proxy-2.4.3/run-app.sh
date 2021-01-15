#!/bin/bash

case "$SHINYPROXY_CONF_URL" in 
    s3*) 
        echo "[INFO] - Fetching application.yml file from S3"
        aws s3 cp $SHINYPROXY_CONF_URL /opt/shinyproxy/application.yml;;
    http*)
        echo "[INFO] - Fetching application.yml file"
        wget $SHINYPROXY_CONF_URL -O /opt/shinyproxy/application.yml;;
    *)
        echo "[WARN] - application.yml configuration file cannot be fetched : protocol not compatible => choose between s3 or http"
        echo "[INFO] - Sample application.yml file will be used"
esac

sed -i 's#SAAGIE_BASE_PATH#'"$SAAGIE_BASE_PATH"'#g' /opt/shinyproxy/application.yml
java -jar /opt/shinyproxy/shinyproxy.jar