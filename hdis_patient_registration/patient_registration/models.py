from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
# Create your models here.
class Facility(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    uniqueFacilityIdentificationNumber = models.CharField(max_length=64, blank=True, null=True)
    facilityTypeCode = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    facilityServiceCode = models.CharField(max_length=18, blank=True, null=True)
    departmentName = models.CharField(max_length=99, blank=True, null=True)
    referralFacilityIdentificationNumber = models.CharField(max_length=10, blank=True, null=True)
    referralFacilityTypeCode = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    referralFromFacilityIdentificationNumber = models.CharField(max_length=10, blank=True, null=True)
    referralFromFacilityTypeCode = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    facilityGlobalUniqueIdentifier = models.BinaryField(blank=True, null=True)
    facilitySpecialtyCode = models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    class Meta:
        verbose_name_plural = 'Facility'
        db_table = 'Facility'
    def __str__(self):
        return str(self.PrimaryKey)
    
class Person(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    UniqueHealthIdentificationNumber = models.CharField(max_length=18, blank=True, null=True)
    UniqueHealthIdentificationID = models.CharField(max_length=254, blank=True, null=True)
    AlternateUniqueIdentificationNumberType = models.IntegerField(default=0)
    AlternateUniqueIdentificationNumber = models.CharField(max_length=18, blank=True, null=True)
    NationalityCode = models.IntegerField(default=0)
    class Meta:

        verbose_name_plural = 'Person'
        db_table = 'Person'
    def __str__(self):
        return str(self.PrimaryKey)
    
class Patient(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    personId =models.ForeignKey(Person, on_delete=models.CASCADE,null=True)
    localFacilityPatientId = models.CharField(max_length=18, blank=True, null=True)
    PatientName = models.CharField(max_length=99, blank=True, null=True)
    PatientAge = models.CharField(max_length=9, default="999,99,99")
    PatientDOB = models.DateTimeField(null=True, blank=True)
    PatientGender = models.CharField(max_length=12, blank=True, null=True)
    IdentityUnknownIndicator = models.IntegerField(default=0)
    PatientAddress = models.CharField(max_length=254, blank=True, null=True)
    PatientAddressType = models.CharField(max_length=1, blank=True, null=True)
    patientLandlineNumber = models.CharField(max_length=8, blank=True, null=True)
    patientMobileNumber = models.CharField(max_length=10, blank=True, null=True)
    patientEmailAddressURL = models.CharField(max_length=254, blank=True, null=True)
    contactPersonName = models.CharField(max_length=99, blank=True, null=True)
    contactType = models.CharField(max_length=1, blank=True, null=True)
    contactRelationship = models.CharField(max_length=10, blank=True, null=True)
    contactPersonLandLineNumber = models.CharField(max_length=8, blank=True, null=True)
    ListofcontactPersonMobileNumber = models.CharField(max_length=10, blank=True, null=True)
    contactPersonEmailAddressURL = models.CharField(max_length=254, blank=True, null=True)
    AmbulanceIdentificationNumber = models.CharField(max_length=18, blank=True, null=True)
    AmbulanceType = models.CharField(max_length=1, blank=True, null=True)
    AmbulanceOrignationSiteName = models.CharField(max_length=50, blank=True, null=True)
    AmbulanceOriginationStartDateTime = models.DateTimeField(null=True)
    #facility name if registered
    AmbulanceReachLocationSiteName = models.CharField(max_length=50, blank=True, null=True)
    AmbulanceReachLocationFinishedDateTime = models.DateTimeField(null=True)
    RouteEvent = models.CharField(max_length=50, blank=True, null=True)
    RouteEventDateTime = models.DateTimeField(null=True)
    EnRouteDeliveryOutcome = models.CharField(max_length=1, blank=True, null=True)
    DestinationRationale = models.CharField(max_length=50, blank=True, null=True)
    AmbulanceParamedicID = models.CharField(max_length=18, blank=True, null=True)
    AmbulanceDriverIdentificationNumber = models.CharField(max_length=18, blank=True, null=True)
    patientStatus = models.CharField(max_length=1, blank=True, null=True)
    patientArrivalDateTime = models.DateTimeField(null=True)
    MLCStatus = models.CharField(max_length=1, blank=True, null=True)
    FIRNumber = models.CharField(max_length=18, blank=True, null=True)
    PatientClass = models.CharField(max_length=1, blank=True, null=True)
    facilityId = models.ForeignKey(Facility, on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Patient'
        db_table = 'Patient'
    def __str__(self):
        return str(self.PrimaryKey)

class patientAddressDetail(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    PatientAddress = models.CharField(max_length=254, blank=True, null=True)
    PatientAddressType = models.CharField(max_length=1, blank=True, null=True)
    patientLandlineNumber = models.CharField(max_length=8, blank=True, null=True)
    patientMobileNumber = models.CharField(max_length=10, blank=True, null=True)
    patientEmailAddressURL = models.CharField(max_length=254, blank=True, null=True)
    class Meta:
        verbose_name_plural = 'patientAddressDetail'
        db_table = 'patientAddressDetail'
    def __str__(self):
        return str(self.PrimaryKey)

class Employee(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    EmployeeID = models.CharField(max_length=18, blank=True, null=True)
    EmployerID = models.CharField(max_length=18, blank=True, null=True)
    PatientID = models.ManyToManyField(Patient)
    EmployeeTelephoneNumber = models.CharField(max_length=8, blank=True, null=True)
    EmployeeMobileNumber = models.CharField(max_length=10, blank=True, null=True)
    EmployeeEmailAddress = models.CharField(max_length=254, blank=True, null=True)
    EmployeeDesignationCode = models.CharField(max_length=2, blank=True, null=True)
    EmployeeOrganizationName = models.CharField(max_length=254, blank=True, null=True)
    class Meta:
        verbose_name_plural = 'Employee'
        db_table = 'Employee'
    def __str__(self):
        return str(self.PrimaryKey)

class Payment(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #SourceOfPaymentID = models.IntegerField(primary_key=True)
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    InsuredCardID = models.CharField(max_length=18, blank=True, null=True)
    TPACode = models.CharField(max_length=18, blank=True, null=True)
    HealthPlanTypeCode = models.CharField(max_length=18, blank=True, null=True)
    InsurancePolicyID = models.CharField(max_length=18, blank=True, null=True)
    SourceOfPayment = models.CharField(max_length=18, blank=True, null=True)
    SecondaryPolicyIndicator = models.CharField(max_length=18, blank=True, null=True)
    ListofSecondaryPolicyID = models.CharField(max_length=18, blank=True, null=True)
    class Meta:
        verbose_name_plural = 'Payment'
        db_table = 'Payment'
    def __str__(self):
        return str(self.PrimaryKey)

#class AmbulanceRouteDetail(models.Model):

#class EmergencyPatientDetail(models.Model):

#class PatientContactPersonDetails(models.Model):

#class patientAddressDetail(models.Model):
