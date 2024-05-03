from .models import *
from rest_framework import serializers

class EmployeeSerializer(serializers.ModelSerializer):
    facility_id = serializers.UUIDField(format='hex', required=False)
    
    class Meta:
        model = Employee
        fields = '__all__'

    def validate_facility_id(self, value):
        # Throw an error if there is an attempt to update facility_id
        if self.instance:
            if not value:
                value = self.instance.facility_id
            elif value != self.instance.facility_id:
                raise serializers.ValidationError("facility_id cannot be updated.")
        return value


class ProviderSerializer(EmployeeSerializer):
    """Represents a Healthcare Provider. Includes fields from superclass Employee object."""
    employee_id = serializers.CharField(source='employee_ptr')
    
    class Meta:
        model = Provider
        exclude = ('employee_ptr',)
        extra_kwargs = {"primary_key": { "format": "hex" }}


class EmployeeDocumentsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = EmployeeDocuments
        fields = '__all__'
        extra_kwargs = {"primary_key": { "format": "hex" }, "document_file": { "use_url": False }}


class EmployeeQualificationsSerializer(serializers.ModelSerializer):
    #certificate_file = serializers.SerializerMethodField()

    class Meta:
        model = EmployeeQualifications
        fields = '__all__'
        extra_kwargs = {"primary_key": { "format": "hex" }}

    # def get_certificate_file(self):
    #     return self.certificate_file.path


class DoctorFieldDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorFieldDetails
        fields = '__all__'
        extra_kwargs = {"primary_key": { "format": "hex" }}
