import json
import pika
from static_variables import *


def publish(method, body):
    params = pika.URLParameters(param_location)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange='hdis_patient_management', exchange_type='fanout')
    channel.queue_bind(queue='queue_patient_registration', exchange='hdis_patient_management')
    
    if body:
        properties = pika.BasicProperties(headers={'content_type': method})
        channel.basic_publish(exchange='hdis_patient_management', routing_key='', body=json.dumps(body),
                              properties=properties)
    else:
        pass

    channel.close()    
    connection.close(0)