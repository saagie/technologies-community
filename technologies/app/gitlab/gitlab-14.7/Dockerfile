FROM gitlab/gitlab-ce:14.7.2-ce.0

USER root

COPY assets/gitlab.rb /tmp/gitlab.rb

EXPOSE 80 22 443
ADD entrypoint.sh /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]