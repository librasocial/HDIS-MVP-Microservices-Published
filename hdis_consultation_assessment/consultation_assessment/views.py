from .models import *
from .serializers import *
from .oauth2helper import get_client_credentials_access_token
#from .producer import publish
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

class ConsultationAssessmentViewSet(viewsets.ViewSet):

    permission_classes = [TokenHasReadWriteScope]
    
    def list(self, request):
        """ Retrieve all available Clinical Notes. Meant for Superuser troubleshooting. Avoid usage in Production environment. """

        assessment_clinical_note = ClinicalNote.objects.all()
        serializer = ClinicalNoteSerializer(assessment_clinical_note, many=True)
        return Response(serializer.data)


    def create(self, request):
        """ Creates a generic Clinical Note or creates a specialized Objective Entity and links it to a Clinical Note. """

        request_body = request.data
        print("Request Body:", request_body) #Debug

        # Generic Clinical Note creation
        cn_created = False
        if 'clinical_note' in request.data:    #Generic Clinical Note
            # Parse and validate core Clinical Note data.
            cn_serializer = ClinicalNoteSerializer(data=request.data['clinical_note'])
            cn_serializer.is_valid(raise_exception=True)
            new_clinical_note = cn_serializer.save()
            encounter_id = cn_serializer.validated_data['encounter_id']
            cn_created = True
        else: #For specialized Clinical Notes
            try:
                encounter_id = uuid.UUID(request_body['encounter_id'])
            except:
                error_body = {
                    "type": request.build_absolute_uri("/errors/bad-request-data"),
                    "title": "Invalid Encounter ID.",
                    "detail": "A valid Encounter ID must be passed in the 'encounter_id' parameter."
                }
                return Response(error_body, status=status.HTTP_400_BAD_REQUEST)

        # Parse Provider IDs to be associated with the Encounter from the Request Body.
        try:
            provider_ids = request_body['provider_ids']
        except KeyError:
            error_body = {
                "type": request.build_absolute_uri("/errors/bad-request-data"),
                "title": "Missing Provider ID(s).",
                "detail": "At least one Provider ID associated with the Encounter must be passed in via the 'provider_ids' list parameter."
            }
            return Response(error_body, status=status.HTTP_400_BAD_REQUEST)
        
        # For each Provider ID, make an entry to associate it with the specified Encounter ID
        for pid in provider_ids:
            try:
                provider_id = uuid.UUID(pid)
            except ValueError:
                error_body = {
                    "type": request.build_absolute_uri("/errors/bad-request-data"),
                    "title": "Invalid Provider ID.",
                    "detail": f"Invalid Provider ID '{pid}' passed in as parameter."
                }
                return Response(error_body, status=status.HTTP_400_BAD_REQUEST)
            
            encounter_provider, created = EncounterProvider.objects.get_or_create(encounter_id=encounter_id, provider_id=provider_id)
        
        if not cn_created:    #If a generic Clinical Note was not created...
            if 'diagnosis' in request_body:
                cn_serializer = ClinicalNoteSerializer(data={"encounter_id": encounter_id, "clinical_document_type": 2})
                cn_serializer.is_valid(raise_exception=True)
                new_clinical_note = cn_serializer.save()
                
                for count, diagnosis_type in enumerate(request_body['health_condition_type_list']):
                    diagnosis_details = Diagnosis(
                        clinical_note=new_clinical_note,
                        health_condition_type=diagnosis_type,
                        health_condition_name=request_body['health_condition_name_list'][count],
                        health_condition_description=request_body['health_condition_description_list'][count],
                        health_condition_category=request_body['health_condition_category_list'][count],
                        health_condition_status=request_body['health_condition_status_list'][count],
                        diagnosis_priority=request_body['diagnosis_priority_list'][count],
                        present_health_condition_onset_date=request_body['present_health_condition_onset_date_list'][count]
                    )
                    diagnosis_details.save()
        
        return Response(cn_serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, cnid):
        """ Retrieve Clinical Note details by ID. """

        clinical_note = get_object_or_404(ClinicalNote.objects.all(), primary_key=cnid)
        serializer = ClinicalNoteSerializer(clinical_note)
        # TODO: Consider whether to also retrieve specialized Clinical Note details.
        return Response(serializer.data)

    
    def retrieve_for_encounter(self, request, eid):
        """
        Retrieve all Clinical Note details for a specified Encounter ID and Provider ID.
        Only the Patient concerned and the Providers associated with an Encounter should have access.
        """
        
        # Get Providers associated with Encounter; Return error if none are found
        encounter_providers = EncounterProvider.objects.filter(encounter_id=eid)
        if not encounter_providers.exists():
            error_body = {
                "type": request.build_absolute_uri("/errors/bad-request-data"),
                "title": "No Providers associated with specified Encounter ID.",
                "detail": f"Encounter ID '{eid}' is not associated with any Providers."
            }
            return Response(error_body, status=status.HTTP_400_BAD_REQUEST)
        
        # TODO: Add check to also allow a logged-in Patient to access their Encounter details after Patient Login is implemented.
        #       Patient ID for an Encounter ID can be retrieved by calling a Visit Management service endpoint.

        # Retrieve details for associated Providers from the Employee Management service.
        # Step 1 - Retrieve Access Token for Client Credentials grant type
        try:
            access_token = get_client_credentials_access_token()
        except Exception as e:
            error_body = { "details": f"Failed to get Client Credentials token due to the following error: {e}" } #TODO: Review message
            print(f"{error_body}") #TODO: Log error details
            return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Step 2 - Build URL to validate Encounter ID
        visit_mgt_url = settings.GET_ENCOUNTER_URL.format(eid)
        print("Get Encounter By ID URL:", visit_mgt_url) #Debug

        # Step 3 - Invoke URL to get Encounter Details by ID
        encounter_details_response = requests.get(
            visit_mgt_url, headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
        )
        if encounter_details_response.status_code == status.HTTP_200_OK:
            encounters = encounter_details_response.json()
            if not encounters:
                error_body = { "details": f"Failed to extract Encounter details from Visit Management service response. Response Content: {encounter_details_response.content}" } #TODO: Review message
                return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif encounter_details_response.status_code == status.HTTP_404_NOT_FOUND:
            error_body = { "details": f"Error retrieving Encounter Details from Visit Management service. Invalid Encounter ID input." }
            return Response(error_body, status.HTTP_400_BAD_REQUEST)
        else:
            error_body = { "details": f"Error retrieving Encounter Details from Visit Management service. Status Code: '{encounter_details_response.status_code}', Response Content: {encounter_details_response.content}" } #TODO: Log error details
            return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        print("Enounters:", encounters) #Debug

        # Deny access if no Auth Token supplied or if the logged-in user is not one of the Providers associated with the Encounter
        if (not request.auth) or (request.user and request.user.username not in {provider.member_username for provider in encounter_providers}):
            error_body = {
                "type": request.build_absolute_uri("/errors/forbidden"),
                "title": "Access denied.",
                "detail": "Only the concerned Patient or Provider are allowed to access Encounter details."
            }
            return Response(error_body, status=status.HTTP_403_FORBIDDEN)

        clinical_notes = ClinicalNote.objects.filter(encounter_id=eid)
        clinical_notes_serializer = ClinicalNoteSerializer(clinical_notes, many=True)

        # Populate header data for response.
        assessment_details_for_encounter = {}
        assessment_details_for_encounter['encounter_id'] = eid
        assessment_details_for_encounter['provider_ids'] =  [ep.provider_id.hex for ep in encounter_providers]
        assessment_details_for_encounter['patient_id'] = encounters[0]['patient_id']

        # Populate details of generic Clinical Notes
        assessment_details_for_encounter['clinical_notes'] = clinical_notes_serializer.data

        # Initialize attributes for specialized Clinical Note details.
        assessment_details_for_encounter['diagnosis'] = []

        # Retrieve and append all specialized Clinical Note details based on type.
        if clinical_notes.exists():
            for note in clinical_notes:
                diagnosis = {}
                diagnosis['note_date'] = note.author_datetime.strftime("%Y-%m-%d, %H:%M:%S")
                diagnosis['data'] = DiagnosisSerializer(note.diagnoses.all(), many=True).data
                if diagnosis['data']:
                    assessment_details_for_encounter['diagnosis'].append(diagnosis)
        
        print("Assessment details for Encounter:", assessment_details_for_encounter) #Debug
        return Response(assessment_details_for_encounter)
