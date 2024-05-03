from datetime import datetime
import json
import os
import time
import pika
import django
import random
import uuid

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hdis_patient_management.settings")
django.setup()
from patient_management.serializers import *

from patient_management.models import *

params = pika.URLParameters("amqp://hdis_patient_management:hdis_patient_management_password@rabbitmq.openhdis.com/hdis_staging")

#params = pika.URLParameters("amqps://rndprzsn:zeIkUCI2t94fBGZTEy_BI6IYa2FuaFtc@puffin.rmq2.cloudamqp.com/rndprzsn")

connection = pika.BlockingConnection(params)
channel = connection.channel()


channel.queue_declare(queue='queue_patient_management')

channel.queue_bind(queue='queue_patient_management', exchange='hdis_facility')


def callback(ch, method, properties, body):
    print('Received in Patient Management')
    print(properties.headers['content_type'])
    print(body)
    data = json.loads(body)

    if properties.headers['content_type'] == 'facility created':

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


channel.basic_consume(queue='queue_patient_management', on_message_callback=callback, auto_ack=True)

print('Start Consuming')

channel.start_consuming()
channel.close()

