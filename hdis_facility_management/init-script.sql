-- MDDS 05.008.0002, CD05.002
CREATE TABLE IF NOT EXISTS facility_management.facility_type (
    code INT PRIMARY KEY,
    description VARCHAR(64) NOT NULL,
    short_name VARCHAR(4) NOT NULL,
    internal_name VARCHAR(64) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/facilityTypenew.csv'
INTO TABLE facility_management.facility_type
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 LINES
(code, description, short_name, internal_name);


CREATE TABLE IF NOT EXISTS facility_management.default_roles_by_facility_type (
    facility_type_internal_name VARCHAR(64) NOT NULL,
    role_code VARCHAR(64) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/DefaultRolesByFacilityType_Data.csv'
INTO TABLE facility_management.default_roles_by_facility_type
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 LINES
(facility_type_internal_name, role_code);


-- MDDS 05.008.0010, CD05.011
CREATE TABLE IF NOT EXISTS facility_management.specialty_type (
    code CHAR(2) PRIMARY KEY,
    name VARCHAR(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/CD05.011_medical_speciality_type_values.csv'
INTO TABLE facility_management.specialty_type
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 LINES
(code, name);
