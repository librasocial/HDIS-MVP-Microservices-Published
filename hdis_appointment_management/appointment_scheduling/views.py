import json
import requests
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from appointment_scheduling.models import *
from .serializers import *
from datetime import datetime, date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from appointment_scheduling.producer import publish,publish_soap
from .decorators import jwt_token_required

##### todo ###
## decorator as per standard
## provider updated event handling
## provider active,inactive
## book nearest appointment slot for walkins
## checkin autmatically after booking nearest appointment
## handle negative cases
##             token = args[0].headers.get('Authorization', None)

# Create your views here.
from uuid import UUID
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)
@jwt_token_required
def getProviders(request):
        data=json.loads(request.body.decode('utf-8'))
        facilityId=data['uniqueFacilityIdentificationNumber']
        facility=Facility.objects.get(uniqueFacilityIdentificationNumber=facilityId)
        provider = Provider.objects.filter(facilityId=facility)
        serializer = ProviderSerializers(provider, many=True)
        return Response(serializer.data)

@jwt_token_required
def getProviderSchedule(request):
    
        values = json.loads(request.body.decode('utf-8'))
        provider=Provider.objects.filter(uniqueIndividualHealthCareProviderNumber=values['uniqueIndividualHealthCareProviderNumber'])
        provider_schedule=ProviderSchedule.objects.filter(providerId=provider)
        serializer=ProviderScheduleSerializers(provider_schedule,many=False)
        return Response(serializer.data)



def createProviderSchedule(request):
    

    print(2)
@jwt_token_required
@csrf_exempt
def createAppointment(request):
    values = json.loads(request.body.decode('utf-8'))
    print(values)
    #search for person
    facilityId=values['uniqueFacilityIdentificationNumber']
    print(facilityId)

    provider=Provider.objects.get(uniqueIndividualHealthCareProviderNumber=values['uniqueIndividualHealthCareProviderNumber'])
    try:
        facility = Facility.objects.get(uniqueFacilityIdentificationNumber=facilityId)
    except Facility.DoesNotExist:
        return Response("", status=status.HTTP_401_UNAUTHORIZED)

    try:
        patient = Patient.objects.get(PrimaryKey=values['uniqueHealthIdentificationId'])
        #patient.providerId.add(provider)
        #patient.save()
    except Person.DoesNotExist:
        return Response("", status=status.HTTP_401_UNAUTHORIZED)
        

    
    
    print(provider)
    #person_serializer=PersonSerializers(person)
    #   publish_soap('person created',person_serializer.data)
    #  patient_serializer=PatientSerializers(patient)
    # publish_soap('patient created',patient_serializer.data)
    #provider_serializer=ProviderSerializers(provider)
    #publish_soap('provider created',provider_serializer.data)
    

    provider_schedule=ProviderSchedule.objects.get(providerId=provider)

    appointment_slot=AppointmentSessionSlots(providerscheduleId=provider_schedule)
    reqdate=values['date']
    thisdate=datetime.strptime(reqdate, '%m/%d/%Y').date()
    sessiontime=datetime.strptime(values['time'], '%H:%M').time()
    
    appointment_slot.AppointmentSessionStartDate=thisdate
    appointment_slot.AppointmentSessionStartTime=datetime.combine(thisdate, sessiontime)
    appointment_slot.AppointmentScheduleDate=datetime.now()
    appointment_slot.save()
    print("appointment slots saved")
    #patient=Patient.objects.get(personId=person)
    #get appointment start time and date
    appointment=Appointment(patientId=patient,appointmentsessionslotsId=appointment_slot,providerId=provider,facilityId=facility)
    appointment.AppointmentBookingDate=datetime.now()
    appointment.save()
    print('appointment created')
    #appointment_details={}
    #appointment_details['AppointmentId']=str(appointment.PrimaryKey)
    #appointment_details['startTime']=values['date']+' '+values['time']
    #appointment_details['facilityId']=facilityId
    #publish
    
    appointment_serializer=AppointmentSerializers(appointment)
    print(appointment_serializer.data)
    publish_soap('appointment created', json.dumps(appointment_serializer.data, cls=UUIDEncoder))
    #return Response(json.dumps(appointment_serializer.data, cls=UUIDEncoder))
    
    return JsonResponse(json.dumps(appointment_serializer.data, cls=UUIDEncoder),safe=False, status=201)

    
@jwt_token_required
def getProviderAppointmentSlots(request):

        values = json.loads(request.body.decode('utf-8'))
        provider=Provider.objects.filter(uniqueIndividualHealthCareProviderNumber=values['uniqueIndividualHealthCareProviderNumber'])
        provider_schedule=ProviderSchedule.objects.filter(providerId=provider)
        appointment_slots=AppointmentSessionSlots.objects.filter(providerscheduleId=provider_schedule)
        serializer=AppointmentSerializers(appointment_slots,many=True)
        return Response(serializer.data)

@csrf_exempt
@jwt_token_required
def getAppointmentsforProvider(request):
        
        values = json.loads(request.body.decode('utf-8'))
        reqdate=values['requestdate']
        thisdate=datetime.strptime(reqdate, '%m/%d/%Y')
        print(values)
        provider=Provider.objects.get(uniqueIndividualHealthCareProviderNumber=values['uniqueIndividualHealthCareProviderNumber'])
        print(provider)
        provider_schedule=ProviderSchedule.objects.get(providerId=provider)
        
        if AppointmentSessionSlots.objects.filter(providerscheduleId=provider_schedule,AppointmentSessionStartDate=thisdate.date()).count()>0:
            print('here')
            appointment_slots= AppointmentSessionSlots.objects.filter(providerscheduleId=provider_schedule,AppointmentSessionStartDate=thisdate.date())
            serializer=AppointmentSessionSlotsSerializers(appointment_slots,many=True)
            return JsonResponse(serializer.data,safe=False,status=200)
        else:
            data={"error":"no appt"}
            return JsonResponse(data,status=301)




    

@csrf_exempt
@jwt_token_required
def getAppointmentsforPatient(request):
    
    values = json.loads(request.body.decode('utf-8'))
    
    #search for person
    facilityid=values['uniqueFacilityIdentificationNumber']
    print(values)
    person=Person.objects.get(UniqueHealthIdentificationID=values['uniqueHealthIdentificationId'])
    facility=Facility.objects.get(uniqueFacilityIdentificationNumber=facilityid)
    patient=Patient.objects.get(personId=person,facilityId=facility)
    current_datetime = datetime.now()

    # Extract only the date part
    current_date = current_datetime.date()

    if Appointment.objects.filter(patientId=patient,appointmentsessionslotsId__AppointmentSessionStartDate=current_date).count()>0:
        appointment=Appointment.objects.filter(patientId=patient,appointmentsessionslotsId__AppointmentSessionStartDate=current_date)
        print('here')
        serializer=AppointmentSerializers(appointment,many=True)
        return JsonResponse(serializer.data,safe=False,status=200)
    else:
        data={"error":"no appt"}
        return JsonResponse(data,status=301)



    

 

