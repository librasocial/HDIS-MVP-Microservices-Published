from .models import *
from .producer import publish
from .serializers import *
from .oauth2helper import get_client_credentials_access_token
from datetime import datetime
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope


class VisitViewSet(viewsets.ViewSet):

    permission_classes = [TokenHasReadWriteScope]
    
    @csrf_exempt
    def create(self, request):
        """ Check-in a Visit for a previously Registered Patient with an active Appointment.
            This results in the creation of an Episode and an Encounter with the Provider.
            Note: Currently, each Encounter is mapped one-to-one with a new Episode but the 
            long-term intent is for an Episode to span multiple related Encounters.
        """
        
        request_body = request.data
        print(request_body)
        
        # Fetch mandatory inputs
        uhpn = request_body.get('unique_individual_health_care_provider_number')
        lfpid = request_body.get('local_facility_patient_id')
        appointment_id = request_body.get('appointment_id')
        # Ensure mandatory inputs have been provided
        if not all([uhpn, lfpid]):
            return Response({"detail": "Input parameters 'unique_individual_health_care_provider_number' and 'local_facility_patient_id' must all be specified."}, 
                            status=status.HTTP_400_BAD_REQUEST)

        # Retrieve Access Token for Client Credentials grant type
        try:
            access_token = get_client_credentials_access_token()
        except Exception as e:
            error_body = { "details": f"Failed to get Client Credentials token due to the following error: {e}" } #TODO: Review message
            print(f"{error_body}") #TODO: Log error details
            return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Build URL to get Provider details by UHPN
        emp_mgt_url = settings.GET_PROVIDER_BY_UHPN_URL.format(uhpn)
        print("Get Provider By UHPN URL:", emp_mgt_url) #Debug

        # Invoke URL to get Provider details
        provider_details_response = requests.get(
            emp_mgt_url, headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
        )
        if provider_details_response.status_code == status.HTTP_200_OK:
            provider = provider_details_response.json()
            if not provider:
                error_body = { "details": f"Failed to extract Provider details from Employee Management service response. Response Content: {provider_details_response.content}" } #TODO: Review message
                return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            error_body = { "details": f"Error retrieving Provider Details from Employee Management service. Status Code: '{provider_details_response.status_code}', Response Content: {provider_details_response.content}" } #TODO: Log error details
            return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        print("Provider:", provider) #Debug
        
        # Build URL to get Patient details by LFPID
        ptn_mgt_url = settings.GET_PATIENT_BY_LFPID_URL.format(lfpid)
        print("Get Patient Details URL:", ptn_mgt_url) #Debug

        # Invoke URL to get Patient details
        patient_details_response = requests.get(
            ptn_mgt_url, headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
        )
        if patient_details_response.status_code == status.HTTP_200_OK:
            patient = patient_details_response.json()
            if not patient:
                error_body = { "details": f"Failed to extract Patient details from Patient Management service response. Response Content: {patient_details_response.content}" } #TODO: Review message
                return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            error_body = { "details": f"Error retrieving Patient Details from Patient Management service. Status Code: '{patient_details_response.status_code}', Response Content: {patient_details_response.content}" } #TODO: Log error details
            return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        print("Patient:", patient) #Debug
        

        # TODO: Wrap in a traansaction
        # Create Episode and Encounter
        episode_serializer = EpisodeSerializer(data={})
        episode_serializer.is_valid(raise_exception=True)
        episode = episode_serializer.save()

        encounter_dict = dict(episode=episode.primary_key, type=Encounter.Type.Outpatient, 
                              patient_id=lfpid, appointment_id=appointment_id)   #TODO: Encounter Types to be master data
        encounter_serializer = EncounterFlatSerializer(data=encounter_dict)
        encounter_serializer.is_valid(raise_exception=True)
        encounter_serializer.save()

        # Publish new Episode and Encounter
        #publish('episode created', json.dumps(episode_serializer.data, cls=UUIDEncoder))
        #publish('encounter created', json.dumps(encounter_serializer.data, cls=UUIDEncoder))
        #print("published")

        return Response(encounter_serializer.data, status=status.HTTP_200_OK)


    def update(self, request, pk):
        """Allows update to limited attributes (status_code) of an Encounter."""

        new_status = int(request.data.get('status_code'))
        if new_status:
            encounter = get_object_or_404(Encounter.objects.all(), primary_key=pk)
            encounter.status_code = new_status
            encounter.save()
            serializer = EncounterSerializer(encounter)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No updateable parameters provided. Note that updates are allowed only to 'status'."}, status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['GET'], name='Search')
    def search(self, request, *args, **kwargs):
        """Visit Search based on various attributes of Encounter."""

        #TODO: Limit results by Facility depending on Role of requestor?
        # Get query parameters from the request
        patient_id = request.query_params.get('patient_id')
        #patient_mobile = request.query_params.get('patient_mobile')    #TODO: Include in search
        encounter_id = request.query_params.get('encounter_id')
        encounter_status = request.query_params.get('encounter_status')
        encounter_from_date_input = request.query_params.get('encounter_from_date')
        encounter_to_date_input = request.query_params.get('encounter_to_date')
        
        # Ensure minimum mandatory parameters have been provided to avoid returning excessive data and hampering performance
        if not any([patient_id, encounter_id]):
            return Response({"detail": "At least one search parameter among Patient ID and Encounter ID must be specified."}, status=status.HTTP_400_BAD_REQUEST)
        elif encounter_from_date_input and not encounter_to_date_input:
            return Response({"detail": "If 'encounter_from_date' is specified, 'encounter_to_date' must also be specified."}, status=status.HTTP_400_BAD_REQUEST)
                
        # Filter the queryset based on the optional parameters
        queryset = Encounter.objects.all()
        if encounter_id:
            queryset = queryset.filter(primary_key=encounter_id)
        elif patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        if encounter_status:
            queryset = queryset.filter(status_code=encounter_status)
        if encounter_from_date_input:
            try:    #Parse Date parameters
                encounter_from_date = datetime.strptime(encounter_from_date_input,"%Y-%m-%d").date()
                encounter_to_date = datetime.strptime(encounter_to_date_input,"%Y-%m-%d").date()
            except (TypeError, ValueError):
                return Response({"detail": "Invalid Date input. Please specify valid date parameters in yyyy-mm-dd format."}, status=status.HTTP_400_BAD_REQUEST)
            
            queryset = queryset.filter(timestamp__date__gte=encounter_from_date, timestamp__date__lte=encounter_to_date)
        
        # Serialize the filtered queryset
        serializer = EncounterSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class EpisodeViewSet(viewsets.ViewSet):

    permission_classes = [TokenHasReadWriteScope]
    
    def retrieve(self, request, pk):
        episode = get_object_or_404(Episode.objects.all(), primary_key=pk)
        serializer = EpisodeSerializer(episode)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def update(self, request, pk):
        """Allows update to limited attributes (status) of Episode. An Episode can be marked 'Closed' only by a Provider."""

        #TODO: Add permission checks to only allow Providers to proceed.
        new_status = request.data.get('status')
        if new_status:
            episode = get_object_or_404(Episode.objects.all(), primary_key=pk)
            episode.status = new_status
            serializer = EpisodeSerializer(episode)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "No updateable parameters provided. Note that updates are allowed only to 'status'."}, status.HTTP_400_BAD_REQUEST)
