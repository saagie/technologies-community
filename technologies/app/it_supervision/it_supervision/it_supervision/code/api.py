import utils
import os
import pyarrow as pa

http_session = utils.create_http_session()
hdfs = pa.hdfs.connect(os.environ["IP_HDFS"], port=8020, user="hdfs")


def get_hadoop_capacity():
    """
    Get Datalake total capacity
    :return: total capacity in GB rounded to 2 decimals
    """
    return utils.bytes_to_gb(hdfs.get_capacity())


def get_hadoop_space_used():
    """
    Get Datalake total space used
    :return: total space used in GB rounded to 2 decimals
    """
    return utils.bytes_to_gb(hdfs.get_space_used())


def get_hadoop_space_used_by_use_case():
    """
    Get Datalake space used for each folder in /data (corresponding to a use case)
    :return: dict of total space used in GB rounded to 2 decimals, for each use case
    """
    result = {}
    for path in hdfs.ls("/data"):
        result[path] = get_hadoop_space_used_by_path(path)
    return result


def get_hadoop_space_used_by_path(path):
    """
    Get Datalake space used  for a given folder
    :param path: HDFS Path to gather usage
    :return: dict of total space used in GB rounded to 2 decimals, for this path
    """
    return utils.bytes_to_gb(hdfs.disk_usage(path))


def get_projects():
    """
       Call Saagie graphql API to get the list of projects
       :return: a JSON containing the project names and ids
       """
    projects_query = "{projects {id name}}"
    projects = utils.call_api(projects_query)
    return projects['projects']


def get_project_name(project_id):
    """
    Call Saagie graphql API to get the name of the Saagie project for a given project id
    :param project_id: Saagie Project ID
    :return: a JSON containing the project name
    """
    project_query = f"""{{ project(id: \"{project_id}\" ) {{
                                       name
                                       }}}}"""
    project = utils.call_api(project_query)
    return project['project']


def get_job_instances(project_id):
    """
    Call Saagie graphql API to get the jobs of a Saagie project for a given project id
    :param project_id: Saagie Project ID
    :return: a JSON containing a list of jobs
    """
    jobs_query = f"""{{ jobs(projectId: \"{project_id}\" ) {{
                                       id
                                       name
                                       instances {{
                                         id
                                         startTime
                                         endTime
                                         status
                                       }}
                                       }}}}"""
    jobs = utils.call_api(jobs_query)
    return jobs['jobs']


def get_pipelines(project_id):
    """
    Call Saagie graphql API to get the pipelines of a Saagie project for a given project id
    :param project_id: Saagie Project ID
    :return: a JSON containing a list of pipelines
    """
    pipelines_query = f"""{{ pipelines(projectId: \"{project_id}\" ) {{
                                       id
                                       name
                                       instances {{
                                         id
                                         startTime
                                         endTime
                                         status
                                       }}
                                       }}}}"""
    pipelines = utils.call_api(pipelines_query)
    return pipelines['pipelines']


def get_jobs(project_id):
    jobs_query = f"""{{ jobs(projectId: \"{project_id}\" ) {{
                                       id
                                       name
                                       category
                                       countJobInstance
                                       creationDate
                                       technology {{label}}
                                       }}}}"""
    jobs = utils.call_api(jobs_query)
    return jobs['jobs']


def get_webapps(project_id):
    jobs_query = f"""{{ labWebApps(projectId: \"{project_id}\" ) {{
                                       id
                                       name
                                       countJobInstance
                                       creationDate
                                       technology {{label}}
                                       }}}}"""
    webapps = utils.call_api(jobs_query)
    return webapps['labWebApps']
