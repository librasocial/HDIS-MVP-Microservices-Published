from .models import *
from .serializers import *
from .producer import publish
from .oauth2helper import *
import json
import requests
from uuid import UUID
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from oauth2_provider.models import AccessToken
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

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

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # If the obj is a UUID, we simply return its string form
            return str(obj)
        return json.JSONEncoder.default(self, obj)


class IsReadOnlyOperation(permissions.BasePermission):
    """Custom Permission permitting read-only HTTP methods to all users, even if unauthenticated."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsFacilityAdminPermission(permissions.BasePermission):
    """Custom Permission permitting actions only for Administrators of the Facility ID passed as a View parameter."""

    def has_permission(self, request, view):
        if request.auth is None or not isinstance(request.auth, AccessToken):    #Ensures that an OAuth2 Access Token is present
            print("IsFacilityAdminPermission: Access denied due to missing Access Token.") #Debug TODO: Log error details
            return False
        
        requestor = request.user
        if not requestor:
            print("IsFacilityAdminPermission: Access denied to Anonymous User.") #Debug TODO: Log error details
            return False
        
        # Process requests from an Authenticated User holding a valid Access Token.
        print(f"Request received from User: '{requestor.__dict__}'") #Debug
        mid = requestor.id   #Get ID of Requesting User
        fid = view.kwargs.get('fid')    #Get Facility ID passed to the View
        if not fid:
            print("IsFacilityAdminPermission: Access denied as no Facility ID was passed to the View.") #Debug TODO: Log error details
            return False   #Deny access if Member ID or Facility ID parameter has not been passed
        
        # Build Access Management URL used to check Membership
        url = settings.HDIS_AUTH_SERVER + settings.MEMBERSHIP_URL_PATH.format(mid, fid)
        print("URL: ", url) #Debug

        # Retrieve Access Token for Facility Management Client Credentials grant type
        try:
            access_token = get_client_credentials_access_token(request)
        except Exception as e:
            error_message = f"Failed to get Client Credentials grant due to the following error: {e}" #TODO: Review message
            print(f"{error_message}") #TODO: Log error details
            return False
        
        # Invoke Access Management endpoint to check Membership
        membership_response = requests.get(
            url, headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
        )
        if membership_response.status_code == 201:
            response_body = json.loads(membership_response.content.decode('utf-8'))
            if response_body:
                if response_body.roles:
                    # Proceed only if Requesting User is an Administrator of the Facility being acted upon.
                    return "Admin" in response_body.roles 
            print(f"Failed to receive details of Requesting User's Roles at the specified Facility from Access Management. Response Body: {response_body}") #TODO: Review message
            return False
        else:
            print(f"Access Management Membership Check endpoint returned error '{membership_response.status_code}'. Details: '{response_body}'") #TODO: Log error details
            return False


class FacilityTypeViewSet(viewsets.ModelViewSet):
    """Defines CRUD operations on the Facility Type entity managed only by the Superuser Role."""

    queryset = FacilityType.objects.all()
    serializer_class = FacilityTypeSerializer
    permission_classes = [TokenHasReadWriteScope] #TODO: Limit write access to Superuser

    def list_roles_for_facility_type(self, request, facility_type_code):
        """Lists all Roles applicable to a specified Facility Type Code."""

        # Get the Internal Facility Type corresponding to the specified Facility Type Code
        facility_type = get_object_or_404(FacilityType.objects.all(), facility_type_code=facility_type_code)
        facility_type_internal = facility_type.facility_type_internal

        # Retrieve the Roles applicable to the Internal Facility Type
        roles = DefaultRolesByFacilityType.objects.filter(facility_type_internal=facility_type_internal.strip()).values_list('role_code', flat=True).distinct()
        response_body = []
        for role in roles:
            response_body.append(role.strip())
        return JsonResponse(response_body, status=status.HTTP_200_OK, safe=False)


class FacilityViewSet(viewsets.ModelViewSet):
    """Defines actions on the Facility entity."""

    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = [TokenHasReadWriteScope]

    class MemberDTO:
        pass

    class FacilityMembersDTO:
        pass
    
    def create_facility_and_default_users(self, data):
        """Internal method used to create a new Facility and look up default Roles for its Facility Type."""

        try:
            facility_type = FacilityType.objects.get(facility_type_code=data["facility_type_code"])
            facility_type_internal = facility_type.facility_type_internal
            print("Facility Type Internal: ", facility_type_internal)
        except FacilityType.DoesNotExist:
            facility_type_internal = "Clinic"   #TODO: Confirm that it is not better to return an error in this scenario

        print("Data:", data) #Debug
        # Create Facility
        facility = Facility(name = data["facility_name"], 
                            facility_type_code = data["facility_type_code"], 
                            facility_type_service = facility_type_internal.strip(),   #TODO: Does this need renaming to facilityTypeInternal?
                            organization_id = data["organization"])
        facility.save()

        # TODO: Publish Facility Creation Event
        #facility_serializer = FacilitySerializer(facility)
        #publish('facility created', facility_serializer.data)

        facility_members = self.FacilityMembersDTO()
        facility_members.facility_id = facility.facility_id
        facility_members.members = []
        # Get the Default Roles for the Facility Type
        default_roles = DefaultRolesByFacilityType.objects.filter(facility_type_internal=facility_type_internal.strip()).values_list('role_code', flat=True).distinct()
        # Allot a new Member for each Role with the Applicant set as Facility Admin
        for role in default_roles:
            member = self.MemberDTO()
            if role == "Admin":
                # Aassign Name and Email for Facility Admin as per the submitted Application.
                member.username = uuid.uuid4().hex
                member.email = data["applicant_email"]
                member.name = data["applicant_name"]
            else:
                member.username = uuid.uuid4().hex
                member.email = ""
                member.name = "Default " + role
            member.roles = [ role ]

            facility_members.members.append(member.__dict__)

            # # Publish all Members        
            # member_serializer = MembersSerializer(member)
            # member_serializer_to_publish = { 'uniqueFacilityIdentificationNumber': str(facility.facility_id.hex) }
            # member_serializer_to_publish.update(member_serializer.data)
            # publish(member.userRole.lower() + ' created', member_serializer_to_publish)    
            # print(member_serializer_to_publish)
        
        return facility_members

    # TODO: Override class-level permissions to allow anonymous users to invoke this operation
    def create_from_application(self, request):
        """From an anonymously submitted Application, create a new Facility & its default Users based on its Facility Type."""

        # Parse, deserialize and validate the POST request body 
        request_data = request.data
        print("Request Data:", request_data) #Debug
        application_serializer = FacilityApplicationSerializer(data=request_data)
        application_serializer.is_valid(raise_exception=True)

        # If a Facility Application with the same Applicant Email, Mobile Number and Facility Name exists, block the operation
        # TODO: Check whether this should check against Facility objects, whether Mobile should be removed for validation and if Facility Name duplication is okay across Facility Admins
        if FacilityApplication.objects.filter(
            applicant_email = request_data['applicant_email'], 
            applicant_mobile = request_data['applicant_mobile'], 
            facility_name = request_data['facility_name']
        ).exists():
            print('Facility Application exists with the same Email, Mobile and Facility Name. Block duplicate Facility creation.') #Debug
            error_body = {
                "type": request.build_absolute_uri("/errors/duplicate-entity"),
                "title": "Attempt to create duplicate Facility.",
                "detail": "A Facility Application with the same Facility Name, Admin Email & Mobile Number already exists."
            }
            return JsonResponse(error_body, status=status.HTTP_409_CONFLICT)

        print("Identical Facility Application does not exist. Continuing with Facility creation.")
        application_serializer.save()
        data = self.create_facility_and_default_users(application_serializer.data)
        if data.members:
            for member in data.members:
                member["password"] = uuid.uuid4()    #Set a default password

        # Register default set of Facility Users based on the Facility Type
        url = settings.HDIS_AUTH_SERVER + settings.REGISTRATION_URL_PATH
        payload = json.dumps(data.__dict__, cls=UUIDEncoder)
        print("Payload:", payload) #Debug

        try:    #Retrieval of Access Token for Client Credentials grant type
            access_token = get_client_credentials_access_token()
        except Exception as e:
            error_body = { "detail": f"Failed to get access token due to the following error: {e}" } #TODO: Review message
            return JsonResponse(error_body, status=status.HTTP_403_FORBIDDEN)
        
        # Invoke Access Management service endpoint to register new users
        registration_response = requests.post(
            url, data=payload, 
            headers={'Authorization': f'Bearer {access_token}', 'Content-type': 'application/json', 'Accept': 'application/json'}
        )
        http_response = registration_response.status_code
        print(f"Response code from Registration endpoint: {http_response}") #Debug
        data_to_return = json.loads(registration_response.content.decode('utf-8'))
        # if (not data_to_return) or data_to_return[0].input_username:
        #     data_to_return["error_message"] = "Failure creating one or more Default Users. Error details per user below."
        print(f"Response content from Registration endpoint:\n{registration_response.content}") #Debug
        return Response(data_to_return, status=http_response)
   
    
    def list(self, request):  #TODO: Discuss whether method override to add root node is required. If so, make it "facilities".
        """Overrides standard list method of FacilityViewSet to add a root node to the response."""

        default_response = super().list(request)
        response_body = { "facility": default_response.data }
        return Response(response_body, status=status.HTTP_200_OK)  


    @action(detail=False, methods=['GET'], url_path='fid/(?P<fid>[^/.]+)', name='Retrieve By Facility ID')
    def retrieve_by_fid(self, request, fid):
        """Retrieve details for a Facility based on a specified Facility ID."""

        print("FID: ", fid) #Debug
        facility = get_object_or_404(Facility.objects.all(), facility_id=fid)
        serializer = FacilitySerializer(facility)
        return Response(serializer.data)


class OrganizationViewSet(viewsets.ModelViewSet):
    """Defines CRUD operations on the Organization entity managed only by the Superuser Role."""

    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [TokenHasReadWriteScope] #TODO: Limit write access to Superuser


class PackageTypeViewSet(viewsets.ModelViewSet):
    """Defines CRUD operations on the Package Type entity managed only by the Superuser Role."""

    queryset = PackageType.objects.all()
    serializer_class = PackageTypeSerializer
    permission_classes = [TokenHasReadWriteScope] #TODO: Limit write access to Superuser


class PackageViewSet(viewsets.ModelViewSet):
    """Defines CRUD operations on the Package entity managed by Facility Admins."""

    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [TokenHasReadWriteScope, IsReadOnlyOperation | IsFacilityAdminPermission]
