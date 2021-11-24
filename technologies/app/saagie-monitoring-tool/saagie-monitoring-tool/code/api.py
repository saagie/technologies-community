import utils

http_session = utils.create_http_session()


def get_hadoop_capacity(hdfs):
    """
    Get Datalake total capacity
    :return: total capacity in GB rounded to 2 decimals
    """
    return utils.bytes_to_gb(hdfs.get_capacity())


def get_hadoop_space_used(hdfs):
    """
    Get Datalake total space used
    :return: total space used in GB rounded to 2 decimals
    """
    return utils.bytes_to_gb(hdfs.get_space_used())


def get_projects():
    """
       Call Saagie graphql API to get the list of projects
       :return: a JSON containing the project names and ids
       """
    projects_query = "{projects {id name}}"
    projects = utils.call_api(projects_query)
    return projects['projects'] if projects else []


def get_job_instances(project_id):
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
                                       instances {{
                                         id
                                         startTime
                                         endTime
                                         status
                                       }}
                                       }}}}"""
    jobs = utils.call_api(jobs_query)
    return jobs['jobs'] if jobs else []


def get_apps_and_pipelines(project_id):
    """
    Call Saagie graphql API to get the pipelines and apps of a Saagie project for a given project id
    :param project_id: Saagie Project ID
    :return: a JSON containing two lists :pipelines and apps
    """
    apps_and_pipelines_query = f"""{{ project(id: \"{project_id}\" ) {{
                                       apps {{
                                            id
                                            name
                                            creationDate
                                            technology {{label}}
                                        }}
                                     pipelines {{
                                        id
                                        name
                                        instances {{
                                            id
                                            startTime
                                            endTime
                                            status
                                       }}
                                    }}
                               }}}}"""
    apps_and_pipelines = utils.call_api(apps_and_pipelines_query)
    return apps_and_pipelines['project'] if apps_and_pipelines else {}
