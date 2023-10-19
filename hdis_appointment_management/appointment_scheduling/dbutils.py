from datetime import datetime
import json
import os
import time
import pika
import django
import datetime
import uuid
from dateutil.relativedelta import relativedelta
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hdis_appointment_management.settings")
django.setup()

from appointment_scheduling.models import Provider,Person,Patient,Facility,ProviderSchedule,AppointmentSessionSlots


def CreateProviderSchedule(PrimaryKey,UniqueFacilityIdentificationNumber,uniqueIndividualHealthCareProviderNumber,careProviderName,startDate,endDate):
    
    if Facility.objects.filter(uniqueFacilityIdentificationNumber=UniqueFacilityIdentificationNumber).count()>0:
        facility=Facility.objects.get(uniqueFacilityIdentificationNumber=UniqueFacilityIdentificationNumber)
    else:
        facility=Facility(uniqueFacilityIdentificationNumber=UniqueFacilityIdentificationNumber)
        facility.save()
    
    print(facility)
   # provider_details = Provider(PrimaryKey=uuid.UUID(PrimaryKey),facilityId=facility ,uniqueIndividualHealthCareProviderNumber=uniqueIndividualHealthCareProviderNumber, careProviderName=careProviderName)
    provider_details=Provider.objects.get(PrimaryKey=uuid.UUID(PrimaryKey))
    #provider_details.save()
    #create provider schedule
    provider_schedule=ProviderSchedule(providerId=provider_details)
    provider_schedule.ResourceScheduleStartDate=startDate
    provider_schedule.ResourceScheduleEndDate=endDate
    provider_schedule.ResourceScheduleStartTime="08:00"
    provider_schedule.ResourceScheduleEndTime="22:00"
    provider_schedule.save()

def CreateAppointmentSessionSlots(UniqueIndividualHealthCareProviderNumber,startTime,endTime):
    #check for condition where healthcareprovider is not present
    while endTime > startTime:
        provider_id=Provider.objects.get(uniqueIndividualHealthCareProviderNumber=UniqueIndividualHealthCareProviderNumber)
        provider_schedule=ProviderSchedule.objects.get(providerId=provider_id)
        appointmentSessionSlots=AppointmentSessionSlots(providerscheduleId=provider_schedule,AppointmentSessionStartTime=startTime,AppointmentSessionEndTime=endTime)
        appointmentSessionSlots.AppointmentScheduleDate=datetime.date.today()
        appointmentSessionSlots.save()
        startTime=startTime+relativedelta(minutes=+10)

        


