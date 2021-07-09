FROM saagie/python:3.7-1.46.0

RUN apt update -qq \
        && apt-get install -y alien python-pip libaio1 libaio-dev \
        && wget https://download.oracle.com/otn_software/linux/instantclient/211000/oracle-instantclient-basic-21.1.0.0.0-1.x86_64.rpm \
        && alien -i oracle-instantclient-basic-21.1.0.0.0-1.x86_64.rpm \
        && pip install cx_Oracle \
        && pip install boto3==1.17.28 \
        && pip install awswrangler

ENV ORACLE_HOME=/usr/lib/oracle/21/client64
ENV PATH="${PATH}:${ORACLE_HOME}/bin"
ENV PATH="${PATH}:${ORACLE_HOME}/lib"

RUN rm -rf /root/.cachex \
    && rm -rf /boot/.cache/pip \
    && rm -rf ~/.cache/pip