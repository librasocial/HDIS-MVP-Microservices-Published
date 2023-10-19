from rest_framework import serializers

from patient_registration.models import Patient,Person,Facility



class FacilitySerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = Facility
        fields = '__all__'



class PersonSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = Person
        fields = '__all__'        

class PatientSerializers(serializers.ModelSerializer):
        PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
        personId=PersonSerializers()
        facilityId=FacilitySerializers()
        #PatientDOB=serializers.DateTimeField(format="%Y-%m-%d")

        class Meta:
            model = Patient
            fields = '__all__' 


class PersonSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = Person
        fields = '__all__'

class BasicPatientSerializers(serializers.ModelSerializer):
        PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
        personId=PersonSerializers()
        facilityId=FacilitySerializers()
        PatientDOB=serializers.DateTimeField(format="%Y-%m-%d")

        class Meta:
            model = Patient
            fields = ('PrimaryKey','personId','PatientName','PatientAge','PatientGender','PatientDOB','facilityId','IdentityUnknownIndicator')