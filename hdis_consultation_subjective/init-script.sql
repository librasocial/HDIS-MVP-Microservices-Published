CREATE TABLE IF NOT EXISTS consultation_subjective.speciality_type (
    code INT PRIMARY KEY NOT NULL,
    name VARCHAR(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/CD05.011_medical_speciality_type_values.csv'
INTO TABLE consultation_subjective.speciality_type
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 LINES
(code, name);


CREATE TABLE IF NOT EXISTS consultation_subjective.allergy_product (
    code VARCHAR(2) PRIMARY KEY NOT NULL,
    description VARCHAR(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Allergy Product CD05_018.csv'
INTO TABLE consultation_subjective.allergy_product
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(code, description);


CREATE TABLE IF NOT EXISTS consultation_subjective.body_site (
    code VARCHAR(2) PRIMARY KEY NOT NULL,
    name VARCHAR(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Body Site CD05_026.csv'
INTO TABLE consultation_subjective.body_site
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(code, name);


CREATE TABLE IF NOT EXISTS consultation_subjective.body_site_examination (
    code VARCHAR(10)  NOT NULL,
    name VARCHAR(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Body Site Examination.csv'
INTO TABLE consultation_subjective.body_site_examination
CHARACTER SET utf8
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(code, name);


CREATE TABLE IF NOT EXISTS consultation_subjective.body_site_loinc (
    code VARCHAR(12) PRIMARY KEY NOT NULL,
    name VARCHAR(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/bodySite LOINC.csv'
INTO TABLE consultation_subjective.body_site_loinc
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(code, name);


CREATE TABLE IF NOT EXISTS consultation_subjective.clinical_document_type (
    code INT PRIMARY KEY NOT NULL,
    name VARCHAR(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Clinical Document Type CD05_046.csv'
INTO TABLE consultation_subjective.clinical_document_type
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(code, name);


CREATE TABLE IF NOT EXISTS consultation_subjective.examination_type (
    code VARCHAR(2) PRIMARY KEY NOT NULL,
    description VARCHAR(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Examination Type CD05_061.csv'
INTO TABLE consultation_subjective.examination_type
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(code, description);


CREATE TABLE IF NOT EXISTS consultation_subjective.family_member_relationship (
    code VARCHAR(2) PRIMARY KEY NOT NULL,
    name VARCHAR(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Family Member Relationship CD05_06.csv'
INTO TABLE consultation_subjective.family_member_relationship
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(code, name);


CREATE TABLE IF NOT EXISTS consultation_subjective.health_condition (
    code VARCHAR(3) PRIMARY KEY NOT NULL,
    name VARCHAR(250) NOT NULL,
    description VARCHAR(250),
    type_id VARCHAR(3)  NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Health Condition CD05_019.csv'
INTO TABLE consultation_subjective.health_condition
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(code, name, description, type_id);


CREATE TABLE IF NOT EXISTS consultation_subjective.health_condition_status (
    code VARCHAR(2) PRIMARY KEY NOT NULL,
    description VARCHAR(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Health Condition Status CD05_021.csv'
INTO TABLE consultation_subjective.health_condition_status
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(code, description);


CREATE TABLE IF NOT EXISTS consultation_subjective.health_condition_type (
    code VARCHAR(2) PRIMARY KEY NOT NULL,
    name VARCHAR(128) NOT NULL,
    icd_code_range VARCHAR(7) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Health Condition Type CD05_022.csv'
INTO TABLE consultation_subjective.health_condition_type
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(code, name, icd_code_range);


CREATE TABLE IF NOT EXISTS consultation_subjective.medication_frequency (
    code VARCHAR(4) PRIMARY KEY NOT NULL,
    description VARCHAR(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Medication Frequency CD05_023.csv'
INTO TABLE consultation_subjective.medication_frequency
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(code, description);


CREATE TABLE IF NOT EXISTS consultation_subjective.order_status (
    code VARCHAR(2) PRIMARY KEY NOT NULL,
    name VARCHAR(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Order Status CD05_121.csv'
INTO TABLE consultation_subjective.order_status
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(code, name);


CREATE TABLE IF NOT EXISTS consultation_subjective.organ_system (
    code VARCHAR(2) PRIMARY KEY NOT NULL,
    name VARCHAR(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Organ System CD05_033.csv'
INTO TABLE consultation_subjective.organ_system
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(code, name);


CREATE TABLE IF NOT EXISTS consultation_subjective.severity_code (
    code VARCHAR(2) PRIMARY KEY NOT NULL,
    description VARCHAR(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Severity Code CD05_020.csv'
INTO TABLE consultation_subjective.severity_code
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(code, description);


CREATE TABLE IF NOT EXISTS consultation_subjective.unit_of_measurement (
    code VARCHAR(2) PRIMARY KEY NOT NULL,
    name VARCHAR(50) NOT NULL,
    short_name VARCHAR(10) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Unit Of Measurement CD05_025.csv'
INTO TABLE consultation_subjective.unit_of_measurement
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(code, name, short_name);


CREATE TABLE IF NOT EXISTS consultation_subjective.vital_signs_result_type (
    code VARCHAR(2) PRIMARY KEY NOT NULL,
    name VARCHAR(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Vital Sign Result Type CD05_041.csv'
INTO TABLE consultation_subjective.vital_signs_result_type
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(code, name);


CREATE TABLE IF NOT EXISTS consultation_subjective.vital_signs_result_status (
    code VARCHAR(2) PRIMARY KEY NOT NULL,
    description VARCHAR(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Vital Signs Result Status CD05_38.csv'
INTO TABLE consultation_subjective.vital_signs_result_status
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(code, description);
