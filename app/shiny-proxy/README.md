# ShinyProxy

## Description
This directory contains version of ShinyProxy containerized and customized for Saagie Platform.
See ShinyProxy official documentation for more information https://shinyproxy.io/documentation/

## How to build in local

```
docker build -t saagie/shinyproxy-<version> .
docker push saagie/shinyproxy-<version>
```


## Job/App specific information
In order to run it, you must specifiy through an environment variable `SHINYPROXY_CONF_URL` where your application.yml configuration file is stored (can be either WebHDFS or S3). Examples  : 
* `export SHINYPROXY_CONF_URL=http://<your hdfs namenode url>:50070/webhdfs/v1/path/to/application.yml?op=OPEN&user.name=my.username`
* `export SHINYPROXY_CONF_URL=s3://path/to/application.yml`

A template for this `application.yml` file is provided in this repository. In order to be compatible within Saagie, you must be careful about keeping the `context-path: SAAGIE_BASE_PATH` entry, mandatory for Saagie. To configure ShinyProxy based ou your requirements, follow the [official documentation](https://shinyproxy.io/documentation/configuration)

## Customize ShinyProxy

This Docker image relies on 2 forks from Open Analytics open source projects.

https://github.com/saagie/shinyproxy
https://github.com/saagie/containerproxy

If you want to customize these implementations, just pull the `containerproxy`, make your changes and build it with the following command : 


```
mvn -U clean install
```

Do the same for the `shinyproxy` repository (make sure to update your `pom.xml` to refer to the previously built containerproxy jar).

The build will result in a single `.jar` file that is made available in the `target` directory, you can replace the **shinyproxy-2.4.3-saagie** of this repository with this new jar.

