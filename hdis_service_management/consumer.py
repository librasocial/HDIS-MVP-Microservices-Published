import json
import os
import pika
import django
from static_variables import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_file)
django.setup()

from service_management.serializers import *
from service_management.models import *

params = pika.URLParameters(param_location)

#params = pika.URLParameters("amqps://rndprzsn:zeIkUCI2t94fBGZTEy_BI6IYa2FuaFtc@puffin.rmq2.cloudamqp.com/rndprzsn")

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='queue_service_master')


def callback(ch, method, properties, body):    #TODO: Remove consumer if it is unnecessary
    print('Received in Service Master')
   
    print(body) #Debug
    print(properties.headers) #Debug


channel.basic_consume(queue='queue_service_master', on_message_callback=callback, auto_ack=True)

print('Start Consuming')
channel.start_consuming()
channel.close()
