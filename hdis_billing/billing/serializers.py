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

class Billing(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = Billing
        fields = '__all__'

class Payment(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = Payment
        fields = '__all__'

class Bills(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = Bills
        fields = '__all__'