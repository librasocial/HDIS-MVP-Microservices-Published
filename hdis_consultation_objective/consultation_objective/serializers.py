from rest_framework import serializers

from .models import *


class FacilitySerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = Facility
        fields = '__all__'

class ProviderSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = Provider
        fields = '__all__'

class PersonSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = Person
        fields = '__all__'


class PatientSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = Patient
        fields = '__all__'

class EmployeeSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = Employee
        fields = '__all__'

class EmergencySerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=True)
    class Meta:
        model = Emergency
        fields = '__all__'

class EpisodeSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = Episode
        fields = '__all__'


class EncounterSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = Encounter
        fields = '__all__'


class outreachSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = outreach
        fields = '__all__'
class clinicalNotesSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    authorDateTime = serializers.DateTimeField(format="%Y-%m-%d")
    class Meta:
        model = clinicalNotes
        fields = '__all__'

class examinationSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = examination
        fields = '__all__'

class vitalSignsSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = vitalSigns
        fields = '__all__'

class labSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = lab
        fields = '__all__'

class radiologySerializers(serializers.ModelSerializer):
    class Meta:
        model = radiology
        fields = '__all__'
