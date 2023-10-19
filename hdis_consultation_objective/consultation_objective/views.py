#from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime
from .models import *
import json
# Create your views here.
#from .producer import publish
from .serializers import *
from uuid import UUID
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)
class ConsultationObjectivetViewSet(viewsets.ViewSet):
    def list(self, request):
        encounterConsultationObjective = clinicalNotes.objects.all()
        serializer = clinicalNotesSerializers(encounterConsultationObjective, many=True)
        #publish()
        return Response(serializer.data)

    def create(self, request):
        values = json.loads(request.body.decode('utf-8'))
        print(values)
        encounter_details = Encounter.objects.get(PrimaryKey = values['eId'])
        if 'clinicalNotes' in request.data:
            try:
                clinicalNotes.objects.get(clinicalNotesID=request.data['clinicalNotes']['clinicalNotesID'])
            except clinicalNotes.DoesNotExist:
                serializer = clinicalNotesSerializers(data=request.data['clinicalNotes'])
                serializer.is_valid(raise_exception=True)
                serializer.save()
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
        elif 'vitalSigns' in values:
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
            return Response(status=status.HTTP_201_CREATED)
        elif 'lab' in request.data:
            try:
                request.data['lab']['clinicalNotes'] = clinicalNotes.objects.get(
                    clinicalNotesID=request.data['clinicalNotes']['clinicalNotesID'])
                serializer = labSerializers(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except clinicalNotes.DoesNotExist:
                return Response("lab not added", status=status.HTTP_300_MULTIPLE_CHOICES)
        elif 'radiology' in request.data:
            try:
                request.data['radiology']['clinicalNotes'] = clinicalNotes.objects.get(
                    clinicalNotesID=request.data['clinicalNotes']['clinicalNotesID'])
                serializer = radiologySerializers(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except clinicalNotes.DoesNotExist:
                return Response("radiology not added", status=status.HTTP_300_MULTIPLE_CHOICES)
        return Response(status=status.HTTP_201_CREATED)
    def retrieve(self, request, pId):
        try:
            patient_details = Patient.objects.get(patientId=int(pId))
            serializer = ConsultationObjectiveSerializers(patient_details)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            patient_details = Patient.objects.all()[0]
            serializer = ConsultationObjectiveSerializers(patient_details)
            return Response(serializer.data)


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
            encounter_dict['examination'] = []
            encounter_dict['vitalSigns'] = []
            encounter_dict['lab'] = []
            encounter_dict['radiology'] = []
            for notes in clinical_notes:
                examination = {}
                examination['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                examination['data'] = examinationSerializers(notes.examination_set.all(), many=True).data
                if examination['data']:
                    encounter_dict['examination'].append(examination)
                vitalSigns = {}
                vitalSigns['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                vitalSigns['data'] = vitalSignsSerializers(notes.vitalsigns_set.all(), many=True).data
                if vitalSigns['data']:
                    encounter_dict['vitalSigns'].append(vitalSigns)
                lab = {}
                lab['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                lab['data'] = labSerializers(notes.lab_set.all(), many=True).data
                if lab['data']:
                    encounter_dict['lab'].append(lab)
                radiology = {}
                radiology['note_date'] = notes.authorDateTime.strftime("%Y-%m-%d, %H:%M:%S")
                radiology['data'] = radiologySerializers(notes.radiology_set.all(), many=True).data
                if radiology['data']:
                    encounter_dict['radiology'].append(radiology)
        else:
            encounter_dict['examination'] = []
            encounter_dict['vitalSigns'] = []
            encounter_dict['lab'] = []
            encounter_dict['radiology'] = []
        print(encounter_dict)
        return Response(json.dumps(encounter_dict, cls=UUIDEncoder))