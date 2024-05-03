from datetime import datetime
import json
import os
import time

import pika
import django
from static_variables import *
os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_file)
django.setup()

from patient_registration.models import *
from patient_registration.serializers import *

params = pika.URLParameters(param_location)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='queue_patient_registration')

channel.queue_bind(queue='queue_patient_registration', exchange='hdis_facility')
channel.queue_bind(queue='queue_patient_registration', exchange='hdis_patient_registration')



def callback(ch, method, properties, body):
    print('Received in Patient Registration')


    if properties.headers['content_type'] == 'facility created':

        print("in here")
        #print(data)
        data = json.loads(body)
       # print(data)
        
        serializer = FacilitySerializers(data=data)

        serializer.is_valid(raise_exception=True)

        try:
            Facility.objects.get(uniqueFacilityIdentificationNumber=data['uniqueFacilityIdentificationNumber'])
        except Facility.DoesNotExist:
            serializer.save()        


    #elif properties.content_type == 'patient updated':
     #   providersPatientID = str(time.mktime(datetime.now().timetuple()))[:-2]
      #  patient_details = Patient(PatientName=data['PatientName'], PatientAge=data['PatientAge'], ProvidersPatientID=providersPatientID)
       # patient_details.save()


channel.basic_consume(queue='queue_patient_registration', on_message_callback=callback, auto_ack=True)

print('Start Consuming')

channel.start_consuming()
channel.close()
