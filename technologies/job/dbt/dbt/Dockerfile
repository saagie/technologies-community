FROM python:3.8.12

# Update and install system packages
RUN apt-get update -y && \
  apt-get install --no-install-recommends -y -q \
    git  \
    libpq-dev  \
    python-dev  \
    python3-pip && \
    apt-get clean && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install DBT
RUN pip install --upgrade pip wheel setuptools &&  \
    pip install  \
    cffi  \
    cryptography~=3.4 \
    dbt-core \
    dbt-postgres \
    dbt-redshift \
    dbt-snowflake \
    dbt-bigquery &&  \
    rm -rf /root/.cachex && \
    rm -rf /boot/.cache/pip && \
    rm -rf ~/.cache/pip

# Move scripts and frequently changing directive to the end of the build
COPY resources/entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

WORKDIR /sandbox

ENTRYPOINT  ["bash","/entrypoint.sh"]