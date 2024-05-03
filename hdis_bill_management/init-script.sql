CREATE TABLE IF NOT EXISTS bill_management.unit_of_measurement (
code varchar(2) PRIMARY KEY NOT NULL,
name varchar(50) NOT NULL,
short_name varchar(10) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Unit Of Measurement CD05_025.csv'
INTO TABLE bill_management.unit_of_measurement
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(code, name, short_name);
