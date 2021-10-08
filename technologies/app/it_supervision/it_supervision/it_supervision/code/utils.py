from datetime import datetime
import requests
import urllib3
import psycopg2
from psycopg2.extensions import AsIs
import json
from json import JSONDecodeError
import logging
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%f%z'
ALTERNATIVE_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

SUPERVISION_SAAGIE_PG_TABLE = os.environ["SUPERVISION_SAAGIE_PG_TABLE"]
SUPERVISION_SAAGIE_JOBS_PG_TABLE = os.environ["SUPERVISION_SAAGIE_JOBS_PG_TABLE"]
SUPERVISION_SAAGIE_JOBS_SNAPSHOT_PG_TABLE = os.environ["SUPERVISION_SAAGIE_JOBS_SNAPSHOT_PG_TABLE"]
SUPERVISION_DATALAKE_PG_TABLE = os.environ["SUPERVISION_DATALAKE_PG_TABLE"]

postgre_db = os.environ["SUPERVISION_PG_DB"]
postgre_user = os.environ['SUPERVISION_PG_USER']

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
        cursor.execute(f'TRUNCATE TABLE {SUPERVISION_SAAGIE_PG_TABLE}')
        cursor.execute(f'TRUNCATE TABLE {SUPERVISION_SAAGIE_JOBS_PG_TABLE}')
    except:
        logging.error("Unable to connect to Postgres")
    finally:
        if connection:
            cursor.close()
            connection.close()


def supervision_saagie_to_pg(project_id, project_name, orchestration_type, orchestration_id, orchestration_name,
                             instance_id, instance_start_time,
                             instance_end_time,
                             instance_status, instance_duration, instance_saagie_url):
    """
    Log saagie metrics to PostgresSQL.
    :param instance_duration: Duration of the instance
    :param instance_status: Status of the instance
    :param instance_end_time: End time of the instance
    :param instance_start_time: Start time of the instance
    :param instance_id: Saagie instance ID
    :param orchestration_id:job or pipeline id
    :param orchestration_name:job or pipeline name
    :param orchestration_type: job or pipeline
    :param instance_saagie_url: link on Saagie
    :param project_name: Saagie project Name
    :param project_id:Saagie project ID
    :return:
    """

    now = datetime.now()
    connection = None
    cursor = None
    #try:
    connection = connect_to_pg()
    connection.autocommit = True
    cursor = connection.cursor()
    logging.debug('''INSERT INTO %s (supervision_timestamp, project_id, project_name, orchestration_type, orchestration_id,
        orchestration_name, instance_id, instance_start_time,instance_end_time,instance_status,instance_duration,
        instance_saagie_url)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''' % (SUPERVISION_SAAGIE_PG_TABLE, now, project_id, project_name, orchestration_type, orchestration_id,
            orchestration_name, instance_id, instance_start_time, instance_end_time, instance_status,
            instance_duration,
            instance_saagie_url))
    cursor.execute(
        '''INSERT INTO %s (supervision_timestamp, project_id, project_name, orchestration_type, orchestration_id,
        orchestration_name, instance_id, instance_start_time,instance_end_time,instance_status,instance_duration,
        instance_saagie_url)
        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
        (AsIs(SUPERVISION_SAAGIE_PG_TABLE), now, project_id, project_name, orchestration_type, orchestration_id,
            orchestration_name, instance_id, instance_start_time, instance_end_time, instance_status,
            instance_duration,
            instance_saagie_url))

    #except:
    #    logging.error("Unable to connect to Postgres")
    #finally:
    #    if connection:
    cursor.close()
    connection.close()


def supervision_saagie_jobs_to_pg(project_id, project_name, orchestration_type, orchestration_id, orchestration_name,
                                  orchestration_category, creation_date,
                                  instance_count,
                                  technology):
    """
    Log saagie jobs metrics to PostgresSQL.
    :param orchestration_category: Saagie category (Extraction, Processing..)
    :param creation_date: Creation date of the job or the app
    :param instance_count: # of instances
    :param technology: Technology of the jbo or the app
    :param orchestration_id:job or app id
    :param orchestration_name:job or app name
    :param orchestration_type: job or app
    :param project_name: Saagie project Name
    :param project_id:Saagie project ID
    :return:
    """

    connection = None
    cursor = None
    try:
        connection = connect_to_pg()
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(
            '''INSERT INTO %s (project_id, project_name, orchestration_type, orchestration_id,
             orchestration_name, orchestration_category, creation_date, instance_count, technology)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
            (AsIs(SUPERVISION_SAAGIE_JOBS_PG_TABLE), project_id, project_name, orchestration_type, orchestration_id,
             orchestration_name, orchestration_category, creation_date, instance_count, technology))

    except:
        logging.error("Unable to connect to Postgres")
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
            '''INSERT INTO %s (project_id, project_name, snapshot_date, job_count)
            VALUES(%s,%s,%s,%s)
            ON CONFLICT ON CONSTRAINT supervision_saagie_jobs_snapshot_pkey
            DO
            UPDATE
            SET job_count = EXCLUDED.job_count''',
            (AsIs(SUPERVISION_SAAGIE_JOBS_SNAPSHOT_PG_TABLE), project_id, project_name, today, job_count))
    except:
        logging.error("Unable to connect to Postgres")
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
        logging.debug("Starting execute request supervision_datalake_to_pg")
        logging.debug(f"Values : {today}, {supervision_label}, {supervision_value}")
        cursor.execute(
            '''INSERT INTO %s (supervision_date, supervision_label, supervision_value)
            VALUES(%s,%s,%s)
            ON CONFLICT ON CONSTRAINT supervision_datalake_pkey
            DO
            UPDATE
            SET (supervision_label, supervision_value) = (EXCLUDED.supervision_label, EXCLUDED.supervision_value)''',
            (AsIs(SUPERVISION_DATALAKE_PG_TABLE), today, supervision_label, supervision_value))
        logging.debug("Ending execute request supervision_datalake_to_pg")
    except:
        logging.error("Unable to connect to Postgres")
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
                                 auth=BearerAuth(), json={"query": query},
                                 verify=False).content.decode("utf-8")
            response = json.loads(
                data)['data']

            break
        except JSONDecodeError:
            attempts += 1
    return response


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
