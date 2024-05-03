from .oauth2helper import get_client_credentials_access_token
from .models import *
from .serializers import *
import datetime
import requests
from django.conf import settings
from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

class QueueViewSet(viewsets.ViewSet):

    permission_classes = [TokenHasReadWriteScope]
    
    def join_queue(self, request):
        """Issues a new, sequential Token Number """

        #TODO: Wrap in transaction
        request_body = request.data
        print("Request Body:", request_body) #Debug

        # Parse input parameters
        uhpn = request_body.get('provider_uhpn')
        visit_date_input = request_body.get('visit_datetime')
        try:
            visit_date = datetime.datetime.strptime(visit_date_input, "%Y-%m-%d %H:%M").date()
        except (TypeError, ValueError):
            return Response({"detail": "Invalid Date input. Please specify a valid 'vist_datetime' parameter in yyyy-mm-dd format."}, status=status.HTTP_400_BAD_REQUEST)
        encounter_id_input = request_body.get('encounter_id')        
        
        # Validate the supplied Resource ID and Date
        # Retrieve Access Token for Client Credentials grant type
        try:
            access_token = get_client_credentials_access_token()
        except Exception as e:
            error_body = { "details": f"Failed to get Client Credentials token due to the following error: {e}" } #TODO: Review message
            print(f"{error_body}") #TODO: Log error details
            return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Build URL to get Provider details by UHPN
        visit_mgt_url = settings.GET_PROVIDER_BY_UHPN_URL.format(uhpn)
        print("Get Provider By UHPN URL:", visit_mgt_url) #Debug

        # Invoke URL to get Provider Details by UHPN
        provider_details_response = requests.get(
            visit_mgt_url, headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
        )
        if provider_details_response.status_code == status.HTTP_200_OK:
            provider = provider_details_response.json()
            if not provider:
                error_body = { "details": f"Failed to extract Provider details from Employee Management service response. Response Content: {provider_details_response.content}" } #TODO: Review message
                return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif provider_details_response.status_code == status.HTTP_404_NOT_FOUND:
            error_body = { "details": f"Error retrieving Provider Details from Employee Management service. Invalid UHPN input." }
            return Response(error_body, status.HTTP_400_BAD_REQUEST)
        else:
            error_body = { "details": f"Error retrieving Provider Details from Employee Management service. Status Code: '{provider_details_response.status_code}', Response Content: {provider_details_response.content}" } #TODO: Log error details
            return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        provider["employee_id"] = "E314864344"    #TODO: Remove after resolving issue with Emp ID
        print("Provider:", provider) #Debug
        employee_id = provider["employee_id"]
        
        # Build URL to validate Encounter ID
        visit_mgt_url = settings.GET_ENCOUNTER_URL.format(encounter_id_input)
        print("Get Encounter By ID URL:", visit_mgt_url) #Debug

        # Invoke URL to get Encounter Details by ID
        encounter_details_response = requests.get(
            visit_mgt_url, headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
        )
        if encounter_details_response.status_code == status.HTTP_200_OK:
            encounter = encounter_details_response.json()
            if not encounter:
                error_body = { "details": f"Failed to extract Encounter details from Visit Management service response. Response Content: {encounter_details_response.content}" } #TODO: Review message
                return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif encounter_details_response.status_code == status.HTTP_404_NOT_FOUND:
            error_body = { "details": f"Error retrieving Encounter Details from Visit Management service. Invalid Encounter ID input." }
            return Response(error_body, status.HTTP_400_BAD_REQUEST)
        else:
            error_body = { "details": f"Error retrieving Encounter Details from Visit Management service. Status Code: '{encounter_details_response.status_code}', Response Content: {encounter_details_response.content}" } #TODO: Log error details
            return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        print("Provider:", provider) #Debug
        
        # Track issued Tokens for the specified date, creating an entry with Current Token Number set to  
        #   1 if it does not exist or incrementing Current Token Number by 1 if it does.
        token, created = Token.objects.get_or_create(resource_id=employee_id, date=visit_date, defaults={"last_token_number": 1})
        if not created:
            token.last_token_number += 1
            token.save()
        
        # Make a corresponding Queue entry 
        queue = Queue.objects.create(resource_id=employee_id, date=visit_date, token_number=token.last_token_number, encounter_id=uuid.UUID(encounter_id_input))
        serializer = QueueSerializer(queue)
        return Response(serializer.data, status=status.HTTP_201_CREATED, 
                        headers={ 'Location': f"{reverse('queue-search')}?encounter_id={encounter_id_input}" })
    

    def search(self, request, *args, **kwargs):
        """Queue Search based on various parameters."""

        #TODO: Limit results by Facility depending on Role of requestor?
        # Get query parameters from the request
        resource_id = request.query_params.get('resource_id')
        for_date_input = request.query_params.get('for_date')
        encounter_id = request.query_params.get('encounter_id')

        # Ensure minimum mandatory parameter sets have been provided and filter accordingly
        if encounter_id:
            if resource_id or for_date_input:
                return Response({"detail": "Invalid input combination. Please specify either 'encounter_id' only or both 'for_date' and 'resource_id'."}, status=status.HTTP_400_BAD_REQUEST)
            queryset = Queue.objects.filter(encounter_id=encounter_id)
        elif all([resource_id, for_date_input]):
            try:
                for_date = datetime.datetime.strptime(for_date_input, "%Y-%m-%d").date()
            except (TypeError, ValueError):
                return Response({"detail": "Invalid Date input. Please specify a valid 'for_date' parameter in yyyy-mm-dd format."}, status=status.HTTP_400_BAD_REQUEST)
            queryset = Queue.objects.filter(resource_id=resource_id, date=for_date)
        else:
            return Response({"detail": "Either 'encounter_id' or both 'for_date' and 'resource_id' must be provided as inputs."}, status=status.HTTP_400_BAD_REQUEST)

        # Serialize the filtered queryset
        serializer = QueueSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
