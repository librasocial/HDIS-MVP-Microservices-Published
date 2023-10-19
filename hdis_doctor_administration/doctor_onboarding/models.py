from django.db import models
from django.core.validators import MaxValueValidator
import uuid
# Create your models here.

######To Do ############
# add bank details and other details of doctor to the model


class DoctorDetails(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #DoctorId = models.AutoField(primary_key=True)
    UniqueIndividualHealthCareProviderNumber = models.CharField(max_length=64, blank=True, null=True)
    UniqueFacilityIdentificationNumber = models.CharField(max_length=64, blank=True, null=True)
    LocalHealthCareProviderNumber = models.CharField(max_length=64, blank=True, null=True)
    doctorName = models.CharField(max_length=240, blank=True, null=True)
    doctorUserId = models.CharField(max_length=240, blank=True, null=True)
    doctorSpeciality=models.CharField(max_length=240, blank=True,default='Physician', null=False)
    doctorBankDetails=models.CharField(max_length=240, blank=True, null=True)
    #all facilityDoctorFields need to be part of doctor details
    #0: inactive 1:under review 2:some information missing 3:Active 4:blacklisted
    profileStatus = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = 'DoctorDetails'
        db_table = 'DoctorDetails'
    def __str__(self):
        return str(self.PrimaryKey)

class DoctorDocuments(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor_id = models.ForeignKey(DoctorDetails, on_delete=models.CASCADE)
    documentType = models.CharField(max_length=128, blank=True, null=True)
    documentFile = models.FileField(upload_to='doctorDocuments/', blank=True, null=True)
    class Meta:
        verbose_name_plural = 'DoctorDocuments'
        db_table = 'DoctorDocuments'
    def __str__(self):
        return str(self.PrimaryKey)

class DoctorPersonalDetails(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor_id = models.ForeignKey(DoctorDetails, on_delete=models.CASCADE)
    doctorRegistrationNumber = models.CharField(max_length=240, blank=True, null=True)
    doctorContactNumber = models.CharField(max_length=10, blank=True, null=True)
    languagesKnown = models.CharField(max_length=240, blank=True, null=True)
    currentCity = models.CharField(max_length=18, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'DoctorPersonalDetails'
        db_table = 'DoctorPersonalDetails'
    def __str__(self):
        return str(self.PrimaryKey)

class DoctorQualificationDetails(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor_id = models.ForeignKey(DoctorDetails, on_delete=models.CASCADE)
    doctor_degree = models.CharField(max_length=150, blank=True, null=True)
    doctor_institute = models.CharField(max_length=250, blank=True, null=True)
    doctor_qualification_year = models.CharField(max_length=10, blank=True, null=True)
    class Meta:
        verbose_name_plural = 'DoctorQualificationDetails'
        db_table = 'DoctorQualificationDetails'
    def __str__(self):
        return str(self.PrimaryKey)
    

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
    facilityGlobalUniqueIdentifier = models.BinaryField(default=False,blank=True, null=True)
    facilitySpecialtyCode = models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    class Meta:
        verbose_name_plural = 'Facility'
        db_table = 'Facility'
    def __str__(self):
        return str(self.PrimaryKey)

class FacilityDoctorFields(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facility_id = models.ForeignKey(Facility, on_delete=models.CASCADE)
    doctorType = models.BooleanField(default=True)
    doctorRegistration = models.BooleanField(default=True)
    doctorRegistrationCertificate = models.BooleanField(default=True)
    doctorLanguage = models.BooleanField(default=False)
    doctorCity = models.BooleanField(default=False)
    doctorSpeciality = models.BooleanField(default=False)
    doctorQualification = models.BooleanField(default=True)
    doctorDescription = models.BooleanField(default=False)
    doctorImage = models.BooleanField(default=False)
    doctorSignatures = models.BooleanField(default=False)
    doctorSchedule = models.BooleanField(default=False)
    doctorBankDetails = models.BooleanField(default=False)
    doctorLeaves = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = 'FacilityDoctorFields'
        db_table = 'FacilityDoctorFields'
    def __str__(self):
        return str(self.PrimaryKey)
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
        return str(self.PrimaryKey)