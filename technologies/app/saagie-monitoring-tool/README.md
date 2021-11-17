# Saagie Monitoring Tool

![Docker Image Size (tag)](https://img.shields.io/docker/image-size/saagie/saagie-monitoring-tool/0.2?label=v0.2%20image%20size&style=for-the-badge)

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
- SAAGIE_REALM : Realm of your Saagie plateform (i.e: `saagie` if your URL is `https://saagie-workspace.prod.saagie.io`)
- SAAGIE_PLATFORM_ID : ID of your plateform (i.e. : `4`)

Finally, you can choose the monitoring type and the frequency :

- MONITORING_OPT : `SAAGIE` if you want to monitor only Saagie or `SAAGIE_AND_DATALAKE` if you want to monitor Saagie and HDFS
- IP_HDFS (Required if MONITORING_OPT=`SAAGIE_AND_DATALAKE`) : Namenode IP
- CRON_DAYS (Optional, default : `1`) : This application is based on script that will pull data from Saagie platform and HDFS. This option set the interval between two runs (i.e. : `1` for daily basis, `7` for weekly basis, etc.)

## Known issues

In case of restart, all data will be lost. Indeed, data are persisted yet.
