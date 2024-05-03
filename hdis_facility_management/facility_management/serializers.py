from rest_framework.serializers import UUIDField, ModelSerializer
from .models import *

class FacilitySerializer(ModelSerializer):
    primary_key = UUIDField(format='hex', read_only=True)
    facility_id = UUIDField(format='hex', read_only=True)
    class Meta:
        model = Facility
        fields = '__all__'

class FacilityApplicationSerializer(ModelSerializer):
    primary_key = UUIDField(format='hex', read_only=True)
    class Meta:
        model = FacilityApplication
        fields = '__all__'

class FacilityTypeSerializer(ModelSerializer):
    class Meta:
        model = FacilityType
        fields = '__all__'

class OrganizationSerializer(ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class PackageTypeSerializer(ModelSerializer):
    class Meta:
        model = PackageType
        fields = '__all__'

class PackageSerializer(ModelSerializer):
    class Meta:
        model = Package
        fields = '__all__'
