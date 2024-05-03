import datetime
import uuid
from django.db import models
from django.core.validators import MaxValueValidator

def current_time():
    """
    Callable used to set the default time for TimeFields to the current time. 
    Note that Timezone awareness of the return value will be based on the USE_TZ setting.
    """
    return datetime.datetime.now().time()


class EncounterProvider(models.Model):
    """ Tracks the Provider(s) associated with a Consultation Encounter. """

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    encounter_id = models.UUIDField()
    provider_id = models.UUIDField()
    
    class Meta:
        verbose_name = 'Encounter Provider'
        verbose_name_plural = 'Encounter Providers'
        db_table = 'encounter_provider'
        unique_together = ('encounter_id', 'provider_id',)

    def _str_(self):
        return str(self.primary_key)


class ClinicalNote(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    encounter_id = models.UUIDField()
    author_datetime = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=99, blank=True, null=True)
    information_source_name = models.CharField(max_length=99, blank=True, null=True)
    clinical_document = models.TextField(blank=True, null=True)
    clinical_document_type = models.PositiveSmallIntegerField(default=18, validators=[MaxValueValidator(99)])

    class Meta:
        verbose_name = 'Clinical Note'
        verbose_name_plural = 'Clinical Notes'
        db_table = 'clinical_note'
    
    def _str_(self):
        return str(self.primary_key)


class Examination(models.Model):
    """ Each Examination Type will have specific Templates for data capture based on Specialty. """

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinical_note = models.ForeignKey(ClinicalNote, on_delete=models.CASCADE, related_name='examinations')
    examination_type = models.PositiveSmallIntegerField(default=999, validators=[MaxValueValidator(999)])    #Optional field
    examination_finding = models.TextField()    #Mandatory field
    examined_system = models.PositiveSmallIntegerField(default=99, validators=[MaxValueValidator(99)])    #Optional field
    body_site_name = models.CharField(max_length=60, blank=True, null=True)
    # TODO: Check whether Author details are required. Not included in LSRF spec.
    #author_datetime = models.DateTimeField(default=datetime.datetime.now)
    #author_id = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        verbose_name = 'Examination'
        verbose_name_plural = 'Examinations'
        db_table = 'examination'
    
    def _str_(self):
        return str(self.primary_key)


class VitalSign(models.Model):
    """ Typically a Facility would capture a specific subset of Vital parameters as per their Specialty for each Patient. """

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinical_note = models.ForeignKey(ClinicalNote, on_delete=models.CASCADE, related_name='vital_signs')
    result_id = models.IntegerField(blank=True, null=True)
    result_date = models.DateField(default=datetime.date.today)
    result_time = models.TimeField(default=current_time)
    result_type = models.CharField(max_length=2, blank=True, null=True)    #MDDS CD05.041
    result_type_name = models.CharField(max_length=99, blank=True, null=True)
    result_status = models.CharField(max_length=128, blank=True, null=True)    #MDDS CD05.038
    result_value = models.CharField(max_length=20, blank=True, null=True)
    result_unit = models.CharField(max_length=10, blank=True, null=True)
    result_interpretation = models.PositiveSmallIntegerField(default=99, validators=[MaxValueValidator(99)])
    result_reference_range_lower_limit = models.PositiveSmallIntegerField(default=999, validators=[MaxValueValidator(999)])
    result_reference_range_upper_limit = models.PositiveSmallIntegerField(default=999, validators=[MaxValueValidator(999)])

    class Meta:
        verbose_name = 'Vital Sign'
        verbose_name_plural = 'Vital Signs'
        db_table = 'vital_sign'
    
    def _str_(self):
        return str(self.primary_key)


class LabResult(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinical_note = models.ForeignKey(ClinicalNote, on_delete=models.CASCADE, related_name='lab_results')
    result_datetime = models.DateTimeField(null=True)
    result_type = models.CharField(max_length=10, blank=True, null=True)
    result_status = models.CharField(max_length=2, blank=True, null=True)
    result_value = models.CharField(max_length=20, blank=True, null=True)
    result_interpretation = models.PositiveSmallIntegerField(default=99, validators=[MaxValueValidator(99)])
    result_reference_range_lower_limit = models.IntegerField(default=9999999, validators=[MaxValueValidator(9999999)])
    result_reference_range_upper_limit = models.IntegerField(default=9999999, validators=[MaxValueValidator(9999999)])
    result_category = models.CharField(max_length=10, blank=True, null=True)
    specimen_type = models.PositiveSmallIntegerField(default=999, validators=[MaxValueValidator(999)])
    lab_order_code = models.CharField(max_length=10, blank=True, null=True)
    lab_id = models.PositiveSmallIntegerField(default=0)
    lab_type = models.PositiveSmallIntegerField(default=9, validators=[MaxValueValidator(9)])
    lab_result_id = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'Lab Result'
        verbose_name_plural = 'Lab Results'
        db_table = 'lab_result'
    
    def _str_(self):
        return str(self.primary_key)


class RadiologyResult(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinical_note = models.ForeignKey(ClinicalNote, on_delete=models.CASCADE, related_name='radiology_results')
    radiology_center_id = models.PositiveSmallIntegerField(default=0)
    radiology_center_type = models.PositiveSmallIntegerField(default=9, validators=[MaxValueValidator(9)])
    radiology_procedure_datetime = models.DateTimeField(null=True)
    radiology_technician_comments = models.CharField(max_length=99, blank=True, null=True)
    radiologist_impression = models.CharField(max_length=254, blank=True, null=True)
    radiology_procedure_name = models.CharField(max_length=255, blank=True, null=True)
    radiology_procedure_code = models.CharField(max_length=18, blank=True, null=True)
    radiology_result_status = models.CharField(max_length=3, blank=True, null=True)
    radiology_result_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = 'Radiology Result'
        verbose_name_plural = 'Radiology Results'
        db_table = 'radiology_result'
    
    def _str_(self):
        return str(self.primary_key)
