from rest_framework import serializers

from .models import *



class FacilitySerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    uniqueFacilityIdentificationNumber=serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = Facility
        fields = '__all__'

class MembersSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    class Meta:
        model = Members
        fields = '__all__'

class FacilityApplicationSerializers(serializers.ModelSerializer):
    class Meta:
        model = FacilityApplication
        fields = '__all__'


class FacilityMemberSerializers(serializers.ModelSerializer):
    PrimaryKey = serializers.UUIDField(format='hex', read_only=False)
    facilityId=FacilitySerializers()
    memberId=MembersSerializers(many=True)
    class Meta:
        model = FacilityMembers
        fields = '__all__'

class FacilityTypeSerializers(serializers.ModelSerializer):
    facility_type_code = serializers.IntegerField()
    facility_type_description = serializers.CharField()
    facility_short_type_name = serializers.CharField()


    class Meta:
        model = Facilitytype
        fields = '__all__'
       

 

