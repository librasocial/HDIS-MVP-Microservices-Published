import json
import os
import pika
import django
from static_variables import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_file)
django.setup()

from consultation_plan.models import *
from consultation_plan.serializers import *

params = pika.URLParameters(param_location)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='hdis_consultation_plan')

def callback(ch, method, properties, body):
    print('Received in Consultation Plan')
    print(properties.headers)

channel.basic_consume(queue='hdis_consultation_plan', on_message_callback=callback, auto_ack=True)

print('Start Consuming')

channel.start_consuming()
channel.close()