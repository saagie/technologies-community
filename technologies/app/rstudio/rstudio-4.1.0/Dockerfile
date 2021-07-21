FROM rocker/tidyverse:4.1.0

LABEL maintainer="Saagie <tony@saagie.com>"

USER root

ENV DEBIAN_FRONTEND noninteractive

ENV CDH_MAIN_VERSION 5
ENV CDH_VERSION ${CDH_MAIN_VERSION}.7.1
ENV HADOOP_VERSION 2.6.0
ENV HIVE_VERSION 1.2.2
ENV HIVE_ODBC_VERSION 2.6.4.1004
ENV HIVE_ODBC_VERSION_FULL ${HIVE_ODBC_VERSION}-2_amd64
ENV IMPALA_ODBC_VERSION 2.5.41.1029
ENV IMPALA_ODBC_VERSION_FULL ${IMPALA_ODBC_VERSION}-2_amd64

# Hive client installation
# TODO use oneline curl -o with env var to simplify
RUN wget --no-verbose http://apache.mirrors.ovh.net/ftp.apache.org/dist/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz \
    && tar -xvzf apache-hive-${HIVE_VERSION}-bin.tar.gz \
    && rm apache-hive-${HIVE_VERSION}-bin.tar.gz
ENV HIVE_HOME=/apache-hive-${HIVE_VERSION}-bin
ENV PATH=$HIVE_HOME/bin:$PATH

# Install Hive ODBC driver
RUN apt update -qq && apt install -yqq --no-install-recommends \
      libsasl2-modules-gssapi-mit \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && cd /tmp \
    && wget --no-verbose https://downloads.cloudera.com/connectors/ClouderaHive_ODBC_${HIVE_ODBC_VERSION}/Debian/clouderahiveodbc_${HIVE_ODBC_VERSION_FULL}.deb \
    && dpkg -i clouderahiveodbc_${HIVE_ODBC_VERSION_FULL}.deb \
    && odbcinst -i -d -f /opt/cloudera/hiveodbc/Setup/odbcinst.ini \
    && rm /tmp/clouderahiveodbc_${HIVE_ODBC_VERSION_FULL}.deb

# Install Impala ODBC dependency
RUN cd /tmp \
    && wget --no-verbose https://downloads.cloudera.com/connectors/impala_odbc_${IMPALA_ODBC_VERSION}/Debian/clouderaimpalaodbc_${IMPALA_ODBC_VERSION_FULL}.deb \
    && dpkg -i clouderaimpalaodbc_${IMPALA_ODBC_VERSION_FULL}.deb \
    && odbcinst -i -d -f /opt/cloudera/impalaodbc/Setup/odbcinst.ini \
    && rm -rf /tmp/clouderaimpalaodbc_${IMPALA_ODBC_VERSION_FULL}.deb \
    && sed -i 's/DriverManagerEncoding=UTF-32/DriverManagerEncoding=UTF-16/g' /opt/cloudera/impalaodbc/lib/64/cloudera.impalaodbc.ini

# JAVA_HOME define
ENV JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Packages install
RUN install2.r --error --skipinstalled \
    aws.s3 \
    arrow \
    openxlsx


# Nginx isntall and remove default conf
RUN apt-get update -qq && apt-get install -yqq --no-install-recommends \
      nginx \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/ \
    && rm /etc/nginx/sites-enabled/default
COPY resources/server.conf /etc/nginx/sites-enabled/rstudio.conf

# Store Root envvar to be able to exclude it at runtime when propagating envvars to every user
RUN env >> /ROOT_ENV_VAR && chmod 400 /ROOT_ENV_VAR

COPY resources/userconf /etc/cont-init.d/userconf
COPY resources/init_rstudio.sh /init_rstudio.sh

# Be sure rstudio user has full access to his home directory
RUN mkdir -p /home/rstudio && \
    chown -R rstudio:rstudio /home/rstudio && \
    chmod -R 755 /home/rstudio && \
    chmod 500 /init_rstudio.sh

EXPOSE 80

COPY resources/entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]

CMD ["/bin/sh", "-c", "/init_rstudio.sh"]

