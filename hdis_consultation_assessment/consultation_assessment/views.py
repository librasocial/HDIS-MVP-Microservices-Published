#from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
# Create your views here.
#from .producer import publish
from .serializers import *
import json
from uuid import UUID
from django.utils import timezone
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)
class ConsultationAssessmentViewSet(viewsets.ViewSet):
    def list(self, request):
        encounterConsultationAssessment = clinicalNotes.objects.all()
        serializer = clinicalNotesSerializers(encounterConsultationAssessment, many=True)
        #publish()
        return Response(serializer.data)

    def create(self, request):
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
        elif 'complications' in request.data:
            clinical_notes_creation = clinicalNotes(encounterId=encounter_details, authorDateTime=timezone.now(),
                                                    clinicalDocumentType=11)
            clinical_notes_creation.save()
            for count, complication in enumerate(values['complicationName_list']):
                complication_details = complications(clinicalNotesId=clinical_notes_creation,
                                                     complicationDate=values['complicationDate_list'][count],
                                                     complicationType=values['complicationType_list'][count],
                                                     complicationName=complication,
                                                     complicationDescription=values['complicationDescription_list'][
                                                         count])
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
        elif 'examination' in request.data:
            clinical_notes_creation = clinicalNotes(encounterId=encounter_details, authorDateTime=timezone.now(),
                                                    clinicalDocumentType=11)
            clinical_notes_creation.save()
            for count, examinations in enumerate(values['examinationSystem_list']):
                examination_details = examination(clinicalNotesId=clinical_notes_creation,
                                          examinationSystem=examinations,
                                          examinationType=values['examinationType_list'][count],
                                          bodySiteName=values['bodySiteName_list'][count],
                                          examinationFinding=values['examinationFinding_list'][count])
                examination_details.save()
        elif 'vitalSigns' in request.data:
            clinical_notes_creation = clinicalNotes(encounterId=encounter_details, authorDateTime=timezone.now(),
                                                    clinicalDocumentType=2)
            clinical_notes_creation.save()
            if 'body_height' in values:
                if values['body_height'] != '':
                    patient_height = vitalSigns(clinicalNotesId=clinical_notes_creation,
                                                vitalSignResultType='01',
                                                vitalSignResultTypeName='Body Height',
                                                vitalSignResultStatus='Complete, final results stored and verified',
                                                vitalSignResultValue=str(values['body_height']),
                                                vitalSignResultUnit='Cm')
                    patient_height.save()
            if 'body_weight' in values:
                if values['body_weight'] != '':
                    body_weight = vitalSigns(clinicalNotesId=clinical_notes_creation,
                                             vitalSignResultType='01',
                                             vitalSignResultTypeName='Body Weight',
                                             vitalSignResultStatus='Complete, final results stored and verified',
                                             vitalSignResultValue=str(values['body_weight']),
                                             vitalSignResultUnit='Kg')
                    body_weight.save()
            if 'systolic' in values:
                if values['systolic'] != '':
                    systolic = vitalSigns(clinicalNotesId=clinical_notes_creation,
                                          vitalSignResultType='01',
                                          vitalSignResultTypeName='Systolic Blood Pressure',
                                          vitalSignResultStatus='Complete, final results stored and verified',
                                          vitalSignResultValue=str(values['systolic']),
                                          vitalSignResultUnit='Mmhg')
                    systolic.save()
            if 'diastolic' in values:
                if values['diastolic'] != '':
                    diastolic = vitalSigns(clinicalNotesId=clinical_notes_creation,
                                           vitalSignResultType='01',
                                           vitalSignResultTypeName='Diastolic Blood Pressure',
                                           vitalSignResultStatus='Complete, final results stored and verified',
                                           vitalSignResultValue=str(values['diastolic']),
                                           vitalSignResultUnit='Mmhg')
                    diastolic.save()
            if 'body_temperature' in values:
                if values['body_temperature'] != '':
                    body_temperature = vitalSigns(clinicalNotesId=clinical_notes_creation,
                                                  vitalSignResultType='01',
                                                  vitalSignResultTypeName='Temperature',
                                                  vitalSignResultStatus='Complete, final results stored and verified',
                                                  vitalSignResultValue=str(values['diastolic']),
                                                  vitalSignResultUnit='0F')
                    body_temperature.save()
            if 'heart_rate' in values:
                if values['heart_rate'] != '':
                    heart_rate = vitalSigns(clinicalNotesId=clinical_notes_creation,
                                            vitalSignResultType='01',
                                            vitalSignResultTypeName='Heart Rate',
                                            vitalSignResultStatus='Complete, final results stored and verified',
                                            vitalSignResultValue=str(values['diastolic']),
                                            vitalSignResultUnit='/min')
                    heart_rate.save()
            if 'oxygen_saturation' in values:
                if values['oxygen_saturation'] != '':
                    oxygen_saturation = vitalSigns(clinicalNotesId=clinical_notes_creation,
                                                   vitalSignResultType='01',
                                                   vitalSignResultTypeName='Oxygen Saturation',
                                                   vitalSignResultStatus='Complete, final results stored and verified',
                                                   vitalSignResultValue=str(values['diastolic']),
                                                   vitalSignResultUnit='%')
                    oxygen_saturation.save()
        elif 'diagnosis' in request.data:
            clinical_notes_creation = clinicalNotes(encounterId=encounter_details, authorDateTime=timezone.now(),
                                                    clinicalDocumentType=18)
            clinical_notes_creation.save()
            for count, diagnosis_type in enumerate(values['healthConditionType_list']):
                diagnosis_details = diagnosis(clinicalNotesId=clinical_notes_creation,
                                              healthConditionType=diagnosis_type,
                                              healthConditionName=values['healthConditionName_list'][count],
                                              healthConditionDescription=values['healthConditionDescription_list'][count],
                                              healthConditionCategory=values['healthConditionCategory_list'][count],
                                              healthConditionStatus=values['healthConditionStatus_list'][count],
                                              diagnosisPriority=values['diagnosisPriority_list'][count],
                                              presentHealthConditionOnsetDate=values['presentHealthConditionOnsetDate_list'][count])
                diagnosis_details.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pId):
        try:
            patient_details = Patient.objects.get(patientId=int(pId))
            serializer = ConsultationAssessmentSerializers(patient_details)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            patient_details = Patient.objects.all()[0]
            serializer = ConsultationAssessmentSerializers(patient_details)
            return Response(serializer.data)


    def update(self, request):
        pass
    def destroy(self, request):
        pass
    def update(self, request):
        pass
    def destroy(self, request):
        pass
    def update_encounter(self, request):
        pass
    def destroy_encounter(self, request):
        pass
    def retrieve_encounter(self, request, eId, prId):
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
            encounter_dict['complications_assessment'] = []
            encounter_dict['disability_assessment'] = []
            encounter_dict['relapse_assessment'] = []
            encounter_dict['remission_assessment'] = []
            encounter_dict['allergy_assessment'] = []
            encounter_dict['examination_assessment'] = []
            encounter_dict['vitalSigns_assessment'] = []
            encounter_dict['diagnosis'] = []
            for notes in clinical_notes:
                complications = {}
                complications['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                complications['data'] = complicationsSerializers(notes.complications_set.all(), many=True).data
                if complications['data']:
                    encounter_dict['complications_assessment'].append(complications)
                disability = {}
                disability['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                disability['data'] = disabilitySerializers(notes.disability_set.all(), many=True).data
                if disability['data']:
                    encounter_dict['disability_assessment'].append(disability)
                relapse = {}
                relapse['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                relapse['data'] = relapseSerializers(notes.relapse_set.all(), many=True).data
                if relapse['data']:
                    encounter_dict['relapse_assessment'].append(relapse)
                remission = {}
                remission['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                remission['data'] = remissionSerializers(notes.remission_set.all(), many=True).data
                if remission['data']:
                    encounter_dict['remission_assessment'].append(remission)
                allergy = {}
                allergy['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                allergy['data'] = allergySerializers(notes.allergy_set.all(), many=True).data
                if allergy['data']:
                    encounter_dict['allergy_assessment'].append(allergy)
                examination = {}
                examination['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                examination['data'] = examinationSerializers(notes.examination_set.all(), many=True).data
                if examination['data']:
                    encounter_dict['examination_assessment'].append(examination)
                vitalSigns = {}
                vitalSigns['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                vitalSigns['data'] = vitalSignsSerializers(notes.vitalsigns_set.all(), many=True).data
                if vitalSigns['data']:
                    encounter_dict['vitalSigns_assessment'].append(vitalSigns)
                diagnosis = {}
                diagnosis['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                diagnosis['data'] = diagnosisSerializers(notes.diagnosis_set.all(), many=True).data
                if diagnosis['data']:
                    encounter_dict['diagnosis'].append(diagnosis)
        else:
            encounter_dict['complications_assessment'] = {}
            encounter_dict['disability_assessment'] = {}
            encounter_dict['relapse_assessment'] = {}
            encounter_dict['remission_assessment'] = {}
            encounter_dict['allergy_assessment'] = {}
            encounter_dict['examination_assessment'] = {}
            encounter_dict['vitalSigns_assessment'] = {}
            encounter_dict['diagnosis'] = {}
        print(encounter_dict)
        return Response(json.dumps(encounter_dict, cls=UUIDEncoder))