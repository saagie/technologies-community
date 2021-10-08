#DROP table supervision_saagie;

CREATE TABLE supervision_saagie (
    supervision_timestamp TIMESTAMP,
    project_id       varchar(60),
    project_name         VARCHAR(60),
    orchestration_type         VARCHAR(10),
    orchestration_id   VARCHAR(60),
    orchestration_name        VARCHAR(60),
    instance_id         VARCHAR(60) PRIMARY KEY,
    instance_start_time TIMESTAMP,
    instance_end_time TIMESTAMP,
    instance_status VARCHAR(30),
    instance_duration BIGINT,
    instance_saagie_url VARCHAR(200)
);

#DROP table supervision_saagie_jobs;

CREATE TABLE supervision_saagie_jobs (
project_id       varchar(60),
    project_name         VARCHAR(60),
    creation_date TIMESTAMP,
    orchestration_type         VARCHAR(10),
    orchestration_category         VARCHAR(60),
    orchestration_id   VARCHAR(60)  PRIMARY KEY,
    orchestration_name        VARCHAR(60),
    instance_count         INT,
    technology VARCHAR(60)
);

#DROP table supervision_saagie_jobs_snapshot;

CREATE TABLE supervision_saagie_jobs_snapshot (
	project_id       varchar(60),
    project_name         VARCHAR(60),
    snapshot_date DATE,
    job_count INT,
    PRIMARY KEY (snapshot_date, project_id)
);


#DROP table supervision_datalake;

CREATE TABLE supervision_datalake (
    supervision_date DATE,
    supervision_label varchar(60),
    supervision_value NUMERIC(20,2),
PRIMARY KEY (supervision_date, supervision_label)
);
