from rest_framework import serializers

from .models import *

class FacilitySerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)

    class Meta:
        model = Facility
        fields = '__all__'

class PersonSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)

    class Meta:
        model=Person
        fields='__all__'    

class ProviderSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    facilityId=FacilitySerializers()

    class Meta:
        model=Provider
        fields='__all__'
    def update(self, instance, validated_data):
        print("here now")
        providerStatus = validated_data.pop('providerStatus',instance.providerStatus)
        careProviderName=validated_data.pop('careProviderName',instance.careProviderName)
        instance = super().update(instance, validated_data)
        instance.providerStatus.set(*[providerStatus])
        instance.careProviderName.set(*[careProviderName])

        return instance






class PatientSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    facilityId = FacilitySerializers()
    personId=PersonSerializers()
    #patientArrivalDateTime=serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Patient
        fields = '__all__'


class ServiceSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    facilityId = FacilitySerializers()
    providerId=ProviderSerializers()

    class Meta:
        model = Service
        fields = '__all__'
    


      



class ConsumerPatientSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    #facilityId = FacilitySerializers()
    #personId=PersonSerializers()
    #patientArrivalDateTime=serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Patient
        fields = '__all__'