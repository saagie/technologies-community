FROM openjdk:8-jre

#AWS CLI needed when application.yml is stored on S3
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" \
    && unzip awscliv2.zip \
    && ./aws/install

RUN mkdir -p /opt/shinyproxy/

COPY shinyproxy-2.4.3-saagie.jar /opt/shinyproxy/shinyproxy.jar
COPY run-app.sh /opt/shinyproxy/
COPY templates /opt/shinyproxy/templates
COPY application.yml /opt/shinyproxy/application.yml

EXPOSE 8080
WORKDIR /opt/shinyproxy/
ENTRYPOINT ["sh", "/opt/shinyproxy/run-app.sh"]