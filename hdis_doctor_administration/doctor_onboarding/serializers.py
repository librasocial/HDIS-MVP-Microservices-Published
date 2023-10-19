from rest_framework import serializers
from rest_framework import serializers

from doctor_onboarding.models import *


class DoctorSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)

    class Meta:
        model = DoctorDetails
        fields = '__all__'

class FacilityDoctorFieldSerializers(serializers.ModelSerializer):
    class Meta:
        model = FacilityDoctorFields
        fields = '__all__'

class FacilitySerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = Facility
        fields = '__all__'

class ProviderSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    facilityId= FacilitySerializers()

    class Meta:
        model = Provider
        fields = '__all__'

class DoctorDocumentsSerializers(serializers.ModelSerializer):
    #PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    #doctor_id=DoctorSerializers()
    class Meta:
        model = DoctorDocuments
        fields = ('documentType','documentFile')

class DoctorPersonalDetailsSerializers(serializers.ModelSerializer):
    #PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    #doctor_id=DoctorSerializers()
    class Meta:
        model = DoctorPersonalDetails
        fields = ('doctorRegistrationNumber','doctorContactNumber','languagesKnown','currentCity')