from rest_framework import serializers

from .models import Facility,Extra
from django.contrib.auth.models import User,Group,Permission


from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,TokenVerifySerializer

from django.contrib.auth import authenticate
from .auth_backend import OpenHDISRefreshToken




class OpenHDISTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'  # customize the username field to use email instead of username
    def validate(self, attrs):
        # Use the email and password fields from the request data for authentication
        print("i am here")

        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        # Add the custom claims to the token
        
        refresh = OpenHDISRefreshToken(user)
        user_serializer=BasicUserSerializers(user)
        data = {'refresh': str(refresh), 'access': str(refresh.access_token),'user':user_serializer.data}
        return data

class FacilitySerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    uniqueFacilityIdentificationNumber = serializers.UUIDField(format='hex', read_only=False)


    class Meta:
        model = Facility
        fields = '__all__'

class UserSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    facilityId=FacilitySerializers(many=True)
    class Meta:
        model = User
        fields = '__all__'         

class BasicFacilitySerializers(serializers.ModelSerializer):
    uniqueFacilityIdentificationNumber = serializers.UUIDField(format='hex', read_only=False)

    class Meta:
        model = Facility
        fields = ('uniqueFacilityIdentificationNumber','facilityTypeCode','departmentName',)

class ExtraSerializers(serializers.ModelSerializer):
    facilityId=BasicFacilitySerializers(many=True)
    class Meta:
        model = Extra
        fields = ('userMobile','facilityId')

class PermissionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ('codename',)

class GroupSerializers(serializers.ModelSerializer):
    permissions=PermissionSerializers(many=True)
    class Meta:
        model = Group
        fields = ('permissions','name')
    
class BasicUserSerializers(serializers.ModelSerializer):
    extra=ExtraSerializers()
    groups=GroupSerializers(many=True)
    is_authenticated = serializers.SerializerMethodField()

    def get_is_authenticated(self, obj):
        # Perform custom logic to compute the value of my_field
        # You can access the object being serialized using 'obj'
        return True
    class Meta:
        model = User
        fields = ('extra','groups','username','email','is_authenticated')

