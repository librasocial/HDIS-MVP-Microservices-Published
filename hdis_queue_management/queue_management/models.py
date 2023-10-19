from django.db import models
from django.core.validators import MaxValueValidator
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
        return self.uniqueFacilityIdentificationNumber

class Department(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facilityId = models.ForeignKey(Facility, on_delete=models.CASCADE)
    departmentName=models.CharField(max_length=99, blank=True, null=True)
    departmentCode=models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    class Meta:
        verbose_name_plural = 'Department'
        db_table = 'Department'
    def __str__(self):
        return self.departmentName




class Provider(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facilityId = models.ForeignKey(Facility, on_delete=models.CASCADE)
    uniqueIndividualHealthCareProviderNumber = models.CharField(max_length=64, blank=True, null=True)
    careProviderMobileNumber = models.CharField(max_length=10, blank=True, null=True)
    careProviderEmailAddress = models.CharField(max_length=254, blank=True, null=True)
    careProviderName = models.CharField(max_length=99, blank=True, null=True)
    healthServiceProviderRoleCode = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    healthServiceProviderRoleFreeText = models.CharField(max_length=99, blank=True, null=True)
    healthServiceProviderType = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    providerCreationDate= models.DateTimeField(null=True)
    providerStatus=models.IntegerField(default=0)
    class Meta:
        verbose_name_plural = 'Provider'
        db_table = 'Provider'
    def __str__(self):
        return self.uniqueIndividualHealthCareProviderNumber


class Person(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True)
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
    PrimaryKey = models.UUIDField(primary_key=True)
    personId = models.OneToOneField(Person, on_delete=models.CASCADE)
    facilityId = models.ForeignKey(Facility, on_delete=models.CASCADE)
    localFacilityPatientId = models.CharField(max_length=18, blank=True, null=True)
    PatientName = models.CharField(max_length=99, blank=True, null=True)
    PatientAge = models.CharField(max_length=9, blank=True, null=True)
    PatientDOB = models.DateTimeField(null=True)
    PatientGenderCode = models.CharField(max_length=1, blank=True, null=True)
    patientArrivalDateTime = models.DateTimeField(null=True)
    patientLandlineNumber = models.CharField(max_length=8, blank=True, null=True)
    patientMobileNumber = models.CharField(max_length=10, blank=True, null=True)
    patientEmailAddress = models.CharField(max_length=254, blank=True, null=True)
    reasonForVisit = models.CharField(max_length=99, blank=True, null=True)
    birthOrder = models.IntegerField(default=0)
    parity = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    gravida = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    pregnancyIndicator = models.BooleanField(default=0)
    durationOfPregnancy = models.IntegerField(default=99, validators=[MaxValueValidator(99)])

    # patient_address
    # patient_address_type

    class Meta:
        verbose_name_plural = 'Patient'
        db_table = 'Patient'

    def __str__(self):
        return str(self.PrimaryKey)

class Billing(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facilityId = models.ForeignKey(Facility, on_delete=models.CASCADE)
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    providerId = models.ManyToManyField('queue_management.Provider', related_name='bills')
    serviceType = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    serviceItemName = models.CharField(max_length=99, blank=True, null=True)
    quantityOfService = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        verbose_name_plural = 'Billing'
        db_table = 'Billing'
    def __str__(self):
        return self.serviceType

class Service(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facilityId = models.ForeignKey(Facility, on_delete=models.CASCADE)
    serviceType = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    serviceItemName = models.CharField(max_length=99, blank=True, null=True)





#class Payment(models.Model):
#    class Meta:
#        verbose_name_plural = 'Payment'
#        db_table = 'Payment'
#    def __str__(self):
#        return self.PaymentId

#class GenericDetails(models.Model):
#    class Meta:
#        verbose_name_plural = 'GenericDetails'
#        db_table = 'GenericDetails'
#    def __str__(self):
#        return self.GenericDetailsId

class Episode(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facilityId = models.ForeignKey(Facility, on_delete=models.CASCADE)
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    providerId = models.ForeignKey(Provider, on_delete=models.CASCADE)
    EpisodeId = models.CharField(max_length=64, blank=True, null=True)
    EpisodeType = models.IntegerField(default=1, validators=[MaxValueValidator(4)])

    class Meta:
        verbose_name_plural = 'Episode'
        db_table = 'Episode'
    def __str__(self):
        return self.EpisodeId


class Encounter(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    episodeId = models.ForeignKey(Episode, on_delete=models.CASCADE)
    encounterID=models.CharField(max_length=64, blank=True, null=True)
    encounterType=models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    encounterTime = models.DateTimeField(null=True)
    encounterTypeDescription = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Encounter'
        db_table = 'Encounter'
    def __str__(self):
        return self.encounterID

class Waitlist(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facilityId=models.ForeignKey(Facility, on_delete=models.CASCADE)
    departmentId=models.ForeignKey(Department, on_delete=models.CASCADE)
    waitlistDay=models.DateField(null=True)
    waitlistNumber=models.IntegerField(default=1, validators=[MaxValueValidator(9999)])

    class Meta:
        verbose_name_plural = 'Waitlist'
        db_table = 'Waitlist'
    def __str__(self):
        return self.waitlistNumber

class Token(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facilityId=models.ForeignKey(Facility, on_delete=models.CASCADE)
    providerId=models.ForeignKey(Provider, on_delete=models.CASCADE)
    tokenDay=models.DateField(null=True)
    tokenNumber=models.IntegerField(default=1, validators=[MaxValueValidator(9999)])

    class Meta:
        verbose_name_plural = 'Token'
        db_table = 'Token'
    def __str__(self):
        return self.waitlistNumber

class Queue(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    departmentId=models.ForeignKey(Department, on_delete=models.CASCADE)
    tokenId=models.CharField(max_length=64, blank=True, null=True)
    encounterId=models.ForeignKey(Encounter, on_delete=models.CASCADE)
    serviceId=models.ForeignKey(Service, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Queue'
        db_table = 'Queue'
    def __str__(self):
        return self.tokenId







