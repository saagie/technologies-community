# Airbyte

![Docker Image Size (tag)](https://img.shields.io/docker/image-size/saagie/airbyte/1.0)

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

- AIRBYTE_URL : URL of the VM containing Airbyte
- AIRBYTE_LOGIN : Login of the VM containing Airbyte
- AIRBYTE_PASSWORD : Password of the VM containing Airbyte
- SAAGIE_LOGIN: Login of Saagie platform (please make sure that this user have access on `SAAGIE_PROJECT_NAME`)
- SAAGIE_PASSWORD: Password of Saagie platform
- SAAGIE_URL: URL of the Saagie platform (i.e. : `https://saagie-workspace.prod.saagie.io`)
- SAAGIE_PLATFORM_ID : ID of your plateform  (Default value : `1`)
- SAAGIE_PROJECT_NAME: Project name of Saagie
- AIRBYTE_WORKSPACE_NAME (optional): Workspace's name of Airbyte, if not set, it will be the same as `SAAGIE_PROJECT_NAME`