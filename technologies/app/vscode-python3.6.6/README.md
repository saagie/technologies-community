# VS Code

## Description
This directory contains a VsCode server contenairized and customized for Saagie Platform.
See Vscode server official documentation for more information https://code.visualstudio.com/docs/

## How to build in local

```
docker build -t saagie/vscode-<version> .
docker push saagie/vscode-<version>
```

## Job/App specific information
If you want to configure a password to access your VsCode Server, you need to setup an environment Variable named "PASSWORD" and enter your password (see Saagie [documentation](https://docs.saagie.io/user/latest/tutorials/projects-module/projects/envar/index.html#projects-create-envar-global))