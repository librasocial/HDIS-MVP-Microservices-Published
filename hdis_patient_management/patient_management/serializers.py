from .models import *
from rest_framework import serializers

class PersonSerializer(serializers.ModelSerializer):
    primary_key = serializers.UUIDField(format='hex', read_only=True)
    
    class Meta:
        model = Person
        fields = '__all__'        


class PatientSerializer(serializers.ModelSerializer):
    primary_key = serializers.UUIDField(format='hex', read_only=True)
    person = PersonSerializer()
    patient_dob = serializers.DateField(format="%Y-%m-%d")
    facility_id = serializers.UUIDField(format='hex')
    
    class Meta:
        model = Patient
        fields = '__all__'


class PatientWithoutNestedPersonSerializer(serializers.ModelSerializer):     
    primary_key = serializers.UUIDField(format='hex', read_only=True)
    patient_dob = serializers.DateField(format="%Y-%m-%d")
    facility_id = serializers.UUIDField(format='hex')
    
    class Meta:
        model = Patient
        fields = '__all__'


class BasicPatientSerializers(serializers.ModelSerializer):
    primary_key = serializers.UUIDField(format='hex', read_only=True)
    person = PersonSerializer()
    patient_dob = serializers.DateField(format="%Y-%m-%d")
    facility_id = serializers.UUIDField(format='hex')

    class Meta:
        model = Patient
        fields = ('primary_key','person','patient_name','patient_age','patient_gender',
                'patient_dob','facility_id','identity_unknown_indicator')
