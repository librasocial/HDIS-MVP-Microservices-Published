from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

class Organization(models.Model):
    """An Organization is a grouping of one or more related Facilities."""
    description = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'
        db_table = 'Organization'
    def __str__(self):
        return str(self.id)


class Facility(models.Model):
    """Represents an entity providing healthcare services"""

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4)
    facility_id = models.UUIDField(default=uuid.uuid4)
    facility_type_code = models.IntegerField(default=99, validators=[MaxValueValidator(99)]) #TODO: Make foreign kay and change default value
    name = models.CharField(max_length=99, blank=True, null=True)
    unique_facility_id = models.BinaryField(blank=True, null=True)
    facility_specialty_code = models.IntegerField(default=999, validators=[MaxValueValidator(999)]) #TODO: Confirm whether each Facility has a single or multiple Specialty
    facility_type_service = models.CharField(max_length=99, default="Clinic")     #TODO: Check if this is required
    organization = models.ForeignKey(Organization, default=None, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = 'Facility'
        verbose_name_plural = 'Facilities'
        db_table = 'Facility'
    def __str__(self):
        return str(self.primary_key)


# TODO: To confirm how this is used
# class Department(models.Model):
#     primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     facility_id = models.ForeignKey(Facility, on_delete=models.RESTRICT)
#     code = models.IntegerField(default=99, validators=[MaxValueValidator(99)]) #TODO: Load Standardized codes into master data table
#     name = models.CharField(max_length=99, blank=True, null=True)
#     class Meta:
#         verbose_name = 'Department'
#         verbose_name_plural = 'Departments'
#         db_table = 'department'
#     def __str__(self):
#         return str(self.primary_key)


class FacilityApplication(models.Model):
    """Represents an Application submitted by an anonymous user requesting creating of a new Facility."""

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    applicant_name = models.CharField(max_length=64)
    applicant_email = models.CharField(max_length=128)
    applicant_mobile = models.CharField(max_length=15)
    applicant_country = models.CharField(max_length=64)
    applicant_city = models.CharField(max_length=64)
    facility_name = models.CharField(max_length=128)
    facility_type_code = models.IntegerField()
    facility_internal_class = models.IntegerField()      #TODO: Check if this is required
    facility_applicant_remarks = models.CharField(max_length=255, blank=True)
    organization = models.ForeignKey(Organization, default=None, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = 'Facility Application'
        verbose_name_plural = 'Facility Applications'
        db_table = 'FacilityApplication'
    def __str__(self):
        return str(self.primary_key)


class FacilityType(models.Model):
    """Defines the Type of a Facility (e.g. Clinic, Primary Health Centre, District Hospital)"""
    
    facility_type_code = models.IntegerField(primary_key=True)
    facility_type_description = models.CharField(max_length=64)
    facility_short_type_name = models.CharField(max_length=4)
    facility_type_internal = models.CharField(max_length=64)

    class Meta:
        managed = False
        verbose_name = 'Facility Type'
        verbose_name_plural = 'Facility Types'
        db_table = 'FacilityType'
    def __str__(self):
        return str(self.facility_type_code)


class DefaultRolesByFacilityType(models.Model):
    """For each Facility Type, defines the default User Roles and Permissions."""

    facility_type_internal = models.CharField(max_length=64)
    role_code = models.CharField(max_length=64)

    class Meta:
        managed = False
        unique_together = ("facility_type_internal", "role_code")
        db_table = 'DefaultRolesByFacilityType'
    def __str__(self):
        return str(self.facility_type + "/" + self.role_code)


class PackageType(models.Model):
    """Package Types define the basic structure of a payment model for a Customer (e.g. Monthly, Transactional)."""

    description = models.CharField(max_length=255)

    class Meta:
        #managed = False #TODO: Decide on preloading of master data
        verbose_name = 'Package Type'
        verbose_name_plural = 'Package Types'
        db_table = 'PackageType'
    def __str__(self):
        return str(self.id)


class Package(models.Model):
    """A Package is used to specify customized payment models for different customers."""

    package_type = models.ForeignKey(PackageType, on_delete=models.RESTRICT)
    description = models.CharField(max_length=255)
    rate = models.DecimalField(max_digits=65, decimal_places=2)

    class Meta:
        verbose_name = 'Package'
        verbose_name_plural = 'Packages'
        db_table = 'Package'
    def __str__(self):
        return str(self.id)
