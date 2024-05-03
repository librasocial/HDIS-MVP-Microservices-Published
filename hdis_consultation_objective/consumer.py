import json
import os
import pika
import django
from static_variables import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_file)
django.setup()

from consultation_objective.models import *
from consultation_objective.serializers import *

params = pika.URLParameters(param_location)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='hdis_consultation_objective')

def callback(ch, method, properties, body):
    print('Received in Consultation Objective')
    print(properties.headers)


channel.basic_consume(queue='hdis_consultation_objective', on_message_callback=callback, auto_ack=True)

print('Start Consuming')
channel.start_consuming()
channel.close()
