from django.db import models
from django.core.validators import MaxValueValidator
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
    wardName = models.CharField(max_length=99, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Facility'
        db_table = 'Facility'

    def __str__(self):
        return str(self.PrimaryKey)


class Provider(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True)
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

class serviceType(models.Model):

    serviceTypeCode = models.IntegerField(default=0, validators=[MaxValueValidator(1)])
    serviceTypeName = models.CharField(max_length=50, blank=True, null=True)
    class Meta:

        managed = False
        db_table = 'serviceType'

    def __str__(self):
        return str(self.serviceTypeCode)

        verbose_name_plural = 'ServiceCategory'
        db_table = 'ServiceCategory'

    def __str__(self):
        return str(self.PrimaryKey)


class Discount(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    discountCode = models.IntegerField(default=0)
    discountName = models.CharField(max_length=50, blank=True, null=True)
    dicsountValue=models.IntegerField(default=0)
    

    class Meta:
        verbose_name_plural = 'Discount'
        db_table = 'Discount'

    def __str__(self):
        return str(self.PrimaryKey)

   

class Billing(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True)
    facilityId = models.ForeignKey(Facility, on_delete=models.CASCADE)
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    providerId = models.ManyToManyField('service_manager.Provider', related_name='bills')
    serviceTypeCode = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    serviceItemName = models.CharField(max_length=99, blank=True, null=True)
    quantityOfService = models.CharField(max_length=50, blank=True, null=True)
    class Meta:
        verbose_name_plural = 'Billing'
        db_table = 'Billing'
    def __str__(self):
        return str(self.PrimaryKey)

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

class Service(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facilityId = models.ForeignKey(Facility, on_delete=models.CASCADE)
    providerId = models.ForeignKey(Provider, on_delete=models.CASCADE)
    serviceTypeCode = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    serviceUnit = models.CharField(max_length=50, blank=True, null=True)
    serviceName = models.CharField(max_length=50, blank=True, null=True)
    serviceShortName = models.CharField(max_length=50, blank=True, null=True)
    usageType = models.CharField(max_length=50, blank=True, null=True) #oen time/time based etc
    serviceEffectiveDateFrom = models.DateTimeField(null=True)
    serviceEffectiveDateTo = models.DateTimeField(null=True)
    serviceCost = models.IntegerField(default=0)
    serviceMaximumRate = models.IntegerField(default=0)
    serviceMinimumRate = models.IntegerField(default=0)
    isInventory=models.BooleanField(default=0)
    isActive = models.BooleanField(default=0)
    isTaxable = models.BooleanField(default=0) #if taxable then tax code to be adeed
    taxCode = models.CharField(max_length=50, blank=True, null=True)
    sampleSourceCode = models.CharField(max_length=50, blank=True, null=True) #only for diagnostic services (need to understand what this does)
    isOrderable = models.BooleanField(default=0)
    autoPost = models.BooleanField(default=0)
    appointmentRequired = models.BooleanField(default=0) #procedure master entry if yes
    bundlingAllowed = models.BooleanField(default=0) #excluded from packages
    discountAllowed = models.BooleanField(default=0)
    componentType = models.BooleanField(default=0) #if component type is yes then other services have to be added to this

    serviceCost = models.IntegerField(default=0)
    isInventory=models.BooleanField(default=0)

    class Meta:
        verbose_name_plural = 'Service'
        db_table = 'Service'
    def __str__(self):
        return str(self.PrimaryKey)
#need to discuss component service
class ComponentServcies(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    componentServcie=models.OneToOneField(Service, on_delete=models.CASCADE)
    servicesInComponent=models.CharField(max_length=50, blank=True, null=True) #primary key of service which is a part of the component service
    class Meta:
        verbose_name_plural = 'ComponentServcies'
        db_table = 'ComponentServcies'
    def __str__(self):
        return str(self.PrimaryKey)
#default provider and sharing need to be discussed
class serviceRates(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    serviceId = models.ForeignKey(Service, on_delete=models.CASCADE)
    patientType = models.CharField(max_length=50, blank=True, null=True) #different patient types can have different rates
    glCode = models.CharField(max_length=50, blank=True,
                                   null=True)  # need to find out what is GL code
    servicePrice = models.IntegerField(default=0)
    isSharable = models.BooleanField(default=0) #if yes then needs to add provider and share
    providerId = models.CharField(max_length=50, blank=True, null=True) #primary key of provider with whom the service cost will be shared
    sharePercentage = models.IntegerField(default=0)

    servicePriceEffectiveDateFrom = models.DateTimeField(null=True)
    servicePriceEffectiveDateTrue = models.DateTimeField(null=True)
    class Meta:
        verbose_name_plural = 'serviceRates'
        db_table = 'serviceRates'
    def __str__(self):
        return str(self.PrimaryKey)

#tax rates added
class serviceTaxRates(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    serviceId = models.ForeignKey(Service, on_delete=models.CASCADE)
    taxLocation = models.CharField(max_length=50, blank=True, null=True) #tax can be different based on different locations
    taxRate = models.IntegerField(default=0)
    serviceTaxRateEffectiveDateFrom = models.DateTimeField(null=True)
    serviceTaxRateEffectiveDateTrue = models.DateTimeField(null=True)
    class Meta:
        verbose_name_plural = 'serviceTaxRates'
        db_table = 'serviceTaxRates'
    def __str__(self):
        return str(self.PrimaryKey)



class BillingGroup(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    billingGroupName=models.CharField(max_length=50)
    serviceId=models.ManyToManyField(Service)
    class Meta:
        verbose_name_plural = 'BillingGroup'
        db_table = 'BillingGroup'

    def __str__(self):
        return str(self.PrimaryKey)
    
class MISGroup(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    MISGroupName=models.CharField(max_length=50)
    serviceId=models.ManyToManyField(Service)
    class Meta:
        verbose_name_plural = 'MISGroup'
        db_table = 'MISGroup'

    def __str__(self):
        return str(self.PrimaryKey)    


