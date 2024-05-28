FROM mathworks/matlab:r2024a

USER root

COPY resources/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
