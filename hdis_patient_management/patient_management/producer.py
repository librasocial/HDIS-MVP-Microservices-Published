import json

import pika




def publish(method, body):
    params = pika.URLParameters("amqp://hdis_patient_management:hdis_patient_management_password@rabbitmq.openhdis.com/hdis_staging")
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.exchange_declare(exchange='hdis_patient_registration', exchange_type='fanout')
    channel.queue_bind(queue='queue_patient_registration', exchange='hdis_patient_registration')
    
    if body:
        properties = pika.BasicProperties(headers={'content_type': method})
        channel.basic_publish(exchange='hdis_patient_registration', routing_key='', body=json.dumps(body),
                              properties=properties)
   #     channel.basic_publish(exchange='', routing_key='hdis_consultation_subjective', body=json.dumps(body),
   #                           properties=properties)
   #     channel.basic_publish(exchange='', routing_key='hdis_consultation_objective', body=json.dumps(body),
   #                           properties=properties)
   #     channel.basic_publish(exchange='', routing_key='hdis_consultation_assessment', body=json.dumps(body),
   #                           properties=properties)
   #     channel.basic_publish(exchange='', routing_key='hdis_consultation_plan', body=json.dumps(body),
    #                          properties=properties)
    else:
        pass

    channel.close()    
    connection.close(0)