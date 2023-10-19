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


class SkuDetails(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=18, blank=True, null=True)
    standardCode = models.CharField(max_length=18, blank=True, null=True)
    fullName = models.CharField(max_length=512, blank=True, null=True)
    shortName = models.CharField(max_length=256, blank=True, null=True)
    category = models.CharField(max_length=18, blank=True, null=True)
    schedule = models.CharField(max_length=18, blank=True, null=True)
    form = models.CharField(max_length=18, blank=True, null=True)
    strength = models.CharField(max_length=18, blank=True, null=True)
    strengthUnit = models.CharField(max_length=18, blank=True, null=True)
    genericName = models.CharField(max_length=512, blank=True, null=True)
    composition = models.CharField(max_length=512, blank=True, null=True)
    size = models.CharField(max_length=18, blank=True, null=True)
    sizeUnit = models.CharField(max_length=18, blank=True, null=True)
    partialDispensationAllowed = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = 'SkuDetails'
        db_table = 'SkuDetails'
    def __str__(self):
        return str(self.PrimaryKey)


class batchDetails(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facilityId = models.ForeignKey(Facility, on_delete=models.CASCADE, null=True)
    skuId = models.ForeignKey(SkuDetails, on_delete=models.CASCADE, null=True)
    skuCode = models.CharField(max_length=18, blank=True, null=True)
    batchCode = models.CharField(max_length=18, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    cost = models.FloatField(default=0)
    expiryDate = models.DateTimeField(null=True, blank=True)
    currentStatus = models.CharField(max_length=18, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'batchDetails'
        db_table = 'batchDetails'

    def __str__(self):
        return str(self.PrimaryKey)


class InventoryManagement(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    skuInventoryDetails = models.ForeignKey(batchDetails, on_delete=models.CASCADE)
    currentStatus = models.CharField(max_length=18, blank=True, null=True) #(Available, dispensed, expired, returned, damaged)
    class Meta:
        verbose_name_plural = 'InventoryManagement'
        db_table = 'InventoryManagement'

    def __str__(self):
        return str(self.PrimaryKey)


class InventoryStatusLog(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    skuInventoryDetails = models.ForeignKey(batchDetails, on_delete=models.CASCADE)
    skuStatus = models.CharField(max_length=18, blank=True, null=True) #(Available, dispensed, expired, returned, damaged)
    skuStatusDateTime = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'InventoryStatusLog'
        db_table = 'InventoryStatusLog'

    def __str__(self):
        return str(self.PrimaryKey)