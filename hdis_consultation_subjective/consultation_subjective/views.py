from .models import *
from .serializers import *
from .oauth2helper import get_client_credentials_access_token
import json
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

class ConsultationSubjectiveViewSet(viewsets.ViewSet):

    permission_classes = [TokenHasReadWriteScope]
    
    def list(self, request):
        """ Retrieve all available Clinical Notes. Meant for troubleshooting, not Production use. """

        subjective_clinical_note = ClinicalNote.objects.all()
        serializer = ClinicalNoteSerializer(subjective_clinical_note, many=True)
        return Response(serializer.data)
    

    def create(self, request):
        """ Creates a generic Clinical Note or creates a specialized Subjective Entity and links it to a Clinical Note. """

        request_body = request.data
        print("Request Body:", request_body) #Debug

        # Generic Clinical Note creation
        if 'clinical_note' in request_body:    #Generic Clinical Note
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
            if 'family_history' in request_body:     #Dev Note: Clinical Document Type 8 as per MDDS CD05.046
                cn_serializer = ClinicalNoteSerializer(data={"encounter_id": encounter_id, "clinical_document_type": 8})
                cn_serializer.is_valid(raise_exception=True)
                new_clinical_note = cn_serializer.save()

                for count, family_history in enumerate(request_body['family_member_relationships_list']):
                    if request_body['cause_of_death_known_list'][count] == 'Yes':
                        cause_known = True
                    else:
                        cause_known = False
                    family_history = FamilyHistory(
                        clinical_note=new_clinical_note,
                        family_member_relationship=family_history,
                        family_member_health_condition=request_body['family_member_health_conditions_list'][count],
                        family_member_age_at_onset=request_body['family_member_age_at_onset_list'][count],
                        family_member_health_condition_status=request_body['family_member_health_condition_status_list'][count],
                        cause_of_death_known=cause_known,
                        family_member_age_at_death=request_body['family_member_age_at_death_list'][count]
                    )
                    family_history.save()
            
            elif 'patient_comorbidity' in request_body:    #Dev Note: Not a Clinical Document Type as per MDDS CD05.046
                cn_serializer = ClinicalNoteSerializer(data={"encounter_id": encounter_id, "clinical_document_type": 5})
                cn_serializer.is_valid(raise_exception=True)
                new_clinical_note = cn_serializer.save()

                for count, comorbidity in enumerate(request_body['comorbidity_health_condition_list']):
                    comorbidity = PatientComorbidity(
                        clinical_note=new_clinical_note,
                        comorbidity_health_condition=comorbidity,
                        comorbidity_health_condition_status=request_body['comorbidity_health_condition_status_list'][count],
                        age_at_onset_of_health_condition=request_body['age_at_onset_of_health_condition_list'][count],
                        procedure_performed=request_body['procedure_performed_list'][count],
                        patient_disposition_after_procedure=request_body['patient_disposition_after_procedure_list'][count],
                        procedure_date=request_body['procedure_date_list_list'][count])
                    comorbidity.save()
            
            elif 'chief_complaint' in request_body:    #Dev Note: Not a Clinical Document Type as per MDDS CD05.046
                cn_serializer = ClinicalNoteSerializer(data={"encounter_id": encounter_id, "clinical_document_type": 18})
                cn_serializer.is_valid(raise_exception=True)
                new_clinical_note = cn_serializer.save()

                for count, complaint in enumerate(request_body['chief_complaint_name_list']):
                    chief_complaint = ChiefComplaint(
                        clinical_note=new_clinical_note,
                        chief_complaint_name=complaint,
                        chief_complaint_body_site=request_body['chief_complaint_body_site_list'][count],
                        chief_complaint_duration=request_body['chief_complaint_duration_list'][count],
                        chief_complaint_duration_unit=request_body['chief_complaint_duration_unit_list'][count])
                    chief_complaint.save()

            elif 'social_history' in request_body:     #Dev Note: Clinical Document Type 11 as per MDDS CD05.046
                cn_serializer = ClinicalNoteSerializer(data={"encounter_id": encounter_id, "clinical_document_type": 11})
                cn_serializer.is_valid(raise_exception=True)
                new_clinical_note = cn_serializer.save()

                for count, habit in enumerate(request_body['habit_description_list']):
                    social_history = SocialHistory(
                        clinical_note=new_clinical_note,
                        habit_description=habit,
                        habit_type=request_body['habit_type_list'][count],
                        onset_since=request_body['onset_since_list'][count],
                        current_status=request_body['current_status_list'][count],
                        smoking_freqency=request_body['smoking_freqency_list'][count],
                        alcohol_intake_frequency=request_body['alcohol_intake_frequency_list'][count]
                    )
                    social_history.save()
            
            elif 'complication' in request_body:    #Dev Note: Not a Clinical Document Type as per MDDS CD05.046
                cn_serializer = ClinicalNoteSerializer(data={"encounter_id": encounter_id, "clinical_document_type": 18})
                cn_serializer.is_valid(raise_exception=True)
                new_clinical_note = cn_serializer.save()

                for count, complication in enumerate(request_body['complication_name_list']):
                    complication_details = Complication(
                        clinical_note=new_clinical_note,
                        complication_date=request_body['complication_date_list'][count],
                        complication_type=request_body['complication_type_list'][count],
                        complication_name=complication,
                        complication_description=request_body['complication_description_list'][count])
                    complication_details.save()
            
            elif 'disability' in request_body:    #Dev Note: Not a Clinical Document Type as per MDDS CD05.046
                cn_serializer = ClinicalNoteSerializer(data={"encounter_id": encounter_id, "clinical_document_type": 18})
                cn_serializer.is_valid(raise_exception=True)
                new_clinical_note = cn_serializer.save()
                
                for count, disabilities in enumerate(request_body['disability_name_list']):
                    disability_details = Disability(clinical_note=new_clinical_note,
                                                    disability_date=request_body['disability_date_list'][count],
                                                    disability_type=request_body['disability_type_list'][count],
                                                    disability_name=disabilities,
                                                    disability_description=request_body['disabilityDescription_list'][count])
                    disability_details.save()
            
            elif 'relapse' in request_body:    #Dev Note: Not a Clinical Document Type as per MDDS CD05.046
                cn_serializer = ClinicalNoteSerializer(data={"encounter_id": encounter_id, "clinical_document_type": 18})
                cn_serializer.is_valid(raise_exception=True)
                new_clinical_note = cn_serializer.save()

                for count, relapses in enumerate(request_body['relapseName_list']):
                    relapse_details = Relapse(clinical_note=new_clinical_note,
                                                    relapse_date=request_body['relapse_date_list'][count],
                                                    relapse_type=request_body['relapse_type_list'][count],
                                                    relapse_name=relapses,
                                                    relapse_description=request_body['relapse_description_list'][count])
                    relapse_details.save()
            
            elif 'remission' in request_body:    #Dev Note: Not a Clinical Document Type as per MDDS CD05.046
                cn_serializer = ClinicalNoteSerializer(data={"encounter_id": encounter_id, "clinical_document_type": 18})
                cn_serializer.is_valid(raise_exception=True)
                new_clinical_note = cn_serializer.save()

                for count, remissions in enumerate(request_body['remission_name_list']):
                    remission_details = Remission(clinical_note=new_clinical_note,
                                                remission_date=request_body['remission_date_list'][count],
                                                remission_type=request_body['remission_type_list'][count],
                                                remission_name=remissions,
                                                remission_description=request_body['remission_description_list'][count])
                    remission_details.save()
            
            elif 'allergy' in request_body:    #Dev Note: Not a Clinical Document Type as per MDDS CD05.046
                cn_serializer = ClinicalNoteSerializer(data={"encounter_id": encounter_id, "clinical_document_type": 18})
                cn_serializer.is_valid(raise_exception=True)
                new_clinical_note = cn_serializer.save()
                
                for count, allergy in enumerate(request_body['allergy_rection_description_list']):
                    allergy_details = Allergy(
                        clinical_note=new_clinical_note,
                        allergy_produce_description=request_body['allergy_produce_description_list'][count],
                        allergy_reaction_name=request_body['allergy_reaction_name_list'][count],
                        allergy_reaction_description=allergy,
                        allergy_severity_description=request_body['allergy_severity_description_list'][count],
                        allergy_status=request_body['allergy_status_list'][count],
                        allergy_event_type=request_body['allergy_event_type_list'][count],
                        allergy_history=request_body['allergy_history_list'][count])
                    allergy_details.save()
            else:
                error_body = {
                    "type": request.build_absolute_uri("/errors/bad-request-data"),
                    "title": "Invalid Subjective Clinical Note Type.",
                    "detail": "Only the following Clinical Note Types are recognized: clinical_note, family_history, patient_comorbidity, chief_complaint, social_history, complication, disability, relapse, remission, allergy."
                }
                return Response(error_body, status=status.HTTP_400_BAD_REQUEST)
            
        # TODO: Publish new Clinical Note.

        return Response(cn_serializer.data, status=status.HTTP_201_CREATED)


    def retrieve(self, request, cnid):
        """ Retrieve Clinical Note details by ID. """

        clinical_note = get_object_or_404(ClinicalNote.objects.all(), primary_key=cnid)
        serializer = ClinicalNoteSerializer(clinical_note)
        # TODO: Consider whether to also retrieve specialized Clinical Note details based on Type.
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

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
        subjective_details_for_encounter = {}
        subjective_details_for_encounter['encounter_id'] = eid
        subjective_details_for_encounter['provider_ids'] =  [ep.provider_id for ep in encounter_providers]
        subjective_details_for_encounter['patient_id'] = encounters[0]['patient_id']

        # Populate details of generic Clinical Notes
        subjective_details_for_encounter['clinical_notes'] = clinical_notes_serializer.data

        # Initialize attributes for specialized Clinical Note details.
        subjective_details_for_encounter['family_history'] = []
        subjective_details_for_encounter['patient_comorbidity'] = []
        subjective_details_for_encounter['chief_complaint'] = []
        subjective_details_for_encounter['social_history'] = []
        subjective_details_for_encounter['complication'] = []
        subjective_details_for_encounter['disability'] = []
        subjective_details_for_encounter['relapse'] = []
        subjective_details_for_encounter['remission'] = []
        subjective_details_for_encounter['allergy'] = []

        # Retrieve and append all specialized Clinical Note details based on type.
        # TODO: Shift to JSON instead of parallel arrays.
        if clinical_notes.exists():
            for note in clinical_notes:
                family_history = {}
                family_history['note_date'] = note.author_datetime.strftime("%Y-%m-%d, %H:%M:%S")
                family_history['data'] = FamilyHistorySerializer(note.family_histories.all(), many=True).data
                if family_history['data']:
                    subjective_details_for_encounter['family_history'].append(family_history)
                
                patient_comorbidity = {}
                patient_comorbidity['note_date'] = note.author_datetime.strftime("%Y-%m-%d, %H:%M:%S")
                patient_comorbidity['data'] = PatientComorbiditySerializer(note.patient_comorbidities.all(), many=True).data
                if patient_comorbidity['data']:
                    subjective_details_for_encounter['patient_comorbidity'].append(patient_comorbidity)
                
                chief_complaint = {}
                chief_complaint['note_date'] = note.author_datetime.strftime("%Y-%m-%d, %H:%M:%S")
                chief_complaint['data'] = ChiefComplaintSerializer(note.chief_complaints.all(), many=True).data
                if chief_complaint['data']:
                    subjective_details_for_encounter['chief_complaint'].append(chief_complaint)
                
                social_history = {}
                social_history['note_date'] = note.author_datetime.strftime("%Y-%m-%d, %H:%M:%S")
                social_history['data'] = SocialHistorySerializer(note.social_histories.all(), many=True).data
                if social_history['data']:
                    subjective_details_for_encounter['social_history'].append(social_history)
                
                complication = {}
                complication['note_date'] = note.author_datetime.strftime("%Y-%m-%d, %H:%M:%S")
                complication['data'] = ComplicationSerializer(note.complications.all(), many=True).data
                if complication['data']:
                    subjective_details_for_encounter['complication'].append(complication)
                
                disability = {}
                disability['note_date'] = note.author_datetime.strftime("%Y-%m-%d, %H:%M:%S")
                disability['data'] = DisabilitySerializer(note.disabilities.all(), many=True).data
                if disability['data']:
                    subjective_details_for_encounter['disability'].append(disability)
                
                relapse = {}
                relapse['note_date'] = note.author_datetime.strftime("%Y-%m-%d, %H:%M:%S")
                relapse['data'] = RelapseSerializer(note.relapses.all(), many=True).data
                if relapse['data']:
                    subjective_details_for_encounter['relapse'].append(relapse)
                
                remission = {}
                remission['note_date'] = note.author_datetime.strftime("%Y-%m-%d, %H:%M:%S")
                remission['data'] = RemissionSerializer(note.remissions.all(), many=True).data
                if remission['data']:
                    subjective_details_for_encounter['remission'].append(remission)
                
                allergy = {}
                allergy['note_date'] = note.author_datetime.strftime("%Y-%m-%d, %H:%M:%S")
                allergy['data'] = AllergySerializer(note.allergies.all(), many=True).data
                if allergy['data']:
                    subjective_details_for_encounter['allergy'].append(allergy)
        
        print("Subjective details for Encounter:", subjective_details_for_encounter) #Debug
        return Response(subjective_details_for_encounter, status.HTTP_200_OK)
