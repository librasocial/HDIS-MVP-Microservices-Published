from django.shortcuts import render
from rest_framework import viewsets, status
import json
import requests
from .models import FacilityApplication,FacilityMembers,Members,Facility,Facilitytype,RoleAccess
from .serializers import FacilityApplicationSerializers,FacilityMemberSerializers,MembersSerializers,FacilitySerializers,FacilityTypeSerializers
from rest_framework.response import Response
from django.http import JsonResponse
from .decorators import jwt_token_required
from django.conf import settings 
from .producer import publish
from uuid import UUID


###################### TO DO ################################
# publish user created event for all users including default user
# update user event whenever a user is updated
# handle auth events in decorator
# decorator will check userid and facility id when checking token
# fetch facility and userid from request instead of token
# publish the full profile for created user
# capture phone number in profile
# create a change log
# does facility support ABDM
# fail cases handle 


import uuid
# Create your views here.
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)
class MemberViewSet(viewsets.ViewSet):

    @jwt_token_required 
    def addUser(self,request):
        values = json.loads(request.body.decode('utf-8'))
        print(values)
        facilityId=values['uniqueFacilityIdentificationNumber']
        role=values['userGroup']
        if role !='Admin':
            return JsonResponse({}, status=status.HTTP_403_FORBIDDEN)

        member=Members(memberName=values['userName'],memberEmail=values['userEmail'])

        try:
            facility_type_object=Facilitytype.objects.get(facility_type_code=values['facilityTypeCode'])
            facility_type=facility_type_object.facility_type_internal
            print(facility_type)
        except Facilitytype.DoesNotExist:
            facility_type="Clinic"


        permissions=RoleAccess.objects.filter(Facility_type=facility_type.strip(),Facility_User=values['usertType']).values_list('Facility_Permission',flat=True).distinct()
        permission_string = ', '.join([permission.strip() for permission in permissions])
        member.memberPermissions=permission_string
        member.userRole=values['usertType']
        member.save()
        
        memberSerializer=MembersSerializers(member)
        memberSerializer_to_publish = {'uniqueFacilityIdentificationNumber': facilityId}
        memberSerializer_to_publish.update(memberSerializer.data)
        publish(member.userRole.lower()+' created',memberSerializer_to_publish)
    

        facility_members=FacilityMembers.objects.get(facilityId__uniqueFacilityIdentificationNumber=facilityId)
        facility_members.memberId.add(member)
        facility_members.save()
        member_serializer=MembersSerializers(member)
        url = settings.HDIS_AUTH_SERVER+"/access/add_user/"
        payload = json.dumps(member_serializer.data)
        print('this is the payload')
        print(payload)
        token=request.headers.get('Authorization', None)

        r = requests.post(url, data=payload,
                            headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization':token})
        datatoSend={"created":str(member.PrimaryKey.hex)}
        if r.status_code==201:
            
            #publish facility
            print('success')
            return JsonResponse(datatoSend, status=status.HTTP_201_CREATED)
        
        else:
            return JsonResponse(datatoSend, status=status.HTTP_403_FORBIDDEN)


        

    

    @jwt_token_required
    def retrieveUser(self,request,Upk):
        
        print(Upk)
        member=Members.objects.get(PrimaryKey=Upk)
        member_serializer=MembersSerializers(member)
        return JsonResponse(member_serializer.data, status=status.HTTP_200_OK)
    
    @jwt_token_required
    def updateUser(self,request,Upk):

        values = json.loads(request.body.decode('utf-8'))
        member=Members.objects.get(PrimaryKey=values['userid'])
        member.memberName=values['name']
        member.memberEmail=values['email']
        member.memberMobile=values['mobile']
        member.save()
        
        #publish member updated
        memberSerializer=MembersSerializers(member)
        memberSerializer_to_publish = {'uniqueFacilityIdentificationNumber': values['uniqueFacilityIdentificationNumber']}
        memberSerializer_to_publish.update(memberSerializer.data)
        publish(member.userRole.lower()+' updated',memberSerializer_to_publish)
 
        
        url = settings.HDIS_AUTH_SERVER+"/access/update_user/"
        payload = json.dumps(values)
        token=request.headers.get('Authorization', None)
        r = requests.post(url, data=payload,
                            headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization':token})
        datatoSend={}
        if r.status_code==200:
            
            #publish facility
            return JsonResponse(datatoSend, status=status.HTTP_201_CREATED)
        
        else:
            return JsonResponse(datatoSend, status=status.HTTP_403_FORBIDDEN)

        
        



         


class FacilityViewSet(viewsets.ViewSet):

    @jwt_token_required
    def listUserType(self,request):
        values = json.loads(request.body.decode('utf-8'))
        try:
            facility_type_object=Facilitytype.objects.get(facility_type_code=values['facilityTypeCode'])
            facility_type=facility_type_object.facility_type_internal
            print(facility_type)
        except Facilitytype.DoesNotExist:
            facility_type="Clinic"

        users=RoleAccess.objects.filter(Facility_type=facility_type.strip()).values_list('Facility_User',flat=True).distinct()
        userTypes=[]
        for user in users:
            userTypes.append(user.strip())
        return JsonResponse(json.dumps(userTypes), status=status.HTTP_200_OK,safe=False)



    def facilityType(self,request):
        facilities=Facilitytype.objects.all()
        all_facilities=FacilityTypeSerializers(facilities,many=True)
      #  print(all_facilities.data)
        return JsonResponse(all_facilities.data, status=status.HTTP_200_OK,safe=False)


    def createFacilityandDefaultUsers(self,data):

        print(data["facilityTypeCode"])
        try:
            facility_type_object=Facilitytype.objects.get(facility_type_code=data["facilityTypeCode"])
            facility_type=facility_type_object.facility_type_internal
            print(facility_type)
        except Facilitytype.DoesNotExist:
            facility_type="Clinic"


        

        #create Facility
        facility=Facility(departmentName=data["facilityName"],facilityTypeCode=data["facilityTypeCode"],facilityTypeService=facility_type.strip())
        facility.save()

        facility_serializer=FacilitySerializers(facility)
        publish('facility created',facility_serializer.data)



        facility_members=FacilityMembers.objects.create(facilityId=facility)

        
        users=RoleAccess.objects.filter(Facility_type=facility_type.strip()).values_list('Facility_User',flat=True).distinct()

        for user in users:
            member=Members(userRole=user)
            if user=="Admin":
                member.memberEmail=data["facilityApplicantEmail"]
                member.memberName=data["facilityApplicantName"]
            else:
                member.memberName= "Default " + user

            permissions=RoleAccess.objects.filter(Facility_type=facility_type.strip(),Facility_User=user).values_list('Facility_Permission',flat=True).distinct()
            permission_string = ', '.join([permission.strip() for permission in permissions])
            member.memberPermissions=permission_string
            member.save()

            #if user=="Doctor":
            #    datatoSend={"facilityID":str(facility.uniqueFacilityIdentificationNumber.hex),"userid":str(member.PrimaryKey.hex),"name":member.memberName}
            #    publish('doctor created',datatoSend)

            #publish all members instead of just doctor
        
            memberSerializer=MembersSerializers(member)
            memberSerializer_to_publish = {'uniqueFacilityIdentificationNumber': str(facility.uniqueFacilityIdentificationNumber.hex)}
            memberSerializer_to_publish.update(memberSerializer.data)
            publish(member.userRole.lower()+' created',memberSerializer_to_publish)    
            print(memberSerializer_to_publish)    
            facility_members.memberId.add(member)



        facility_members.save()

        facility_members_serializers=FacilityMemberSerializers(facility_members)
        return facility_members_serializers.data



    
    def create(self,request):

        values = json.loads(request.body.decode('utf-8'))
        print(values)
        
        serializer=FacilityApplicationSerializers(data=values)
        serializer.is_valid(raise_exception=True)
        try:
            FacilityApplication.objects.get(facilityApplicantEmail=values['facilityApplicantEmail'],facilityApplicantMobile=values['facilityApplicantMobile'],facilityName=values['facilityName'])
            print('Existing Facility')
        except FacilityApplication.DoesNotExist:
            print("facility does not exist")
            serializer.save()
            #create facility & users
            data=self.createFacilityandDefaultUsers(serializer.data)
            #create users
            #print(json.dumps(data))
            #print(data)


            url = settings.HDIS_AUTH_SERVER+"/access/register/"
            payload = json.dumps(data)
            print(payload)
            r = requests.post(url, data=payload,
                                headers={'Content-type': 'application/json', 'Accept': 'application/json'})

            datatoSend = json.loads(r.content.decode('utf-8'))

            if r.status_code==201:
                
                
                #publish facility
                return JsonResponse(datatoSend, status=status.HTTP_201_CREATED)
            
            else:
                return JsonResponse(datatoSend, status=status.HTTP_403_FORBIDDEN)


                ##sendTokenBack and return to frontend
   
      

    
        

    def update(self,request):

        print(2)
    
    
    @jwt_token_required
    def list(self,request):
        data=json.loads(request.body.decode('utf-8'))
        print(data['uniqueFacilityIdentificationNumber'])
        facility_members=FacilityMembers.objects.filter(facilityId__uniqueFacilityIdentificationNumber=data['uniqueFacilityIdentificationNumber'])
        member_serializer=FacilityMemberSerializers(facility_members,many=True)
        
        datatoSend={"users":member_serializer.data,"facility":data}

        return JsonResponse(datatoSend,status=status.HTTP_200_OK,safe=False)

    #@jwt_token_required
    def retrieve(self, request, fId):
        print(fId)
        #print(data['extra']['facilityId'][0]['uniqueFacilityIdentificationNumber'])
        facility = Facility.objects.get(PrimaryKey=fId)
        facility_serializer = FacilitySerializers(facility)
        return Response(json.dumps(facility_serializer.data, cls=UUIDEncoder))
        #return JsonResponse(facility_serializer.data, status=status.HTTP_200_OK, safe=False)
        


    def delete(self,request):

        print(4) 

    def adduser(self,request):

        print(5)

    def listusers(self,request):
        print(6)

    def updateuser(self,request):
        print(7)

    def deleteuser(self,request):
        print(8)    




    

