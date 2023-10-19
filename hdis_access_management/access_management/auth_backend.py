from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework_simplejwt.tokens import RefreshToken
#from .models import User
from django.contrib.auth.models import User
from django.core import serializers

User = get_user_model()

class OpenHDISAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            # Your custom authentication logic here
            print("herehere")
            print(email)
            print(password)
            user = User.objects.get(email=email)
            print(user)
            if user.check_password(password):
                return user
            else:
                return None

            #if user.check_password(password):
            #    return user
        except User.DoesNotExist:
            print('user not exist')
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class OpenHDISRefreshToken(RefreshToken):
    def __init__(self, user, *args, **kwargs):
        # Call the parent constructor to create the token
        super().__init__(*args, **kwargs)

        # Add your custom payload data here
        print('user here')
        print(user)
        self['userid'] = user.id
        self['username']=user.username
        self['name']=user.first_name
        self['email']=user.email
        self['group']=serializers.serialize( 'json',user.groups.all())
        facility=user.extra.facilityId.all()[0]
        self['tenantID']=str(facility.uniqueFacilityIdentificationNumber)

            
        

    