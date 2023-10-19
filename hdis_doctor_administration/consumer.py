from datetime import datetime
import json
import os
import time
import pika
import django
import random
import uuid
from doctor_onboarding.producer import publish
from static_variables import *
os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_file)
django.setup()
from doctor_onboarding.serializers import *
from doctor_onboarding.models import *

params = pika.URLParameters(param_location)

#params = pika.URLParameters("amqps://rndprzsn:zeIkUCI2t94fBGZTEy_BI6IYa2FuaFtc@puffin.rmq2.cloudamqp.com/rndprzsn")

connection = pika.BlockingConnection(params)
channel = connection.channel()


channel.exchange_declare(exchange='hdis_doctor_administration', exchange_type='fanout')

channel.queue_bind(queue='queue_doctor_administration', exchange='hdis_facility')
channel.queue_bind(queue='queue_doctor_administration', exchange='hdis_doctor_administration')



def callback(ch, method, properties, body):
    print('Received in Doctor Administration')
    print(properties.headers['content_type'])
    print(body)
    data = json.loads(body)


    if properties.headers['content_type'] == 'doctor created':



        LocalHealthCareProviderNumber='LPH'+str(random.randint(100000000, 999999999))
        doctor_details = DoctorDetails(UniqueFacilityIdentificationNumber=data['uniqueFacilityIdentificationNumber'] , doctorName=data['memberName'], doctorUserId=data['PrimaryKey'])

        present=True
        while present==True:
            if DoctorDetails.objects.filter(LocalHealthCareProviderNumber=LocalHealthCareProviderNumber).count()>0:
                present=True
                LocalHealthCareProviderNumber = 'LPH'+str(random.randint(100000000, 999999999))
            else:
                present=False
        doctor_details.LocalHealthCareProviderNumber=LocalHealthCareProviderNumber

        UniqueIndividualHealthCareProviderNumber='UHP'+str(random.randint(10000000, 99999999))
        present=True
        while present==True:
            if DoctorDetails.objects.filter(LocalHealthCareProviderNumber=LocalHealthCareProviderNumber,UniqueIndividualHealthCareProviderNumber=UniqueIndividualHealthCareProviderNumber).count()>0:
                present=True
                UniqueIndividualHealthCareProviderNumber = 'UHP'+str(random.randint(10000000, 99999999))
            else:
                present=False
        doctor_details.UniqueIndividualHealthCareProviderNumber=UniqueIndividualHealthCareProviderNumber
        


        doctor_details.save()

        print("Doctor Details Added")
        serializer = DoctorSerializers(doctor_details)
        doctor_personal=DoctorPersonalDetails(doctor_id=doctor_details)
        doctor_personal.save()


        publish('doctor user created', serializer.data)

        try:
            facility_details = Facility.objects.get(uniqueFacilityIdentificationNumber=data['uniqueFacilityIdentificationNumber'])
        except Facility.DoesNotExist:
            #fetch facility
            print(1)

        provider=Provider(facilityId=facility_details,uniqueIndividualHealthCareProviderNumber=LocalHealthCareProviderNumber,careProviderName=doctor_details.doctorName)
        provider.providerCreationDate=datetime.today()
        provider.save()

        provider_serializer=ProviderSerializers(provider)

        print(provider_serializer.data)
        publish('provider created', provider_serializer.data)



    if properties.headers['content_type'] == 'doctor updated':

        doctor_details = DoctorDetails.objects.get(doctorUserId=data['PrimaryKey'])
        doctor_details.doctorName= data['memberName']
        doctor_details.save()
        provider=Provider.objects.get(uniqueIndividualHealthCareProviderNumber=doctor_details.LocalHealthCareProviderNumber)
        provider.careProviderName=doctor_details.doctorName
        provider.save()

        provider_serializer=ProviderSerializers(provider)

        print(provider_serializer.data)
        publish('provider updated', provider_serializer.data)


    if properties.headers['content_type'] == 'facility created':

        #print(data)
        data = json.loads(body)
       # print(data)

        serializer = FacilitySerializers(data=data)

        serializer.is_valid(raise_exception=True)

        try:
            Facility.objects.get(uniqueFacilityIdentificationNumber=data['uniqueFacilityIdentificationNumber'])
        except Facility.DoesNotExist:
            serializer.save()
            fd = Facility.objects.get(uniqueFacilityIdentificationNumber=data['uniqueFacilityIdentificationNumber'])
            try:
                fields_needed = FacilityDoctorFields.objects.get(facility_id=fd)
            except FacilityDoctorFields.DoesNotExist:
                fields_needed = FacilityDoctorFields(facility_id=fd)
                fields_needed.save()




    #elif properties.content_type == 'patient updated':
     #   providersPatientID = str(time.mktime(datetime.now().timetuple()))[:-2]
      #  patient_details = Patient(PatientName=data['PatientName'], PatientAge=data['PatientAge'], ProvidersPatientID=providersPatientID)
       # patient_details.save()


channel.basic_consume(queue='queue_doctor_administration', on_message_callback=callback, auto_ack=True)

print('Start Consuming')

channel.start_consuming()
channel.close()

