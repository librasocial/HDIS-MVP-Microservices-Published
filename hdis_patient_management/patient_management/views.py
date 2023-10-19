#from django.shortcuts import render
import json
import random
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
import time
from datetime import datetime

# Create your views here.
from .producer import publish
from .serializers import PatientSerializers,PersonSerializers


class PatientViewSet(viewsets.ViewSet):
    def list(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializers(patients, many=True)
        #publish()
        return Response(serializer.data)

    def create(self, request):
        #content = list(request.POST.items())
        values = json.loads(request.body.decode('utf-8'))
        print(values)
        dob = datetime.strptime(values['dob'], '%Y-%m-%d').date()
        dob_year = str(datetime.now().year - dob.year)
        dob_month = str(datetime.now().month - dob.month)
        dob_day = str(datetime.now().day - dob.day)
        patient_age = dob_year + ',' + dob_month + ',' + dob_day
        values['PatientAge'] = patient_age
        #serializer = PatientSerializers(data = request.data)
        #serializer.is_valid(raise_exception=True)

        if Patient.objects.filter(PatientName=values['name'], PatientGender=values['patient_gender'], PatientDOB__year=dob.year).count() > 0:
            patient_details = Patient.objects.filter(PatientName=values['name'], PatientGender=values['patient_gender'],
                                   PatientDOB__year=dob.year)
            patient_list = []
            for patients in patient_details:
                response_details = {}
                response_details['patient_UHID'] = patients.personId.UniqueHealthIdentificationID
                response_details['patient_UHID_number'] = patients.personId.UniqueHealthIdentificationNumber
                response_details['patient_alternateIDType'] = patients.personId.AlternateUniqueIdentificationNumberType
                response_details['patient_alternateID'] = patients.personId.AlternateUniqueIdentificationNumber
                response_details['PatientName'] = patients.PatientName
                response_details['PatientAge'] = patients.PatientAge
                response_details['PatientGender'] = patients.PatientGender
                response_details['patientId'] = str(patients.PrimaryKey)

                response_details['PatientDOB'] = patients.PatientDOB.strftime('%Y-%m-%d')
                patient_list.append(response_details)

            print("from here")
            return Response(patient_list, status=status.HTTP_300_MULTIPLE_CHOICES)
        else:
            
            if 'UniqueHealthIdentificationNumber' in values:
                print("UID present")
                person_details = Person(NationalityCode=1,
                                        UniqueHealthIdentificationNumber=values['UniqueHealthIdentificationNumber'],
                                        UniqueHealthIdentificationID=values['UniqueHealthIdentificationID'])
            else:
                print("UID not present")
                person_details = Person(NationalityCode=1)
                #create UHID ++
                localUHIDNumber = 'OH'+str(random.randint(100000000, 999999999))

                present=True
                while present==True:
                    if Person.objects.filter(UniqueHealthIdentificationNumber=localUHIDNumber).count()>0:
                        present=True
                        localUHIDNumber = 'OH'+str(random.randint(100000000, 999999999))
                    else:
                        present=False
                person_details.UniqueHealthIdentificationNumber=localUHIDNumber
                localUHID='UID'+str(random.randint(10000000, 99999999))
                present=True
                while present==True:
                    if Person.objects.filter(UniqueHealthIdentificationNumber=localUHIDNumber,UniqueHealthIdentificationID=localUHID).count()>0:
                        present=True
                        localUHID = 'UID'+str(random.randint(10000000, 99999999))
                    else:
                        present=False
                person_details.UniqueHealthIdentificationID=localUHID
                
            person_details.save()
            person_serializer=PersonSerializers(person_details)
            publish('person created', person_serializer.data)


            try:
                facility=Facility.objects.get(uniqueFacilityIdentificationNumber=values['facilityID'])
            except Facility.DoesNotExist:
                facility=Facility(uniqueFacilityIdentificationNumber=values['facilityID'])
                facility.save()

            dob = datetime.strptime(values['dob'], '%Y-%m-%d')
            patient_details = Patient(personId=person_details, PatientName=values['name'], PatientAge=patient_age,
                                      PatientGender=values['patient_gender'], PatientDOB=dob,facilityId=facility)
            patient_details.save()
            pAddress = values['address'] + ' ' + values['location'] + ' ' + values['city'] + ' ' + values['pin']
            patient_contact = patientAddressDetail(patientId=patient_details, PatientAddress=pAddress,
                                                   PatientAddressType='C', patientMobileNumber=values['mobile'],
                                                   patientEmailAddressURL=values['email'])
            patient_contact.save()
            values['patientId'] = str(patient_details.PrimaryKey)
            values['PatientAddress'] = pAddress
            values['ProvidersPatientID'] = str(time.mktime(datetime.now().timetuple()))[:-2]
            values['UniqueHealthIdentificationNumber']=localUHIDNumber
            values['UniqueHealthIdentificationID']=localUHID
            

            

            publish('patient registered', values)

            patient_serializer=PatientSerializers(patient_details)
            print(patient_serializer.data)
            print(patient_details)
            publish('patient created',patient_serializer.data)

            return Response(str(patient_details.PrimaryKey), status=status.HTTP_201_CREATED)
            # serializer.save()
            # publish('patient created', serializer.data)
            # return Response(serializer.data, status=status.HTTP_201_CREATED)


    def retrieve(self, request, pId):
        try:
            patient_details = Patient.objects.get(PrimaryKey=uuid.UUID(pId))
            serializer = PatientSerializers(patient_details)
            patient_list = []
            response_details = serializer.data
            response_details['patient_UHID'] = patient_details.personId.UniqueHealthIdentificationID
            response_details['patient_UHID_number'] = patient_details.personId.UniqueHealthIdentificationNumber
            response_details['patient_alternateIDType'] = patient_details.personId.AlternateUniqueIdentificationNumberType
            response_details['patient_alternateID'] = patient_details.personId.AlternateUniqueIdentificationNumber
            response_details['patientId'] = str(patient_details.PrimaryKey)

            patient_list.append(response_details)
            return Response(patient_list)
        except Patient.DoesNotExist:
            patient_details = Patient.objects.all()[0]
            serializer = PatientSerializers(patient_details)
            return Response(serializer.data)
    def update(self, request):
        serializer = PatientSerializers(data = request.data)
        serializer.is_valid(raise_exception=True)
        try:
            patient_details = Patient.objects.get(patientId=serializer.data['patientId'])
            publish('patient updated', serializer.data)
            return Response("Patient updated", status=status.HTTP_300_MULTIPLE_CHOICES)
        except Patient.DoesNotExist:
            return Response("Patient does not exist, please verify", status=status.HTTP_300_MULTIPLE_CHOICES)

    def destroy(self, request):
        pass


    def search(self,request,uhid):
        try:
            patient_details = Patient.objects.get(personId=Person.objects.get(UniqueHealthIdentificationID=uhid))
            serializer = PatientSerializers(patient_details)
            patient_list = []
            response_details = serializer.data
            response_details['patient_UHID'] = patient_details.personId.UniqueHealthIdentificationID
            response_details['patient_UHID_number'] = patient_details.personId.UniqueHealthIdentificationNumber
            response_details['patient_alternateIDType'] = patient_details.personId.AlternateUniqueIdentificationNumberType
            response_details['patient_alternateID'] = patient_details.personId.AlternateUniqueIdentificationNumber
            response_details['patientId'] = str(patient_details.PrimaryKey)


            patient_list.append(response_details)
            print(patient_list)
            return Response(patient_list,status=status.HTTP_200_OK)
        except Person.DoesNotExist:
            #patient_details = Patient.objects.all()[0]
            serializer = PatientSerializers()
            return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)
