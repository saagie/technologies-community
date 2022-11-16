FROM tsl0922/ttyd:1.7.2

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y \
    wget \
    curl \
    vim \
    openjdk-11-jdk \
    nano \
    ca-certificates-java \
    bzip2 \
    software-properties-common \
    ftp \
    git \
    unzip \
    python3-dev \
    libpq-dev \
    gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN update-ca-certificates -f;

ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/

# Python (Vanilla)
RUN add-apt-repository ppa:deadsnakes/ppa \
    && apt-get update \
    && apt install -y python3.9 \
    && ln -s /usr/bin/python3 /usr/bin/python \
    && apt-get install -y python3-pip

#AWS CLI
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install

#PostgreSQL
RUN apt-get update \
    && apt-get install -y postgresql postgresql-contrib

CMD ["ttyd", "bash"]
