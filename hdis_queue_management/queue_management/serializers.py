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
    class Meta:
        model=Provider
        fields=('PrimaryKey','careProviderMobileNumber','careProviderEmailAddress','careProviderName','providerStatus')
    def update(self, instance, validated_data):
        print("here now")
        providerStatus = validated_data.pop('providerStatus',instance.providerStatus)
        careProviderName=validated_data.pop('careProviderName',instance.careProviderName)
        careProviderMobileNumber=validated_data.pop('careProviderMobileNumber',instance.careProviderMobileNumber)
        careProviderEmailAddress=validated_data.pop('careProviderEmailAddress',instance.careProviderEmailAddress)
        instance = super().update(instance, validated_data)
        instance.providerStatus=providerStatus
        instance.careProviderName=careProviderName
        instance.careProviderMobileNumber=careProviderMobileNumber
        instance.careProviderEmailAddress=careProviderEmailAddress
        instance.save()

        return instance



    

class PatientSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    facilityId = FacilitySerializers()
    personId=PersonSerializers()
    #patientArrivalDateTime=serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Patient
        fields = '__all__'


    




class BillingSerializers(serializers.ModelSerializer):
    class Meta:
        model=Billing
        fields='__all__'        



class ConsumerPatientSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    #facilityId = FacilitySerializers()
    #personId=PersonSerializers()
    #patientArrivalDateTime=serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Patient
        fields = '__all__'