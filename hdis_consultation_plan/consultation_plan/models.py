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
    careProviderLandlineTelephoneNumber = models.CharField(max_length=10, blank=True, null=True)
    registrationAuthorityNumber =models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    class Meta:
        verbose_name_plural = 'Provider'
        db_table = 'Provider'

    def __str__(self):
        return str(self.PrimaryKey)


class Person(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True)
    UniqueHealthIdentificationNumber = models.CharField(max_length=64)
    UniqueHealthIdentificationID = models.CharField(max_length=64)
    AlternateUniqueIdentificationNumberType = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    AlternateUniqueIdentificationNumber = models.CharField(max_length=18, null=True)
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

class Employee(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True)
    EmployeeID = models.CharField(max_length=18, blank=True, null=True)
    EmployerID = models.CharField(max_length=18, blank=True, null=True)
    PatientID = models.ManyToManyField(Patient)
    EmployeeTelephoneNumber = models.CharField(max_length=8, blank=True, null=True)
    EmployeeMobileNumber = models.CharField(max_length=10, blank=True, null=True)
    EmployeeEmailAddress = models.CharField(max_length=254, blank=True, null=True)
    EmployeeDesignationCode = models.CharField(max_length=2, blank=True, null=True)
    EmployeeOrganizationName = models.CharField(max_length=254, blank=True, null=True)
    EmployeeGenderCode = models.CharField(max_length=2, blank=True, null=True)
    EmployeeName = models.CharField(max_length=255, blank=True, null=True)
    AcademicQualificationLevelCode = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    AcademicQualificationTypeCode = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    AcademicQualification = models.TextField(null=True, blank=True)
    class Meta:
        verbose_name_plural = 'Employee'
        db_table = 'Employee'
    def __str__(self):
        return str(self.PrimaryKey)

class Billing(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True)
    facilityId = models.ForeignKey(Facility, on_delete=models.CASCADE)
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    providerId = models.ManyToManyField(Provider, related_name='bills')
    serviceType = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    serviceItemName = models.CharField(max_length=99, blank=True, null=True)
    quantityOfService = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Billing'
        db_table = 'Billing'

    def __str__(self):
        return str(self.PrimaryKey)


class Episode(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True)
    facilityId = models.ForeignKey(Facility, on_delete=models.CASCADE)
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    providerId = models.ManyToManyField(Provider, related_name='episodes')
    EpisodeId = models.CharField(max_length=64, blank=True, null=True)
    EpisodeType = models.IntegerField(default=1, validators=[MaxValueValidator(4)])

    class Meta:
        verbose_name_plural = 'Episode'
        db_table = 'Episode'

    def _str_(self):
        return str(self.PrimaryKey)

class Encounter(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True)
    episodeId = models.ForeignKey(Episode, on_delete=models.CASCADE)
    encounterID = models.CharField(max_length=64, blank=True, null=True)
    encounterType = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    encounterTypeDescription = models.CharField(max_length=254, blank=True, null=True)
    encounterTime = models.DateTimeField(null=True)
    # ideally should not be blank an encounter shoudl always have a status
    encounterStatusCode = models.CharField(max_length=20, default='planned')
    encounterStatusDisplay = models.CharField(max_length=35, default='Planned')
    encounterStatusDefinition = models.CharField(max_length=350, default='The Encounter has not yet started')
    class Meta:
        verbose_name_plural = 'Encounter'
        db_table = 'Encounter'

    def _str_(self):
        return str(self.PrimaryKey)


class Emergency(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True)
    episodeId = models.ForeignKey(Episode, on_delete=models.CASCADE)
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    encounterId = models.OneToOneField(Encounter, on_delete=models.CASCADE)
    providerId = models.ForeignKey(Provider, on_delete=models.CASCADE)
    patientArrivalDateTime = models.DateTimeField(null=True)
    patientStatus = models.IntegerField(default=9, validators=[MaxValueValidator(9)])
    ambulatoryStatus = models.CharField(max_length=2, blank=True, null=True)
    mlcIndicator = models.BooleanField(default=0)
    massInjuryIndicator = models.BooleanField(default=0)
    casueOfMassInjury = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    accidentLocation = models.CharField(max_length=254, blank=True, null=True)
    referralCategory = models.CharField(max_length=1, blank=True, null=True)
    dateOfReferral = models.DateTimeField(null=True)
    reasonForReferral = models.CharField(max_length=254, blank=True, null=True)
    class Meta:
        verbose_name_plural = 'Emergency'
        db_table = 'Emergency'
    def _str_(self):
        return str(self.PrimaryKey)

class clinicalNotes(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    encounterId = models.ForeignKey(Encounter, on_delete=models.CASCADE)
    authorDateTime = models.DateTimeField(null=True)
    clinicalNotesID = models.CharField(max_length=64, unique=True)
    reference = models.CharField(max_length=99, blank=True, null=True)
    informationSourceName = models.CharField(max_length=99, blank=True, null=True)
    clinicalDocument = models.TextField(blank=True, null=True)
    clinicalDocumentType = models.IntegerField(default=99, validators=[MaxValueValidator(99)])

    class Meta:
        verbose_name_plural = 'clinicalNotes'
        db_table = 'clinicalNotes'
    def _str_(self):
        return str(self.PrimaryKey)

class clinicalOrders(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinicalNotesId = models.OneToOneField(clinicalNotes, on_delete=models.CASCADE)
    clinicalOrderDescription = models.CharField(max_length=254, blank=True, null=True)
    orderId = models.CharField(max_length=12, blank=True, null=True)
    parentOrderId = models.CharField(max_length=10, blank=True, null=True)
    orderVerifyingCareProviderId = models.CharField(max_length=18, blank=True, null=True)
    orderStatus = models.CharField(max_length=2, blank=True, null=True)
    orderPriority = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    placerOrderId = models.CharField(max_length=10, blank=True, null=True)
    fillerOrderId = models.CharField(max_length=10, blank=True, null=True)
    class Meta:
        verbose_name_plural = 'clinicalOrders'
        db_table = 'clinicalOrders'
    def _str_(self):
        return str(self.PrimaryKey)

class lab(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinicalOrderId = models.ForeignKey(clinicalOrders, on_delete=models.CASCADE)
    labOrderCode = models.CharField(max_length=10, blank=True, null=True)
    labOrderName = models.CharField(max_length=256, blank=True, null=True)
    labId = models.IntegerField(default=9999999999, validators=[MaxValueValidator(9999999999)])
    labType = models.IntegerField(default=9, validators=[MaxValueValidator(9)])
    class Meta:
        verbose_name_plural = 'lab'
        db_table = 'lab'
    def _str_(self):
        return str(self.PrimaryKey)
class radiology(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinicalOrderId = models.ForeignKey(clinicalOrders, on_delete=models.CASCADE)
    radiologyCenterId = models.IntegerField(default=9999999999, validators=[MaxValueValidator(9999999999)])
    radiologyCenterType = models.IntegerField(default=9, validators=[MaxValueValidator(9)])
    radiologyProcedureName = models.CharField(max_length=255, blank=True, null=True)
    radiologyProcedureCode = models.CharField(max_length=18, blank=True, null=True)
    class Meta:
        verbose_name_plural = 'radiology'
        db_table = 'radiology'

    def _str_(self):
        return str(self.PrimaryKey)
class pharmacy(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinicalOrderId = models.ForeignKey(clinicalOrders, on_delete=models.CASCADE)
    drugClassificationCode = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    routeOfAdministration = models.CharField(max_length=6, blank=True, null=True)
    medicationFrequency = models.CharField(max_length=5, blank=True, null=True)
    medicationAdministrationInterval = models.CharField(max_length=40, blank=True, null=True)
    dose = models.CharField(max_length=60, blank=True, null=True)
    medicationStoppedIndicator = models.IntegerField(default=9, validators=[MaxValueValidator(9)])
    bodySite = models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    medicationStatus = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    patientInstructions = models.CharField(max_length=255, blank=True, null=True)
    prescriptionId = models.CharField(max_length=20, blank=True, null=True)
    orderDateTime = models.DateTimeField(null=True)
    indication = models.CharField(max_length=10, blank=True, null=True)
    contraindication = models.CharField(max_length=10, blank=True, null=True)
    medicationFills = models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    medicationInstructions = models.CharField(max_length=254, blank=True, null=True)
    fillStatus = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    class Meta:
        verbose_name_plural = 'pharmacy'
        db_table = 'pharmacy'

    def _str_(self):
        return str(self.PrimaryKey)
class immunizationOrder(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinicalOrderId = models.ForeignKey(clinicalOrders, on_delete=models.CASCADE)
    immunizationRefusalReason = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    immunizationAdministrationDateTime = models.DateTimeField(null=True)
    immunizationPerformerIdentificationNumber = models.CharField(max_length=18, blank=True, null=True)
    immunizationProductCode = models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    immunizationProductDescription = models.CharField(max_length=99, blank=True, null=True)
    medicationSeriesNumber = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    immunizationInformationSource = models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    class Meta:
        verbose_name_plural = 'immunizationOrder'
        db_table = 'immunizationOrder'

    def _str_(self):
        return str(self.PrimaryKey)
class procedure(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinicalOrderId = models.ForeignKey(clinicalOrders, on_delete=models.CASCADE)
    procedureName = models.CharField(max_length=255, blank=True, null=True)
    procedureModifier = models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    procedureCode = models.CharField(max_length=18, blank=True, null=True)
    procedureType = models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    procedureTypeDescription = models.CharField(max_length=99, blank=True, null=True)
    procedureDateTime = models.DateTimeField(null=True)
    multipleProcedureFlag = models.BooleanField(default=0)
    class Meta:
        verbose_name_plural = 'procedure'
        db_table = 'procedure'

    def _str_(self):
        return str(self.PrimaryKey)

class orderSet(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True)
    facilityId = models.ForeignKey(Facility, on_delete=models.CASCADE)
    providerId = models.CharField(max_length=99, blank=True, null=True)
    orderSetName = models.CharField(max_length=255, blank=True, null=True)
    orderSetType = models.CharField(max_length=99, blank=True, null=True)
    diagnosisConditionName = models.CharField(max_length=99, blank=True, null=True)
    class Meta:
        verbose_name_plural = 'orderSet'
        db_table = 'orderSet'
    def _str_(self):
        return str(self.PrimaryKey)

class orderSetMedicine(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    orderSetId = models.ForeignKey(orderSet, on_delete=models.CASCADE)
    drugClassificationCode = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    routeOfAdministration = models.CharField(max_length=6, blank=True, null=True)
    medicationFrequency = models.CharField(max_length=5, blank=True, null=True)
    medicationAdministrationInterval = models.CharField(max_length=40, blank=True, null=True)
    dose = models.CharField(max_length=60, blank=True, null=True)
    medicationStoppedIndicator = models.IntegerField(default=9, validators=[MaxValueValidator(9)])
    bodySite = models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    medicationStatus = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    patientInstructions = models.CharField(max_length=255, blank=True, null=True)
    prescriptionId = models.CharField(max_length=20, blank=True, null=True)
    orderDateTime = models.DateTimeField(null=True)
    indication = models.CharField(max_length=10, blank=True, null=True)
    contraindication = models.CharField(max_length=10, blank=True, null=True)
    medicationFills = models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    medicationInstructions = models.CharField(max_length=254, blank=True, null=True)
    fillStatus = models.IntegerField(default=99, validators=[MaxValueValidator(99)])

    class Meta:
        verbose_name_plural = 'orderSetMedicine'
        db_table = 'orderSetMedicine'

    def _str_(self):
        return str(self.PrimaryKey)

class orderSetLab(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    orderSetId = models.ForeignKey(orderSet, on_delete=models.CASCADE)
    labOrderCode = models.CharField(max_length=10, blank=True, null=True)
    labId = models.IntegerField(default=9999999999, validators=[MaxValueValidator(9999999999)])
    labType = models.IntegerField(default=9, validators=[MaxValueValidator(9)])

    class Meta:
        verbose_name_plural = 'orderSetLab'
        db_table = 'orderSetLab'

    def _str_(self):
        return str(self.PrimaryKey)

class orderSetRadiology(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    orderSetId = models.ForeignKey(orderSet, on_delete=models.CASCADE)
    radiologyCenterId = models.IntegerField(default=9999999999, validators=[MaxValueValidator(9999999999)])
    radiologyCenterType = models.IntegerField(default=9, validators=[MaxValueValidator(9)])
    radiologyProcedureName = models.CharField(max_length=255, blank=True, null=True)
    radiologyProcedureCode = models.CharField(max_length=18, blank=True, null=True)

    class Meta:
        verbose_name_plural = 'orderSetRadiology'
        db_table = 'radiorderSetRadiologyology'

    def _str_(self):
        return str(self.PrimaryKey)

class orderSetImmunizationOrder(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    orderSetId = models.ForeignKey(orderSet, on_delete=models.CASCADE)
    immunizationRefusalReason = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    immunizationAdministrationDateTime = models.DateTimeField(null=True)
    immunizationPerformerIdentificationNumber = models.CharField(max_length=18, blank=True, null=True)
    immunizationProductCode = models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    immunizationProductDescription = models.CharField(max_length=99, blank=True, null=True)
    medicationSeriesNumber = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    immunizationInformationSource = models.IntegerField(default=999, validators=[MaxValueValidator(999)])

    class Meta:
        verbose_name_plural = 'orderSetImmunizationOrder'
        db_table = 'orderSetImmunizationOrder'

    def _str_(self):
        return str(self.PrimaryKey)

class orderSetProcedure(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    orderSetId = models.ForeignKey(orderSet, on_delete=models.CASCADE)
    procedureName = models.CharField(max_length=255, blank=True, null=True)
    procedureModifier = models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    procedureCode = models.CharField(max_length=18, blank=True, null=True)
    procedureType = models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    procedureTypeDescription = models.CharField(max_length=99, blank=True, null=True)
    procedureDateTime = models.DateTimeField(null=True)
    multipleProcedureFlag = models.BooleanField(default=0)
    class Meta:
        verbose_name_plural = 'orderSetProcedure'
        db_table = 'orderSetProcedure'
    def _str_(self):
        return str(self.PrimaryKey)
class outreach(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True)
    encounterId = models.ForeignKey(Encounter, on_delete=models.CASCADE)
    outreachServiceDeliveryPlaceName = models.CharField(max_length=99, blank=True, null=True)
    outreachServiceDeliveryPlaceAddress = models.CharField(max_length=255, blank=True, null=True)
    outreachServiceDeliveryPlaceType = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    outreachServicePurpose = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    outreachServiceProviderName = models.CharField(max_length=99, blank=True, null=True)
    outreachServiceProviderType = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    outreachServiceProviderIdentificationNumber = models.CharField(max_length=20, blank=True, null=True)
    referralSupportIndicator = models.BooleanField(default=0)
    class Meta:
        verbose_name_plural = 'outreach'
        db_table = 'outreach'
    def _str_(self):
        return str(self.PrimaryKey)