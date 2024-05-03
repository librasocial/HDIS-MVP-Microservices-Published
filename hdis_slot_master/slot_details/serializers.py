from rest_framework import serializers

from slot_details.models import ProviderSchedule,ProviderWeekDayDetails


class DoctorSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProviderSchedule
        fields = '__all__'

class ProviderWeekdaySerializers(serializers.ModelSerializer):
    class Meta:
        model = ProviderWeekDayDetails
        fields = '__all__'

