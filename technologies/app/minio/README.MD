# Minio

MinIO is a High Performance Object Storage released under GNU Affero General Public License v3.0.
It is API compatible with Amazon S3 cloud storage service.
Use MinIO to build high performance infrastructure for machine learning, analytics and application data workloads.

## Deployment

For this app to function properly,
make sure the following environment variables are configured in the app environment variables:

- `MINIO_BROWSER_REDIRECT_URL` : The external URL to access the console.
To obtain this variable, run the app inside Saagie, then in the Overview page, under the paragraph "HTTP ports",
copy the external url of the port 9001. Once the variable is created, restart the app.

- `MINIO_ROOT_USER` : The username of the root user.

- `MINIO_ROOT_PASSWORD` : The password of the root user.
