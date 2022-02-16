#!/bin/bash
set -xeuo pipefail
echo "_____________________________________________________________________________________________________"
echo "Gitlab is initializing, it can take a few minute for the service to be up and running, please wait..."
echo "_____________________________________________________________________________________________________"

export GITLAB_LOG_LEVEL="warn"
cp /tmp/gitlab.rb /etc/gitlab/gitlab.rb

/assets/wrapper > /dev/null