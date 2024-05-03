from .models import *
from rest_framework import serializers

class ServiceTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceType
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, "facility_id": { "format": "hex" }  }


class ComponentServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ComponentService
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" }, 
                         "component_service": {"pk_field": serializers.UUIDField(format='hex')}, 
                         "component": {"pk_field": serializers.UUIDField(format='hex')} }


class ServicePriceSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ServicePrice
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" } }


class ServiceDiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceDiscount
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" } }


class ServiceTaxSerializer(serializers.ModelSerializer):

    class Meta:
        model = ServiceTax
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" } }
