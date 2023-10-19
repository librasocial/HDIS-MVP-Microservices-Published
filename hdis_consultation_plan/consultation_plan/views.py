#from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import *
import json
# Create your views here.
#from .producer import publish
from .serializers import *
from django.utils import timezone
from uuid import UUID
class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return str(obj)
        return json.JSONEncoder.default(self, obj)
class ConsultationPlanViewSet(viewsets.ViewSet):
    def list(self, request):
        encounterconsultationPlan = clinicalNotes.objects.all()
        serializer = clinicalNotesSerializers(encounterconsultationPlan, many=True)
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
        elif 'clinicalOrders' in request.data:
            try:
                request.data['clinicalOrders']['clinicalNotes'] = clinicalNotes.objects.get(
                    clinicalNotesID=request.data['clinicalNotes']['clinicalNotesID'])
                serializer = clinicalOrdersSerializers(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
            except clinicalNotes.DoesNotExist:
                return Response("clinicalOrders not added", status=status.HTTP_300_MULTIPLE_CHOICES)
        elif 'lab' in request.data:
            clinical_notes_creation = clinicalNotes(encounterId=encounter_details, authorDateTime=timezone.now(),
                                                    clinicalDocumentType=18)
            clinical_notes_creation.save()
            clinical_order_creation = clinicalNotes(clinicalNotesId=clinical_notes_creation)
            clinical_order_creation.save()
            for count, tests in enumerate(values['test_name_list']):
                lab_details = lab(clinicalOrderId=clinical_order_creation,
                                              labOrderName=tests)
                lab_details.save()
        elif 'radiology' in request.data:
            clinical_notes_creation = clinicalNotes(encounterId=encounter_details, authorDateTime=timezone.now(),
                                                    clinicalDocumentType=18)
            clinical_notes_creation.save()
            clinical_order_creation = clinicalNotes(clinicalNotesId=clinical_notes_creation)
            clinical_order_creation.save()
            for count, tests in enumerate(values['test_name_list']):
                lab_details = lab(clinicalOrderId=clinical_order_creation,
                                  labOrderName=tests)
                lab_details.save()
        elif 'pharmacy' in request.data:
            clinical_notes_creation = clinicalNotes(encounterId=encounter_details, authorDateTime=timezone.now(),
                                                    clinicalDocumentType=18)
            clinical_notes_creation.save()
            clinical_order_creation = clinicalNotes(clinicalNotesId=clinical_notes_creation)
            clinical_order_creation.save()
            for count, tests in enumerate(values['test_name_list']):
                lab_details = lab(clinicalOrderId=clinical_order_creation,
                                  labOrderName=tests)
                lab_details.save()
        elif 'immunizationOrder' in request.data:
            clinical_notes_creation = clinicalNotes(encounterId=encounter_details, authorDateTime=timezone.now(),
                                                    clinicalDocumentType=18)
            clinical_notes_creation.save()
            clinical_order_creation = clinicalNotes(clinicalNotesId=clinical_notes_creation)
            clinical_order_creation.save()
            for count, tests in enumerate(values['test_name_list']):
                lab_details = lab(clinicalOrderId=clinical_order_creation,
                                  labOrderName=tests)
                lab_details.save()
        elif 'procedure' in request.data:
            clinical_notes_creation = clinicalNotes(encounterId=encounter_details, authorDateTime=timezone.now(),
                                                    clinicalDocumentType=18)
            clinical_notes_creation.save()
            clinical_order_creation = clinicalNotes(clinicalNotesId=clinical_notes_creation)
            clinical_order_creation.save()
            for count, tests in enumerate(values['test_name_list']):
                lab_details = lab(clinicalOrderId=clinical_order_creation,
                                  labOrderName=tests)
                lab_details.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pId):
        try:
            patient_details = Patient.objects.get(patientId=int(pId))
            serializer = ConsultationSubjectiveSerializers(patient_details)
            return Response(serializer.data)
        except Patient.DoesNotExist:
            patient_details = Patient.objects.all()[0]
            serializer = ConsultationSubjectiveSerializers(patient_details)
            return Response(serializer.data)
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
            encounter_dict['clinicalOrders'] = clinicalOrdersSerializers(clinical_notes.clinicalOrders_set.all(),
                                                                   many=True).data
            if clinical_notes.clinicalOrders_set.all().count() > 0:
                for clinical_orders in clinical_notes.clinicalOrders_set.all():
                    encounter_dict['lab_plan'] = labSerializers(clinical_orders.lab_set.all(),
                                                                               many=True).data
                    encounter_dict['radiology_plan'] = radiologySerializers(clinical_orders.radiology_set.all(),
                                                                               many=True).data
                    encounter_dict['pharmacy'] = pharmacySerializers(clinical_orders.pharmacy_set.all(),
                                                                               many=True).data
                    encounter_dict['immunizationOrder'] = immunizationOrderSerializers(clinical_orders.immunizationOrder_set.all(),
                                                                               many=True).data
                    encounter_dict['procedure'] = procedureSerializers(clinical_orders.procedure_set.all(),
                                                                               many=True).data
            else:
                encounter_dict['lab_plan'] = {}
                encounter_dict['radiology_plan'] = {}
                encounter_dict['pharmacy'] = {}
                encounter_dict['immunizationOrder'] = {}
                encounter_dict['procedure'] = {}
        else:
            encounter_dict['clinicalOrders'] = {}
            encounter_dict['lab_plan'] = {}
            encounter_dict['radiology_plan'] = {}
            encounter_dict['pharmacy'] = {}
            encounter_dict['immunizationOrder'] = {}
            encounter_dict['procedure'] = {}
        print(encounter_dict)
        return Response(json.dumps(encounter_dict, cls=UUIDEncoder))

    def update(self, request):
        pass
    def destroy(self, request):
        pass
    def update_encounter(self, request):
        pass
    def destroy_encounter(self, request):
        pass
