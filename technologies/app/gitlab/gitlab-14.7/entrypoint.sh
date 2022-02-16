#!/bin/bash
set -xeuo pipefail

export GITLAB_LOG_LEVEL="warn"
yes | cp -f /tmp/gitlab.rb /etc/gitlab/gitlab.rb

/assets/wrapper #> /dev/null