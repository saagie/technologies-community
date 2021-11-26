# Saagie Monitoring Tool

![Docker Image Size (tag)](https://img.shields.io/docker/image-size/saagie/saagie-monitoring-tool/0.9?label=v0.9%20image%20size&style=for-the-badge)

## Description

This directory contains Saagie Monitoring Tool based on Grafana dashboards.

## How to build in local

Inside the `saagie-monitoring-tool` folder corresponding to your version, run :
```
docker build -t saagie/saagie-monitoring-tool:<version> .
docker push saagie/saagie-monitoring-tool:<version>
```

## How to launch it

To deploy Saagie Monitoring Tool on your platform, you need to create a user with viewer rights on all projects at least and then set the following environment variables in Saagie :

- SAAGIE_SUPERVISION_LOGIN : Application user's username
- SAAGIE_SUPERVISION_PASSWORD : Application user's password
- SAAGIE_URL : URL of the Saagie plateform (i.e. : `https://saagie-workspace.prod.saagie.io`)
- SAAGIE_REALM : Realm of your Saagie plateform (i.e: `saagie` if your URL is `https://saagie-workspace.prod.saagie.io`)
- SAAGIE_PLATFORM_ID : ID of your plateform (i.e. : `4`)
- MONITORING_OPT : `SAAGIE` if you want to monitor only Saagie or `SAAGIE_AND_DATALAKE` if you want to monitor Saagie and HDFS
- IP_HDFS (Required if MONITORING_OPT=`SAAGIE_AND_DATALAKE`) : Namenode IP

