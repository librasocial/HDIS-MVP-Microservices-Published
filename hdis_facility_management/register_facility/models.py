from django.db import models

# Create your models here.
class facility_for_trial(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    mobile = models.CharField(max_length=100, blank=True, null=True)
    #country = models.CharField(max_length=100, blank=True, null=True)
    #city = models.CharField(max_length=100, blank=True, null=True)
    organisation_name = models.CharField(max_length=100, blank=True, null=True)
    facility_type = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name_plural = 'facility_for_trial'
        db_table = 'facility_for_trial'
    def __str__(self):
        return self.organisation_name


#CD05.002
class facilityType(models.Model):
    facilityTypeCode = models.CharField(max_length=2, primary_key=True)
    facilityTypeDescription = models.CharField(max_length=40, unique=True)
    facilityShortTypeName = models.CharField(max_length=5, unique=True)

    class Meta:

        verbose_name_plural = 'facilityType'
        db_table = 'facilityType'

    def __str__(self):
        return self.facilityTypeDescription
