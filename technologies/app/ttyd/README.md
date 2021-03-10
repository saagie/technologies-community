# TTYD - Interactive Bash

![Docker Image Size (tag)](https://img.shields.io/docker/image-size/saagie/ttyd-saagie/1.0?label=v1.0%20image%20size&style=for-the-badge)

## Description
This directory contains TTYD, an interactive Bash for Saagie Platform.
Contains :
- Hadoop (hdfs commands)
- Hive commands
- Sqoop commands
- Spark (local mode only)
- Python 3.7 vanilla


## How to build in local

Inside the `ttyd` folder, run :
```
docker build -t saagie/ttyd:<tag> .
docker push saagie/ttyd-<tag>
```


