#from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import JsonResponse
from .models import Patient,Person,Facility,patientAddressDetail
import uuid
import json
from datetime import datetime
import random
import time
# Create your views here.
##   Todo ####
## decorator standards
## handle negative cases

from .serializers import PatientSerializers,PersonSerializers,BasicPatientSerializers
from .producer import publish
from uuid import UUID
from .decorators import jwt_token_required
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)
class PatientViewSet(viewsets.ViewSet):
    @jwt_token_required
    def list(self, request):
        print("Here")
        patients = Patient.objects.all()
        serializer = BasicPatientSerializers(patients, many=True)
        return Response(serializer.data)

    @jwt_token_required
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
        patient_details = Patient.objects.filter(PatientName=values['name'],
                                                 PatientGender=values['patient_gender'],
                                                 PatientDOB__year=dob.year)
        print(patient_details)
        if patient_details.count() > 0:
            details_to_send = PatientSerializers(patient_details, many=True)
            return Response(json.dumps(details_to_send.data, cls=UUIDEncoder), status=300)
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
                facility=Facility.objects.get(uniqueFacilityIdentificationNumber=values['uniqueFacilityIdentificationNumber'])
            except Facility.DoesNotExist:
                facility=Facility(uniqueFacilityIdentificationNumber=values['uniqueFacilityIdentificationNumber'])
                facility.save()
                #facility_serializer = FacilitySerializers(facility)
                #publish('facility created', facility_serializer.data)

            dob = datetime.strptime(values['dob'], '%Y-%m-%d')
            present = True
            while present == True:
                if Patient.objects.filter(localFacilityPatientId=localUHIDNumber).count() > 0:
                    present = True
                    localUHIDNumber = 'OH' + str(random.randint(100000000, 999999999))
                else:
                    present = False

            patient_details = Patient(personId=person_details, PatientName=values['name'], PatientAge=patient_age,
                                      localFacilityPatientId = localUHIDNumber, PatientGender=values['patient_gender'],
                                      PatientDOB=dob,facilityId=facility,patientMobileNumber=values['mobile'])
            patient_details.save()
            pAddress = values['address'] + ' ' + values['location'] + ' ' + values['city'] + ' ' + values['pin']
            patient_contact = patientAddressDetail(patientId=patient_details, PatientAddress=pAddress,
                                                   PatientAddressType='C', patientMobileNumber=values['mobile'],
                                                   patientEmailAddressURL=values['email'])
            patient_contact.save()
            patient_serializer=PatientSerializers(patient_details)
            publish('patient created', patient_serializer.data)
            data_to_send = PatientSerializers(patient_details)
            return Response(json.dumps(data_to_send.data, cls=UUIDEncoder))

    @jwt_token_required
    def retrieve(self, request,pId):
        try:
            patient_details = Patient.objects.get(PrimaryKey=pId)
            data_to_send = PatientSerializers(patient_details)
            return Response(json.dumps(data_to_send.data, cls=UUIDEncoder))
        except Patient.DoesNotExist:
            patient_details = Patient.objects.all()[0]
            data_to_send = PatientSerializers(patient_details)
            return Response(json.dumps(data_to_send.data, cls=UUIDEncoder))

    @jwt_token_required
    def fetch(self, request,):
        values = json.loads(request.body.decode('utf-8'))
        mode=values['mode']

        if mode=='demo':
            dob_year=values['patient_yob']
            patient_details = Patient.objects.filter(PatientName=values['patient_name'],
                                                    PatientGender=values['patient_gender'],
                                                    PatientDOB__year=dob_year)
            if patient_details.count() > 0:
                deetails_to_send = PatientSerializers(patient_details, many=True)
                #patient_list = []
                #for patients in patient_details:
                #    response_details = {}
                #    response_details['patient_UHID'] = patients.personId.UniqueHealthIdentificationID
                #    response_details['patient_UHID_number'] = patients.personId.UniqueHealthIdentificationNumber
                #    response_details['patient_alternateIDType'] = patients.personId.AlternateUniqueIdentificationNumberType
                #    response_details['patient_alternateID'] = patients.personId.AlternateUniqueIdentificationNumber
                #    response_details['PatientName'] = patients.PatientName
                #    response_details['PatientAge'] = patients.PatientAge
                #    response_details['PatientGender'] = patients.PatientGender
                #    response_details['patientId'] = str(patients.PrimaryKey)

                #    response_details['PatientDOB'] = patients.PatientDOB.strftime('%Y-%m-%d')
                #    patient_list.append(response_details)

                print("from here")
                return Response(json.dumps(deetails_to_send.data, cls=UUIDEncoder))
            else:
                return Response({"error":"not found"},status=404)

        elif mode=='mobile':
            patient_details = Patient.objects.filter(patientMobileNumber=values['patient_mobile'])
            if patient_details.count() > 0:
                deetails_to_send = PatientSerializers(patient_details, many=True)
                return Response(json.dumps(deetails_to_send.data, cls=UUIDEncoder))
            else:
                return Response({"error":"not found"},status=404)


            pass

    @jwt_token_required
    def destroy(self, request):
        pass

    @jwt_token_required
    def retrievePerson(self, request, pId):
        try:
            person_details = Person.objects.get(PrimaryKey=pId)
            serializer = PersonSerializers(person_details)
            return Response(json.dumps(serializer.data, cls=UUIDEncoder))

        except Person.DoesNotExist:
            patient_details = Patient.objects.all()[0]
            serializer = BasicPatientSerializers(patient_details)
            return Response(json.dumps(serializer.data, cls=UUIDEncoder))

    @jwt_token_required
    def update(self, request, pId):
        pass
    @jwt_token_required
    def updatePerson(self, request):
        pass

    @jwt_token_required
    def destroyPerson(self, request):
        pass

    @jwt_token_required
    def search(self,request,uhid):
        try:
            patient_details = Patient.objects.filter(personId=Person.objects.get(UniqueHealthIdentificationID=uhid))
            serializer = PatientSerializers(patient_details,many=True)

            return JsonResponse(json.dumps(serializer.data, cls=UUIDEncoder),safe=False)
        except Person.DoesNotExist:
            #patient_details = Patient.objects.all()[0]
            #serializer = PatientSerializers()
            return Response({"error":"not found"},status=404)

    @jwt_token_required
    def searchByLocalID(self, request, lfpId):
        try:
            patient_details = Patient.objects.get(localFacilityPatientId=lfpId)
            serializer = PatientSerializers(patient_details)
            # patient_list = []
            # response_details = serializer.data
            # response_details['patient_UHID'] = patient_details.personId.UniqueHealthIdentificationID
            # response_details['patient_UHID_number'] = patient_details.personId.UniqueHealthIdentificationNumber
            # response_details['patient_alternateIDType'] = patient_details.personId.AlternateUniqueIdentificationNumberType
            # response_details['patient_alternateID'] = patient_details.personId.AlternateUniqueIdentificationNumber
            # response_details['patientId'] = str(patient_details.PrimaryKey)

            # patient_list.append(response_details)
            # print(patient_list)
            return Response(json.dumps(serializer.data, cls=UUIDEncoder))
        except Person.DoesNotExist:
            # patient_details = Patient.objects.all()[0]
            serializer = BasicPatientSerializers()
            return Response(serializer.data)
