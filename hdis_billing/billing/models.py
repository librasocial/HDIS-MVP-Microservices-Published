from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
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

class Billing(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facilityId = models.ForeignKey(Facility, on_delete=models.CASCADE)
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    providerId = models.ManyToManyField(Provider, related_name='Billing')
    serviceType = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    serviceItemPrice = models.FloatField(default=99, validators=[MinValueValidator(0.0)])
    serviceItemName = models.CharField(max_length=99, blank=True, null=True)
    packageItemName = models.CharField(max_length=99, blank=True, null=True)
    packageItemPrice = models.FloatField(validators=[MinValueValidator(0.0)])
    quantityOfService = models.CharField(max_length=50, blank=True, null=True)
    totalBillAmount = models.FloatField(validators=[MinValueValidator(0.0)], blank=True, null=True)
    class Meta:
        verbose_name_plural = 'Billing'
        db_table = 'Billing'
    def __str__(self):
        return str(self.PrimaryKey)

class Payment(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    #SourceOfPaymentID = models.IntegerField(primary_key=True)
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    InsuredCardID = models.CharField(max_length=18, blank=True, null=True)
    TPACode = models.CharField(max_length=18, blank=True, null=True)
    TPAName = models.CharField(max_length=99, blank=True, null=True)
    InsurancePolicyTypeCode = models.CharField(max_length=18, blank=True, null=True)
    HealthPlanTypeCode = models.CharField(max_length=18, blank=True, null=True)
    InsurancePolicyID = models.CharField(max_length=18, blank=True, null=True)
    InsurancePolicyName = models.CharField(max_length=99, blank=True, null=True)
    SourceOfPayment = models.CharField(max_length=18, blank=True, null=True)
    SecondaryPolicyIndicator = models.CharField(max_length=18, blank=True, null=True)
    ListofSecondaryPolicyID = models.CharField(max_length=18, blank=True, null=True)
    totalClaimAmount = models.FloatField(validators=[MinValueValidator(0.0)])
    claimBillID = models.CharField(max_length=18, blank=True, null=True)
    billType = models.CharField(max_length=18, blank=True, null=True)
    typeOfHospital = models.CharField(max_length=18, blank=True, null=True)
    claimsDocumentsSubmissionCheckList = models.CharField(max_length=18, blank=True, null=True)
    patientEmployeeID = models.CharField(max_length=18, blank=True, null=True)
    class Meta:
        verbose_name_plural = 'Payment'
        db_table = 'Payment'
    def __str__(self):
        return str(self.PrimaryKey)

class Bills(models.Model):
    PrimaryKey = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    facilityId = models.ForeignKey(Facility, on_delete=models.CASCADE)
    patientId = models.ForeignKey(Patient, on_delete=models.CASCADE)
    providerId = models.ManyToManyField(Provider, related_name='bills')
    billDate = models.DateTimeField(null=True)
    billGenerationType = models.CharField(max_length=18, blank=True, null=True)
    billCopyType = models.CharField(max_length=18, blank=True, null=True)
    reasonforDuplicateBillCopy = models.CharField(max_length=18, blank=True, null=True)
    approvalIndicatorforDuplicateBillCopy = models.BooleanField(default=0)
    tariffCategory = models.CharField(max_length=18, blank=True, null=True)
    serviceType = models.CharField(max_length=18, blank=True, null=True)
    paymentType = models.CharField(max_length=18, blank=True, null=True)
    sponsoringEntity = models.CharField(max_length=18, blank=True, null=True)
    approvingEntity = models.CharField(max_length=18, blank=True, null=True)
    insuranceCompanyName = models.CharField(max_length=18, blank=True, null=True)
    insuranceCompanyCode = models.CharField(max_length=18, blank=True, null=True)
    sponsorApprovalIndicator = models.CharField(max_length=18, blank=True, null=True)
    serviceItemName = models.CharField(max_length=18, blank=True, null=True)
    serviceItemPrice = models.FloatField(validators=[MinValueValidator(0.0)])
    packageItemName= models.CharField(max_length=18, blank=True, null=True)
    packageItemPrice = models.FloatField(validators=[MinValueValidator(0.0)])
    quantityofService = models.FloatField(validators=[MinValueValidator(0.0)])
    tax = models.FloatField(validators=[MinValueValidator(0.0)])
    totalBilledAmount = models.FloatField(validators=[MinValueValidator(0.0)])
    discountApprovalIndicator = models.BooleanField(default=0)
    discountApproverName = models.CharField(max_length=18, blank=True, null=True)
    discountIndicator = models.BooleanField(default=0)
    discount = models.FloatField(validators=[MinValueValidator(0.0)])
    discountRemark = models.CharField(max_length=18, blank=True, null=True)
    advanceDepositAmount = models.FloatField(validators=[MinValueValidator(0.0)])
    balancePayable = models.FloatField(validators=[MinValueValidator(0.0)])
    amountPayablebyPatient = models.FloatField(validators=[MinValueValidator(0.0)])
    amountPayablebySponsor = models.FloatField(validators=[MinValueValidator(0.0)])
    amountPaidbyPatient = models.FloatField(validators=[MinValueValidator(0.0)])
    patientDues = models.FloatField(validators=[MinValueValidator(0.0)])
    transactionID = models.CharField(max_length=18, blank=True, null=True)
    class Meta:
        verbose_name_plural = 'Bills'
        db_table = 'Bills'
    def __str__(self):
        return str(self.PrimaryKey)
