CREATE TABLE IF NOT EXISTS service_master.unit_of_measurement (
    code varchar(2) PRIMARY KEY NOT NULL,
    name varchar(50) NOT NULL,
    short_name varchar(10) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Unit Of Measurement CD05_025.csv'
INTO TABLE service_master.unit_of_measurement
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(code, name, short_name);


CREATE TABLE IF NOT EXISTS service_master.service_type (
    code smallint PRIMARY KEY NOT NULL,
    name varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Service_Type_CD05_080.csv'
INTO TABLE service_master.service_type
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(code, name);
