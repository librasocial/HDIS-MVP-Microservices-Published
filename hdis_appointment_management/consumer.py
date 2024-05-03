from appointment_management.models import ResourceSchedule
import json
import os
import django
import pika
from static_variables import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_file)
django.setup()

params = pika.URLParameters(param_location)

connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='provider_registration')
channel.queue_bind(queue='provider_registration', exchange='hdis_employee_management')

def callback(ch, method, properties, body):
    print("Content Type:", properties.headers['content_type']) #Debug
    if properties.headers['content_type'] == 'provider created':
        print('Received Provider Registration Details') #Debug
        parsed_body = json.loads(body)
        print(parsed_body) #Debug

        ResourceSchedule.create_new_schedule(parsed_body)        
        print("Default Sessions Created.") #Debug

channel.basic_consume(queue='provider_registration', on_message_callback=callback, auto_ack=True)

print('Start Consuming') #Debug
channel.start_consuming()

channel.close()
