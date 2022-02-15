# Metabase

![Docker Image Size (tag)](https://img.shields.io/docker/image-size/thomassaagie/gitlab-ce/1.3?label=v14.7%20image%20size&style=for-the-badge)

## Description
This directory contains version of Gitlab CE contenairized and customized for Saagie Platform.

Current restrictions : 
- The Docker images don’t include a mail transport agent (MTA) (see [here](https://docs.gitlab.com/ee/install/docker.html) for more details)
- SSH protocol is not available with Saagie Apps so HTTP must be used when using this App as your Git Repository


## Deployment

Before launching this app, make sure the following environment variables are configured within your project : 
- `GITLAB_INITIAL_ROOT_PASSWORD` = initial password of the `root` user, must be changed after first login
- `SAAGIE_PLATFORM_URL` = e.g. `http://mycompany-workspace.hostname.io` must be specified in order for Gitlab to configure the relative url. 
  - :warning: You must specify a http endpoint and not a https because https will force Gitlab to self register certificates on lets encrypt. 
  - :warning: Do not add a trailing slash in your url. 


## Administration

### User creation
As there is no SMTP server, you don't have the possibility to reset passwords nor create users via the root user.
In order to create a new user, you must activate user self registration (activated by default) and let users self register. Once done, the root user must activate this pending account via the admin `Users` panel.

