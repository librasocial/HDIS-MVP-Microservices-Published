from .models import *
from .serializers import *
from .oauth2helper import get_client_credentials_access_token
#from .producer import publish
import json
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

class ConsultationObjectiveViewSet(viewsets.ViewSet):

    permission_classes = [TokenHasReadWriteScope]
    
    def list(self, request):
        """ Retrieve all available Clinical Notes. Meant for Superuser troubleshooting. Avoid usage in Production environment. """

        objective_clinical_note = ClinicalNote.objects.all()
        serializer = ClinicalNoteSerializer(objective_clinical_note, many=True)
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
            # Creation of Specialized Clinical Notes, each with specific attributes.
            if 'examination' in request_body:     #Dev Note: Mapped to Clinical Document Type 18 (Clinical note) - ref: MDDS CD05.046
                cn_serializer = ClinicalNoteSerializer(data={"encounter_id": encounter_id, "clinical_document_type": 18})
                cn_serializer.is_valid(raise_exception=True)
                new_clinical_note = cn_serializer.save()

                for count, examined_system in enumerate(request_body['examined_system_list']):
                    examination_details = Examination(clinical_note=new_clinical_note,
                                                    examined_system=examined_system,
                                                    examination_type=request_body['examination_type_list'][count],
                                                    body_site_name=request_body['body_site_name_list'][count],
                                                    examination_finding=request_body['examination_finding_list'][count])
                    examination_details.save()
            elif 'vital_sign' in request_body:     #Dev Note: Mapped to Clinical Document Type 2 (Admission Note) - ref: MDDS CD05.046
                cn_serializer = ClinicalNoteSerializer(data={"encounter_id": encounter_id, "clinical_document_type": 2})
                cn_serializer.is_valid(raise_exception=True)
                new_clinical_note = cn_serializer.save()
                
                if 'body_height' in request_body:
                    if request_body['body_height'] != '':
                        patient_height = VitalSign(
                            clinical_note=new_clinical_note,
                            result_type='01',
                            result_type_name='Body Height',
                            result_status='Complete, final results stored and verified',
                            result_value=str(request_body['body_height']),
                            result_unit='Cm'
                        )
                        patient_height.save()
                if 'body_weight' in request_body:
                    if request_body['body_weight'] != '':
                        body_weight = VitalSign(
                            clinical_note_id=new_clinical_note,
                            result_type='01',
                            result_type_name='Body Weight',
                            result_status='Complete, final results stored and verified',
                            result_value=str(request_body['body_weight']),
                            result_unit='Kg'
                        )
                        body_weight.save()
                if 'systolic' in request_body:
                    if request_body['systolic'] != '':
                        systolic = VitalSign(
                            clinical_note=new_clinical_note,
                            result_type='01',
                            result_type_name='Systolic Blood Pressure',
                            result_status='Complete, final results stored and verified',
                            result_value=str(request_body['systolic']),
                            result_unit='Mmhg'
                        )
                        systolic.save()
                if 'diastolic' in request_body:
                    if request_body['diastolic'] != '':
                        diastolic = VitalSign(
                            clinical_note=new_clinical_note,
                            result_type='01',
                            result_type_name='Diastolic Blood Pressure',
                            result_status='Complete, final results stored and verified',
                            result_value=str(request_body['diastolic']),
                            result_unit='Mmhg'
                        )
                        diastolic.save()
                if 'body_temperature' in request_body:
                    if request_body['body_temperature'] != '':
                        body_temperature = VitalSign(
                            clinical_note=new_clinical_note,
                            result_type='01',
                            result_type_name='Temperature',
                            result_status='Complete, final results stored and verified',
                            result_value=str(request_body['body_temperature']),
                            result_unit='0F'
                        )
                        body_temperature.save()
                if 'heart_rate' in request_body:
                    if request_body['heart_rate'] != '':
                        heart_rate = VitalSign(
                            clinical_note=new_clinical_note,
                            result_type='01',
                            result_type_name='Heart Rate',
                            result_status='Complete, final results stored and verified',
                            result_value=str(request_body['heart_rate']),
                            result_unit='/min'
                        )
                        heart_rate.save()
                if 'oxygen_saturation' in request_body:
                    if request_body['oxygen_saturation'] != '':
                        oxygen_saturation = VitalSign(
                            clinical_note=new_clinical_note,
                            result_type='01',
                            result_type_name='Oxygen Saturation',
                            result_status='Complete, final results stored and verified',
                            result_value=str(request_body['oxygen_saturation']),
                            result_unit='%'
                        )
                        oxygen_saturation.save()
            
            elif 'lab_result' in request_body:
                try:
                    request.data['lab_result']['clinical_note'] = ClinicalNote.objects.get(
                        clinical_note_id=request.data['clinical_note']['clinical_note_id'])
                    serializer = LabResultSerializer(data=request_body)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                except ClinicalNote.DoesNotExist:
                    return Response("Lab Result not added", status=status.HTTP_300_MULTIPLE_CHOICES)
            elif 'radiology_result' in request_body:
                try:
                    request.data['radiology']['clinical_note'] = ClinicalNote.objects.get(
                        clinical_note_id=request.data['clinical_note']['clinical_note_id'])
                    serializer = RadiologyResultSerializers(data=request_body)
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                except ClinicalNote.DoesNotExist:
                    return Response("Radiology Result not added", status=status.HTTP_300_MULTIPLE_CHOICES)
            else:
                error_body = {
                    "type": request.build_absolute_uri("/errors/bad-request-data"),
                    "title": "Invalid Objective Clinical Note Type.",
                    "detail": "Only the following Clinical Note Types are recognized: clinical_note, examination, vital_sign, lab_result, radiology_result."
                }
                return Response(error_body, status=status.HTTP_400_BAD_REQUEST)
            
        # TODO: Publish new Clinical Note.
        
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
        objective_details_for_encounter = {}
        objective_details_for_encounter['encounter_id'] = eid
        objective_details_for_encounter['provider_ids'] =  [ep.provider_id.hex for ep in encounter_providers]
        objective_details_for_encounter['patient_id'] = encounters[0]['patient_id']

        # Populate details of generic Clinical Notes
        objective_details_for_encounter['clinical_notes'] = clinical_notes_serializer.data

        # Initialize attributes for specialized Clinical Note details.
        objective_details_for_encounter['examination'] = []
        objective_details_for_encounter['vital_sign'] = []
        objective_details_for_encounter['lab_results'] = []
        objective_details_for_encounter['radiology_results'] = []

        # Retrieve and append all specialized Clinical Note details based on type.
        # TODO: Shift to JSON instead of parallel arrays.
        if clinical_notes.exists():
            for note in clinical_notes:
                examination = {}
                examination['note_date'] = note.author_datetime.strftime("%Y-%m-%d, %H:%M:%S")
                examination['data'] = ExaminationSerializer(note.examinations.all(), many=True).data
                if examination['data']:
                    objective_details_for_encounter['examination'].append(examination)
                vital_sign = {}
                vital_sign['note_date'] = note.author_datetime.strftime("%Y-%m-%d, %H:%M:%S")
                vital_sign['data'] = VitalSignSerializer(note.vital_signs.all(), many=True).data
                if vital_sign['data']:
                    objective_details_for_encounter['vital_sign'].append(vital_sign)
                lab_result = {}
                lab_result['note_date'] = note.author_datetime.strftime("%Y-%m-%d, %H:%M:%S")
                lab_result['data'] = LabResultSerializer(note.lab_results.all(), many=True).data
                if lab_result['data']:
                    objective_details_for_encounter['lab_results'].append(lab_result)
                radiology_result = {}
                radiology_result['note_date'] = note.author_datetime.strftime("%Y-%m-%d, %H:%M:%S")
                radiology_result['data'] = RadiologyResultSerializers(note.radiology_results.all(), many=True).data
                if radiology_result['data']:
                    objective_details_for_encounter['radiology_results'].append(radiology_result)

        print("Objective details for Encounter:", objective_details_for_encounter) #Debug
        return Response(objective_details_for_encounter)
    