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
    providerCreationDate = models.DateTimeField(null=True)
    providerStatus = models.IntegerField(default=0)
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


class Billing(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True)
    facilityId = models.ForeignKey(Facility, on_delete=models.CASCADE)
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    providerId = models.ManyToManyField('appointment_scheduling.Provider', related_name='bills')
    serviceType = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
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

class AppointmentDetails(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facilityId = models.ForeignKey(Facility, on_delete=models.CASCADE)
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    providerId = models.ForeignKey(Provider, on_delete=models.CASCADE)
    appointmentBookingStatusCode = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    appointmentProviderAvailabilityStatusCode = models.BooleanField(default=1)
    appointmentSessionAvailabilityStatusCode = models.BooleanField(default=1)
    resourceScheduleAvailabilityStatusCode = models.BooleanField(default=1)
    appointmentSessionStartDateTime = models.DateTimeField(null=True)
    appointmentSessionEndDateTime = models.DateTimeField(null=True)
    resourceScheduleStartDateTime = models.DateTimeField(null=True)
    resourceScheduleEndDateTime = models.DateTimeField(null=True)
    resourceType = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    appointmentRequestReferenceNumber = models.CharField(max_length=50, blank=True, null=True)
    appointmentRequestedDateTime = models.DateTimeField(null=True)
    appointmentChannel = models.CharField(max_length=20, blank=True, null=True)
    class Meta:
        verbose_name_plural = 'AppointmentDetails'
        db_table = 'AppointmentDetails'
    def __str__(self):
        return str(self.PrimaryKey)

class ProviderSchedule(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    providerId=models.ForeignKey(Provider, on_delete=models.CASCADE)
    #ResourceScheduleId=models.AutoField(primary_key=True)
    ResourceScheduleStartDate=models.DateTimeField(null=True)
    ResourceScheduleEndDate=models.DateTimeField(null=True)
    ResourceScheduleStartTime=models.CharField(max_length=10,default='09:00')
    ResourceScheduleEndTime=models.CharField(max_length=10,default='17:00')
    #Array of NonWorkingDates //Schedule creation will exclude non working days and leaves
    ResourceType= models.CharField(max_length=50,default='CareProvider')
    class Meta:
        verbose_name_plural = 'ProviderSchedule'
        db_table = 'ProviderSchedule'

    def __str__(self):
        return str(self.PrimaryKey)

class AppointmentSessionSlots(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    providerscheduleId=models.ForeignKey(ProviderSchedule, on_delete=models.CASCADE)
    #AppointmentSessionSlotsId=models.AutoField(primary_key=True)
    AppointmentSessionStartDate=models.DateField(null=True)
    AppointmentSessionStartTime =models.DateTimeField(null=True)
    AppointmentSessionEndTime=models.DateTimeField(null=True)
    AppointmentScheduleDate=models.DateTimeField(null=True)
    AppointmentBookingStatusCode =models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    AppointmentSessionAvailabilityStatusCode=models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    AppointmentProviderAvailabilityStatusCode=models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    class Meta:
        verbose_name_plural = 'AppointmentSessionSlots'
        db_table = 'AppointmentSessionSlots'

    def __str__(self):
        return str(self.PrimaryKey)


class Appointment(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #AppointmentId =models.AutoField(primary_key=True)
    facilityId = models.ForeignKey(Facility, on_delete=models.CASCADE)
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    providerId=models.ForeignKey(Provider, on_delete=models.CASCADE)
    appointmentsessionslotsId=models.ForeignKey(AppointmentSessionSlots, on_delete=models.CASCADE)
    AppointmentReferenceNumber=models.IntegerField(default=99, validators=[MaxValueValidator(99999)])
    AppointmentBookingDate=models.DateTimeField(null=True)
    AppointmentBookingTime=models.DateTimeField(null=True)
    AppointmentBookingStatusCode=models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    AppointmentChannel=models.CharField(max_length=50,default='Walkin')

    class Meta:
        verbose_name_plural = 'Appointment'
        db_table = 'Appointment'

    def __str__(self):
        return str(self.PrimaryKey)