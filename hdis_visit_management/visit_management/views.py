import json
import requests
import pika
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from rest_framework import viewsets, status
from rest_framework.response import Response
from visit_management.models import *
import datetime
#from .serializers import *
from datetime import datetime, date
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from visit_management.producer import publish
import uuid
from visit_management.serializers import *
from .decorators import jwt_token_required
from .serializers import *
from uuid import UUID
# Create your views here.
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class VisitViewSet(viewsets.ViewSet):

    @csrf_exempt
    @jwt_token_required
    def checkin(self,request):
        
        values = json.loads(request.body.decode('utf-8'))
        print(values)
        
        #mark visit create episode/encounter and trigger
        facilityId=values['uniqueFacilityIdentificationNumber']
        try:
            facility = Facility.objects.get(uniqueFacilityIdentificationNumber=facilityId)
        except Facility.DoesNotExist:
            return Response("", status=status.HTTP_401_UNAUTHORIZED)
        try:
            provider = Provider.objects.get(uniqueIndividualHealthCareProviderNumber=values['providerLHID'])
        except Provider.DoesNotExist:
            return Response("", status=status.HTTP_401_UNAUTHORIZED)
        try:
            patient = Patient.objects.get(PrimaryKey = values['PatientId'])
        except Patient.DoesNotExist:
            return Response("", status=status.HTTP_401_UNAUTHORIZED)

        #create Episode and Encounter
        
        episode=Episode(facilityId=facility,patientId=patient,EpisodeId=str(uuid.uuid4()))
        episode.save()
        episode.providerId.add(provider)
        episode.save()
        episode_serializer=EpisodeSerializers(episode)
        publish('episode created', json.dumps(episode_serializer.data, cls=UUIDEncoder))

        encounter=Encounter(episodeId=episode,encounterID=str(uuid.uuid4()),encounterType=1,encounterTypeDescription="Outpatient")
        encounter.encounterTime=datetime.strptime(values['appointmentdatetime'],"%Y-%m-%d %H:%M")
        encounter.save()
        encounter_serializer=EncounterSerializers(encounter)
        publish('encounter created', json.dumps(encounter_serializer.data, cls=UUIDEncoder))
        print("published")
        return JsonResponse(json.dumps(encounter_serializer.data, cls=UUIDEncoder), safe=False, status=200)



    def retrieveEpisode(self, request, epId):
        episode_details = Episode.objects.get(PrimaryKey=epId)
        serializer = EpisodeSerializers(episode_details)
        return Response(json.dumps(serializer.data, cls=UUIDEncoder))







     