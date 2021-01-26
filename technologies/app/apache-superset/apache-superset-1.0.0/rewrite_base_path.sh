#!/bin/bash

## JS
patterns=(
    static
    chart/add
    dashboard/new
    superset/sqllab
    api/
    superset/
)

for pattern in "${patterns[@]}"; do
    sed -i 's#/'$pattern'#'"$SAAGIE_BASE_PATH/$pattern/"'#g' /usr/local/lib/python3.8/site-packages/superset/static/assets/*.js
done

## Python

patterns=(
    accessrequestsmodelview
    dashboardmodelview
    druiddatasourcemodelview
    druidclustermodelvie
)

for pattern in "${patterns[@]}"; do
    #sed -i 's#/'$pattern'/#'"$SAAGIE_BASE_PATH/$pattern/"'#g' /usr/local/lib/python3.8/site-packages/superset/*.py
    echo $pattern
done

## HTML
patterns=(
    chart/add
    dashboard/new
    superset/sqllab
)

for pattern in "${patterns[@]}"; do
    sed -i 's#/'$pattern'#'"$SAAGIE_BASE_PATH/$pattern/"'#g' /usr/local/lib/python3.8/site-packages/superset/templates/appbuilder/navbar_right.html
done