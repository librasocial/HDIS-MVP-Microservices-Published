#from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import ProviderSchedule, ProviderWeekDayDetails, AppointmentSessionSlots
import json,requests
from django.conf import settings
from .decorators import jwt_token_required

# Create your views here.
#from .producer import publish
from .serializers import DoctorSerializers,ProviderWeekdaySerializers


class DoctorViewSet(viewsets.ViewSet):

    @jwt_token_required
    def list(self, request,data,token,status):
        if status!=200:
            return Response("", status=status.HTTP_401_UNAUTHORIZED)
        else:
            doctors = ProviderSchedule.objects.all()
            serializer = ProviderSchedule(doctors, many=True)
            #publish()
            return Response(serializer.data)

    @jwt_token_required
    def create(self, request,data,token,status):
        if status!=200:
            return Response("", status=status.HTTP_401_UNAUTHORIZED)
        else:
            serializer = DoctorSerializers(data = request.data)
            serializer.is_valid(raise_exception=True)
            if ProviderSchedule.objects.filter(LocalHealthCareProviderNumber = serializer.data['LocalHealthCareProviderNumber']).count() > 0:
                return Response("Doctor may already exist, please verify", status=status.HTTP_300_MULTIPLE_CHOICES)
            else:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
    @jwt_token_required
    def retrieve(self, request,data,token,status, dId,dayId=None):
        if status!=200:
            return Response("", status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                if dayId is not None:
                    print("found")
                    doctor_details = ProviderSchedule.objects.get(LocalHealthCareProviderNumber=dId)
                    doctor_workday = ProviderWeekDayDetails.objects.filter(providerWeekDayId=doctor_details,dayOfTheWeek=dayId).get()
                    print(doctor_workday)    
                    daily_slots = {}
                    daily_slots['weekday'] = doctor_workday.dayOfTheWeek
                    daily_slots['weekday_status'] = doctor_workday.dayOfTheWeekWorkingStatus
                    daily_slots['daily_slot_list'] = []
                    for slots in AppointmentSessionSlots.objects.filter(slotId = doctor_workday):
                        slots_in_day = {}
                        slots_in_day['dayOfTheWeekSlotStartTime'] = slots.dayOfTheWeekSlotStartTime
                        slots_in_day['dayOfTheWeekSlotEndTime'] = slots.dayOfTheWeekSlotEndTime
                        slots_in_day['dayOfTheWeekSlotDuration'] = slots.dayOfTheWeekSlotDuration
                        slots_in_day['dayOfTheWeekSlotStatus'] = slots.dayOfTheWeekSlotStatus
                        daily_slots['daily_slot_list'].append(slots_in_day)
                # serializer = DoctorSerializers(doctor_details)
                    return Response(daily_slots)
                else:
                    print("not found")
                    doctor_details = ProviderSchedule.objects.get(LocalHealthCareProviderNumber=dId)
                    doctor_weekdays = ProviderWeekDayDetails.objects.filter(providerWeekDayId=doctor_details)
                    doctor_slots = []
                    for days in doctor_weekdays:
                        daily_slots = {}
                        daily_slots['weekday'] = days.dayOfTheWeek
                        daily_slots['weekday_status'] = days.dayOfTheWeekWorkingStatus
                        daily_slots['daily_slot_list'] = []
                        for slots in AppointmentSessionSlots.objects.filter(slotId = days):
                            slots_in_day = {}
                            slots_in_day['dayOfTheWeekSlotStartTime'] = slots.dayOfTheWeekSlotStartTime
                            slots_in_day['dayOfTheWeekSlotEndTime'] = slots.dayOfTheWeekSlotEndTime
                            slots_in_day['dayOfTheWeekSlotDuration'] = slots.dayOfTheWeekSlotDuration
                            slots_in_day['dayOfTheWeekSlotStatus'] = slots.dayOfTheWeekSlotStatus
                            daily_slots['daily_slot_list'].append(slots_in_day)

                        doctor_slots.append(daily_slots)
                    # serializer = DoctorSerializers(doctor_details)
                    return Response(doctor_slots)

            except ProviderSchedule.DoesNotExist:
                doctor_details = ProviderSchedule.objects.all()[0]
                serializer = DoctorSerializers(doctor_details)
                return Response(serializer.data)
    def update(self, request):
        pass
    def destroy(self, request):
        pass


