# Airbyte

![Docker Image Size (tag)](https://img.shields.io/docker/image-size/saagie/saagie-monitoring-tool/0.27?label=v0.27%20image%20size&style=for-the-badge)

## Description

This folder contains the image of the redirection to the VM containing the Airbyte software allowing the creation of data flows.

## How to build in local

Inside the `airbyte` folder corresponding to your version, run :
```
docker build -t saagie/airbyte:<version> .
docker push saagie/airbyte:<version>
```

## How to launch it

To deploy Airbyte on your platform (already configured on the platform) :

- URL_AIRBYTE : URL of the VM containing Airbyte
- LOGIN_AIRBYTE : Login of the VM containing Airbyte
- PASSWORD_AIRBYTE : Password of the VM containing Airbyte