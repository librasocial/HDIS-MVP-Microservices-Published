CREATE TABLE IF NOT EXISTS employee_management.provider_type (
    code int PRIMARY KEY NOT NULL,
    name varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Provider_Types_WHO_Documents.csv'
INTO TABLE employee_management.provider_type
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 LINES
(code, name);


CREATE TABLE IF NOT EXISTS employee_management.specialty_type (
    code int PRIMARY KEY NOT NULL,
    name varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/CD05.011_medical_speciality_type_values.csv'
INTO TABLE employee_management.specialty_type
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 LINES
(code, name);


CREATE TABLE IF NOT EXISTS employee_management.address_type (
    code varchar(1) PRIMARY KEY NOT NULL,
    name varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Address Type Code CD05_120.csv'
INTO TABLE employee_management.address_type
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(code, name);


CREATE TABLE IF NOT EXISTS employee_management.district_code_directory (
    code int PRIMARY KEY NOT NULL,
    name varchar(128) NOT NULL,
    state_code int NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/District Codes CD02_03.csv'
INTO TABLE employee_management.district_code_directory
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(code, name, state_code);


CREATE TABLE IF NOT EXISTS employee_management.family_member_relationship (
    code varchar(2) PRIMARY KEY NOT NULL,
    name varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Family Member Relationship CD05_06.csv'
INTO TABLE employee_management.family_member_relationship
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(code, name);


CREATE TABLE IF NOT EXISTS employee_management.state_code_directory (
    state_land_region_code int PRIMARY KEY NOT NULL,
    state_name varchar(128) NOT NULL,
    subdistrict_nomenclature_in_the_state varchar(128) NOT NULL,
    recognized_official_language_code int NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/State Codes CD02_02.csv'
INTO TABLE employee_management.state_code_directory
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(state_land_region_code, state_name, subdistrict_nomenclature_in_the_state, recognized_official_language_code);


CREATE TABLE IF NOT EXISTS employee_management.subdistrict_code_directory (
    subdistrict_code int PRIMARY KEY NOT NULL,
    subdistrict_name varchar(128) NOT NULL,
    district_code int NOT NULL,
    state_code int NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Sub District Codes CD02_04.csv'
INTO TABLE employee_management.subdistrict_code_directory
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(subdistrict_code, subdistrict_name, district_code, state_code);


CREATE TABLE IF NOT EXISTS employee_management.town_code_directory (
    town_code int PRIMARY KEY NOT NULL,
    town_name varchar(128) NOT NULL,
    subdistrict_code int NOT NULL,
    district_code int NOT NULL,
    state_code int NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Town Codes CD02_06.csv'
INTO TABLE employee_management.town_code_directory
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(town_code, town_name, subdistrict_code, district_code, state_code);
