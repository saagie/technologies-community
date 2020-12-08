import os

# Prevents workers from trying to initialize database and permissions (might lead to race conditions)
os.environ["SUPERSET_UPDATE_PERMS"] = "false"
