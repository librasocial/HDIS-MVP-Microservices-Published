from .models import *
from rest_framework import serializers


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = Token
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" } }


class QueueSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Queue
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "encounter_id": { "format": "hex" } }
