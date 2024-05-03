from rest_framework import serializers
from .models import *

class EncounterProviderSerializer(serializers.ModelSerializer):

    class Meta:
        model = EncounterProvider
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" } }


class EmergencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Emergency
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" } }


class OutreachSerializer(serializers.ModelSerializer):

    class Meta:
        model = Outreach
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" } }


class ClinicalNoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClinicalNote
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "encounter_id": { "format": "hex" } }


class FamilyHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FamilyHistory
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "clinical_note_id": { "format": "hex" } }


class PatientComorbiditySerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientComorbidity
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "clinical_note_id": { "format": "hex" } }


class ChiefComplaintSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChiefComplaint
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "clinical_note_id": { "format": "hex" } }


class SocialHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SocialHistory
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "clinical_note_id": { "format": "hex" } }


class ComplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Complication
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "clinical_note_id": { "format": "hex" } }


class DisabilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = Disability
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "clinical_note_id": { "format": "hex" } }


class RelapseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Relapse
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "clinical_note_id": { "format": "hex" } }


class RemissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Remission
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "clinical_note_id": { "format": "hex" } }


class AllergySerializer(serializers.ModelSerializer):

    class Meta:
        model = Allergy
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "clinical_note_id": { "format": "hex" } }
