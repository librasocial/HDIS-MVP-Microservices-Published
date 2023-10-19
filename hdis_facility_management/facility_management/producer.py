import json

import pika

from static_variables import *


def publish(method, body):
    params = pika.URLParameters(param_location)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange='hdis_facility', exchange_type='fanout')
    channel.queue_bind(queue='queue_patient_registration', exchange='hdis_facility')
    
    if body:
        properties = pika.BasicProperties(headers={'content_type': method})

        if 'facility' in method:
            channel.basic_publish(exchange='hdis_facility', routing_key='', body=json.dumps(body),
                              properties=properties)
        else:
            channel.basic_publish(exchange='hdis_doctor_administration', routing_key='', body=json.dumps(body),
                              properties=properties)
        

    else:
        pass

    channel.close()    
    connection.close(0)