# Neo4j
## Description
Neo4j gives developers and data scientists the most trusted and advanced tools to quickly build today’s intelligent applications and machine learning workflows. Available as a fully managed cloud service or self-hosted.

## How to build in local

```
docker build -t saagie/neo4j .
docker push saagie/neo4j
```

## Run Neo4j container  
  
Default Neo4j admin user is:  
login: neo4j  
password: test  
  
Note that the login cannot be set to another value, it must be 'neo4j'.  
The password can be set to another value (See all information about environement variable 'NEO4J_PASSWORD' below)

### On Saagie's Platform  

This container is designed to run on Saagie platform.  

The official documentation is available here: [Saagie's official documentation](https://docs.saagie.io/product/latest/sdk/index.html).  

### On premise / your local server

It's possible (mainly for development and testing) to run this image outside of a Saagie platform.
Please note that Saagie cannot provide any support for images launched outside its platform.

Run:
```
docker run -e "SAAGIE_BASE_PATH=/test" -p 80:80 -p 7687:7687 saagie/neo4j:4-4-3
```
And access it with this adress: [localhost/test/](localhost/test/)

- `SAAGIE_BASE_PATH` variable is **mandatory** and should be equal to / . It's used to customize the path to the application when behind a reverse proxy.  
- `NEO4J_PASSWORD` is optional and defaulted to 'test', it allows you to change the password of the Neo4j admin user (the login cannot be must be 'neo4j').  
