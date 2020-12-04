#!/bin/bash
sleep 30
if [ -e $SUPERSET_HOME/superset.db ]
then
    echo "Superset Database already exists"
else
    echo "Superset Database does not exists, initalization in progress"
    superset db upgrade

    superset fab create-user \
    --role Admin \
    --username admin \
    --firstname admin \
    --lastname admin \
    --email user@example.com \
    --password admin

    superset init
fi