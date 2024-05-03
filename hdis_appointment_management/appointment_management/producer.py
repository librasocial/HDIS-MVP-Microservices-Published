import json

import pika
from static_variables import *
params = pika.URLParameters(param_location)



def publish(method, body):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    if body:
        properties = pika.BasicProperties(headers={'content_type': method})

        channel.basic_publish(exchange='', routing_key='queue_queue_management', body=json.dumps(body),
                              properties=properties)
        channel.basic_publish(exchange='', routing_key='queue_visit_management', body=json.dumps(body),
                              properties=properties)
    else:
        pass
    channel.close()
    connection.close()

def publish_soap(method,body):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange='hdis_appointment_management', exchange_type='fanout')
    #channel.queue_bind(queue='test_queue', exchange='hdis_appointment_management')

    if body:
        properties = pika.BasicProperties(headers={'content_type': method})

        channel.basic_publish(exchange='hdis_appointment_management', routing_key='', body=body,
                              properties=properties)
        
    else:
        pass

    channel.close()
    connection.close()
        