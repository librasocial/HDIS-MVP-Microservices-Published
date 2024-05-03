from datetime import datetime
import json
import os
import time
import pika
import django
import random
import uuid
from static_variables import *
from employee_management.producer import publish
from employee_management.serializers import *
from employee_management.models import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_file)
django.setup()
params = pika.URLParameters(param_location)
#params = pika.URLParameters("amqps://rndprzsn:zeIkUCI2t94fBGZTEy_BI6IYa2FuaFtc@puffin.rmq2.cloudamqp.com/rndprzsn")
connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.exchange_declare(exchange='hdis_employee_management', exchange_type='fanout')
channel.queue_bind(queue='queue_employee_management', exchange='hdis_employee_management')

# TODO: To be reviewed
def callback(ch, method, properties, body):
    print('Received in Employee Management') #TODO: Logging
    print(properties.headers['content_type']) #Debug
    print(body) #Debug
    data = json.loads(body)

    if properties.headers['content_type'] == 'provider created':

        unique_individual_health_care_provider_number = 'LPH' + str(random.randint(100000000, 999999999))
        provider_details = Provider(facility_id=data['facility_id'], doctorName=data['member_username'], employee_id=data['employee_id'])

        present = True
        while present == True:
            if Provider.objects.filter(unique_individual_health_care_provider_number=unique_individual_health_care_provider_number).exists():
                present = True
                unique_individual_health_care_provider_number = 'LPH' + str(random.randint(100000000, 999999999))
            else:
                present = False
        provider_details.local_healthcare_provider_number = unique_individual_health_care_provider_number

        unique_individual_healthcare_provider_number = 'UHP' + str(random.randint(10000000, 99999999))
        present = True
        while present == True:
            if Provider.objects.filter(unique_individual_health_care_provider_number=unique_individual_health_care_provider_number).exists():
                present = True
                unique_individual_healthcare_provider_number = 'UHP' + str(random.randint(10000000, 99999999))
            else:
                present = False
        provider_details.unique_individual_healthcare_provider_number = unique_individual_healthcare_provider_number
        
        provider_details.save()

        print("Provider Details:", provider_details.data) #Debug
        serializer = ProviderSerializer(provider_details)
        publish('provider created', serializer.data)

    if properties.headers['content_type'] == 'provider updated':

        provider_details = Provider.objects.get(employee_id=data['employee_id'])
        provider_details.unique_individual_health_care_provider_number = data['unique_individual_health_care_provider_number']
        provider_details.save()

channel.basic_consume(queue='queue_employee_management', on_message_callback=callback, auto_ack=True)    #TODO: Check why consuming from this queue
print('Start Consuming')
channel.start_consuming()
channel.close()
