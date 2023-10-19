
CREATE TABLE IF NOT EXISTS frontend.FacilityType (
facility_type_code int PRIMARY KEY NOT NULL,
facility_type_description varchar(64) NOT NULL,
facility_short_type_name varchar(4) NOT NULL,
facility_type_internal varchar(64)
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/facilityTypenew.csv'
INTO TABLE frontend.FacilityType
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 ROWS
(facility_type_code,facility_type_description,facility_short_type_name,facility_type_internal);

CREATE TABLE IF NOT EXISTS frontend.RoleAccess (
Facility_type varchar(64) NOT NULL,
Facility_User varchar(64) NOT NULL,
Facility_Permission varchar(64) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/OpenHDIS_defaults.csv'
INTO TABLE frontend.RoleAccess
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 LINES
(Facility_type,Facility_User,Facility_Permission);



CREATE TABLE IF NOT EXISTS frontend.ProviderType (
providerTypeCode int PRIMARY KEY NOT NULL,
providerTypeName varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Provider_Types_WHO_Documents.csv'
INTO TABLE frontend.ProviderType
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 LINES
(providerTypeCode,providerTypeName);

CREATE TABLE IF NOT EXISTS frontend.SpecialityType (
Medical_Specialty_Type_Code int PRIMARY KEY NOT NULL,
Medical_Specialty_Type_Name varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/CD05.011_medical_speciality_type_values.csv'
INTO TABLE frontend.SpecialityType
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n' 
IGNORE 1 LINES
(Medical_Specialty_Type_Code,Medical_Specialty_Type_Name);


CREATE TABLE IF NOT EXISTS frontend.addressType (
addressTypeCode varchar(1) PRIMARY KEY NOT NULL,
addressTypeName varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Address Type Code CD05_120.csv'
INTO TABLE frontend.addressType
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(addressTypeCode,addressTypeName);


CREATE TABLE IF NOT EXISTS frontend.allergyProduct (
allergyProductCode varchar(2) PRIMARY KEY NOT NULL,
allergyProductDescription varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Allergy Product CD05_018.csv'
INTO TABLE frontend.allergyProduct
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(allergyProductCode,allergyProductDescription);


CREATE TABLE IF NOT EXISTS frontend.bodySite (
bodySiteCode varchar(2) PRIMARY KEY NOT NULL,
bodySiteName varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Body Site CD05_026.csv'
INTO TABLE frontend.bodySite
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(bodySiteCode,bodySiteName);


CREATE TABLE IF NOT EXISTS frontend.bodySiteExamination (
bodySiteCode varchar(10)  NOT NULL,
bodySiteName varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Body Site Examination.csv'
INTO TABLE frontend.bodySiteExamination
CHARACTER SET utf8
FIELDS TERMINATED BY ',' 
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(bodySiteCode,bodySiteName);



CREATE TABLE IF NOT EXISTS frontend.bodySiteLOINC (
bodySiteCode varchar(12) PRIMARY KEY NOT NULL,
bodySiteName varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/bodySite LOINC.csv'
INTO TABLE frontend.bodySiteLOINC
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(bodySiteCode,bodySiteName);


CREATE TABLE IF NOT EXISTS frontend.clinicalDocumentType (
clinicalDocumentTypeCode int PRIMARY KEY NOT NULL,
clinicalDocumentTypeName varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Clinical Document Type CD05_046.csv'
INTO TABLE frontend.clinicalDocumentType
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(clinicalDocumentTypeCode,clinicalDocumentTypeName);


CREATE TABLE IF NOT EXISTS frontend.districtCodeDirectory (
districtCode int PRIMARY KEY NOT NULL,
districtName varchar(128) NOT NULL,
stateCode int NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/District Codes CD02_03.csv'
INTO TABLE frontend.districtCodeDirectory
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(districtCode,districtName,stateCode);


CREATE TABLE IF NOT EXISTS frontend.encounterStatus (
encounterStatusCode varchar(20) PRIMARY KEY NOT NULL,
encounterStatusDescription varchar(128) NOT NULL,
encounterStatusDefinition varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Encounter Status.csv'
INTO TABLE frontend.encounterStatus
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(encounterStatusCode,encounterStatusDescription,encounterStatusDefinition);


CREATE TABLE IF NOT EXISTS frontend.encounterType (
encounterTypeCode int PRIMARY KEY NOT NULL,
encounterTypeDescription varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Encounter Type CD05_047.csv'
INTO TABLE frontend.encounterType
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(encounterTypeCode,encounterTypeDescription);


CREATE TABLE IF NOT EXISTS frontend.examinationType (
examinationTypeCode varchar(2) PRIMARY KEY NOT NULL,
examinationTypeDescription varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Examination Type CD05_061.csv'
INTO TABLE frontend.examinationType
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(examinationTypeCode,examinationTypeDescription);


CREATE TABLE IF NOT EXISTS frontend.familyMemberRelationship (
familyMemberRelationshipCode varchar(2) PRIMARY KEY NOT NULL,
familyMemberRelationshipName varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Family Member Relationship CD05_06.csv'
INTO TABLE frontend.familyMemberRelationship
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(familyMemberRelationshipCode,familyMemberRelationshipName);


CREATE TABLE IF NOT EXISTS frontend.healthCondition (
healthConditionCode varchar(3) PRIMARY KEY NOT NULL,
healthConditionName varchar(250) NOT NULL,
healthConditionDescription varchar(250),
health_condition_type_id varchar(3)  NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Health Condition CD05_019.csv'
INTO TABLE frontend.healthCondition
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(healthConditionCode,healthConditionName,healthConditionDescription,health_condition_type_id);


CREATE TABLE IF NOT EXISTS frontend.healthConditionStatus (
healthConditionStatusCode varchar(2) PRIMARY KEY NOT NULL,
healthConditionStatusDescription varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Health Condition Status CD05_021.csv'
INTO TABLE frontend.healthConditionStatus
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(healthConditionStatusCode,healthConditionStatusDescription);


CREATE TABLE IF NOT EXISTS frontend.healthConditionType (
healthConditionTypeCode varchar(2) PRIMARY KEY NOT NULL,
healthConditionTypeName varchar(128) NOT NULL,
icdCodeRange varchar(7) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Health Condition Type CD05_022.csv'
INTO TABLE frontend.healthConditionType
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(healthConditionTypeCode,healthConditionTypeName,icdCodeRange);


CREATE TABLE IF NOT EXISTS frontend.medicationFrequency (
medicationFrequencyCode varchar(4) PRIMARY KEY NOT NULL,
medicationFrequencyDescription varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Medication Frequency CD05_023.csv'
INTO TABLE frontend.medicationFrequency
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(medicationFrequencyCode,medicationFrequencyDescription);


CREATE TABLE IF NOT EXISTS frontend.orderStatus (
orderStatusCode varchar(2) PRIMARY KEY NOT NULL,
orderStatusName varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Order Status CD05_121.csv'
INTO TABLE frontend.orderStatus
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(orderStatusCode,orderStatusName);


CREATE TABLE IF NOT EXISTS frontend.organSystem (
organSystemCode varchar(2) PRIMARY KEY NOT NULL,
organSystemName varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Organ System CD05_033.csv'
INTO TABLE frontend.organSystem
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(organSystemCode,organSystemName);


CREATE TABLE IF NOT EXISTS frontend.severityCodeDirectory (
severityCode varchar(2) PRIMARY KEY NOT NULL,
severityDescription varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Severity Code CD05_020.csv'
INTO TABLE frontend.severityCodeDirectory
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(severityCode,severityDescription);


CREATE TABLE IF NOT EXISTS frontend.stateCodeDirectory (
stateLandRegionCode int PRIMARY KEY NOT NULL,
stateName varchar(128) NOT NULL,
subDistrictNomenclatureInTheState varchar(128) NOT NULL,
recognizedOfficialLanguageCode int NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/State Codes CD02_02.csv'
INTO TABLE frontend.stateCodeDirectory
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(stateLandRegionCode,stateName,subDistrictNomenclatureInTheState,recognizedOfficialLanguageCode);


CREATE TABLE IF NOT EXISTS frontend.subDistrictCodeDirectory (
subDistrictCode int PRIMARY KEY NOT NULL,
subDistrictName varchar(128) NOT NULL,
districtCode int NOT NULL,
stateCode int NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Sub District Codes CD02_04.csv'
INTO TABLE frontend.subDistrictCodeDirectory
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(subDistrictCode,subDistrictName,districtCode,stateCode);



CREATE TABLE IF NOT EXISTS frontend.townCodeDirectory (
townCode int PRIMARY KEY NOT NULL,
townName varchar(128) NOT NULL,
subDistrictCode int NOT NULL,
districtCode int NOT NULL,
stateCode int NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Town Codes CD02_06.csv'
INTO TABLE frontend.townCodeDirectory
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(townCode,townName,subDistrictCode,districtCode,stateCode);


CREATE TABLE IF NOT EXISTS frontend.unitOfMeasurement (
unitOfMeasurementCode varchar(2) PRIMARY KEY NOT NULL,
unitOfMeasurementName varchar(50) NOT NULL,
unitOfMeasurementShortName varchar(10) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Unit Of Measurement CD05_025.csv'
INTO TABLE frontend.unitOfMeasurement
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(unitOfMeasurementCode,unitOfMeasurementName,unitOfMeasurementShortName);


CREATE TABLE IF NOT EXISTS frontend.vitalSignsResultType (
vitalSignsResultTypeCode varchar(2) PRIMARY KEY NOT NULL,
vitalSignsResultTypeName varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Vital Sign Result Type CD05_041.csv'
INTO TABLE frontend.vitalSignsResultType
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n'
IGNORE 1 LINES
(vitalSignsResultTypeCode,vitalSignsResultTypeName);


CREATE TABLE IF NOT EXISTS frontend.vitalSignsResultStatus (
vitalSignsResultStatusCode varchar(2) PRIMARY KEY NOT NULL,
vitalSignsResultStatusDescription varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Vital Signs Result Status CD05_38.csv'
INTO TABLE frontend.vitalSignsResultStatus
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(vitalSignsResultStatusCode,vitalSignsResultStatusDescription);

CREATE TABLE IF NOT EXISTS frontend.serviceType (
serviceTypeCode int PRIMARY KEY NOT NULL,
serviceTypeName varchar(128) NOT NULL
);

LOAD DATA INFILE '/docker-entrypoint-initdb.d/init_data/Service_Type_CD05_080.csv'
INTO TABLE frontend.serviceType
FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES
(serviceTypeCode,serviceTypeName);