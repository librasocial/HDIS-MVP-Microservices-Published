import json
import os
import pika
import django
from static_variables import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_file)
django.setup()

from consultation_assessment.models import *
from consultation_assessment.serializers import *

params = pika.URLParameters(param_location)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='hdis_consultation_assessment')

def callback(ch, method, properties, body):
    print('Received in Consultation Assessment')
    print(properties.headers)


channel.basic_consume(queue='hdis_consultation_assessment', on_message_callback=callback, auto_ack=True)

print('Start Consuming')
channel.start_consuming()
channel.close()
