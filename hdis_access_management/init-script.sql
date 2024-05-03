CREATE TABLE IF NOT EXISTS access_management.RolePermissions (
    role_code VARCHAR(64) NOT NULL,
    facility_permission VARCHAR(64) NOT NULL,
    PRIMARY KEY (role_code, facility_permission)
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/RolePermissions_Data.csv'
INTO TABLE access_management.RolePermissions
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 LINES
(role_code, facility_permission);
