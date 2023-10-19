import json
import os
import time
import pika
import django
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from rest_framework.exceptions import ValidationError
from static_variables import *
os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_file)
django.setup()
from service_manager.serializers import *
from service_manager.models import Provider,Person,Patient,Facility
params = pika.URLParameters(param_location)

#params = pika.URLParameters("amqps://rndprzsn:zeIkUCI2t94fBGZTEy_BI6IYa2FuaFtc@puffin.rmq2.cloudamqp.com/rndprzsn")

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='queue_service_master')
channel.queue_bind(queue='queue_service_master', exchange='hdis_facility')
channel.queue_bind(queue='queue_service_master', exchange='hdis_doctor_administration')
channel.queue_bind(queue='queue_service_master', exchange='hdis_patient_registration')



def callback(ch, method, properties, body):
    print('Received in Service Master')
   
    print(body)
    print(properties.headers['content_type'])
    data = json.loads(body)
    
    if properties.headers['content_type'] == 'provider created':

        uniqueFacilityIdentificationNumber=data['facilityId']['uniqueFacilityIdentificationNumber']
        print(uniqueFacilityIdentificationNumber)
        try:
            facility=Facility.objects.get(uniqueFacilityIdentificationNumber=uniqueFacilityIdentificationNumber)
            try:
                Provider.objects.get(uniqueIndividualHealthCareProviderNumber=data['uniqueIndividualHealthCareProviderNumber'])
            except Provider.DoesNotExist:

                ext_data=data
                del ext_data['facilityId']
                pk=ext_data['PrimaryKey']
                del ext_data['PrimaryKey']
                provider=Provider(**ext_data) 
                provider.facilityId=facility
                provider.PrimaryKey=uuid.UUID(pk)
                provider.save()

        except Facility.DoesNotExist:
            fac_data=data['facilityId']
            pk=fac_data['PrimaryKey']
            del fac_data['PrimaryKey']
            facility=Facility(**fac_data)
            facility.PrimaryKey=uuid.UUID(pk)
            facility.save()
            ext_data=data
            del ext_data['facilityId']
            pk=ext_data['PrimaryKey']
            del ext_data['PrimaryKey']
            provider=Provider(**ext_data)
            provider.facilityId=facility
            provider.PrimaryKey=uuid.UUID(pk)
            provider.save()

    

        print("Doctor Details Added")


    elif properties.headers['content_type'] == 'provider updated':
        print('here')
        data = json.loads(body)
        print(data)
        try:
            provider=Provider.objects.get(uniqueIndividualHealthCareProviderNumber=data['uniqueIndividualHealthCareProviderNumber'])
            print('correct')
            serializer = ProviderSerializers(provider, data=data, partial=True)
            if serializer.is_valid():
                serializer.update()
                print("provider updated")
            else:
                serializer.is_valid(raise_exception=True)

        

        except Provider.DoesNotExist:
            serializer.save()

    elif properties.headers['content_type'] == 'facility created':
        data = json.loads(body)
        print(data)
        serializer = FacilitySerializers(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            Facility.objects.get(uniqueFacilityIdentificationNumber=data['uniqueFacilityIdentificationNumber'])
        except Facility.DoesNotExist:
            serializer.save()
        
    

    elif properties.headers['content_type'] == 'person created':
        data = json.loads(body)
        print(data)
        serializer = PersonSerializers(data=data)
        try:
            Person.objects.get(UniqueHealthIdentificationNumber=data['UniqueHealthIdentificationNumber'])
        except Person.DoesNotExist:
            serializer.is_valid(raise_exception=True)
            serializer.save()
    elif properties.headers['content_type'] == 'patient created':
        data = json.loads(body)
        print(data)
        facility_details = data['facilityId']
        data['facilityId'] = facility_details['PrimaryKey']
        person_details = data['personId']
        data['personId'] = person_details['PrimaryKey']
        serializer = ConsumerPatientSerializers(data=data)
        try:
            Patient.objects.get(personId=person_details['PrimaryKey'])
        except Patient.DoesNotExist:
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except ValidationError as errors:
                for field, errors_list in errors.detail.items():
                    if field == 'facilityId' and 'does not exist' in errors_list[0]:
                        serializer_facility = FacilitySerializers(data=facility_details)
                        serializer_facility.is_valid(raise_exception=True)
                        serializer_facility.save()
                for field, errors_list in errors.detail.items():
                    if field == 'personId' and 'does not exist' in errors_list[0]:
                        serializer_person = PersonSerializers(data=person_details)
                        serializer_person.is_valid(raise_exception=True)
                        serializer_person.save()
                serializer = ConsumerPatientSerializers(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()


channel.basic_consume(queue='queue_service_master', on_message_callback=callback, auto_ack=True)

print('Start Consuming')

channel.start_consuming()
channel.close()
