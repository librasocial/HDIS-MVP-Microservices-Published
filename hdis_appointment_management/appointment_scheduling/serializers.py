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
    facilityId=FacilitySerializers()

    class Meta:
        model=Provider
        fields='__all__'
    def update(self, instance, validated_data):
        print("here now")
        providerStatus = validated_data.pop('providerStatus',instance.providerStatus)
        careProviderName=validated_data.pop('careProviderName',instance.careProviderName)
        instance = super().update(instance, validated_data)
        instance.providerStatus.set(*[providerStatus])
        instance.careProviderName.set(*[careProviderName])

        return instance




class ProviderScheduleSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    providerId=ProviderSerializers()
    ResourceScheduleStartDate=serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    ResourceScheduleEndDate=serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    class Meta:
        model=ProviderSchedule
        fields='__all__'        

class PatientSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    facilityId = FacilitySerializers()
    personId=PersonSerializers()
    #patientArrivalDateTime=serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Patient
        fields = '__all__'


    

class AppointmentDetailsSerializers(serializers.ModelSerializer):
    class Meta:
        model=AppointmentDetails
        fields='__all__'






class AppointmentSessionSlotsSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    AppointmentSessionStartDate=serializers.DateField(format="%Y-%m-%d %H:%M")
    AppointmentSessionStartTime =serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    AppointmentSessionEndTime=serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    AppointmentScheduleDate=serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    providerscheduleId=ProviderScheduleSerializers()
    class Meta:
        model=AppointmentSessionSlots
        fields='__all__'


class AppointmentSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    appointmentsessionslotsId=AppointmentSessionSlotsSerializers()
    providerId=ProviderSerializers()
    patientId=PatientSerializers()
    facilityId=FacilitySerializers()
    appointmentsessionslotsId=AppointmentSessionSlotsSerializers()
    AppointmentBookingDate=serializers.DateTimeField(format="%Y-%m-%d")
    AppointmentBookingTime=serializers.DateTimeField(format="%H:%M")
    class Meta:
        model=Appointment
        fields='__all__'

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