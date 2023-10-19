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
    #clinicalNotesID = models.CharField(max_length=64, unique=True)
    clinicalDocument = models.TextField(blank=True, null=True)
    clinicalDocumentType = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    class Meta:
        verbose_name_plural = 'clinicalNotes'
        db_table = 'clinicalNotes'
    def _str_(self):
        return str(self.PrimaryKey)

class examination(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinicalNotesId = models.ForeignKey(clinicalNotes, on_delete=models.CASCADE)
    examinationType = models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    examinationFinding = models.TextField(blank=True, null=True)
    examinationSystem = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    bodySiteName = models.CharField(max_length=60, blank=True, null=True)
    #authorDateTime = models.DateTimeField(null=True)
    authorId = models.CharField(max_length=32, blank=True, null=True)
    class Meta:
        verbose_name_plural = 'examination'
        db_table = 'examination'
    def _str_(self):
        return str(self.PrimaryKey)

class vitalSigns(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinicalNotesId = models.ForeignKey(clinicalNotes, on_delete=models.CASCADE)
    #vitalSignResultTime = models.DateTimeField(null=True)
    vitalSignResultType = models.CharField(max_length=2, blank=True, null=True)
    vitalSignResultTypeName = models.CharField(max_length=99, blank=True, null=True)
    vitalSignResultStatus = models.CharField(max_length=128, blank=True, null=True)
    vitalSignResultValue = models.CharField(max_length=20, blank=True, null=True)
    vitalSignResultUnit = models.CharField(max_length=10, blank=True, null=True)
    vitalSignResultInterpretation = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    vitalSignResultReferenceRangeLowerLimit = models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    vitalSignResultReferenceRangeUpperLimit = models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    #vitalSignResultDate = models.DateTimeField(null=True)
    #vitalSignResultId = models.IntegerField(default=9999999999, validators=[MaxValueValidator(9999999999)])
    class Meta:
        verbose_name_plural = 'vitalSigns'
        db_table = 'vitalSigns'
    def _str_(self):
        return str(self.PrimaryKey)

class lab(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinicalNotesId = models.ForeignKey(clinicalNotes, on_delete=models.CASCADE)
    #resultDateTime = models.DateTimeField(null=True)
    resultType = models.CharField(max_length=10, blank=True, null=True)
    resultStatus = models.CharField(max_length=2, blank=True, null=True)
    resultValue = models.CharField(max_length=20, blank=True, null=True)
    resultInterpretation = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    resultReferenceRangeLowerLimit = models.IntegerField(default=9999999, validators=[MaxValueValidator(9999999)])
    resultReferenceRangeUpperLimit = models.IntegerField(default=9999999, validators=[MaxValueValidator(9999999)])
    resultCategory = models.CharField(max_length=10, blank=True, null=True)
    specimenType = models.IntegerField(default=999, validators=[MaxValueValidator(999)])
    labOrderCode = models.CharField(max_length=10, blank=True, null=True)
    labId = models.IntegerField(default=9999999999, validators=[MaxValueValidator(9999999999)])
    labType = models.IntegerField(default=9, validators=[MaxValueValidator(9)])
    labResultId = models.CharField(max_length=20, blank=True, null=True)
    class Meta:
        verbose_name_plural = 'lab'
        db_table = 'lab'
    def _str_(self):
        return str(self.PrimaryKey)
class radiology(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinicalNotesId = models.ForeignKey(clinicalNotes, on_delete=models.CASCADE)
    radiologyCenterId = models.IntegerField(default=9999999999, validators=[MaxValueValidator(9999999999)])
    radiologyCenterType = models.IntegerField(default=9, validators=[MaxValueValidator(9)])
    #radiologyProcedureDateTime = models.DateTimeField(null=True)
    radiologyTechnicianComments = models.CharField(max_length=99, blank=True, null=True)
    radiologistImpression = models.CharField(max_length=254, blank=True, null=True)
    radiologyProcedureName = models.CharField(max_length=255, blank=True, null=True)
    radiologyProcedureCode = models.CharField(max_length=18, blank=True, null=True)
    radiologyResultStatus = models.CharField(max_length=3, blank=True, null=True)
    radiologyResultId = models.CharField(max_length=10, blank=True, null=True)
    class Meta:
        verbose_name_plural = 'radiology'
        db_table = 'radiology'
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