from .models import *
from rest_framework import serializers


class EpisodeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Episode
        fields = '__all__'
        extra_kwargs = {"primary_key": { "format": "hex" }, "facility_id": { "format": "hex" }}


class EncounterSerializer(serializers.ModelSerializer):
    episode = EpisodeSerializer()
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    appointment_id = serializers.UUIDField(format='hex', allow_null=True)

    class Meta:
        model = Encounter
        fields = '__all__'
        extra_kwargs = {"primary_key": { "format": "hex" }}


class EncounterFlatSerializer(serializers.ModelSerializer):
    episode = serializers.PrimaryKeyRelatedField(queryset=Episode.objects.all(), pk_field=serializers.UUIDField(format='hex'))
    timestamp = serializers.DateTimeField(format="%Y-%m-%d %H:%M", read_only=True)
    appointment_id = serializers.UUIDField(format='hex', allow_null=True)

    class Meta:
        model = Encounter
        fields = '__all__'
        extra_kwargs = {"primary_key": { "format": "hex" }}
