# Python MLflow

## Description

This directory contains version of MLflow server contenairized and customized for Saagie Platform.

## How to build in local

Inside the `mlflow-server` folder, run :
```
docker build -t courbix/mlflow-server:<version> .
docker push courbix/mlfloww-server:<version>
```

## Job/App specific information

Some environment variable should be set to run the MLflow server:

* MYSQL_USER_LOGIN: User login of Mysql in order to store backend data
* MYSQL_USER_PASSWORD: User password of Mysql in oder to store backend data
* MYSQL_HOST: Mysql Host
* MYSQL_DB: Database of Mysql to store backend data
* HDFS_URI: HDFS URI to store artifact data (eg. hdfs://nn1.p4.saagie.prod.saagie.io:8020/)

Once you have created an application with the MLflow server, don't forget to set the *MLFLOW_TRACKING_URI* environment variable with the url of the application when you opened it.
