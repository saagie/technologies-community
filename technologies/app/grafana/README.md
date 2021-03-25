# Grafana
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/saagie/grafana/7.3.4?label=v7.3.4%20image%20size&style=for-the-badge)

## Description
This directory contains version of Grafana contenairized and customized for Saagie Platform.
See Grafana official documentation for more information https://grafana.com/docs/grafana/latest/

## How to build in local

Inside the `grafana-x.y.z` folder corresponding to your version, run :
```
docker build -t saagie/grafana-<version> .
docker push saagie/grafana-<version>
```


## Job/App specific information
Default admin credentials are `admin/admin`. Change them during your first connection.
