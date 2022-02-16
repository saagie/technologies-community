#External URL to use on Saagie
external_url ENV["SAAGIE_PLATFORM_URL"].to_s + ENV["GITLAB_RELATIVE_URL"].to_s

#Lower log level
registry['log_level'] = 'warn'
gitlab_shell['log_level'] = 'warn'
gitaly['logging_level'] = 'warn'

#Disable Grafana and Prometheus to optimize Gitlab performance
grafana['enable'] = false
prometheus_monitoring['enable'] = false


#Initial root password is set with an environment variable in your Saagie project
gitlab_rails['initial_root_password'] = ENV["GITLAB_INITIAL_ROOT_PASSWORD"].to_s