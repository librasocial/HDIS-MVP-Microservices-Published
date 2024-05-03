import json
import os
import pika
import django
from static_variables import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_file)
django.setup()

from bill_management.models import *
from bill_management.serializers import *

params = pika.URLParameters(param_location)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='hdis_bill_management')


def callback(ch, method, properties, body):    #TODO: Remove consumer if it is unnecessary
    print('Received in Bill Management')
    print(properties.headers) #Debug


channel.basic_consume(queue='hdis_bill_management', on_message_callback=callback, auto_ack=True)

print('Start Consuming')
channel.start_consuming()
channel.close()
