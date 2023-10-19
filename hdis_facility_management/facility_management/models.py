from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid


##### To Do #######
# Add is user active in memebers



# Create your models here.
class Facility(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True,default=uuid.uuid4)
    uniqueFacilityIdentificationNumber = models.UUIDField(default=uuid.uuid4)
    facilityTypeCode = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    facilityServiceCode = models.CharField(max_length=18, blank=True, null=True)
    departmentName = models.CharField(max_length=99, blank=True, null=True)
    referralFacilityIdentificationNumber = models.CharField(max_length=10, blank=True, null=True)
    referralFacilityTypeCode = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    referralFromFacilityIdentificationNumber = models.CharField(max_length=10, blank=True, null=True)
    referralFromFacilityTypeCode = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    facilityGlobalUniqueIdentifier = models.BinaryField(blank=True, null=True)
    facilitySpecialtyCode = models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    facilityTypeService=models.CharField(max_length=99, default="Clinic")
    class Meta:
        verbose_name_plural = 'Facility'
        db_table = 'Facility'
    def __str__(self):
        return str(self.PrimaryKey)
    
class Members(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    userRole=models.CharField(max_length=64)
    memberName=models.CharField(max_length=64)
    memberEmail=models.CharField(max_length=128,blank=True)
    memberMobile=models.CharField(max_length=64,blank=True)
    memberPermissions=models.CharField(max_length=512,blank=True)
    class Meta:
        verbose_name_plural = 'Members'
        db_table = 'Members'
    def __str__(self):
        return str(self.PrimaryKey)


    
class FacilityMembers(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facilityId=models.ForeignKey(Facility, on_delete=models.CASCADE)
    memberId=models.ManyToManyField(Members,related_name="members")
    class Meta:
        verbose_name_plural = 'FacilityMembers'
        db_table = 'FacilityMembers'
    def __str__(self):
        return str(self.PrimaryKey)


class FacilityApplication(models.Model):
     PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
     facilityApplicantName=models.CharField(max_length=64)
     facilityApplicantEmail=models.CharField(max_length=128)
     facilityApplicantMobile=models.CharField(max_length=15)
     facilityApplicantCountry=models.CharField(max_length=64)
     facilityApplicantCity=models.CharField(max_length=64)
     facilityName=models.CharField(max_length=128)
     facilityTypeCode=models.IntegerField()
     facilityInternalClass=models.IntegerField()
     facilityApplicantRemarks=models.CharField(max_length=128,blank=True)
     class Meta:
        verbose_name_plural = 'FacilityApplication'
        db_table = 'FacilityApplication'
     def __str__(self):
        return str(self.PrimaryKey)


class Facilitytype(models.Model):
    facility_type_code = models.IntegerField(primary_key=True)
    facility_type_description = models.CharField(max_length=64)
    facility_short_type_name = models.CharField(max_length=4)
    facility_type_internal=models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'FacilityType'
    def __str__(self):
        return str(self.facility_type_code)
    
class RoleAccess(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    Facility_type = models.CharField(max_length=64)
    Facility_User = models.CharField(max_length=64)
    Facility_Permission=models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'RoleAccess'
    def __str__(self):
        return str(self.PrimaryKey)


    

