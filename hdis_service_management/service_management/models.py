from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid


class ServiceType(models.Model):
    """Service Types are used to categorize the various Services on offer at Facilities."""

    code = models.SmallIntegerField(primary_key=True, validators=[MinValueValidator(1)])
    name = models.CharField(max_length=50)
    
    class Meta:
        managed = False
        verbose_name = "Service Type"
        verbose_name_plural = "Service Types"
        db_table = 'service_type'

    def __str__(self):
        return str(self.code)


class Service(models.Model):
    """Defines various Healthcare-related Services offered at individual Facilities."""

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facility_id = models.UUIDField()    # TODO: REMOVE? To discuss further
    service_type = models.ForeignKey(ServiceType, on_delete=models.PROTECT, db_column='service_type_code')
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=50, blank=True, null=True)
    effective_from = models.DateField()    #TODO: Required here?
    effective_to = models.DateField()    #TODO: Required here?
    minimum_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)], blank=True, null=True)
    maximum_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)], blank=True, null=True)
    usage_type = models.CharField(max_length=50, blank=True, null=True) #oen time/time based etc    TODO: Master table?
    is_inventory = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_taxable = models.BooleanField(default=False)
    tax_code = models.CharField(max_length=50, blank=True, null=True)    #Applicable if is_taxable is true; TODO: Master table?
    #sample_source_code = models.CharField(max_length=50, blank=True, null=True) #only for diagnostic services (TODO: need to understand what this does)
    is_orderable = models.BooleanField(default=False)
    is_auto_post = models.BooleanField(default=False)
    is_appointment_required = models.BooleanField(default=False) #procedure master entry if yes
    is_bundling_allowed = models.BooleanField(default=False) #excluded from packages
    is_discount_allowed = models.BooleanField(default=False)
    is_component_type = models.BooleanField(default=False) #if component type is yes then other services have to be added to this
    
    class Meta:
        verbose_name = 'Service'
        verbose_name_plural = 'Services'
        db_table = 'service'
    def __str__(self):
        return str(self.primary_key)


class ComponentService(models.Model):
    """Defines Component Services that are a combination of multiple constituent Services."""

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    component_service = models.ForeignKey(Service, on_delete=models.PROTECT, db_column='component_service_pk')
    component = models.ForeignKey(Service, on_delete=models.PROTECT, db_column='component_pk', related_name='component')

    class Meta:
        constraints = [models.UniqueConstraint(fields=['component_service', 'component'], name='unique_component_service_and_component')]
        verbose_name = 'Component Service'
        verbose_name_plural = 'Component Services'
        db_table = 'component_service'
    def __str__(self):
        return str(self.primary_key)


#default provider and sharing need to be discussed
class ServicePrice(models.Model):
    """Defines Pricing for various Services offered, including Component Services."""

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, db_column='service_pk')
    #facility_id = 
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])    #TODO: Single default Currency assumed?
    effective_from = models.DateField()    #TODO: Confirm that this is mandatory and without need of a Time component
    effective_to = models.DateField()    #TODO: Confirm that this is mandatory and without need of a Time component
    unit = models.CharField(max_length=50, blank=True, null=True) #TODO: Create non-MDDS master table. User should be able to select among multiple Price-Unit combinations.
    resource_id = models.CharField(max_length=64, blank=True, null=True)
    patient_type = models.CharField(max_length=50, blank=True, null=True) #Note: Different patient types can have different rates
    #department_id = 
    #speciality_id = #Note: Will always be within a Department if both Department & Speciality exist for a Facility. TODO: Add table to maintain this mapping for each Facility.
    source_of_payment_code = models.CharField(max_length=2, blank=True, null=True)    #MDDS 05.006.0008, CD05.141 (2-chrarcter code)
    is_shareable = models.BooleanField(default=False) #If yes then Provider ID and Share Percentage must be set
    provider_id = models.CharField(max_length=50, blank=True, null=True) #Provider with whom the service cost will be shared
    share_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], blank=True, null=True)

    class Meta:
        verbose_name = 'Service Price'
        verbose_name_plural = 'Service Prices'
        db_table = 'service_price'
    def __str__(self):
        return str(self.primary_key)


# TODO: Add table to maintain linkage of Facility Specialty Code with Facility Service Codes (custom codes possible for both)

class ServiceDiscount(models.Model):
    """Defines applicable discounts on the prices of various Services offered."""

    class Type(models.IntegerChoices):
        Amount = 1
        Percentage = 2

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, db_column='service_pk')
    discount_type = models.PositiveSmallIntegerField(choices=Type.choices)    #MDDS 05.007.0027 (1-Amount, 2-Percentage)
    name = models.CharField(max_length=50, blank=True, null=True)
    value = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)], blank=True, null=True)
    coupon_code = models.CharField(max_length=50, blank=True, null=True)
    effective_from = models.DateTimeField()
    effective_to = models.DateTimeField()
    # TODO: Discounts at either Service or Bill level, Bill-level discount constraints - minimum Bill value and Max Discount Amount

    class Meta:
        verbose_name = 'Service Discount'
        verbose_name_plural = 'Service Discounts'
        db_table = 'service_discount'

    def __str__(self):
        return str(self.primary_key)


class ServiceTax(models.Model):
    """Defines Tax Rates applicable for the various Services on offer at a particular Facility."""

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, db_column='service_pk')
    tax_location = models.CharField(max_length=50, blank=True, null=True) #Note: Tax can vary by State Code (CD02.02)
    source_of_payment_code = models.CharField(max_length=2, blank=True, null=True)    #MDDS 05.006.0008, CD05.141 (2-chrarcter code)
    tax_rate = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.0), MaxValueValidator(100.0)])
    effective_from = models.DateTimeField()
    effective_to = models.DateTimeField()

    class Meta:
        verbose_name = 'Service Tax'
        verbose_name_plural = 'Service Taxes'
        db_table = 'service_tax'
    def __str__(self):
        return str(self.primary_key)
