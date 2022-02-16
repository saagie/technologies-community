#!/bin/bash
set -euo pipefail


if [[ -z "${GITLAB_INITIAL_ROOT_PASSWORD}" ]]; then
  echo "ERROR : GITLAB_INITIAL_ROOT_PASSWORD environment variable must be set"
  echo "Usage : GITLAB_INITIAL_ROOT_PASSWORD = initial password of the root user, must be changed after first login"
  exit 1
elif [[ -z "${SAAGIE_PLATFORM_URL}" ]]; then
  echo "ERROR : SAAGIE_PLATFORM_URL environment variable must be set"
  echo "Usage : SAAGIE_PLATFORM_URL = must be specified in order for Gitlab to configure the relative url"
  exit 1
else
  echo "_____________________________________________________________________________________________________"
  echo "Gitlab is initializing, it can take a few minute for the service to be up and running, please wait..."
  echo "_____________________________________________________________________________________________________"
  export GITLAB_LOG_LEVEL="warn"
  cp /tmp/gitlab.rb /etc/gitlab/gitlab.rb

  /assets/wrapper > /dev/null
fi

