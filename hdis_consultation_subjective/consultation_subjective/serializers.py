from rest_framework import serializers

from .models import *


class FacilitySerializers(serializers.ModelSerializer):
    PrimaryKey=serializers.UUIDField(format='hex', read_only=False)
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
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
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
    class Meta:
        model = clinicalNotes
        fields = '__all__'

class familyHistorySerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = familyHistory
        fields = '__all__'

class patientComorbiditiesSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = patientComorbidities
        fields = '__all__'

class chiefComplaintsSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = chiefComplaints
        fields = '__all__'

class socialHistorySerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = socialHistory
        fields = '__all__'

class complicationsSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = complications
        fields = '__all__'

class disabilitySerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = disability
        fields = '__all__'

class relapseSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = relapse
        fields = '__all__'

class remissionSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = remission
        fields = '__all__'

class allergySerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = allergy
        fields = '__all__'