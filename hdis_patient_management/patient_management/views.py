from .models import *
from .serializers import *
from .oauth2helper import *
from .producer import publish
from datetime import datetime
import json
import random
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

class IsReadOnlyOperation(permissions.BasePermission):
    """Custom Permission permitting read-only HTTP methods to all users, even if unauthenticated."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsSuperuserPermission(permissions.BasePermission):
    """Custom Permission permitting operations only by Superusers."""

    def has_permission(self, request, view):
        return request.user.is_superuser    #TODO: Need to do this via custom claims in a JWT Token


class IsFacilityMemberPermission(permissions.BasePermission):
    """Custom Permission permitting actions only for trusted clients or Members of the Facility ID passed as a View parameter."""

    def has_permission(self, request, view):
        if request.auth is None or not isinstance(request.auth, AccessToken):    #Ensures that an OAuth2 Access Token is present
            print("IsFacilityMemberPermission: Access denied due to missing Access Token.") #Debug TODO: Log error details
            return False
        
        print(f"Request Auth object: '{request.auth.__dict__}'") #Debug
        requestor = request.user
        if request.auth.application:    #If the Access Token is associated with an Application...
            grant_type = request.auth.application.authorization_grant_type
            print(f"Request Grant Type: '{grant_type}'") #Debug
            if grant_type == 'client-credentials':    #TODO: Check for specific Client ID
                # Grant access when the invocation originates from a trusted service.
                return True
        elif requestor:
            print(f"Request received from User: '{requestor.__dict__}'") #Debug
            # Process requests from an Authenticated User holding a valid Access Token.
            mid = requestor.id   #Get ID of Requesting User
            fid = view.kwargs.get('fid')    #Get Facility ID passed to the View
            if not fid:
                print("IsFacilityMemberPermission: Access denied as no Facility ID was passed to the View.") #Debug TODO: Log error details
                return False   #Deny access if Member ID or Facility ID parameter has not been passed

            # Build Access Management URL used to check Membership
            url = settings.HDIS_AUTH_SERVER + settings.MEMBERSHIP_URL_PATH.format(mid, fid)
            print("URL:", url) #Debug

            # Retrieve Access Token for Facility Management Client Credentials grant type
            try:
                access_token = get_client_credentials_access_token(request)
            except Exception as e:
                error_message = f"Failed to get Client Credentials token due to the following error: {e}" #TODO: Review message
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
                        # TODO: Proceed only if Requesting User has an assigned Role at the Facility.
                        return True
                print(f"Failed to receive details of Requesting User's Roles at the specified Facility from Access Management. Response Body: {response_body}") #TODO: Review message
                return False
            else:
                print(f"Access Management Membership Check endpoint returned error '{membership_response.status_code}'. Details: '{response_body}'") #TODO: Log error details
                return False
        else:    #Grant Type is neither Client Credentials nor Password 
            print("IsFacilityMemberPermission: Access denied - either Client Credentials or Authenticated User required.") #TODO: Log error details
            return False


class PersonViewSet(viewsets.ModelViewSet):
    """Defines CRUD operations on the Person entity. Accessible only to Superusers."""

    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = [TokenHasReadWriteScope]#, IsSuperuserPermission]


class PatientViewSet(viewsets.ModelViewSet):
    """Defines CRUD operations on the Patient entity."""

    queryset = Patient.objects.all()
    #serializer_class = PatientSerializer
    permission_classes = [TokenHasReadWriteScope,]# IsSuperuserPermission|IsFacilityMemberPermission]


    def get_serializer_class(self):
        if self.action == 'update':
            return PatientWithoutNestedPersonSerializer
        else:
            return PatientSerializer


    def create(self, request):
        """Register a new Patient at a particular Facility."""

        #TODO: Wrap in a transaction
        request_data = request.data
        print("Request Data:", request_data) #Debug

        fid = request_data['facility_id']
        print("fid:", fid) #Debug
        if not fid:
            error_body = { "detail": f"Failued due to invalid Facility ID being passed: '{fid}'" }
            return Response(error_body, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate Facility ID using Facility Management endpoint for Facility Details
        url = settings.FACILITY_DETAILS_ENDPOINT.format(fid)
        print("URL:", url) #Debug

        try:    #Retrieval of Access Token for Client Credentials grant type
            access_token = get_client_credentials_access_token()
        except Exception as e:
            error_body = { "detail": f"Failed to get access token due to the following error: {e}" } #TODO: Review message
            return Response(error_body, status=status.HTTP_403_FORBIDDEN)
        
        # Invoke Access Management service endpoint to register new users
        facility_detail_response = requests.get(
            url,
            headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
        )
        http_status = facility_detail_response.status_code
        print(f"Response code from Facility Details endpoint: {http_status}") #Debug
        data_to_return = json.loads(facility_detail_response.content.decode('utf-8'))
        print(f"Response content from Facility Details endpoint:\n{data_to_return}") #Debug
        if http_status != 200:
            data_to_return["detail"] = f"Facility ID could not be validated. Response from Facility Management service: {http_status} {data_to_return['detail']}"
            return Response(data_to_return, status=http_status)
        print("Facility ID validated successfully.") #Debug

        dob = datetime.strptime(request_data['patient_dob'], '%Y-%m-%d').date()

        # Block operation if previously registered Patients with the same Name, Gender and Year of Birth exist at the same Facility
        duplicate_patients = Patient.objects.filter(patient_name=request_data['patient_name'],
                                                   patient_gender=request_data['patient_gender'],
                                                   patient_dob__year=dob.year,
                                                   facility_id = fid)
        print(duplicate_patients)
        if duplicate_patients.exists():
            duplicate_patients_serializer = PatientSerializer(duplicate_patients, many=True)
            print(f"Duplicate Patients: {duplicate_patients_serializer.data.__dict__}") #Debug
            return Response({"detail": "Cannot register Patient because one or more Patients with the same Name, Gender and Year of Birth are already registered at the same Facility."
                            }, status=status.HTTP_409_CONFLICT)
        #TODO: Initial search by mobile, if matching check Name, Gender, YOB - if matched, proceed as same Patient, else create new one. Allow bypass of this operation block via an override flag.


        if 'unique_health_identification_number' in request_data:
            print("UID present") #Debug
            person = Person(nationality_code=1,     #TODO: Check whether other Nationalities are to be supported.
                            unique_health_identification_number=request_data.get('unique_health_identification_number'),
                            unique_health_id=request_data.get('unique_health_id'))
        else:
            print("UID not present") #Debug
            # Allocate unique local Patient ID and UHID; TODO: Separate generated internal ID from ABHA ID
            while True:
                local_UHID_number = 'OH' + str(random.randint(100000000, 999999999))
                if not Person.objects.filter(unique_health_identification_number=local_UHID_number).exists(): break
            while True:
                local_UHID = 'UID' + str(random.randint(10000000, 99999999))
                if not Person.objects.filter(unique_health_id=local_UHID).exists(): break

            person = Person(nationality_code=1, unique_health_identification_number=local_UHID_number, unique_health_id=local_UHID)

        person.save()
        person_serializer = PersonSerializer(person)
        #publish('person created', person_serializer.data)  #Temporarily disabled

        # Generate local, unique Patient ID
        while True:
            local_UHID_number = 'P' + str(random.randint(100000000, 999999999))
            if not Patient.objects.filter(local_facility_patient_id=local_UHID_number).exists(): break

        patient = Patient(person=person, patient_name=request_data['patient_name'], local_facility_patient_id=local_UHID_number, patient_gender=request_data['patient_gender'], 
                          patient_dob=dob, facility_id=uuid.UUID(fid), patient_mobile=request_data.get('patient_mobile'))
        age_years, age_months, age_days = patient.compute_age()
        patient.patient_age = f"{age_years},{age_months},{age_days}"
        print(f"Patient Age: '{patient.patient_age}'") #Debug

        full_address = ' '.join(filter(None, [request_data.get('address'), request_data.get('location'), request_data.get('city'), request_data.get('pin')]))
        address_type = request_data.get("patient_address_type")
        patient.patient_address_type = address_type    #TODO: Remove Address Details from Patient table?
        patient.patient_address = full_address
        patient.save()
        
        patient_address = PatientAddressDetail(patient=patient, patient_address=full_address,
                                               patient_address_type=address_type, patient_mobile=request_data.get('patient_mobile'),
                                               patient_email_url=request_data.get('email'))
        patient_address.save()

        patient_serializer = PatientSerializer(patient)
        #patient_serializer.is_valid(raise_exception=True)
        #publish('patient created', patient_serializer.data)    #Temporarily disabled
        return Response(patient_serializer.data)


    def update(self, request, pk):
        """Updates Patient Data and attempts to publish the corresponding Business Event."""

        response = super().update(request, pk)
        if response.status_code == 200:
            try:
                pass #publish('patient updated', response.data)    #Temporarily disabled
            except Exception:
                print("Failed to publish Business Event for 'patient updated'") #Debug
        return response


    # def destroy(self, request):
    #     """Deactivate Patient."""
    #     pass    #TODO: To be implemented


    @action(detail=False, methods=['GET'], url_path='uhid/(?P<uhid>[^/.]+)', name='Retrieve By UHID')
    def retrieve_by_uhid(self, request, uhid):
        """Retrieve details for a Patient based on their UHID."""

        person = get_object_or_404(Person.objects.all(), unique_health_id=uhid)
        patients = Patient.objects.filter(person=person)  #TODO: Results should be limited to the requesting user's Facility
        if patients.exists():
            serializer = PatientSerializer(patients, many=True)
            return Response(serializer.data)
        else:
            return Response({"details": "No Patients found for specified UHID."}, status=status.HTTP_404_NOT_FOUND)
    
    
    @action(detail=False, methods=['GET'], url_path='lfpid/(?P<lfpid>[^/.]+)', name='Retrieve By Patient ID')
    def retrieve_by_internal_patient_id(self, request, lfpid):
        """Retrieve details for a Patient based on their internal Patient ID."""
        
        patient = get_object_or_404(Patient.objects.all(), local_facility_patient_id=lfpid) #TODO: Results should be limited to requestiing User Facilities
        serializer = PatientSerializer(patient)
        return Response(serializer.data)
    
    
    @action(detail=False, methods=['GET'], name='Search')
    def search(self, request, *args, **kwargs):
        """Patient Search based on various attributes."""

        #TODO: Limit results by Facility depending on Role of requestor?
        # Get optional query parameters from the request query parameters
        name = request.query_params.get('name')
        gender = request.query_params.get('gender')
        yob = request.query_params.get('yob')
        mobile = request.query_params.get('mobile')

        if not any([name, gender, yob, mobile]):
            return Response({"detail": "At least one search parameter must be specified."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter the queryset based on the optional parameters
        queryset = Patient.objects.all()
        if name:
            queryset = queryset.filter(patient_name=name)
        if gender:
            queryset = queryset.filter(patient_gender=gender)
        if yob:
            queryset = queryset.filter(patient_dob__year=yob)  
        if mobile:
            queryset = queryset.filter(patient_mobile=mobile)
        
        # Serialize the filtered queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    # def merge(self, request):
    #     """Merge multiple Patients to link them to the same Person."""
    #     pass    #TODO: To be implemented
        