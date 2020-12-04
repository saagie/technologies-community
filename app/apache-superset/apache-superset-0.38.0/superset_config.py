import os

# Default cache for Superset objects
#CACHE_CONFIG: CacheConfig = {"CACHE_TYPE": "filesystem"}

SQLALCHEMY_DATABASE_URI = "sqlite:////var/lib/superset/superset.db"

# Cache for datasource metadata and query results
#DATA_CACHE_CONFIG: CacheConfig = {"CACHE_TYPE": "filesystem"}

