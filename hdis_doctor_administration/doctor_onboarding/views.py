#from django.shortcuts import render
import json,requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from doctor_onboarding.models import *
from django.conf import settings
from .decorators import jwt_token_required
# Create your views here.
#from .producer import publish

######## To Do #########
#Provider Updated event to be published
#doctor creation date
# on older than 7 days, if no registration certificate given, disable doctor
# Provider model needs a field for active, inactive
# Disabling will be manual or out of bound(cron job) trigegring
#negative flows handle
#all doctor fields to be added to be filled by admin/doctor
#add new doctor, move to edit after this
#use primarykey for facility identifier

from doctor_onboarding.serializers import *
from uuid import UUID
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)
class DoctorViewSet(viewsets.ViewSet):
    @jwt_token_required
    def list(self, request):
        
        data=json.loads(request.body.decode('utf-8'))
        print(data)
        #facilityId=data['extra']['facilityId'][0]['uniqueFacilityIdentificationNumber']
        facilityId=data['uniqueFacilityIdentificationNumber']
        doctors = DoctorDetails.objects.filter(UniqueFacilityIdentificationNumber = facilityId)
        serializer = DoctorSerializers(doctors, many=True)
        #publish()
        return Response(serializer.data)

        

        
    @jwt_token_required
    def create(self, request):
      
        serializer = DoctorSerializers(data = request.data)
        serializer.is_valid(raise_exception=True)
        if DoctorDetails.objects.filter(LocalHealthCareProviderNumber = serializer.data['LocalHealthCareProviderNumber']).count() > 0:
            return Response("Doctor may already exist, please verify", status=status.HTTP_300_MULTIPLE_CHOICES)
        else:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @jwt_token_required
    def retrieve(self, request, dId):

        try:
        
            doctor_details = DoctorDetails.objects.get(doctorUserId=dId)
            print(doctor_details)
            serializer = DoctorSerializers(doctor_details)

            documents=DoctorDocuments.objects.filter(doctor_id=doctor_details)
            #print(documents.documentFile.url)
            document_serializer=DoctorDocumentsSerializers(documents,many=True)
            personal=DoctorPersonalDetails.objects.get(doctor_id=doctor_details)
            personal_serializer=DoctorPersonalDetailsSerializers(personal)
            sendData={'doctor':serializer.data,'documents':document_serializer.data,'personal':personal_serializer.data}
            print(sendData)
            return Response(sendData)

        except DoctorDetails.DoesNotExist:

            doctor_details = DoctorDetails.objects.all()[0]
            serializer = DoctorSerializers(doctor_details)
            return Response(serializer.data)
        

    @jwt_token_required
    def getprovider(self, request, dId):
    
        try:
            doctor_details = DoctorDetails.objects.get(doctorUserId=dId)
            provider_details=Provider.objects.get(uniqueIndividualHealthCareProviderNumber=doctor_details.LocalHealthCareProviderNumber)
            serializer = ProviderSerializers(provider_details)
            return Response(serializer.data)

        except DoctorDetails.DoesNotExist:
            provider_details = Provider.objects.all()[0]
            serializer = ProviderSerializers(provider_details)
            return Response(serializer.data)

    def retrieveProvider(self, request, dId):
        provider_details = Provider.objects.get(PrimaryKey=dId)
        serializer = ProviderSerializers(provider_details)
        return Response(json.dumps(serializer.data, cls=UUIDEncoder))
                
    @jwt_token_required
    def update(self, request,dId):
        print("update called")
        try:
            doctor_details=DoctorDetails.objects.get(doctorUserId=dId)
            doctor_details.doctorSpeciality=request.POST['doctorSpeciality']
            doctor_details.doctorBankDetails=request.POST['doctorBankDetails']
            doctor_details.save()
            doctor_personal=DoctorPersonalDetails.objects.get(doctor_id=doctor_details)
            doctor_personal.doctorRegistrationNumber=request.POST['doctorRegistrationNumber']
            doctor_personal.languagesKnown=request.POST['languagesKnown']
            doctor_personal.currentCity=request.POST['currentCity']
            
            print(request.POST['doctorRegistrationNumber'])
            doctor_personal.save()
            doctorRegistrationCertificate=request.FILES['doctorRegistrationCertificate']
            if doctorRegistrationCertificate:
                try:
                    doctor_documents=DoctorDocuments.objects.get(doctor_id=doctor_details,documentType='doctorRegistrationCertificate')
                    doctor_documents.documentFile.save(doctorRegistrationCertificate.name, doctorRegistrationCertificate)
                    doctor_documents.save()

                except DoctorDocuments.DoesNotExist:
                    doctor_documents=DoctorDocuments(doctor_id=doctor_details,documentType='doctorRegistrationCertificate')    
                    doctor_documents.documentFile.save(doctorRegistrationCertificate.name, doctorRegistrationCertificate)
                    doctor_documents.save()

            doctorSignatures=request.FILES['doctorSignatures']
            if doctorSignatures:
                try:
                    doctor_documents=DoctorDocuments.objects.get(doctor_id=doctor_details,documentType='doctorSignatures')
                    doctor_documents.documentFile.save(doctorSignatures.name, doctorSignatures)
                    doctor_documents.save()

                except DoctorDocuments.DoesNotExist:
                    doctor_documents=DoctorDocuments(doctor_id=doctor_details,documentType='doctorSignatures')    
                    doctor_documents.documentFile.save(doctorSignatures.name, doctorSignatures)
                    doctor_documents.save()



            return Response(status=201)



        except DoctorDetails.DoesNotExist:
            return Response(status=404)




    def destroy(self, request):
        pass
    @jwt_token_required    
    def retrieveFields(self, request, fId):

        print('this is '+fId)
        doctor_field_details = FacilityDoctorFields.objects.get(facility_id=fId)
        print(doctor_field_details.facility_id)
        serializer = FacilityDoctorFieldSerializers(doctor_field_details)
        return Response(serializer.data)
        
    @jwt_token_required
    def updateFields(self, request, fId):
        
        doctor_field_details = FacilityDoctorFields.objects.get(facility_id=fId)
        content = list(request.POST.items())
        values = dict(content)
        doctor_fields = {}
        doctor_field_details.doctorLanguage = values['language']
        doctor_field_details.doctorCity = values['city']
        doctor_field_details.doctorSpeciality = values['speciality']
        doctor_field_details.doctorQualification = values['qualification']
        doctor_field_details.doctorDescription = values['description']
        doctor_field_details.doctorImage = values['image']
        doctor_field_details.doctorSignatures = values['sign']
        doctor_field_details.doctorSchedule = values['schedule']
        doctor_field_details.doctorBankDetails = values['bankDetails']
        doctor_field_details.doctorLeaves = values['leaves']
        doctor_field_details.save()
        return HttpResponse('success')
    




