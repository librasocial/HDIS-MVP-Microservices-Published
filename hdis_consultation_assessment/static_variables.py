setting_file = "hdis_appointment_management.settings.local" #defines which setting file to use for settings
key = '' #need to define the key for the django project
param_location = "" #message-broker params

AUTH_SERVER="http://docker.for.mac.localhost:8080" #define host of the dependent services


ORG_MASTER="http://docker.for.mac.localhost:8081" #define host of the dependent services

PATIENT_REGISTRATION="http://docker.for.mac.localhost:8002" #define host of the dependent services
SLOT_MASTER="http://docker.for.mac.localhost:8004"#define host of the dependent services
DOCTOR_ADMINISTRATION="http://docker.for.mac.localhost:8005" #define host of the dependent services

APPOINTMENT_MANAGEMENT="http://docker.for.mac.localhost:8007" #define host of the dependent services

VISIT_MANAGEMENT="http://docker.for.mac.localhost:8009" #define host of the dependent services

CONSULTATION_SUBJECTIVE="http://docker.for.mac.localhost:8010" #define host of the dependent services

CONSULTATION_OBJECTIVE="http://docker.for.mac.localhost:8012" #define host of the dependent services

CONSULTATION_ASSESSMENT="http://docker.for.mac.localhost:8013"#define host of the dependent services

CONSULTATION_PLAN="http://docker.for.mac.localhost:8014"#define host of the dependent services

CONSULTATION_BILLING="http://docker.for.mac.localhost:8015"#define host of the dependent services
