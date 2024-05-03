import uuid
import random
from django.db import models
from django.core.validators import MaxValueValidator

class Employee(models.Model):
    """Represents an employee of a Healthcare Facility with various Roles such as Doctor / Nurse / Pharmacist."""

    class Status(models.IntegerChoices):
        Inactive = 0
        Active = 1
        UnderReview = 2
        MissingInfo = 3
        Blacklisted = 4

    def generate_employee_id():
        """Randomly generates a new Employee ID in the applicable format and ensures that the generated ID is not pre-existing."""
        while True:
            eid = "E" + str(random.randint(100000000, 999999999))
            if not Employee.objects.filter(employee_id=eid).exists():
                return eid

    employee_id = models.CharField(primary_key=True, max_length=16, default=generate_employee_id)    #Supports specifying or auto-generating ID when creating a new Employee
    facility_id = models.UUIDField(blank=False, null=False)
    member_username = models.CharField(max_length=150, unique=True, blank=True, null=True) #TODO: Make non-nullable
    medical_specialty_type_code = models.IntegerField(blank=True, null=True, default=999, validators=[MaxValueValidator(999)]) #MDDS CD05.011    #TODO: Make Foerign Key
    bank_details = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=10, blank=True, null=True)
    languages_known = models.CharField(max_length=255, blank=True, null=True)
    current_city = models.CharField(max_length=18, blank=True, null=True)    
    status = models.IntegerField(choices=Status.choices, default=Status.Inactive)

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'
        db_table = 'employee'
    
    def __str__(self):
        return str(self.employee_id)
    
    def save(self, *args, **kwargs):
        if self.employee_id is None:    #Generate Employee ID if not provided
            while True:
                generated_employee_id = 'E' + str(random.randint(100000000, 999999999))
                if not Employee.objects.filter(employee_id=generated_employee_id).exists(): break

        super().save(*args, **kwargs)


class EmployeeDocuments(models.Model):
    """Documents pertaining to an Employee of a Healthcare Facility."""

    class DocumentType(models.IntegerChoices):
        Other = 0
        RegistrationCertificate = 1
        
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_id = models.ForeignKey(Employee, blank=False, null=False, on_delete=models.CASCADE)
    document_type = models.IntegerField(choices=DocumentType.choices, blank=False, null=False)
    document_file = models.FileField(upload_to='EmployeeDocuments/', blank=False, null=False)   #TODO: Access control on upload folder; per-user subfolders

    class Meta:
        verbose_name = 'Employee Documents'
        db_table = 'employee_documents'
    def __str__(self):
        return str(self.primary_key)


class EmployeeQualifications(models.Model):
    """Educational / Professional qualifications of an Employee with relevant certificate, if any."""

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    employee_id = models.ForeignKey(Employee, blank=False, null=False, on_delete=models.CASCADE)
    degree = models.CharField(max_length=125, blank=True, null=True)
    institute = models.CharField(max_length=250, blank=True, null=True)
    qualification_year = models.CharField(max_length=4, blank=True, null=True)
    certificate_file = models.FileField(upload_to='EmployeeQualifications/', blank=True, null=True)

    class Meta:
        verbose_name = 'Employee Qualification Details'
        db_table = 'employee_qualification_details'
    def __str__(self):
        return str(self.primary_key)


class RegistrationCouncil(models.Model):
    """Represents an authority (typically at State level) that assigns a Provider a Registration Number."""
    
    code = models.CharField(primary_key=True, max_length=16)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        verbose_name = 'Registration Council'
        verbose_name_plural = 'Registration Councils'
        db_table = 'registration_council'
    def __str__(self):
        return str(self.code)


class SpecialtyType(models.Model):
    """Master data for the medical specialization of a Provider such as General Medicine, Nursing, Pharmacy."""
    
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        managed = False
        verbose_name = 'Specialty Type'
        verbose_name_plural = 'Specialty Types'
        db_table = 'specialty_type'
    def __str__(self):
        return str(self.code)


class Provider(Employee):
    """Represents a Healthcare Provider such as a Doctor, Nurse, Pharmacist, Radiologist."""
    
    # Dev Note: Reference to superclass available via automatically added 'employee_ptr' attribute.
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    unique_individual_health_care_provider_number = models.CharField(max_length=64, blank=True, null=True)
    abha_health_id = models.CharField(max_length=14, blank=True, null=True)
    health_care_provider_role_code = models.IntegerField(default=99, validators=[MaxValueValidator(99)], blank=True, null=False)
    health_care_provider_role_freetext = models.CharField(max_length=99, blank=True, null=True)    #Tentative alternative to standard Role Code
    health_care_provider_type = models.IntegerField(default=9999, validators=[MaxValueValidator(9999)]) #MDDS CD05.010
    registration_council_code = models.CharField(max_length=255, blank=True, null=True)
    registration_number = models.CharField(max_length=240, blank=True, null=True) #State level number that is usually available
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Provider'
        verbose_name_plural = 'Providers'
        db_table = 'provider'
    def __str__(self):
        return str(self.primary_key)


class DoctorFieldDetails(models.Model):
    """Temporarily used to demonstrate configurable field display in the UI."""
    
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctorType = models.BooleanField(default=True)
    doctorRegistration = models.BooleanField(default=True)
    doctorRegistrationCertificate = models.BooleanField(default=True)
    doctorLanguage = models.BooleanField(default=False)
    doctorCity = models.BooleanField(default=False)
    doctorSpeciality = models.BooleanField(default=False)
    doctorQualification = models.BooleanField(default=True)
    doctorDescription = models.BooleanField(default=False)
    doctorImage = models.BooleanField(default=False)
    doctorSignatures = models.BooleanField(default=False)
    doctorSchedule = models.BooleanField(default=False)
    doctorBankDetails = models.BooleanField(default=False)
    doctorLeaves = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Doctor Field Details'
        db_table = 'doctor_field_details'
    def __str__(self):
        return str(self.primary_key)
