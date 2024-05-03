from django.db import models
from django.core.validators import MaxValueValidator
import uuid

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


class Diagnosis(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinical_note = models.ForeignKey(ClinicalNote, on_delete=models.CASCADE, related_name='diagnoses')
    health_condition_type = models.CharField(max_length=20, blank=True, null=True) #MDDS CD05.022
    health_condition_name = models.CharField(max_length=99, blank=True, null=True) #MDDS CD05.019
    health_condition_code = models.CharField(max_length=10, blank=True, null=True) #MDDS CD05.019 (ICD-10 Codes)
    health_condition_description = models.CharField(max_length=254, blank=True, null=True)
    health_condition_category = models.CharField(max_length=20, blank=True, null=True)
    health_condition_status = models.CharField(max_length=20, blank=True, null=True) #MDDS CD05.021
    diagnosis_priority = models.CharField(max_length=20, blank=True, null=True)
    #comorbidityIndicator = models.BooleanField(default=0)
    #comorbidityCode = models.CharField(max_length=10, blank=True, null=True)
    present_health_condition_onset_date = models.DateField(null=True)

    class Meta:
        verbose_name = 'Diagnosis'
        verbose_name_plural = 'Diagnoses'
        db_table = 'diagnosis'
    
    def _str_(self):
        return str(self.primary_key)
