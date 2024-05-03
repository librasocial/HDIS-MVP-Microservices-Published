from datetime import datetime
from dateutil import relativedelta
from django.db import models
import uuid

class Person(models.Model):
    """Represents a person who may or may not be registered as a Patient at one or more Facilities."""

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unique_health_identification_number = models.CharField(max_length=18, blank=True, null=True)    #TODO: Add ABHA Number - unique
    unique_health_id = models.CharField(max_length=254, blank=True, null=True)    #TODO: Use this for internal ID, create ABHA ID separately
    alternate_unique_id_number_type = models.IntegerField(default=0)    #TODO: Replicated Master Data
    alternate_unique_id_number = models.CharField(max_length=18, blank=True, null=True)
    nationality_code = models.IntegerField(default=0)   #TODO: Replicated Master Data

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'Persons'
        db_table = 'person'
    def __str__(self):
        return str(self.primary_key)

class Patient(models.Model):
    """ A person who has registered as a Patient at a specific Facility.
        The same person registered at another Facility is considered a distinct Patient.
    """
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE,null=True)
    local_facility_patient_id = models.CharField(max_length=18, blank=True, null=True)    #TODO: Change to local_patient_id
    patient_name = models.CharField(max_length=99, blank=True, null=True)
    patient_age = models.CharField(max_length=9, default="999,99,99")   #Auto-populated age at point of registration
    patient_dob = models.DateField(null=True, blank=True)
    patient_gender = models.CharField(max_length=12, blank=True, null=True)
    identity_unknown_indicator = models.IntegerField(default=0)
    patient_address_type = models.CharField(max_length=1, blank=True, null=True)    #TODO: Remove Address fields from Patient?
    patient_address = models.CharField(max_length=254, blank=True, null=True)
    patient_landline = models.CharField(max_length=8, blank=True, null=True)
    patient_mobile = models.CharField(max_length=10, blank=True, null=True)
    patient_email_url = models.CharField(max_length=254, blank=True, null=True)    #TODO: Check dubious field name
    contact_person_name = models.CharField(max_length=99, blank=True, null=True)    #TODO: One-to-many in separate table?
    contact_type = models.CharField(max_length=1, blank=True, null=True)
    contact_relationship = models.CharField(max_length=10, blank=True, null=True)
    contact_person_landline = models.CharField(max_length=8, blank=True, null=True)
    contact_person_mobile = models.CharField(max_length=10, blank=True, null=True)
    contact_person_email_url = models.CharField(max_length=254, blank=True, null=True)
    ambulance_identification_number = models.CharField(max_length=18, blank=True, null=True)
    ambulance_type = models.CharField(max_length=1, blank=True, null=True)
    ambulance_orignation_site_name = models.CharField(max_length=50, blank=True, null=True)
    ambulance_origination_start_datetime = models.DateTimeField(null=True)
    ambulance_reach_location_site_name = models.CharField(max_length=50, blank=True, null=True)
    ambulance_reach_location_finished_datetime = models.DateTimeField(null=True)
    route_event = models.CharField(max_length=50, blank=True, null=True)    #TODO: Placeholder for future one-to-many relationship 
    route_event_datetime = models.DateTimeField(null=True)    #TODO: Placeholder for future one-to-many relationship
    en_route_delivery_outcome = models.CharField(max_length=1, blank=True, null=True)
    destination_rationale = models.CharField(max_length=50, blank=True, null=True)
    ambulance_paramedic_id = models.CharField(max_length=18, blank=True, null=True)
    ambulance_driver_identification_number = models.CharField(max_length=18, blank=True, null=True)
    patient_status = models.CharField(max_length=1, blank=True, null=True)
    patient_arrival_datetime = models.DateTimeField(null=True)
    mlc_status = models.CharField(max_length=1, blank=True, null=True)
    fir_number = models.CharField(max_length=18, blank=True, null=True)
    patient_class = models.CharField(max_length=1, blank=True, null=True)
    facility_id = models.UUIDField()

    class Meta:
        verbose_name = 'Patient'
        verbose_name_plural = 'Patients'
        db_table = 'patient'
    
    def __str__(self):
        return str(self.primary_key)

    def compute_age(self):
        """Function to compute Age in years, months and days based on a specified Date of Birth."""

        birthdate = self.patient_dob
        if not birthdate:
            raise Exception("'dob' parameter must be populated in order to compute Patient Age.")
        
        current_date = datetime.now().date()
        if current_date < birthdate:
            raise Exception("Invalid Patient Date of Birth as it falls before Current Date.")
        
        difference = relativedelta.relativedelta(current_date, birthdate)
        return difference.years, difference.months, difference.days        


class PatientAddressDetail(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    patient_address = models.CharField(max_length=254, blank=True, null=True)
    patient_address_type = models.CharField(max_length=1, blank=True, null=True)
    patient_landline = models.CharField(max_length=8, blank=True, null=True)
    patient_mobile = models.CharField(max_length=10, blank=True, null=True)
    patient_email_url = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        verbose_name = 'Patient Address Detail'
        verbose_name_plural = 'Patient Addresses Detail'
        db_table = 'patient_address_detail'
    
    def __str__(self):
        return self.primary_key


#class AmbulanceRouteDetail(models.Model):


#class EmergencyPatientDetail(models.Model):


#class PatientContactPersonDetails(models.Model):