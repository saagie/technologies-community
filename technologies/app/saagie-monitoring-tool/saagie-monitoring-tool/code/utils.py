import logging
import traceback
from datetime import datetime
import requests
import urllib3
import psycopg2
import psycopg2.extras
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter

import json
import os

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

postgresql_db = "supervision_pg_db"
postgresql_user = "supervision_pg_user"

saagie_login = os.environ["SAAGIE_SUPERVISION_LOGIN"]
saagie_password = os.environ["SAAGIE_SUPERVISION_PASSWORD"]
saagie_url = os.environ["SAAGIE_URL"]
saagie_realm = os.environ["SAAGIE_REALM"]
saagie_platform = os.environ["SAAGIE_PLATFORM_ID"]

# Workaround for platforms with too many instances
MAX_INSTANCES_FETCHED = os.environ.get("SMT_MAX_INSTANCES_FETCHED", 1000)


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


class ApiUtils(object):

    def __init__(self):
        retry_strategy = Retry(
            total=3,
            status_forcelist=[401],
            backoff_factor=10,
            method_whitelist=["POST", "GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self._session = requests.Session()
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)
        self._session.auth = BearerAuth()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)

    def call_api(self, query):
        """
        Generic function to submit graphql queries to Saagie API
        :param query: GraphQL query to submit
        :return: the API response decoded in JSON
        """
        response = self._session.post(f"{saagie_url}/api/v1/projects/platform/{saagie_platform}/graphql",
                                      json={"query": query}, verify=False)
        return json.loads(response.content.decode("utf-8"))['data']

    def get_projects(self):
        """
           Call Saagie graphql API to get the list of projects
           :return: a JSON containing the project names and ids
           """
        projects_query = "{projects {id name}}"
        projects = self.call_api(projects_query)
        return projects['projects'] if projects else []

    def get_job_instances(self, project_id):
        """
        Call Saagie graphql API to get the jobs of a Saagie project for a given project id
        :param project_id: Saagie Project ID
        :return: a JSON containing a list of jobs
        """
        jobs_query = f"""{{ jobs(projectId: \"{project_id}\" ) {{
                                           id
                                           name
                                           category
                                           countJobInstance
                                           creationDate
                                           technology {{label}}
                                           instances (limit : {MAX_INSTANCES_FETCHED}) {{
                                             id
                                             startTime
                                             endTime
                                             status
                                           }}
                                           }}}}"""
        jobs = self.call_api(jobs_query)
        return jobs['jobs'] if jobs else []

    def get_pipelines(self, project_id):
        """
        Call Saagie graphql API to get the pipelines of a Saagie project for a given project id
        :param project_id: Saagie Project ID
        :return: a JSON containing a list of pipelines
        """
        pipelines_query = f"""{{ pipelines(projectId: \"{project_id}\" ) {{
                                           id
                                           name
                                           instances (limit : {MAX_INSTANCES_FETCHED}) {{
                                             id
                                             startTime
                                             endTime
                                             status
                                           }}
                                           }}}}"""
        pipelines = self.call_api(pipelines_query)
        return pipelines['pipelines'] if pipelines else []

    def get_webapps(self, project_id):
        jobs_query = f"""{{ labWebApps(projectId: \"{project_id}\" ) {{
                                           id
                                           name
                                           countJobInstance
                                           creationDate
                                           technology {{label}}
                                           }}}}"""
        webapps = self.call_api(jobs_query)
        return webapps['labWebApps'] if webapps else []


class DatabaseUtils(object):

    def __init__(self):
        self._db_connection = psycopg2.connect(f"dbname='{postgresql_db}' port='5432' user='{postgresql_user}'")
        self._db_connection.autocommit = True
        self._db_cur = self._db_connection.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is not None:
            traceback.print_exception(exc_type, exc_value, tb)
        self._db_connection.close()

    def truncate_supervision_saagie_pg(self):
        """
        Truncate the supervision_saagie and supervision_saagie_jobs tables
        """
        try:
            self._db_cur.execute('TRUNCATE TABLE supervision_saagie')
            self._db_cur.execute('TRUNCATE TABLE supervision_saagie_jobs')
        except Exception as e:
            logging.error(e)

    def supervision_saagie_to_pg(self, instances):
        """
        Log saagie metrics to PostgresSQL.
        :param instances: List of instances
        :return:
        """
        try:
            psycopg2.extras.execute_batch(self._db_cur, """
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

    def supervision_saagie_jobs_to_pg(self, jobs_or_apps):
        """
        Log saagie jobs metrics to PostgresSQL.
        :param jobs_or_apps: List of jobs or Apps
        :return:
        """

        try:
            psycopg2.extras.execute_batch(self._db_cur, """
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

    def supervision_saagie_jobs_snapshot_to_pg(self, project_id, project_name, job_count):
        """
        Log saagie job daily snapshot count to PostgresSQL.
        :param project_name: Saagie project Name
        :param project_id:Saagie project ID
        :param job_count:# of Saagie jobs and Apps
        :return:
        """
        today = datetime.today().strftime('%Y-%m-%d')
        try:
            self._db_cur.execute(
                '''INSERT INTO supervision_saagie_jobs_snapshot (project_id, project_name, snapshot_date, job_count)
                VALUES(%s,%s,%s,%s)
                ON CONFLICT ON CONSTRAINT supervision_saagie_jobs_snapshot_pkey
                DO
                UPDATE
                SET job_count = EXCLUDED.job_count''',
                (project_id, project_name, today, job_count))
        except Exception as e:
            logging.error(e)

    def supervision_datalake_to_pg(self, supervision_label, supervision_value):
        """
        Log datalake metrics to PostgresSQL.
        :param supervision_label: Label of the metric (e.g. space_used, total_capacity..)
        :param supervision_value: Value in Gigabytes
        :return:
        """

        today = datetime.today().strftime('%Y-%m-%d')
        try:
            self._db_cur.execute(
                '''INSERT INTO supervision_datalake (supervision_date, supervision_label, supervision_value)
                VALUES(%s,%s,%s)
                ON CONFLICT ON CONSTRAINT supervision_datalake_pkey
                DO
                UPDATE
                SET (supervision_label, supervision_value) = (EXCLUDED.supervision_label, EXCLUDED.supervision_value)''',
                (today, supervision_label, supervision_value))
        except Exception as e:
            logging.error(e)


def parse_instance_timestamp(instance_timestamp):
    """
    Parse a timestamp trying 2 different formats
    :param instance_timestamp: Timestamp to parse (string)
    :return: a datetime object
    """
    datetime_format = '%Y-%m-%dT%H:%M:%S.%f%z'
    alternative_datetime_format = '%Y-%m-%dT%H:%M:%S%z'

    if instance_timestamp:
        try:
            return datetime.strptime(instance_timestamp, datetime_format)
        except ValueError:
            return datetime.strptime(instance_timestamp, alternative_datetime_format)
    else:
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
    return f"{saagie_url}projects/platform/{saagie_platform}/project/{project_id}/{orchestration_type}/" \
           f"{job_or_pipeline_id}/instances/{instance_id} "


def bytes_to_gb(size_in_bytes):
    """
    Convert a size in bytes to gigabytes (rounded to 2 decimals)
    :param size_in_bytes: size to convert
    :return: size in gigabytes
    """
    return round(size_in_bytes / 1024 / 1024 / 1024, 2)


def get_hadoop_capacity(hdfs):
    """
    Get Datalake total capacity
    :return: total capacity in GB rounded to 2 decimals
    """
    return bytes_to_gb(hdfs.get_capacity())


def get_hadoop_space_used(hdfs):
    """
    Get Datalake total space used
    :return: total space used in GB rounded to 2 decimals
    """
    return bytes_to_gb(hdfs.get_space_used())
