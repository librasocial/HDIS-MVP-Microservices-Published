import json

import pika
from static_variables import *
params = pika.URLParameters(param_location)



def publish(method, body):
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange='hdis_visit_management', exchange_type='fanout')
    if body:
        properties = pika.BasicProperties(headers={'content_type': method})
        channel.basic_publish(exchange='hdis_visit_management', routing_key='', body=body,
                              properties=properties)
    else:
        pass
    channel.close()
    connection.close()


