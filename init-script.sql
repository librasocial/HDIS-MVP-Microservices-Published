CREATE TABLE IF NOT EXISTS facility_management.FacilityType (
facility_type_code int PRIMARY KEY NOT NULL,
facility_type_description varchar(64) NOT NULL,
facility_short_type_name varchar(4) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/CD05.002_facility_type_values.csv'
INTO TABLE facility_management.FacilityType
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 LINES
(facility_type_code,facility_type_description,facility_short_type_name);


CREATE TABLE IF NOT EXISTS facility_management.ProviderType (
providerTypeCode int PRIMARY KEY NOT NULL,
providerTypeName varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Provider_Types_WHO_Documents.csv'
INTO TABLE facility_management.ProviderType
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 LINES
(providerTypeCode,providerTypeName);

CREATE TABLE IF NOT EXISTS facility_management.SpecialityType (
Medical_Specialty_Type_Code int PRIMARY KEY NOT NULL,
Medical_Specialty_Type_Name varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/CD05.011_medical_speciality_type_values.csv'
INTO TABLE facility_management.SpecialityType
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 LINES
(Medical_Specialty_Type_Code,Medical_Specialty_Type_Name);
