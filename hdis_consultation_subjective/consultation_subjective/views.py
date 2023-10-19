#from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
from datetime import datetime
# Create your views here.
from django.utils import timezone
#from .producer import publish
from .serializers import *
import json
from uuid import UUID
from .decorators import jwt_token_required
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)
class ConsultationSubjectivetViewSet(viewsets.ViewSet):
    @jwt_token_required
    def list(self, request):
        encounterConsultationSubjective = clinicalNotes.objects.all()
        serializer = clinicalNotesSerializers(encounterConsultationSubjective, many=True)
        #publish()
        return Response(serializer.data)

    @jwt_token_required
    def create(self,request, data, token, status):
        values = json.loads(request.body.decode('utf-8'))
        print(values)
        encounter_details = Encounter.objects.get(PrimaryKey=values['eId'])
        if 'clinicalNotes' in request.data:
            try:
                clinicalNotes.objects.get(clinicalNotesID=request.data['clinicalNotes']['clinicalNotesID'])
            except clinicalNotes.DoesNotExist:
                serializer = clinicalNotesSerializers(data=request.data['clinicalNotes'])
                serializer.is_valid(raise_exception=True)
                serializer.save()
        elif 'familyHistory' in request.data:
            clinical_notes_creation = clinicalNotes(encounterId=encounter_details, authorDateTime=timezone.now(),
                                                    clinicalDocumentType=8)
            clinical_notes_creation.save()
            for count, family_history in enumerate(values['familyMemberRelationship_list']):
                if values['causeOfDeathKnown_list'][count] == 'Yes':
                    cause_known = 1
                else:
                    cause_known = 1
                family_history_save = familyHistory(clinicalNotesId=clinical_notes_creation,
                                                 familyMemberRelationship=family_history,
                                                 familyMemeberHealthCondition=values['familyMemeberHealthCondition_list'][count],
                                                 familyMemeberAgeAtOnset=values['familyMemeberAgeAtOnset_list'][count],
                                                 familyMemberHealthConditionStatus=values['familyMemberHealthConditionStatus_list'][count],
                                                 causeOfDeathKnown=cause_known,
                                                 familyMemeberAgeAtDeath=values['familyMemeberAgeAtDeath_list'][count])
                family_history_save.save()
        elif 'patientComorbidities' in request.data:
            clinical_notes_creation = clinicalNotes(encounterId=encounter_details, authorDateTime=timezone.now(),
                                                    clinicalDocumentType=5)
            clinical_notes_creation.save()
            for count, Comorbidities in enumerate(values['comorbidityHealthCondition_list']):
                Comorbidities = patientComorbidities(clinicalNotesId=clinical_notes_creation,
                                                    comorbidityHealthCondition=Comorbidities,
                                                    comorbidityHealthConditionStatus=
                                                    values['comorbidityHealthConditionStatus_list'][count],
                                                    ageAtOnsetOfHealthCondition=values['ageAtOnsetOfHealthCondition_list'][
                                                        count],
                                                    procedurePerformed=
                                                    values['procedurePerformed_list'][count],
                                                    patientDispositionAfterProcedure=values['patientDispositionAfterProcedure_list'][count],
                                                    procedureDate=values['procedureDate_list'][count])
                Comorbidities.save()
        elif 'chiefComplaints' in request.data:
            clinical_notes_creation = clinicalNotes(encounterId=encounter_details, authorDateTime=timezone.now(),
                                                    clinicalDocumentType=18)
            clinical_notes_creation.save()
            for count, compliants in enumerate(values['chiefComplaintName_list']):
                chief_complaints = chiefComplaints(clinicalNotesId=clinical_notes_creation,
                                                   chiefComplaintName=compliants,
                                                   chiefComplaintBodySite=values['chiefComplaintBodySite_list'][count],
                                                   chiefComplaintDuration=values['chiefComplaintDuration_list'][count],
                                                   chiefComplaintDurationUnit=values['chiefComplaintDurationUnit_list'][count])
                chief_complaints.save()

        elif 'socialHistory' in request.data:
            clinical_notes_creation = clinicalNotes(encounterId=encounter_details, authorDateTime=timezone.now(),
                                                    clinicalDocumentType=11)
            clinical_notes_creation.save()
            for count, habit in enumerate(values['habitDescription_list']):
                social_history = socialHistory(clinicalNotesId=clinical_notes_creation,
                                                     habitDescription=habit,
                                                     habitType=values['habitType_list'][count],
                                                     onsetSince=values['onsetSince_list'][count],
                                                     currentStatus=values['currentStatus_list'][count],
                                                     smokingFreqency=values['smokingFreqency_list'][count],
                                                     alcoholIntakeFrequency=values['alcoholIntakeFrequency_list'][count])
                social_history.save()
        elif 'complications' in request.data:
            clinical_notes_creation = clinicalNotes(encounterId=encounter_details, authorDateTime=timezone.now(),
                                                    clinicalDocumentType=11)
            clinical_notes_creation.save()
            for count, complication in enumerate(values['complicationName_list']):
                complication_details = complications(clinicalNotesId=clinical_notes_creation,
                                               complicationDate=values['complicationDate_list'][count],
                                               complicationType=values['complicationType_list'][count],
                                               complicationName=complication,
                                               complicationDescription=values['complicationDescription_list'][count])
                complication_details.save()
        elif 'disability' in request.data:
            clinical_notes_creation = clinicalNotes(encounterId=encounter_details, authorDateTime=timezone.now(),
                                                    clinicalDocumentType=11)
            clinical_notes_creation.save()
            for count, disabilities in enumerate(values['disabilityName_list']):
                disability_details = disability(clinicalNotesId=clinical_notes_creation,
                                                     disabilityDate=values['disabilityDate_list'][count],
                                                     disabilityType=values['disabilityType_list'][count],
                                                     disabilityName=disabilities,
                                                     disabilityDescription=values['disabilityDescription_list'][
                                                         count])
                disability_details.save()
        elif 'relapse' in request.data:
            clinical_notes_creation = clinicalNotes(encounterId=encounter_details, authorDateTime=timezone.now(),
                                                    clinicalDocumentType=11)
            clinical_notes_creation.save()
            for count, relapses in enumerate(values['relapseName_list']):
                relapse_details = relapse(clinicalNotesId=clinical_notes_creation,
                                                relapseDate=values['relapseDate_list'][count],
                                                relapseType=values['relapseType_list'][count],
                                                relapseName=relapses,
                                                relapseDescription=values['relapseDescription_list'][
                                                    count])
                relapse_details.save()
        elif 'remission' in request.data:
            clinical_notes_creation = clinicalNotes(encounterId=encounter_details, authorDateTime=timezone.now(),
                                                    clinicalDocumentType=11)
            clinical_notes_creation.save()
            for count, remissions in enumerate(values['remissionName_list']):
                remission_details = remission(clinicalNotesId=clinical_notes_creation,
                                                remissionDate=values['remissionDate_list'][count],
                                                remissionType=values['remissionType_list'][count],
                                                remissionName=remissions,
                                                remissionDescription=values['remissionDescription_list'][
                                                    count])
                remission_details.save()
        elif 'allergy' in request.data:
            clinical_notes_creation = clinicalNotes(encounterId=encounter_details, authorDateTime=timezone.now(),
                                                    clinicalDocumentType=11)
            clinical_notes_creation.save()
            for count, allergies in enumerate(values['allergyRectionDescription_list']):
                allergy_details = allergy(clinicalNotesId=clinical_notes_creation,
                                              allergyProduceDescription=values['allergyProduceDescription_list'][count],
                                              allergyReactionName=values['allergyReactionName_list'][count],
                                              allergyRectionDescription=allergies,
                                              allergySeverityDescription=values['allergySeverityDescription_list'][count],
                                          allergyStatus=values['allergyStatus_list'][count],
                                          allergyEventType=values['allergyEventType_list'][count],
                                          allergyHistory=values['allergyHistory_list'][count])
                allergy_details.save()
        return Response(status)

    @jwt_token_required
    def retrieve(self, request, fId, prId, date, data, status, token):
        date_value = datetime.strptime(date, "%Y-%m-%d").date()
        provider_details = Provider.objects.get(uniqueIndividualHealthCareProviderNumber=prId)
        facility_details = Facility.objects.get(uniqueFacilityIdentificationNumber=fId)
        episode_details = Episode.objects.filter(facilityId=facility_details, providerId=provider_details)
        print(episode_details)
        list_of_encounters = []
        if episode_details.count() > 0:
            for episodes in episode_details:
                encounter_details = Encounter.objects.filter(episodeId=episodes,
                                                             encounterStatusCode='planned')
                if encounter_details.count()>0:
                    for encounters in encounter_details:
                        encounter_dict = {}
                        encounter_dict['episode'] = EpisodeSerializers(episodes).data
                        encounter_dict['encounter'] = EncounterSerializers(encounters).data
                        encounter_dict['provider'] = ProviderSerializers(provider_details).data
                        encounter_dict['facility'] = FacilitySerializers(facility_details).data
                        encounter_dict['patient'] = PatientSerializers(episodes.patientId).data
                        list_of_encounters.append(encounter_dict)
            return Response(json.dumps(list_of_encounters, cls=UUIDEncoder))
        else:
            list_of_encounters = []
            #patient_details = Patient.objects.all()[0]
            #serializer = ConsultationSubjectiveSerializers(patient_details)
            return Response(json.dumps(list_of_encounters, cls=UUIDEncoder))

    @jwt_token_required
    def update(self, request):
        pass

    @jwt_token_required
    def destroy(self, request):
        pass

    @jwt_token_required
    def update_encounter(self, request):
        pass

    @jwt_token_required
    def destroy_encounter(self, request):
        pass

    @jwt_token_required
    def retrieve_encounter(self, request, data,token,status, eId, prId):
        encounter_details = Encounter.objects.get(PrimaryKey=eId)
        provider_details = Provider.objects.get(PrimaryKey=prId)
        clinical_notes = clinicalNotes.objects.filter(encounterId=encounter_details)
        encounter_dict = {}
        encounter_dict['episode'] = EpisodeSerializers(encounter_details.episodeId).data
        encounter_dict['encounter'] = EncounterSerializers(encounter_details).data
        encounter_dict['provider'] = ProviderSerializers(provider_details).data
        encounter_dict['facility'] = FacilitySerializers(encounter_details.episodeId.facilityId).data
        encounter_dict['patient'] = PatientSerializers(encounter_details.episodeId.patientId).data
        #encounter_dict['clinicalNotes'] = clinicalNotesSerializers(clinical_notes, many=True).data
        if clinical_notes.count() > 0:
            encounter_dict['familyHistory'] = []
            encounter_dict['patientComorbidities'] = []
            encounter_dict['chiefComplaints'] = []
            encounter_dict['socialHistory'] = []
            encounter_dict['complications'] = []
            encounter_dict['disability'] = []
            encounter_dict['relapse'] = []
            encounter_dict['remission'] = []
            encounter_dict['allergy'] = []
            for notes in clinical_notes:
                familyHistory = {}
                familyHistory['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                familyHistory['data'] = familyHistorySerializers(notes.familyhistory_set.all(), many=True).data
                if familyHistory['data']:
                    encounter_dict['familyHistory'].append(familyHistory)
                patientComorbidities = {}
                patientComorbidities['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                patientComorbidities['data'] = patientComorbiditiesSerializers(notes.patientcomorbidities_set.all(), many=True).data
                if patientComorbidities['data']:
                    encounter_dict['patientComorbidities'].append(patientComorbidities)
                chiefComplaints = {}
                chiefComplaints['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                chiefComplaints['data'] = chiefComplaintsSerializers(notes.chiefcomplaints_set.all(), many=True).data
                if chiefComplaints['data']:
                    encounter_dict['chiefComplaints'].append(chiefComplaints)
                socialHistory = {}
                socialHistory['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                socialHistory['data'] = socialHistorySerializers(notes.socialhistory_set.all(), many=True).data
                if socialHistory['data']:
                    encounter_dict['socialHistory'].append(socialHistory)
                complications = {}
                complications['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                complications['data'] = complicationsSerializers(notes.complications_set.all(), many=True).data
                if complications['data']:
                    encounter_dict['complications'].append(complications)
                disability = {}
                disability['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                disability['data'] = disabilitySerializers(notes.disability_set.all(), many=True).data
                if disability['data']:
                    encounter_dict['disability'].append(disability)
                relapse = {}
                relapse['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                relapse['data'] = relapseSerializers(notes.relapse_set.all(), many=True).data
                if relapse['data']:
                    encounter_dict['relapse'].append(relapse)
                remission = {}
                remission['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                remission['data'] = remissionSerializers(notes.remission_set.all(), many=True).data
                if remission['data']:
                    encounter_dict['remission'].append(remission)
                allergy = {}
                allergy['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                allergy['data'] = allergySerializers(notes.allergy_set.all(), many=True).data
                if allergy['data']:
                    encounter_dict['allergy'].append(allergy)
        else:
            encounter_dict['familyHistory'] = []
            encounter_dict['patientComorbidities'] = []
            encounter_dict['chiefComplaints'] = []
            encounter_dict['socialHistory'] = []
            encounter_dict['complications'] = []
            encounter_dict['disability'] = []
            encounter_dict['relapse'] = []
            encounter_dict['remission'] = []
            encounter_dict['allergy'] = []
        print(encounter_dict)
        return Response(json.dumps(encounter_dict, cls=UUIDEncoder))
