# Saagie Monitoring Tool

![Docker Image Size (tag)](https://img.shields.io/docker/image-size/saagie/metabase/0.38.4?label=v0.38.4%20image%20size&style=for-the-badge)

## Description

This directory contains Saagie Monitoring Tool based on Grafana dashboards.

## How to build in local

Inside the `saagie-monitoring-tool` folder corresponding to your version, run :
```
docker build -t saagie/saagie-monitoring-tool:<version> .
docker push saagie/saagie-monitoring-tool:<version>
```

## Job/App specific information

Default admin login is `admin`. Default admin password must be set with the GRAFANA_ADMIN_PASSWORD environment variable.  
Futhermore, you need to create an application user with viewer rights on all projects at least and then the following environment variables in Saagie :

- SAAGIE_SUPERVISION_LOGIN : Application user's username
- SAAGIE_SUPERVISION_PASSWORD : Application user's password
- SAAGIE_URL : URL of the Saagie plateform (i.e. : `https://saagie-workspace.prod.saagie.io`)
- SAAGIE_REALM : Realm of your Saagie plateform
- SAAGIE_PLATFORM_ID : ID of your plateform (i.e. : `4`)

Finally, you can choose the monitoring type :

- MONITORING_OPT : `SAAGIE` if you want to monitor only Saagie or `SAAGIE_AND_DATALAKE` if you want to monitor Saagie and the datalake
- IP_HDFS (Required if MONITORING_OPT=`SAAGIE_AND_DATALAKE`) : Namenode IP

## Known issues

In case of restart, all data will be lost. Indeed, data are persisted yet.
