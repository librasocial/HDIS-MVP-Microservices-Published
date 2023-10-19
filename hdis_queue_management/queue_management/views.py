from django.shortcuts import render
import json
from uuid import UUID
from rest_framework import viewsets, status
from .models import *
from datetime import datetime
from django.http import JsonResponse
import random
####todo
#### caputre visit encounter and episode
## generate queue token number 
## on post request return token number for episode/encounter
##
# Create your views here.
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class QueueViewSet(viewsets.ViewSet):
    
    def getToken(self,request):

        values = json.loads(request.body.decode('utf-8'))
        print(values)
        uniqueIndividualHealthCareProviderNumber=values['providerLHID']
        uniqueFacilityIdentificationNumber=values['uniqueFacilityIdentificationNumber']
        tokenday_obj=datetime.strptime(values['appointmentdatetime'], "%Y-%m-%d %H:%M")
        tokenDay=tokenday_obj.date()

        try:
            facility=Facility.objects.get(uniqueFacilityIdentificationNumber=uniqueFacilityIdentificationNumber)
            provider=Provider.objects.get(uniqueIndividualHealthCareProviderNumber=uniqueIndividualHealthCareProviderNumber)

            token=Token.objects.get(facilityId=facility,providerId=provider,tokenDay=tokenDay)
            tokenNumber=token.tokenNumber
            data={"CurrentToken":tokenNumber}
            return JsonResponse(json.dumps(data),safe=False)

        except Token.DoesNotExist:
            tokenNumber=random.randrange(1, 50, 3)
            data={"CurrentToken":tokenNumber}
            return JsonResponse(json.dumps(data),status=404,safe=False)


        
        #providerid 
        #facilityid
        #day

        #return current token numbeer
        pass
