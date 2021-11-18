import utils
import api
import logging
import sys
import os
import pyarrow as pa

monitoring_type = os.environ["MONITORING_OPT"]


def get_datalake_metrics():
    """
    Fetch Metrics from Hadoop API about Datalake usage and save it to PostgreSQL in the supervision Database
    :return:
    """
    hdfs = pa.hdfs.connect(os.environ["IP_HDFS"], port=8020, user="hdfs")
    total_capacity = api.get_hadoop_capacity(hdfs)
    total_space_used = api.get_hadoop_space_used(hdfs)
    logging.debug(f"total_capacity : {total_capacity}")
    logging.debug(f"total_space_used : {total_space_used}")
    utils.supervision_datalake_to_pg("total_capacity", total_capacity)
    utils.supervision_datalake_to_pg("total_used", total_space_used)


def get_saagie_metrics():
    """
    Fetch Metrics Saagie API about Jobs and instances and save it to PostgreSQL in the supervision Database
    :return:
    """
    logging.debug("truncate_supervision_saagie_pg starting")
    utils.truncate_supervision_saagie_pg()
    logging.debug("truncate_supervision_saagie_pg finished")
    get_saagie_instance_metrics()
    get_saagie_jobs_metrics()


def get_saagie_instance_metrics():
    """
    Fetch Metrics from Saagie API about Jobs and Pipelines duration and status and save it to PostgreSQL in the supervision Database
    :return:
    """
    utils.truncate_supervision_saagie_pg()
    for project_id in [p["id"] for p in api.get_projects()]:
        project_name = api.get_project_name(project_id)["name"]
        logging.debug(f"Getting metrics for project {project_name}")
        for job in api.get_job_instances(project_id):
            for instance in job["instances"]:
                log_instance_metrics(instance, job, "job", project_id, project_name)
        for pipeline in api.get_pipelines(project_id):
            for instance in pipeline["instances"]:
                log_instance_metrics(instance, pipeline, "pipeline", project_id, project_name)


def get_saagie_jobs_metrics():
    """
    Fetch Metrics from Saagie API about Jobs metadata and save it to PostgreSQL in the supervision Database
    :return:
    """
    project_list = api.get_projects()
    for project in project_list:
        job_list = api.get_jobs(project["id"])
        app_list = api.get_webapps(project["id"])
        for job in job_list:
            logging.debug(f"Current job : {job}")
            utils.supervision_saagie_jobs_to_pg(project["id"], project["name"], "job", job["id"], job["name"],
                                                job["category"], job["creationDate"], job["countJobInstance"],
                                                job["technology"]["label"] if job["technology"] != None else None)
        for app in app_list:
            logging.debug(f"Current app : {app}")
            utils.supervision_saagie_jobs_to_pg(project["id"], project["name"], "app", app["id"], app["name"],
                                                "WebApp", app["creationDate"], app["countJobInstance"],
                                                app["technology"]["label"] if app["technology"] != None else None)
        utils.supervision_saagie_jobs_snapshot_to_pg(project["id"], project["name"], len(job_list) + len(app_list))


def log_instance_metrics(instance, job_or_pipeline, orchestration_type, project_id, project_name):
    """
    For each instance of a job or a pipeline, compute its duration and its Saagie URL and save it to PostgreSQL
    in the supervision Database
    :param instance: instance object returned from Saagie API
    :param job_or_pipeline: job_or_pipeline object returned from Saagie API
    :param orchestration_type: indicating whether its a job or a pipeline
    :param project_id: Saagie Project ID
    :param project_name: Saagie Project Name
    :return:
    """
    instance_start_time = utils.parse_instance_timestamp(instance["startTime"])
    instance_end_time = utils.parse_instance_timestamp(instance["endTime"])
    if instance_end_time and instance_end_time:
        instance_duration = (instance_end_time - instance_start_time).total_seconds() * 1000
        instance_saagie_url = utils.build_saagie_url(project_id, orchestration_type, job_or_pipeline["id"],
                                                     instance["id"])

        utils.supervision_saagie_to_pg(project_id, project_name, orchestration_type, job_or_pipeline["id"],
                                       job_or_pipeline["name"], instance["id"], instance["startTime"],
                                       instance["endTime"],
                                       instance["status"], instance_duration, instance_saagie_url)
    else:
        return


def main():
    if monitoring_type == "SAAGIE":
        logging.info("Get saagie metrics")
        get_saagie_metrics()
    elif monitoring_type == "SAAGIE_AND_DATALAKE":
        logging.info("Get saagie metrics")
        get_saagie_metrics()
        logging.info("Get datalake metrics starting")
        get_datalake_metrics()
    else:
        logging.error("MONITORING_OPT wrong or missing, correct options are : 'SAAGIE' or 'SAAGIE_AND_DATALAKE'")
        sys.exit(1)


if __name__ == "__main__":
    logger = logging.getLogger("saagie-monitoring-tool")

    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %H:%M:%S")
    main()
