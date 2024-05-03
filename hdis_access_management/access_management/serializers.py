from .models import *
from django.contrib.auth.models import Group, Permission
from rest_framework.serializers import ModelSerializer

class MemberSerializer(ModelSerializer):

    class Meta:
        model = Member
        exclude = ('groups',)
        extra_kwargs = {'password': {'write_only': True}, 'user_permissions': {'read_only': True, 'allow_null': True}}


class PermissionCodesSerializer(ModelSerializer):

    class Meta:
        model = Permission
        fields = ('codename',)    #Dev Note: Only Code Name is significant when serializing as part of Group


class GroupSerializer(ModelSerializer):
    permissions = PermissionCodesSerializer(many=True)

    class Meta:
        model = Group
        fields = '__all__'
    

class FacilityMembershipSerializer(ModelSerializer):

    class Meta:
        model = FacilityMembership
        fields = '__all__'
        extra_kwargs = {'facility_id': {'format': 'hex'}}
