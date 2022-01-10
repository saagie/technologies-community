# R Shiny
## Description
This directory contains a RShiny contenairized and customized for Saagie Platform.
See RShiny official documentation for more information https://shiny.rstudio.com/

## How to build in local

```
docker build -t saagie/rshiny .
docker push saagie/rshiny
```

## Run RShiny container

### On Saagie's Platform

This container is designed to run on Saagie platform.

The official documentation is available here: [Saagie's official documentation](https://docs.saagie.io/product/latest/sdk/index.html).

### On premise / your local server

It's possible (mainly for development and testing) to run this image outside of a Saagie platform.
Please note that Saagie cannot provide any support for images launched outside its platform.

Run:
```
docker run -e "SAAGIE_BASE_PATH=/test" -e "SHINY_GIT_URL_REPOSITORY=https://github.com/saagie/demo-r-shiny.git" -e "SHINY_GIT_BRANCH=main" -p 80:80 saagie/rshiny:1.7.1
```
And access it with this adress: [localhost/test/](localhost/test/)

- `SAAGIE_BASE_PATH` variable is **mandatory** and should be equal to / . It's used to customize the path to the application when behind a reverse proxy.
- `SHINY_GIT_URL_REPOSITORY` variable is also **mandatory** and should be set to the name of the git repository continning your RShiny app source code.
- `SHINY_GIT_BRANCH` is optional and defaulted to master, it indicates a specific branch to checkout.
