import logging
from datetime import datetime
import requests
import urllib3
import psycopg2
import psycopg2.extras
import json
from json import JSONDecodeError
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'
ALTERNATIVE_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

postgre_db = "supervision_pg_db"
postgre_user = "supervision_pg_user"

saagie_login = os.environ["SAAGIE_SUPERVISION_LOGIN"]
saagie_password = os.environ["SAAGIE_SUPERVISION_PASSWORD"]
saagie_url = os.environ["SAAGIE_URL"]
saagie_realm = os.environ["SAAGIE_REALM"]
saagie_platform = os.environ["SAAGIE_PLATFORM_ID"]


def parse_instance_timestamp(instance_timestamp):
    """
    Parse a timestamp trying 2 different formats
    :param instance_timestamp: Timestamp to parse (string)
    :return: a datetime object
    """
    try:
        return datetime.strptime(instance_timestamp, DATETIME_FORMAT)
    except ValueError:
        return datetime.strptime(instance_timestamp, ALTERNATIVE_DATETIME_FORMAT)
    except:
        return None


def build_saagie_url(project_id, orchestration_type, job_or_pipeline_id, instance_id):
    """
    Build the Saagie URL of a job or pipeline instance
    :param instance_id: id of the Saagie instance
    :param job_or_pipeline_id: if of the job or the pipeline
    :param orchestration_type: job or pipeline
    :param project_id: Saagie Project ID
    :return: the complete URL of this instance
    """
    return f"{saagie_url}projects/platform/{saagie_platform}/project/{project_id}/{orchestration_type}/{job_or_pipeline_id}/instances/{instance_id} "


def bytes_to_gb(size_in_bytes):
    """
    Convert a size in bytes to gigabytes (rounded to 2 decimals)
    :param size_in_bytes: size to convert
    :return: size in gigabytes
    """
    return round(size_in_bytes / 1024 / 1024 / 1024, 2)


def create_http_session():
    """
    Create a HTTP session
    :return: a requests Session
    """
    s = requests.Session()
    s.verify = False
    return s


def connect_to_pg():
    """
    Connect to PostgreSQL lcbft database
    :return: a Postgresql connection
    """
    conn_string = "dbname='{}' port='{}' user='{}'" \
        .format(postgre_db, "5432", postgre_user)
    return psycopg2.connect(conn_string)


def truncate_supervision_saagie_pg():
    """
    Truncate the supervision_saagie and supervision_saagie_jobs tables
    """
    connection = None
    cursor = None
    try:
        connection = connect_to_pg()
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute('TRUNCATE TABLE supervision_saagie')
        cursor.execute('TRUNCATE TABLE supervision_saagie_jobs')
    except Exception as e:
        logging.error(e)
    finally:
        if connection:
            cursor.close()
            connection.close()


def supervision_saagie_to_pg(instances):
    """
    Log saagie metrics to PostgresSQL.
    :param instances: List of instances
    :return:
    """
    connection = None
    cursor = None
    try:
        connection = connect_to_pg()
        connection.autocommit = True
        cursor = connection.cursor()

        psycopg2.extras.execute_batch(cursor, """
            INSERT INTO supervision_saagie (
                supervision_timestamp, 
                project_id, 
                project_name, 
                orchestration_type, 
                orchestration_id,
                orchestration_name, 
                instance_id, 
                instance_start_time,
                instance_end_time,
                instance_status,
                instance_duration,
                instance_saagie_url)
            VALUES (
                %(supervision_timestamp)s, 
                %(project_id)s, 
                %(project_name)s, 
                %(orchestration_type)s, 
                %(orchestration_id)s,
                %(orchestration_name)s, 
                %(instance_id)s, 
                %(instance_start_time)s,
                %(instance_end_time)s,
                %(instance_status)s,
                %(instance_duration)s,
                %(instance_saagie_url)s
            );
            """, instances)

    except Exception as e:
        logging.error(e)
    finally:
        if connection:
            cursor.close()
            connection.close()


def supervision_saagie_jobs_to_pg(jobs_or_apps):
    """
    Log saagie jobs metrics to PostgresSQL.
    :param jobs_or_apps: List of jobs or Apps
    :return:
    """

    connection = None
    cursor = None
    try:
        connection = connect_to_pg()
        connection.autocommit = True
        cursor = connection.cursor()
        psycopg2.extras.execute_batch(cursor, """
               INSERT INTO supervision_saagie_jobs (
                   project_id, 
                   project_name, 
                   orchestration_type, 
                   orchestration_id, 
                   orchestration_name,
                   orchestration_category, 
                   creation_date, 
                   instance_count,
                   technology)
                   VALUES (
                   %(project_id)s, 
                   %(project_name)s, 
                   %(orchestration_type)s, 
                   %(orchestration_id)s, 
                   %(orchestration_name)s,
                   %(orchestration_category)s, 
                   %(creation_date)s, 
                   %(instance_count)s,
                   %(technology)s
               );
               """, jobs_or_apps)
    except Exception as e:
        logging.error(e)
    finally:
        if connection:
            cursor.close()
            connection.close()


def supervision_saagie_jobs_snapshot_to_pg(project_id, project_name, job_count):
    """
    Log saagie job daily snapshot count to PostgresSQL.
    :param project_name: Saagie project Name
    :param project_id:Saagie project ID
    :param job_count:# of Saagie jobs and Apps
    :return:
    """
    today = datetime.today().strftime('%Y-%m-%d')
    connection = None
    cursor = None
    try:
        connection = connect_to_pg()
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(
            '''INSERT INTO supervision_saagie_jobs_snapshot (project_id, project_name, snapshot_date, job_count)
            VALUES(%s,%s,%s,%s)
            ON CONFLICT ON CONSTRAINT supervision_saagie_jobs_snapshot_pkey
            DO
            UPDATE
            SET job_count = EXCLUDED.job_count''',
            (project_id, project_name, today, job_count))
    except Exception as e:
        logging.error(e)
    finally:
        if connection:
            cursor.close()
            connection.close()


def supervision_datalake_to_pg(supervision_label, supervision_value):
    """
    Log datalake metrics to PostgresSQL.
    :param supervision_label: Label of the metric (e.g. space_used, total_capacity..)
    :param supervision_value: Value in GibaBytes
    :return:
    """

    today = datetime.today().strftime('%Y-%m-%d')
    connection = None
    cursor = None
    try:
        connection = connect_to_pg()
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(
            '''INSERT INTO supervision_datalake (supervision_date, supervision_label, supervision_value)
            VALUES(%s,%s,%s)
            ON CONFLICT ON CONSTRAINT supervision_datalake_pkey
            DO
            UPDATE
            SET (supervision_label, supervision_value) = (EXCLUDED.supervision_label, EXCLUDED.supervision_value)''',
            (today, supervision_label, supervision_value))
    except Exception as e:
        logging.error(e)
    finally:
        if connection:
            cursor.close()
            connection.close()


class BearerAuth(requests.auth.AuthBase):
    def __init__(self):
        self.token = authenticate()

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r


def authenticate():
    """
   Function to authenticate to Saagie given credentials in environment variables
   :return: THE API response containing the Bearer Token
   """
    s = requests.session()
    s.headers["Content-Type"] = "application/json"
    s.headers["Saagie-Realm"] = saagie_realm
    r = s.post(saagie_url + '/authentication/api/open/authenticate',
               json={'login': saagie_login, 'password': saagie_password})
    return r.text


auth = BearerAuth()


def call_api(query):
    """
    Generic function to submit graphgql queries to Saagie API
    :param query: GraphQL query to submit
    :return: the API response decoded in JSON
    """
    attempts = 0
    response = {}
    while attempts < 3:
        try:
            data = requests.post(f"{saagie_url}/api/v1/projects/platform/{saagie_platform}/graphql",
                                 auth=auth, json={"query": query},
                                 verify=False).content.decode("utf-8")
            response = json.loads(
                data)['data']
            break
        except JSONDecodeError:
            attempts += 1
    return response
