FROM mcr.microsoft.com/powershell:ubuntu-22.04

ENV POWERSHELL_TELEMETRY_OPTOUT="1"

COPY resources/entrypoint.sh /entrypoint.sh
RUN chmod 755 /entrypoint.sh

WORKDIR /sandbox

CMD ["/bin/bash", "-c", "/entrypoint.sh"]
