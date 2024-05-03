from datetime import datetime
import uuid
from django.db import models
from django.core.validators import MaxValueValidator

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
    clinical_document_type = models.PositiveSmallIntegerField(blank=True, default=18, validators=[MaxValueValidator(99)])

    class Meta:
        verbose_name = 'Clinical Note'
        verbose_name_plural = 'Clinical Notes'
        db_table = 'clinical_note'
    def _str_(self):
        return str(self.primary_key)


class ClinicalOrder(models.Model):
    """Abstract Base Class for various types of specialized Clinical Orders specified in a Plan stage Clinical Note."""

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinical_note = models.ForeignKey(ClinicalNote, on_delete=models.CASCADE, related_name='clinical_orders')
    description = models.CharField(max_length=254, blank=True, null=True)
    order_id = models.CharField(max_length=12, blank=True, null=True)
    parent_order_id = models.CharField(max_length=10, blank=True, null=True)
    verifying_care_provider_id = models.CharField(max_length=18, blank=True, null=True)
    status = models.CharField(max_length=2, blank=True, null=True)
    priority = models.PositiveSmallIntegerField(blank=True, default=99, validators=[MaxValueValidator(99)])
    placer_order_id = models.CharField(max_length=10, blank=True, null=True)
    filler_order_id = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        verbose_name = 'Clinical Order'
        verbose_name_plural = 'Clinical Orders'
        db_table = 'clinical_order'
    
    def _str_(self):
        return str(self.primary_key)


class LabOrder(ClinicalOrder):
    """Specialized Clinical Order specified in a Plan stage Clinical Note."""
    
    code = models.CharField(max_length=10, blank=True, null=True)
    lab_id = models.IntegerField(blank=True, default=0)
    lab_type = models.PositiveSmallIntegerField(blank=True, default=9, validators=[MaxValueValidator(9)])

    class Meta:
        verbose_name = 'Lab Order'
        verbose_name_plural = 'Lab Orders'
        db_table = 'lab_order'
    
    def _str_(self):
        return str(self.primary_key)


class RadiologyOrder(ClinicalOrder):
    """Specialized Clinical Order specified in a Plan stage Clinical Note."""

    radiology_center_id = models.IntegerField(default=0)
    radiology_center_type = models.PositiveSmallIntegerField(blank=True, default=9, validators=[MaxValueValidator(9)])
    radiology_procedure_name = models.CharField(max_length=255, blank=True, null=True)
    radiology_procedure_code = models.CharField(max_length=18, blank=True, null=True)

    class Meta:
        verbose_name = 'Radiology Order'
        verbose_name_plural = 'Radiology Orders'
        db_table = 'radiology_order'

    def _str_(self):
        return str(self.primary_key)


class PharmacyOrder(ClinicalOrder):
    """Specialized Clinical Order specified in a Plan stage Clinical Note."""

    drug_classification_code = models.PositiveSmallIntegerField(blank=True, default=99, validators=[MaxValueValidator(99)])
    route_of_administration = models.CharField(max_length=6, blank=True, null=True)
    medication_frequency = models.CharField(max_length=5, blank=True, null=True)
    medication_administration_interval = models.CharField(max_length=40, blank=True, null=True)
    dose = models.CharField(max_length=60, blank=True, null=True)
    medication_stopped_indicator = models.PositiveSmallIntegerField(blank=True, default=9, validators=[MaxValueValidator(9)])
    body_site = models.PositiveSmallIntegerField(blank=True, default=999, validators=[MaxValueValidator(999)])
    medication_status = models.PositiveSmallIntegerField(blank=True, default=99, validators=[MaxValueValidator(99)])
    patient_instructions = models.CharField(max_length=255, blank=True, null=True)
    prescription_id = models.CharField(max_length=20, blank=True, null=True)
    order_datetime = models.DateTimeField(blank=True, default=datetime.now)
    indication = models.CharField(max_length=10, blank=True, null=True)
    contraindication = models.CharField(max_length=10, blank=True, null=True)
    medication_fills = models.PositiveSmallIntegerField(blank=True, default=999, validators=[MaxValueValidator(999)])
    medication_instructions = models.CharField(max_length=254, blank=True, null=True)
    fill_status = models.PositiveSmallIntegerField(blank=True, default=99, validators=[MaxValueValidator(99)])

    class Meta:
        verbose_name = 'Pharmacy Order'
        verbose_name_plural = 'Pharmacy Orders'
        db_table = 'pharmacy_order'

    def _str_(self):
        return str(self.primary_key)


class ImmunizationOrder(ClinicalOrder):
    """Specialized Clinical Order specified in a Plan stage Clinical Note."""

    immunization_refusal_reason = models.PositiveSmallIntegerField(blank=True, default=99, validators=[MaxValueValidator(99)])
    immunization_administration_datetime = models.DateTimeField(blank=True, null=True)
    immunization_performer_identification_number = models.CharField(max_length=18, blank=True, null=True)
    immunization_product_code = models.PositiveSmallIntegerField(blank=True, default=999, validators=[MaxValueValidator(999)])
    immunization_product_description = models.CharField(max_length=99, blank=True, null=True)
    medication_series_number = models.PositiveSmallIntegerField(blank=True, default=99, validators=[MaxValueValidator(99)])
    immunization_information_source = models.PositiveSmallIntegerField(blank=True, default=999, validators=[MaxValueValidator(999)])

    class Meta:
        verbose_name = 'Immunization Order'
        verbose_name_plural = 'Immunization Orders'
        db_table = 'immunization_order'

    def _str_(self):
        return str(self.primary_key)


class ProcedureOrder(ClinicalOrder):
    """Specialized Clinical Order specified in a Plan stage Clinical Note."""

    procedure_name = models.CharField(max_length=255, blank=True, null=True)
    procedure_modifier = models.PositiveSmallIntegerField(blank=True, default=999, validators=[MaxValueValidator(999)])
    procedure_code = models.CharField(max_length=18, blank=True, null=True)
    procedure_type = models.PositiveSmallIntegerField(blank=True, default=999, validators=[MaxValueValidator(999)])
    procedure_type_description = models.CharField(max_length=99, blank=True, null=True)
    procedure_datetime = models.DateTimeField(blank=True, null=True)
    multiple_procedure_flag = models.BooleanField(blank=True, default=0)

    class Meta:
        verbose_name = 'Procedure Order'
        verbose_name_plural = 'Procedure Orders'
        db_table = 'procedure_order'

    def _str_(self):
        return str(self.primary_key)


class OrderSet(models.Model):
    """A Group of Orders (possibly of multiple types) that is commonly used by a particular Provider at a Facility."""

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider_id = models.UUIDField()    #Dev Note: A given Provider ID is tied to a single Facility ID 
    order_set_name = models.CharField(max_length=255, blank=True, null=True)
    order_set_type = models.CharField(max_length=99, blank=True, null=True)
    diagnosis_condition_name = models.CharField(max_length=99, blank=True, null=True)

    class Meta:
        verbose_name = 'Order Set'
        verbose_name_plural = 'Order Sets'
        db_table = 'order_set'
    
    def _str_(self):
        return str(self.primary_key)


class OrderSetLab(models.Model):
    """Component of an Order Set representing a Lab Order."""

    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_set = models.ForeignKey(OrderSet, on_delete=models.CASCADE, related_name='lab_order_sets')
    lab_order_code = models.CharField(max_length=10, blank=True, null=True)
    lab_id = models.IntegerField(default=0)
    lab_type = models.PositiveSmallIntegerField(default=9, validators=[MaxValueValidator(9)])

    class Meta:
        verbose_name = 'Order Set Lab'
        verbose_name_plural = 'Order Sets Lab'
        db_table = 'order_set_lab'

    def _str_(self):
        return str(self.primary_key)


class OrderSetRadiology(models.Model):
    """Component of an Order Set representing a Radiology Order."""
    
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_set = models.ForeignKey(OrderSet, on_delete=models.CASCADE, related_name='radiology_order_sets')
    radiology_center_id = models.IntegerField(default=0)
    radiology_center_type = models.PositiveSmallIntegerField(default=9, validators=[MaxValueValidator(9)])
    radiology_procedure_name = models.CharField(max_length=255, blank=True, null=True)
    radiology_procedure_code = models.CharField(max_length=18, blank=True, null=True)

    class Meta:
        verbose_name = 'Order Set Radiology'
        verbose_name_plural = 'Order Sets Radiology'
        db_table = 'order_set_radiology'

    def _str_(self):
        return str(self.primary_key)


class OrderSetPharmacy(models.Model):
    """Component of an Order Set representing a Pharmacy Order."""
    
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_set = models.ForeignKey(OrderSet, on_delete=models.CASCADE, related_name='pharmacy_order_sets')
    drug_classification_code = models.PositiveSmallIntegerField(default=99, validators=[MaxValueValidator(99)])
    route_of_administration = models.CharField(max_length=6, blank=True, null=True)
    medication_frequency = models.CharField(max_length=5, blank=True, null=True)
    medication_administration_interval = models.CharField(max_length=40, blank=True, null=True)
    dose = models.CharField(max_length=60, blank=True, null=True)
    medication_stopped_indicator = models.PositiveSmallIntegerField(blank=True, default=9, validators=[MaxValueValidator(9)])
    body_site = models.PositiveSmallIntegerField(blank=True, default=999, validators=[MaxValueValidator(999)])
    medication_status = models.PositiveSmallIntegerField(default=99, validators=[MaxValueValidator(99)])
    patient_instructions = models.CharField(max_length=255, blank=True, null=True)
    prescription_id = models.CharField(max_length=20, blank=True, null=True)
    order_datetime = models.DateTimeField(null=True)
    indication = models.CharField(max_length=10, blank=True, null=True)
    contraindication = models.CharField(max_length=10, blank=True, null=True)
    medication_fills = models.PositiveSmallIntegerField(default=999, validators=[MaxValueValidator(999)])
    medication_instructions = models.CharField(max_length=254, blank=True, null=True)
    fill_status = models.PositiveSmallIntegerField(default=99, validators=[MaxValueValidator(99)])

    class Meta:
        verbose_name = 'Order Set Pharmacy'
        verbose_name_plural = 'Order Sets Pharmacy'
        db_table = 'order_set_pharmacy'

    def _str_(self):
        return str(self.primary_key)


class OrderSetImmunization(models.Model):
    """Component of an Order Set representing a Immunization Order."""
    
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_set = models.ForeignKey(OrderSet, on_delete=models.CASCADE, related_name='immunization_order_sets')
    immunization_refusal_reason = models.PositiveSmallIntegerField(default=99, validators=[MaxValueValidator(99)])
    immunization_administration_datetime = models.DateTimeField(null=True)
    immunization_performer_identification_number = models.CharField(max_length=18, blank=True, null=True)
    immunization_product_code = models.PositiveSmallIntegerField(default=999, validators=[MaxValueValidator(999)])
    immunization_product_description = models.CharField(max_length=99, blank=True, null=True)
    medication_series_number = models.PositiveSmallIntegerField(default=99, validators=[MaxValueValidator(99)])
    immunization_information_source = models.PositiveSmallIntegerField(default=999, validators=[MaxValueValidator(999)])

    class Meta:
        verbose_name = 'Order Set Immunization'
        verbose_name_plural = 'Order Sets Immunization'
        db_table = 'order_set_immunization'

    def _str_(self):
        return str(self.primary_key)


class OrderSetProcedure(models.Model):
    """Component of an Order Set representing a Procedure Order."""
    
    primary_key = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_set = models.ForeignKey(OrderSet, on_delete=models.CASCADE, related_name='procedure_order_sets')
    procedure_name = models.CharField(max_length=255, blank=True, null=True)
    procedure_modifier = models.PositiveSmallIntegerField(default=999, validators=[MaxValueValidator(999)])
    procedure_code = models.CharField(max_length=18, blank=True, null=True)
    procedure_type = models.PositiveSmallIntegerField(default=999, validators=[MaxValueValidator(999)])
    procedure_type_description = models.CharField(max_length=99, blank=True, null=True)
    procedure_datetime = models.DateTimeField(null=True)
    multiple_procedure_flag = models.BooleanField(default=0)

    class Meta:
        verbose_name = 'Order Set Procedure'
        verbose_name_plural = 'Order Sets Procedure'
        db_table = 'order_set_procedure'
    
    def _str_(self):
        return str(self.primary_key)
