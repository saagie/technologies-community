# Spark for AWS (Hadoop 3.2)

![Docker Image Size (tag)](https://img.shields.io/docker/image-size/saagie/spark/3.0-aws-0.11.2?label=v3.0-aws%20base%20image%20size&style=for-the-badge)

![Docker Image Size (tag)](https://img.shields.io/docker/image-size/saagie/spark/3.0-aws-jre-11-0.11.2?label=v3.0-aws-jre11%20image%20size&style=for-the-badge)

![Docker Image Size (tag)](https://img.shields.io/docker/image-size/saagie/spark/3.0-aws-py-3.7-0.11.2?label=v3.0-aws-py3.7%20image%20size&style=for-the-badge)

## Description
This directory contains version of Spark customized for Saagie Platform to use when working with AWS only (or with Hadoop 3.2). 
This version is based on :
- Spark 3.0.1
- Hadoop 3.2
- Hadoop AWS 3.2.0
- Spark Structured Streaming Kinesis Connector (by Qubole) 1.2.0
- MongoDB connector

## How to build in local

At the root of this repository, run the following command depending of the Spark version you want to build:
```
./gradlew buildSparkJobs
```


