from .models import *
from rest_framework import serializers

class ResourceScheduleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ResourceSchedule
        exclude = ()
        extra_kwargs = {"primary_key": { "format": "hex" }}


class ResourceScheduleDaySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ResourceScheduleDay
        exclude = ()
        extra_kwargs = {"primary_key": { "format": "hex" }}


class ResourceScheduleSessionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ResourceScheduleSession
        exclude = ()
        extra_kwargs = {"primary_key": { "format": "hex" }}


class ResourceScheduleSessionNestedSerializer(ResourceScheduleSessionSerializer):
    
    class Meta(ResourceScheduleSessionSerializer.Meta):
        exclude = ResourceScheduleSerializer.Meta.exclude + ("resource_schedule_day",)


class ResourceScheduleDayNestedSerializer(ResourceScheduleDaySerializer):
    sessions = ResourceScheduleSessionNestedSerializer(many=True, read_only=True)
    
    class Meta(ResourceScheduleDaySerializer.Meta):
        pass


class ResourceScheduleNestedSerializer(ResourceScheduleSerializer):
    days_of_the_week = ResourceScheduleDayNestedSerializer(many=True, read_only=True)
    
    class Meta(ResourceScheduleSerializer.Meta):
        pass


class ResourceUnavailabilitySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ResourceUnavailability
        fields = '__all__'
        extra_kwargs = {"primary_key": { "format": "hex" }}


class AppointmentSerializer(serializers.ModelSerializer):
    
    resource_schedule_session = serializers.PrimaryKeyRelatedField(queryset=ResourceScheduleSession.objects.all(), pk_field=serializers.UUIDField(format='hex'))
    
    class Meta:
        model = Appointment
        fields = '__all__'
        extra_kwargs = {"primary_key": { "format": "hex" }, "facility_id": { "format": "hex" }}
