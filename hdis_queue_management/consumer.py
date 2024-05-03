from datetime import datetime
import json
import os
from static_variables import *
import pika
import django
from rest_framework.exceptions import ValidationError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_file)
django.setup()

from queue_management.models import *
from queue_management.serializers import *

params = pika.URLParameters(param_location)
connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='queue_queue_management')


def callback(ch, method, properties, body):    #TODO: Remove consumer if it is unnecessary
    print('Received Appointment')
    print(properties.headers['content_type'])
    if properties.headers['content_type'] == 'appointment created':
        data = json.loads(body)
        print (data['facilityId']['uniqueFacilityIdentificationNumber'])
    elif properties.headers['content_type'] == 'episode created':
        data = json.loads(body)
        print(data)
    elif properties.headers['content_type'] == 'encounter created':
        data = json.loads(body)
        print(data)


channel.basic_consume(queue='queue_queue_management', on_message_callback=callback, auto_ack=True)

print('Start Consuming')
channel.start_consuming()
channel.close()
