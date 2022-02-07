# Radiant 
![Docker Image Size (tag)](https://img.shields.io/docker/image-size/saagie/radiant/1.9.1?label=v1.9.1%20image%20size&style=for-the-badge)

## Description
This directory contains version of Radiant contenairized and customized for Saagie Platform.
See radiant official documentation for more information https://radiant-rstats.github.io/docs/

## How to build in local

Inside the `radiant-x.y.z` folder corresponding to your version, run :
```
docker build -t saagie/radiant:<version> .
docker push saagie/radiant:<version>
```


