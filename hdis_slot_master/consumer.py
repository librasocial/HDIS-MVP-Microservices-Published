from datetime import datetime
import json
import os
import time

import pika
import django
from static_variables import *
os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_file)
django.setup()

from slot_details.models import ProviderSchedule, AppointmentSessionSlots, ProviderLeaveMaster, ProviderWeekDayDetails

params = pika.URLParameters(param_location)

connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='queue_slot_creation')
channel.queue_bind(queue='queue_slot_creation', exchange='hdis_doctor_administration')


def callback(ch, method, properties, body):
    print('Received Doctor Registration Details')
    print(properties.headers['content_type'])
    if properties.headers['content_type'] == 'provider created':
        data = json.loads(body)
        print(data)
        doctor_schedule_creation = ProviderSchedule(UniqueFacilityIdentificationNumber=data['facilityId']['uniqueFacilityIdentificationNumber'], LocalHealthCareProviderNumber=data['uniqueIndividualHealthCareProviderNumber'])
        doctor_schedule_creation.save()
        weekday_creation = ProviderWeekDayDetails(providerWeekDayId = doctor_schedule_creation, dayOfTheWeek = 'Monday')
        weekday_creation.save()
        slot_creation = AppointmentSessionSlots(slotId = weekday_creation)
        slot_creation.save()
        weekday_creation = ProviderWeekDayDetails(providerWeekDayId=doctor_schedule_creation, dayOfTheWeek='Tuesday')
        weekday_creation.save()
        slot_creation = AppointmentSessionSlots(slotId=weekday_creation)
        slot_creation.save()
        weekday_creation = ProviderWeekDayDetails(providerWeekDayId=doctor_schedule_creation, dayOfTheWeek='Wednesday')
        weekday_creation.save()
        slot_creation = AppointmentSessionSlots(slotId=weekday_creation)
        slot_creation.save()
        weekday_creation = ProviderWeekDayDetails(providerWeekDayId=doctor_schedule_creation, dayOfTheWeek='Thursday')
        weekday_creation.save()
        slot_creation = AppointmentSessionSlots(slotId=weekday_creation)
        slot_creation.save()
        weekday_creation = ProviderWeekDayDetails(providerWeekDayId=doctor_schedule_creation, dayOfTheWeek='Friday')
        weekday_creation.save()
        slot_creation = AppointmentSessionSlots(slotId=weekday_creation)
        slot_creation.save()
        weekday_creation = ProviderWeekDayDetails(providerWeekDayId=doctor_schedule_creation, dayOfTheWeek='Saturday')
        weekday_creation.save()
        slot_creation = AppointmentSessionSlots(slotId=weekday_creation)
        slot_creation.save()
        weekday_creation = ProviderWeekDayDetails(providerWeekDayId=doctor_schedule_creation, dayOfTheWeek='Sunday')
        weekday_creation.save()
        slot_creation = AppointmentSessionSlots(slotId=weekday_creation)
        slot_creation.save()
        print("Default Slots Created")
    #elif properties.content_type == 'patient updated':
     #   providersPatientID = str(time.mktime(datetime.now().timetuple()))[:-2]
      #  patient_details = Patient(PatientName=data['PatientName'], PatientAge=data['PatientAge'], ProvidersPatientID=providersPatientID)
       # patient_details.save()

    


channel.basic_consume(queue='queue_slot_creation', on_message_callback=callback, auto_ack=True)

print('Start Consuming')

channel.start_consuming()
channel.close()
