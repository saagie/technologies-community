#!/bin/bash

## JS
patterns=(
    static
    api
    superset
)

for pattern in "${patterns[@]}"; do
    sed -i 's#/'$pattern'/#'"$SAAGIE_BASE_PATH/$pattern/"'#g' /usr/local/lib/python3.8/site-packages/superset/static/assets/*.js
done

## Python

patterns=(
    accessrequestsmodelview
    dashboardmodelview
    druiddatasourcemodelview
    druidclustermodelvie
)

for pattern in "${patterns[@]}"; do
    sed -i 's#/'$pattern'/#'"$SAAGIE_BASE_PATH/$pattern/"'#g' /usr/local/lib/python3.8/site-packages/superset/*.py
done