# Saagie Monitoring Tool

## Description

This directory contains Saagie Monitoring Tool based on Grafana dashboards.
The version 1.0 works with Saagie >= 3.0.0

## How to launch it

To deploy Saagie Monitoring Tool on your platform, you need to create a user with viewer rights on all projects at least, and then set the following environment variables in Saagie :

- SAAGIE_SUPERVISION_LOGIN : Application user's username
- SAAGIE_SUPERVISION_PASSWORD : Application user's password
- SAAGIE_URL : URL of the Saagie plateform (i.e. : `https://saagie-workspace.prod.saagie.io`)
- SAAGIE_PLATFORM_ID : ID of your plateform  (Default value : `1`)
- MONITORING_OPT (default value : `SAAGIE`): 
  - `SAAGIE` if you want to monitor only Saagie jobs, apps and pipelines 
  - `SAAGIE_AND_DATALAKE` if you want to monitor Saagie and your HDFS Datalake
  - `SAAGIE_AND_S3` if you want to monitor Saagie and S3 buckets
- IP_HDFS (Required if MONITORING_OPT=`SAAGIE_AND_DATALAKE`) : Namenode IP
- AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_S3_ENDPOINT and AWS_REGION_NAME (Required if MONITORING_OPT=`SAAGIE_AND_S3`)
