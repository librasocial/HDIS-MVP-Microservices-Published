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


class DiagnosisSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Diagnosis
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "clinical_note": {"pk_field": serializers.UUIDField(format='hex')} }
