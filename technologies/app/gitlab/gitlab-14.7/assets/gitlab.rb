external_url ENV["SAAGIE_PLATFORM_URL"].to_s + ENV["GITLAB_RELATIVE_URL"].to_s

registry['log_level'] = 'warn'
gitlab_shell['log_level'] = 'warn'
gitaly['logging_level'] = 'warn'

letsencrypt['enable'] = false

gitlab_rails['initial_root_password'] = ENV["GITLAB_INITIAL_ROOT_PASSWORD"].to_s

# Disable the bundled Omnibus provided PostgreSQL
#postgresql['enable'] = false
#https://docs.gitlab.com/ee/install/requirements.html#database
# PostgreSQL connection details
#gitlab_rails['db_adapter'] = 'postgresql'
#gitlab_rails['db_encoding'] = 'unicode'
#gitlab_rails['db_host'] = '10.1.0.5' # IP/hostname of database server
#gitlab_rails['db_password'] = 'DB password'