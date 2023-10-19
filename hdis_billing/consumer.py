from datetime import datetime
import json
import os
import time
import pika
from rest_framework.exceptions import ValidationError
from rest_framework.exceptions import ErrorDetail
import django
import requests
from static_variables import *
os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_file)
django.setup()

from billing.models import *
from billing.serializers import *

params = pika.URLParameters(param_location)

connection = pika.BlockingConnection(params)
channel = connection.channel()
channel.queue_declare(queue='hdis_billing')
channel.queue_bind(queue='hdis_billing', exchange='hdis_facility')
channel.queue_bind(queue='hdis_billing', exchange='hdis_doctor_administration')
channel.queue_bind(queue='hdis_billing', exchange='hdis_patient_registration')
channel.queue_bind(queue='hdis_billing', exchange='hdis_appointment_management')
channel.queue_bind(queue='hdis_billing', exchange='hdis_visit_management')


def callback(ch, method, properties, body):
    print('Received in Billing')
    print(properties.headers)
    if properties.headers['content_type'] == 'facility created':
        data = json.loads(body)
        print(data)
        serializer = FacilitySerializers(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            Facility.objects.get(uniqueFacilityIdentificationNumber=data['uniqueFacilityIdentificationNumber'])
        except Facility.DoesNotExist:
            serializer.save()
    elif properties.headers['content_type'] == 'provider created':
        data = json.loads(body)
        print(data)
        facility_details = data['facilityId']
        print(facility_details)
        data['facilityId'] = facility_details['PrimaryKey']
        serializer = ProviderSerializers(data=data)
        try:
            Provider.objects.get(uniqueIndividualHealthCareProviderNumber=data['uniqueIndividualHealthCareProviderNumber'])
        except Provider.DoesNotExist:
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except ValidationError as errors:
                for field, errors_list in errors.detail.items():
                    #print(errors_list)
                    if field == 'facilityId' and 'does not exist' in errors_list[0]:
                        serializer_facility = FacilitySerializers(data=facility_details)
                        serializer_facility.is_valid(raise_exception=True)
                        serializer_facility.save()
                        print("facility created")
                serializer = ProviderSerializers(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
    elif properties.headers['content_type'] == 'appointment created':
        data = json.loads(body)
        print(data)
        person_details = data['patientId']['personId']
        patient_details = data['patientId']
        patient_details['personId'] = person_details['PrimaryKey']
        facility_details = patient_details['facilityId']
        patient_details['facilityId'] = facility_details['PrimaryKey']
        serializer = PersonSerializers(data=person_details)
        try:
            Person.objects.get(PrimaryKey=person_details['PrimaryKey'])
        except Person.DoesNotExist:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        try:
            Patient.objects.get(PrimaryKey=patient_details['PrimaryKey'])
        except Patient.DoesNotExist:
            serializer_patient = PatientSerializers(data=patient_details)
            try:
                serializer_patient.is_valid(raise_exception=True)
                serializer_patient.save()
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
                serializer_patient = PatientSerializers(data=patient_details)
                serializer_patient.is_valid(raise_exception=True)
                serializer_patient.save()
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
        serializer = PatientSerializers(data=data)
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
                serializer = PatientSerializers(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
    elif properties.headers['content_type'] == 'employee created':
        data = json.loads(body)
        print(data)
        serializer = EmployeeSerializers(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            Employee.objects.get(EmployeeID=data['EmployeeID'],
                                 EmployerID=data['EmployerID'],
                                 PatientID=data['PatientID'])
        except Employee.DoesNotExist:
            serializer.save()
    elif properties.headers['content_type'] == 'emergency created':
        data = json.loads(body)
        print(data)
        serializer = EmergencySerializers(data=data)
        serializer.is_valid(raise_exception=True)
        try:
            Emergency.objects.get(encounterId=data['encounterId'])
        except Emergency.DoesNotExist:
            serializer.save()
    elif properties.headers['content_type'] == 'episode created':
        data = json.loads(body)
        print(data)
        facility_details = data['facilityId']
        data['facilityId'] = facility_details['PrimaryKey']
        person_details = data['patientId']['personId']
        data['personId'] = person_details['PrimaryKey']
        patient_details = data['patientId']
        data['patientId'] = patient_details['PrimaryKey']
        provider_details = data['providerId']
        data['providerId'] = []
        for ids in provider_details:
            data['providerId'].append(ids['PrimaryKey'])
        serializer = EpisodeSerializers(data=data)
        try:
            Episode.objects.get(EpisodeId=data['EpisodeId'])
        except Episode.DoesNotExist:
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
                    if field == 'providerId' and 'does not exist' in errors_list[0]:
                        for providers in provider_details:
                            facility_details = providers['facilityId']
                            providers['facilityId'] = facility_details['PrimaryKey']
                            try:
                                Provider.objects.get(PrimaryKey=providers['PrimaryKey'])
                            except Provider.DoesNotExist:
                                serializer_provider = ProviderSerializers(data=providers)
                                serializer_provider.is_valid(raise_exception=True)
                                serializer_provider.save()
                for field, errors_list in errors.detail.items():
                    if field == 'personId' and 'does not exist' in errors_list[0]:
                        serializer_person = PersonSerializers(data=person_details)
                        serializer_person.is_valid(raise_exception=True)
                        serializer_person.save()
                for field, errors_list in errors.detail.items():
                    if field == 'patientId' and 'does not exist' in errors_list[0]:
                        facility_details = patient_details['facilityId']
                        patient_details['facilityId'] = facility_details['PrimaryKey']
                        person_details = patient_details['personId']
                        patient_details['personId'] = person_details['PrimaryKey']
                        serializer_patient = PatientSerializers(data=patient_details)
                        serializer_patient.is_valid(raise_exception=True)
                        serializer_patient.save()
                serializer = EpisodeSerializers(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
    elif properties.headers['content_type'] == 'encounter created':
        data = json.loads(body)
        print(data)
        episode_details = data['episodeId']
        data['episodeId'] = episode_details['PrimaryKey']
        serializer = EncounterSerializers(data=data)
        try:
            Encounter.objects.get(encounterID=data['encounterID'])
        except Encounter.DoesNotExist:
            try:
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except ValidationError as errors:
                for field, errors_list in errors.detail.items():
                    if field == 'episodeId' and 'does not exist' in errors_list[0]:
                        facility_details = episode_details['facilityId']
                        episode_details['facilityId'] = facility_details['PrimaryKey']
                        person_details = episode_details['patientId']['personId']
                        episode_details['patientId']['personId'] = person_details['PrimaryKey']
                        patient_details = episode_details['patientId']
                        episode_details['patientId'] = patient_details['PrimaryKey']
                        provider_details = episode_details['providerId']
                        episode_details['providerId'] = []
                        for ids in provider_details:
                            episode_details['providerId'].append(ids['PrimaryKey'])
                        serializer_episode = EpisodeSerializers(data=episode_details)
                        serializer_episode.is_valid(raise_exception=True)
                        serializer_episode.save()
                serializer = EncounterSerializers(data=data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

channel.basic_consume(queue='hdis_billing', on_message_callback=callback, auto_ack=True)

print('Start Consuming')

channel.start_consuming()
channel.close()
