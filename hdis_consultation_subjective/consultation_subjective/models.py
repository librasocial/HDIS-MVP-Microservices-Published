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
        return str(self.PrimaryKey)


class Emergency(models.Model):  #Dev Note: Not currently in use
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    episode_id = models.UUIDField(blank=True, null=True)
    encounter_id = models.UUIDField(blank=True, null=True)
    patient_id = models.CharField(max_length=18)
    provider_id = models.CharField(max_length=64)
    patient_arrival_datetime = models.DateTimeField(null=True)
    patient_status = models.IntegerField(default=9, validators=[MaxValueValidator(9)])
    ambulatory_status = models.CharField(max_length=2, blank=True, null=True)
    mlc_indicator = models.BooleanField(default=0)
    mass_injury_indicator = models.BooleanField(default=0)
    cause_of_mass_injury = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    accident_location = models.CharField(max_length=254, blank=True, null=True)
    referral_category = models.CharField(max_length=1, blank=True, null=True)
    date_of_referral = models.DateTimeField(null=True)
    reason_for_referral = models.CharField(max_length=254, blank=True, null=True)

    class Meta:
        verbose_name = 'Emergency'
        verbose_name_plural = 'Emergencies'
        db_table = 'emergency'
    def _str_(self):
        return str(self.primary_key)


class ClinicalNote(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    encounter_id = models.UUIDField()
    author_datetime = models.DateTimeField(auto_now_add=True)
    #clinical_notes_id = models.CharField(max_length=64, unique=True)
    reference = models.CharField(max_length=99, blank=True, null=True)
    information_source_name = models.CharField(max_length=99, blank=True, null=True)
    clinical_document = models.TextField(blank=True, null=True)
    clinical_document_type = models.IntegerField(default=18, validators=[MaxValueValidator(99)]) #Dev NOte: Code 18 represents generic "Clinical note"
    #family_member_multiple_birth_status = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    #family_member_multiple_birth_order = models.IntegerField(default=99, validators=[MaxValueValidator(99)])

    class Meta:
        verbose_name = 'Clinical Note'
        verbose_name_plural = 'Clinical Notes'
        db_table = 'clinical_note'
    def _str_(self):
        return str(self.primary_key)


class FamilyHistory(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinical_note = models.ForeignKey(ClinicalNote, on_delete=models.CASCADE, related_name='family_histories')
    family_member_uid_number = models.CharField(max_length=18, blank=True, null=True)
    family_member_relationship = models.CharField(max_length=128, blank=True, null=True)
    health_condition_code = models.CharField(max_length=10, blank=True, null=True)
    family_member_health_condition = models.CharField(max_length=100, blank=True, null=True)
    family_member_age_at_onset = models.CharField(max_length=9, default="999,99,99")
    family_member_health_condition_status = models.CharField(max_length=24, blank=True, null=True)    #MDDS CD05.021
    cause_of_death_known = models.BooleanField(default=False)
    family_member_age_at_death = models.CharField(max_length=9, default="999,99,99")
    attachments = models.FileField(upload_to='eObjectsFiles/', blank=True, null=True)

    class Meta:
        verbose_name = 'Family History'
        verbose_name_plural = 'Family Histories'
        db_table = 'family_history'
    def __str__(self):
        return str(self.primary_key)


class PatientComorbidity(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinical_note = models.ForeignKey(ClinicalNote, on_delete=models.CASCADE, related_name='patient_comorbidities')
    comorbidity_health_condition_code = models.CharField(max_length=10, blank=True, null=True)
    comorbidity_health_condition = models.CharField(max_length=100, blank=True, null=True)
    comorbidity_health_condition_status = models.CharField(max_length=10, blank=True, null=True)
    age_at_onset_of_health_condition = models.CharField(max_length=9, default="999,99,99")
    procedure_performed = models.CharField(max_length=128, blank=True, null=True)
    procedure_date = models.DateTimeField(null=True)
    patient_disposition_after_procedure = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        verbose_name = 'Patient Comorbidity'
        verbose_name_plural = 'Patient Comorbidities'
        db_table = 'patient_comorbidity'
    def __str__(self):
        return str(self.primary_key)


class ChiefComplaint(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinical_note = models.ForeignKey(ClinicalNote, on_delete=models.CASCADE, related_name='chief_complaints')
    chief_complaint_id = models.CharField(max_length=50, blank=True, null=True)
    chief_complaint_name = models.CharField(max_length=100, blank=True, null=True)
    chief_complaint_body_site = models.CharField(max_length=10, blank=True, null=True)
    chief_complaint_duration = models.CharField(max_length=3, blank=True, null=True)
    chief_complaint_duration_unit = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = 'Chief Complaint'
        verbose_name_plural = 'Chief Complaints'
        db_table = 'chief_complaint'
    def __str__(self):
        return str(self.primary_key)


class SocialHistory(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinical_note = models.ForeignKey(ClinicalNote, on_delete=models.CASCADE, related_name='social_histories')
    habit_description = models.CharField(max_length=255, blank=True, null=True)
    habit_type = models.CharField(max_length=12, blank=True, null=True)
    onset_since = models.DateTimeField(null=True)
    current_status = models.CharField(max_length=12, blank=True, null=True)
    smoking_frequency = models.CharField(max_length=10, blank=True, null=True)
    alcohol_intake_frequency = models.CharField(max_length=10, blank=True, null=True)
    class Meta:
        verbose_name = 'Social History'
        verbose_name_plural = 'Social Histories'
        db_table = 'social_history'
    def __str__(self):
        return str(self.primary_key)


class Complication(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinical_note = models.ForeignKey(ClinicalNote, on_delete=models.CASCADE, related_name='complications')
    complication_date = models.DateTimeField(null=True)
    complication_type = models.CharField(max_length=15, blank=True, null=True)
    #complication_code = models.CharField(max_length=10, blank=True, null=True)
    complication_name = models.CharField(max_length=99, blank=True, null=True)
    complication_description = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'Complication'
        verbose_name_plural = 'Complications'
        db_table = 'complication'
    
    def _str_(self):
        return str(self.primary_key)


class Disability(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinical_note = models.ForeignKey(ClinicalNote, on_delete=models.CASCADE, related_name='disabilities')
    disability_date = models.DateTimeField(null=True)
    disability_type = models.CharField(max_length=15, blank=True, null=True)
    #disability_code = models.CharField(max_length=10, blank=True, null=True)
    disability_name = models.CharField(max_length=99, blank=True, null=True)
    disability_description = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'Disability'
        verbose_name_plural = 'Disabilities'
        db_table = 'disability'
    
    def _str_(self):
        return str(self.primary_key)


class Relapse(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinical_note = models.ForeignKey(ClinicalNote, on_delete=models.CASCADE, related_name='relapses')
    relapse_date = models.DateTimeField(null=True)
    relapse_type = models.CharField(max_length=15, blank=True, null=True)
    #relapse_code = models.CharField(max_length=10, blank=True, null=True)
    relapse_name = models.CharField(max_length=99, blank=True, null=True)
    relapse_description = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'Relapse'
        verbose_name_plural = 'Relapses'
        db_table = 'relapse'
    
    def _str_(self):
        return str(self.primary_key)


class Remission(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinical_note = models.ForeignKey(ClinicalNote, on_delete=models.CASCADE, related_name='remissions')
    remission_date = models.DateTimeField(null=True)
    remission_type = models.CharField(max_length=15, blank=True, null=True)
    #remission_code = models.CharField(max_length=10, blank=True, null=True)
    remission_name = models.CharField(max_length=99, blank=True, null=True)
    remission_description = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        verbose_name = 'Remission'
        verbose_name_plural = 'Remissions'
        db_table = 'remission'
    
    def _str_(self):
        return str(self.primary_key)


class Allergy(models.Model):
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinical_note = models.ForeignKey(ClinicalNote, on_delete=models.CASCADE, related_name='allergies')
    #allergy_product_code = models.IntegerField(default=99999, validators=[MaxValueValidator(99999)])
    allergy_product_description = models.CharField(max_length=99, blank=True, null=True)
    #allergy_reaction_code = models.CharField(max_length=10, blank=True, null=True)
    allergy_reaction_name = models.CharField(max_length=99, blank=True, null=True)
    allergy_rection_description = models.CharField(max_length=99, blank=True, null=True)
    #allergy_severity_code = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    allergy_severity_description = models.CharField(max_length=10, blank=True, null=True)
    allergy_status = models.CharField(max_length=15, blank=True, null=True)
    allergy_history = models.TextField(blank=True, null=True)
    allergy_event_type = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = 'Allergy'
        verbose_name_plural = 'Allergies'
        db_table = 'allergy'
    
    def _str_(self):
        return str(self.primary_key)


class Outreach(models.Model):
    primary_key = models.UUIDField(primary_key=True)
    encounter_id = models.UUIDField(blank=True, null=True)
    outreach_service_delivery_place_name = models.CharField(max_length=99, blank=True, null=True)
    outreach_service_delivery_place_address = models.CharField(max_length=255, blank=True, null=True)
    outreach_service_delivery_place_type = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    outreach_service_purpose = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    outreach_service_provider_name = models.CharField(max_length=99, blank=True, null=True)
    outreach_service_provider_type = models.IntegerField(default=99, validators=[MaxValueValidator(99)])
    outreach_service_provider_identification_number = models.CharField(max_length=20, blank=True, null=True)
    referral_support_indicator = models.BooleanField(default=0)

    class Meta:
        verbose_name = 'Outreach'
        verbose_name_plural = 'Outreaches'
        db_table = 'outreach'
    
    def _str_(self):
        return str(self.primary_key)
