from .models import *
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

def block_updates_to_non_updateable_fields(self, inputs):
        # Block updates to fields that should not be updateable
        if self.instance:    #If Update operation...
            for field in self.Meta.non_updateable_fields:
                if field in inputs:
                    current_value = getattr(self.instance, field)
                    new_value = inputs[field]
                    if current_value != new_value:
                        raise PermissionDenied(detail=f"Updates are not allowed to field '{field}'.")


class BillSerializer(serializers.ModelSerializer):
    """Base ModelSerializer class for a Bill, where each Item within is represented by its Primary Key."""

    class Meta:
        model = Bill
        fields = '__all__'
        extra_kwargs = { "bill_id": { "format": "hex" }, "facility_id": { "format": "hex" }  }
        non_updateable_fields = ('facility_id', 'patient_id', 'bill_id')    #Custom attribute to control updateable fields

    
    def to_internal_value(self, data):
        input_as_primitives = super().to_internal_value(data)
        block_updates_to_non_updateable_fields(self, input_as_primitives)
        return input_as_primitives
    

class BillItemSerializer(serializers.ModelSerializer):
    """Serializer for an individual Item within a Bill."""

    class Meta:
        model = BillItem
        fields = '__all__'
        read_only_fields = ('tax',)
        extra_kwargs = { "primary_key": { "format": "hex" }, "service_id": { "format": "hex" }, "bill": { "required": False } }
        non_updateable_fields = ('bill', 'service_id', 'service_name')    #Custom attribute to control updateable fields
    

    def to_internal_value(self, data):
        input_as_primitives = super().to_internal_value(data)
        block_updates_to_non_updateable_fields(self, input_as_primitives)
        return input_as_primitives


class BillSummarySerializer(BillSerializer):
    """Bill Serializer variant that ignores any Bill Items."""

    bill_items = None

    class Meta(BillSerializer.Meta):
        pass


class BillDetailsSerializer(BillSerializer):
    """Bill Serializer variant that includes details of all Items for the Bill."""
    
    bill_items = BillItemSerializer(many=True, read_only=True)

    class Meta(BillSerializer.Meta):
        pass


class SourceOfPaymentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SourceOfPaymentDetails
        fields = '__all__'
        extra_kwargs = { "primary_key": { "format": "hex" } }
        non_updateable_fields = ('bill',)    #Custom attribute to control updateable fields
    

    def to_internal_value(self, data):
        input_as_primitives = super().to_internal_value(data)
        block_updates_to_non_updateable_fields(self, input_as_primitives)
        return input_as_primitives
