# Spark for AWS (Hadoop 3.2)


![Docker Image Size (tag)](https://img.shields.io/docker/image-size/saagie/spark/3.2-aws-jre-11-0.36?label=v3.2-aws-jre-11%20image%20size&style=for-the-badge)

![Docker Image Size (tag)](https://img.shields.io/docker/image-size/saagie/spark/3.2-aws-py-3.8-0.36?label=v3.2-aws-py-3.8%20image%20size&style=for-the-badge)

![Docker Image Size (tag)](https://img.shields.io/docker/image-size/saagie/spark/3.2-aws-py-3.9-0.36?label=v3.2-aws-py-3.9%20image%20size&style=for-the-badge)

## Description
This directory contains version of Spark customized for Saagie Platform to use when working with AWS only (or with Hadoop 3.2). 
This version is based on :
- Spark 3.2
- Hadoop 3.2
- Hadoop AWS 3.2.0

## How to build in local

At the root of this repository, run the following command depending of the Spark version you want to build:
```
./gradlew buildSparkJobs
```


