from datetime import datetime
import json
import os
import time
from static_variables import *

import pika
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_file)
django.setup()
from queue_management.serializers import *
from rest_framework.exceptions import ValidationError
from queue_management.models import *




params = pika.URLParameters(param_location)

connection = pika.BlockingConnection(params)
channel = connection.channel()

channel.queue_declare(queue='queue_queue_management')
channel.queue_bind(queue='queue_queue_management', exchange='hdis_facility')
channel.queue_bind(queue='queue_queue_management', exchange='hdis_doctor_administration')
channel.queue_bind(queue='queue_queue_management', exchange='hdis_patient_registration')
channel.queue_bind(queue='queue_queue_management', exchange='hdis_appointment_management')
channel.queue_bind(queue='queue_queue_management', exchange='hdis_visit_management')





def callback(ch, method, properties, body):
    print('Received Appointment')
    print(properties.headers['content_type'])
    if properties.headers['content_type'] == 'appointment created':
        data = json.loads(body)
        print (data['facilityId']['uniqueFacilityIdentificationNumber'])
        facilityid=data['facilityId']['uniqueFacilityIdentificationNumber']

        if Facility.objects.filter(uniqueFacilityIdentificationNumber=facilityid).count()>0:
            facility=Facility.objects.get(uniqueFacilityIdentificationNumber=facilityid)
        else:
            facility=Facility(uniqueFacilityIdentificationNumber=facilityid)
            facility.save()


        if Department.objects.filter(facilityId=facility,departmentName="billing").count()>0:
            department=Department.objects.get(facilityId=facility,departmentName="billing")
        else:
            department=Department(facilityId=facility,departmentName="billing")
            department.save()



        #create waitlist in billing
        wday=data['appointmentsessionslotsId']['AppointmentSessionStartTime']
        waitlistday=datetime.strptime(wday, '%Y-%m-%d %H:%M').date()

        if Waitlist.objects.filter(facilityId=facility,departmentId=department,waitlistDay=waitlistday).count()>0:
            waitlist=Waitlist.objects.get(facilityId=facility,departmentId=department,waitlistDay=waitlistday)
            waitlist.waitlistNumber=waitlist.waitlistNumber+1
        else:
            waitlist=Waitlist(facilityId=facility,departmentId=department,waitlistDay=waitlistday)
            waitlist.save()

      

        if Department.objects.filter(facilityId=facility,departmentName="General Medicine").count()>0:
            department=Department.objects.get(facilityId=facility,departmentName="General Medicine")
        else:
            department=Department(facilityId=facility,departmentName="General Medicine")
            department.save()    

        #create waitlist in General Medicine
        if Waitlist.objects.filter(facilityId=facility,departmentId=department,waitlistDay=waitlistday).count()>0:
            waitlist=Waitlist.objects.get(facilityId=facility,departmentId=department,waitlistDay=waitlistday)
            waitlist.waitlistNumber=waitlist.waitlistNumber+1
        else:
            waitlist=Waitlist(facilityId=facility,departmentId=department,waitlistDay=waitlistday)
            waitlist.save()    

    elif properties.headers['content_type'] == 'provider created':
            data = json.loads(body)
            #print(data)
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



    elif properties.headers['content_type'] == 'provider updated':
        print('here')
        data = json.loads(body)
        print(data)
        try:
            provider=Provider.objects.get(uniqueIndividualHealthCareProviderNumber=data['uniqueIndividualHealthCareProviderNumber'])
            print('correct')
            serializer = ProviderSerializers(provider, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                print("provider updated")
            else:
                serializer.is_valid(raise_exception=True)

        

        except Provider.DoesNotExist:
            serializer.save()

    elif properties.headers['content_type'] == 'episode created':
        data = json.loads(body)
        print(data)

        try:
            facility=Facility.objects.get(PrimaryKey=data['facilityId']['PrimaryKey'])
        except Facility.DoesNotExist:
            pass 

        try:
            person=Person.objects.get(UniqueHealthIdentificationNumber=data['patientId']['personId']['UniqueHealthIdentificationNumber'])
            patient=Patient.objects.get(personId=person)
        except Person.DoesNotExist:
            pass    

        try:
            provider=Provider.objects.get(uniqueIndividualHealthCareProviderNumber=data['providerId'][0]['uniqueIndividualHealthCareProviderNumber'])  
        except Provider.DoesNotExist:
            pass  
        
        episode=Episode(facilityId=facility,patientId=patient,providerId=provider,EpisodeId=data['EpisodeId'],EpisodeType=data['EpisodeType'])
        episode.save()

    elif properties.headers['content_type'] == 'encounter created':
        data = json.loads(body)
        print(data)

        try:
            episode=Episode.objects.get(EpisodeId=data['episodeId']['EpisodeId'])
        except Episode.DoesNotExist:
            pass

        encounter=Encounter(episodeId=episode,encounterID=data['encounterID'],encounterType=data['encounterType'],encounterTime=data['encounterTime'],encounterTypeDescription=data['encounterTypeDescription'])
        encounter.save()

        wday=data['encounterTime']
        tokenday=datetime.strptime(wday, '%Y-%m-%d %H:%M').date()
        #create waitlist in General Medicine
        if Token.objects.filter(facilityId=episode.facilityId,providerId=episode.providerId,tokenDay=tokenday).count()>0:
            token=Token.objects.get(facilityId=episode.facilityId,providerId=episode.providerId,tokenDay=tokenday)
            token.tokenNumber=token.tokenNumber+1
            token.save()
            
        else:
            token=Token(facilityId=episode.facilityId,providerId=episode.providerId,tokenDay=tokenday)
            token.save()    



      

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





        
  
     


channel.basic_consume(queue='queue_queue_management', on_message_callback=callback, auto_ack=True)

print('Start Consuming')

channel.start_consuming()
channel.close()
