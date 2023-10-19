from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid
# Create your models here.
class Facility(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True)
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
        return self.uniqueFacilityIdentificationNumber

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
        return self.personId

class Patient(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    personId = models.ForeignKey(Person, on_delete=models.CASCADE)
    PatientName = models.CharField(max_length=99, blank=True, null=True)
    PatientAge = models.CharField(max_length=9, default="999,99,99")
    # extra field
    PatientGender = models.CharField(max_length=12, blank=True, null=True)
    PatientDOB = models.DateTimeField(null=True, blank=True)
    #facilityID = models.CharField(max_length=64, blank=True, null=True)
    facilityId = models.ForeignKey(Facility, on_delete=models.CASCADE)
    IdentityUnknownIndicator = models.IntegerField(default=0)
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
        return self.patientEmailAddressURL