# Metabase

![Docker Image Size (tag)](https://img.shields.io/docker/image-size/saagie/metabase/0.38?label=v0.38%20image%20size&style=for-the-badge)

## Description
This directory contains version of Metabase contenairized and customized for Saagie Platform.
See Metabase official documentation for more information https://www.metabase.com/docs/latest/

## How to build in local

Inside the `metabase-x.y` folder corresponding to your version, run :
```
docker build -t saagie/metabase:<version> .
docker push saagie/metabase:<version>
```

## Job/App specific information
Default admin credentials are to be created during first login.

## Configuration
This version comes with a local H2 table to store Metabase internal data. You can choose to use an external MySQL / PostgreSQL table to do so. This can be configured (among other parameters) through environment variables. Follow this [documentation](https://www.metabase.com/docs/latest/operations-guide/environment-variables.html) for more information.

## Known issues
When you first log in, after having createad your user, you will be redirected to your Saagie Projects instead of the Metabase homepage. Simply return to your Saagie App and try to open the Metabase url (this issue only happens during first login).



