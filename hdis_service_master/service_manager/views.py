from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .decorators import jwt_token_required
from .models import *
from .serializers import *
from uuid import UUID

import json
# Create your views here.
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)
    
class ServiceViewSet(viewsets.ViewSet):
    @jwt_token_required
    def list(self,request):
        data=json.loads(request.body.decode('utf-8'))
        uniqueFacilityIdentificationNumber=data['uniqueFacilityIdentificationNumber']
        try:
            facilityId=Facility.objects.get(uniqueFacilityIdentificationNumber=uniqueFacilityIdentificationNumber)
            service=Service.objects.get(facilityId=facilityId)
        values = json.loads(request.body.decode('utf-8'))
        try:
            serviceCategory=ServiceCategory.objects.get(serviceTypeCode=values['serviceTypeCode'])
            service=Service.objects.get(servicecategoryId=serviceCategory)
            serviceserializer=ServiceSerializers(service)
            return Response(json.dumps(serviceserializer.data, cls=UUIDEncoder))
 
        except serviceType.DoesNotExist:
            pass

        
    @jwt_token_required  
    def create(self,request):
        data=json.loads(request.body.decode('utf-8'))
        serviceName=data['serviceName']
        serviceEffectiveDateFrom=data['serviceEffectiveDateFrom']
        serviceEffectiveDateTo=data["serviceEffectiveDateTo"]
        serviceCost=data["serviceCost"]
        isInventory=data["isInventory"]
        serviceCategory=serviceType.objects.get(serviceTypeName=serviceName)
        uniqueFacilityIdentificationNumber=data['uniqueFacilityIdentificationNumber']
        facilityId=Facility.objects.get(uniqueFacilityIdentificationNumber=uniqueFacilityIdentificationNumber)
        service=Service(servicecategoryId=serviceCategory,facilityId=facilityId,serviceName=serviceName,serviceEffectiveDateFrom=serviceEffectiveDateFrom,serviceEffectiveDateTo=serviceEffectiveDateTo)
        service.serviceCost=serviceCost
        service.isInventory=isInventory
        service.save()
        return Response("", status=status.HTTP_201_CREATED)

    @jwt_token_required 
    def update(self,request):
        data=json.loads(request.body.decode('utf-8'))
        primaryKey=data["primaryKey"]
        serviceEffectiveDateFrom=data['serviceEffectiveDateFrom']
        serviceEffectiveDateTo=data["serviceEffectiveDateTo"]
        serviceCost=data["serviceCost"]
        isInventory=data["isInventory"]
        service=Service.objects.get(primaryKey=primaryKey)
        service.serviceCost=serviceCost
        service.isInventory=isInventory
        service.serviceEffectiveDateFrom=serviceEffectiveDateFrom
        service.serviceEffectiveDateTo=serviceEffectiveDateTo
        service.save()
        return Response("", status=status.HTTP_201_CREATED)


class ProviderServiceViewSet(viewsets.ViewSet):

    @jwt_token_required
    def list(self,request):
        data=json.loads(request.body.decode('utf-8'))
        uniqueIndividualHealthCareProviderNumber=data["uniqueIndividualHealthCareProviderNumber"]
        provider=Provider.objects.get(uniqueIndividualHealthCareProviderNumber=uniqueIndividualHealthCareProviderNumber)
        service=Service.objects.get(providerId=provider)
        serviceserializer=ServiceSerializers(service)
        return Response(json.dumps(serviceserializer.data, cls=UUIDEncoder))











        pass
    def create(self,request):
        

