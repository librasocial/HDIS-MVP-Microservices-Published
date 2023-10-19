from django.shortcuts import render
from rest_framework import viewsets, status
import json
#from .models import User,Facility
from django.contrib.auth.models import User,Group
from .auth_backend import OpenHDISRefreshToken
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .models import Facility
import uuid

from .serializers import OpenHDISTokenObtainPairSerializer,FacilitySerializers,UserSerializers,BasicUserSerializers
# Create your views here.
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView
from rest_framework_simplejwt.tokens import RefreshToken
from .decorators import jwt_token_required
class OpenHDISTokenObtainPairView(TokenObtainPairView):
    serializer_class = OpenHDISTokenObtainPairSerializer

#class OpenHDISTokenRefreshView(TokenRefreshView):
 #   serializer_class = TokenRefreshSerializer
    # Your customization here

#class OpenHDISTokenVerifyView(TokenVerifyView):
 #   serializer_class = TokenVerifySerializer
    # Your customization here    

class AccessViewSet(viewsets.ViewSet):

    def user_belongs_to_group(self,user, group_name):
        try:
            group = Group.objects.get(name=group_name)
            return group in user.groups.all()
        except Group.DoesNotExist:
            return False
        
    def group_has_permission(self,group,permission_name):
        try:
            permission=Permission.objects.get(codename=permission_name)
            return permission in group.permissions.all()
        except Permission.DoesNotExist:
            return False    
    
    @jwt_token_required
    def AddUser(self,request,user):

        print(user)
        if self.user_belongs_to_group(user, 'Admin')==False:
            return Response(data="{}", status=status.HTTP_403_FORBIDDEN)

        
        print(request.body.decode('utf-8'))
        member=json.loads(request.body.decode('utf-8'))
        add_user=User.objects.create(first_name=member['memberName'],email=member['memberEmail'],username=member['PrimaryKey'])
        group_user, _ = Group.objects.get_or_create(name=member['userRole'])
        ct = ContentType.objects.get_for_model(User)

        permissions=member['memberPermissions'].split(',')
        for permission in permissions:
            if self.group_has_permission(group_user,permission.strip())==False:
                new_permission, _=Permission.objects.get_or_create(codename=permission.strip(),content_type=ct)
                group_user.permissions.add(new_permission)


        add_user.groups.add(group_user)        

        #user.extra.userRole=member['userRole'],
        
        add_user.extra.userMobile=member['memberMobile']
        add_user.extra.facilityId.add(user.extra.facilityId.all().first())
        add_user.save()
        print("saved user")




        return Response(data="{}", status=status.HTTP_201_CREATED)


    @jwt_token_required
    def UpdateUser(self,request,user):
        data=json.loads(request.body.decode('utf-8'))
        print(data)
        update_user=User.objects.get(username=data['userid'])
        password=data['password']
        confirm_password=data['confirm_password']
        if len(password)>0:
            if password==confirm_password:
                update_user.set_password(password)
            else:
                return Response(data="{'error':'passwords do not match'}", status=400) 
                
        update_user.first_name=data['name']
        update_user.email=data['email'].strip()
        update_user.extra.userMobile=data['mobile']
        update_user.save()
        return Response(data="{}", status=status.HTTP_200_OK)    






    @jwt_token_required
    def ChangePass(self,request,user):
        data=json.loads(request.body.decode('utf-8'))
        password=data['password']
        print('password is ')
        print(password)
        user.set_password(password)
        user.save()
        
        return Response(data="{}", status=status.HTTP_200_OK)


    @jwt_token_required
    def CheckAccess(self,request,user):
        user_serializer=BasicUserSerializers(user)
        return JsonResponse(user_serializer.data,status=status.HTTP_200_OK)


    def Register(self,request):


        print('here')
        data=json.loads(request.body.decode('utf-8'))
        facility=data['facilityId']
        print(facility)
        facility_serializer=FacilitySerializers(data=facility)
        facility_serializer.is_valid()
        facilityId = facility_serializer.save()
        ct = ContentType.objects.get_for_model(User)

        Members=data['memberId']
        for member in Members:
            user=User.objects.create(first_name=member['memberName'],email=member['memberEmail'],username=member['PrimaryKey'])
            group_user, _= Group.objects.get_or_create(name=member['userRole'])
            print(group_user)
            permissions=member['memberPermissions'].split(',')
            for permission in permissions:
                  if self.group_has_permission(group_user,permission.strip())==False:
                      new_permission, _=Permission.objects.get_or_create(codename=permission.strip(),content_type=ct)
                      group_user.permissions.add(new_permission)

            user.groups.add(group_user)
            user.extra.userMobile=member['memberMobile']
            user.extra.facilityId.add(facilityId)
            user.save()
            print("saved user")
            if member['userRole']=='Admin':
                user_serializer=UserSerializers(data=user)
                user_serializer.is_valid()
                refresh = OpenHDISRefreshToken(user)
                print(refresh)
                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
                print(data)
            

        return JsonResponse(data, status=status.HTTP_201_CREATED)


