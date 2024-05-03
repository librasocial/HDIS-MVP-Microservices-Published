import json
import os
import pika
import django
from static_variables import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_file)
django.setup()

from consultation_subjective.models import *
from consultation_subjective.serializers import *

params = pika.URLParameters(param_location)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='hdis_consultation_subjective')

def callback(ch, method, properties, body):
    print('Received in Consultation Subjective')
    print(properties.headers)
    print(json.loads(body))
    if properties.headers['content_type'] == 'emergency created':
        data = json.loads(body)
        print(data) #Debug
        serializer = EmergencySerializer(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            Emergency.objects.get(encounter_id=data['encounter_id'])
        except Emergency.DoesNotExist:
            serializer.save()
    elif properties.headers['content_type'] == 'outreach created':
        data = json.loads(body)
        print(data) #Debug
        serializer = OutreachSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            Outreach.objects.get(encounter_id=data['encounter_id'])
        except Outreach.DoesNotExist:
            serializer.save()

channel.basic_consume(queue='hdis_consultation_subjective', on_message_callback=callback, auto_ack=True)

print('Start Consuming')
channel.start_consuming()
channel.close()
