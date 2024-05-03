from .models import *
from rest_framework import serializers

class EncounterProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = EncounterProvider
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "encounter_id": { "format": "hex" }, "provider_id": { "format": "hex" } }


class ClinicalNoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClinicalNote
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "encounter_id": { "format": "hex" } }


class ClinicalOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClinicalOrder
        exclude = ()
        extra_kwargs = { "primary_key": { "format": "hex" }, "clinical_note": {"pk_field": serializers.UUIDField(format='hex')} }


class LabOrderSerializer(ClinicalOrderSerializer):

    class Meta(ClinicalOrderSerializer.Meta):
        model = LabOrder


class RadiologyOrderSerializer(ClinicalOrderSerializer):

    class Meta(ClinicalOrderSerializer.Meta):
        model = RadiologyOrder


class PharmacyOrderSerializer(ClinicalOrderSerializer):

    class Meta(ClinicalOrderSerializer.Meta):
        model = PharmacyOrder


class ImmunizationOrderSerializer(ClinicalOrderSerializer):

    class Meta(ClinicalOrderSerializer.Meta):
        model = ImmunizationOrder


class ProcedureOrderSerializer(ClinicalOrderSerializer):
    
    class Meta(ClinicalOrderSerializer.Meta):
        model = ProcedureOrder


class OrderSetSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderSet
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "provider_id": { "format": "hex" } }


class OrderSetLabSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderSetLab
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "order_set": {"pk_field": serializers.UUIDField(format='hex')} }


class OrderSetRadiologySerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderSetRadiology
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "order_set": {"pk_field": serializers.UUIDField(format='hex')} }


class OrderSetPharmacySerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderSetPharmacy
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "order_set": {"pk_field": serializers.UUIDField(format='hex')} }


class OrderSetImmunizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderSetImmunization
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "order_set": {"pk_field": serializers.UUIDField(format='hex')} }


class OrderSetProcedureSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderSetProcedure
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "order_set": {"pk_field": serializers.UUIDField(format='hex')} }
