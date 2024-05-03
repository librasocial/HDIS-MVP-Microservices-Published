from .models import *
from .serializers import *
from .oauth2helper import get_client_credentials_access_token
#from .producer import publish
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

class ConsultationPlanViewSet(viewsets.ViewSet):

    permission_classes = [TokenHasReadWriteScope]
    
    def list(self, request):
        """ Retrieve all available Clinical Notes. Meant for Superuser troubleshooting. Avoid usage in Production environment. """

        assessment_clinical_note = ClinicalNote.objects.all()
        serializer = ClinicalNoteSerializer(assessment_clinical_note, many=True)
        return Response(serializer.data)


    def create(self, request):
        """ Creates a generic Clinical Note and/or specialized Clinical Order linked to a Clinical Note. """

        request_body = request.data
        print("Request Body:", request_body) #Debug

        # Clinical Note processing
        entity_created = False
        response_body = {}
        if 'clinical_note' in request_body:    #The request is to either create a new Note or link to an existing Note

            try:
                # If the specified Clinical Note already exists, retrieve it.
                clinical_note = ClinicalNote.objects.get(primary_key=request.data['clinical_note']['primary_key'])
            except ClinicalNote.DoesNotExist:
                    # If a Clinical Note has been specified but does not exist, return an error.
                    error_body = {
                        "type": request.build_absolute_uri("/errors/bad-request-data"),
                        "title": "Specified Clinical Note does not exist.",
                        "detail": "When not creating a new Clinical Note the specified Clinical Note must exist."
                    }
                    return Response(error_body, status=status.HTTP_400_BAD_REQUEST)
            except KeyError:
                # If no existing Clinical Note has been specified, attempt to create a new Clinical Note.

                # Parse Provider ID(s) to be associated with the new Clinical Note. 
                try:
                    provider_ids = request_body['provider_ids']
                except KeyError:
                    error_body = {
                        "type": request.build_absolute_uri("/errors/bad-request-data"),
                        "title": "Missing Provider ID(s).",
                        "detail": "At least one Provider ID to be associated with the Clinical Note must be passed in via the 'provider_ids' list parameter."
                    }
                    return Response(error_body, status=status.HTTP_400_BAD_REQUEST)
                
                # Parse and validate core Clinical Note data.
                cn_serializer = ClinicalNoteSerializer(data=request_body['clinical_note'])
                cn_serializer.is_valid(raise_exception=True)
                new_clinical_note = cn_serializer.save()
                entity_created = True
                response_body['clinical_note'] = cn_serializer.data
                encounter_id = cn_serializer.validated_data['encounter_id']
                
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
        
        
        # Process specialized Clinical Orders
        if 'lab_order' in request_body:
            lo_serializer = LabOrderSerializer(data=request_body['lab_order'])
            lo_serializer.is_valid(raise_exception=True)
            lo_serializer.save()
            entity_created = True
            response_body['lab_order'] = lo_serializer.data
        
        if 'radiology_order' in request_body:
            ro_serializer = RadiologyOrderSerializer(data=request_body['radiology_order'])
            ro_serializer.is_valid(raise_exception=True)
            ro_serializer.save()
            entity_created = True
            response_body['radiology_order'] = ro_serializer.data

        if 'pharmacy_order' in request_body:
            pho_serializer = PharmacyOrderSerializer(data=request_body['pharmacy_order'])
            pho_serializer.is_valid(raise_exception=True)
            pho_serializer.save()
            entity_created = True
            response_body['pharmacy_order'] = pho_serializer.data
        
        if 'immunization_order' in request_body:
            io_serializer = ImmunizationOrderSerializer(data=request_body['immunization_order'])
            io_serializer.is_valid(raise_exception=True)
            io_serializer.save()
            entity_created = True
            response_body['immunization_order'] = io_serializer.data
        
        if 'procedure_order' in request_body:
            pro_serializer = ProcedureOrderSerializer(data=request_body['procedure_order'])
            pro_serializer.is_valid(raise_exception=True)
            pro_serializer.save()
            entity_created = True
            response_body['procedure_order'] = pro_serializer.data
                
        if not entity_created:
            error_body = {
                "type": request.build_absolute_uri("/errors/bad-request-data"),
                "title": "No Clinical Note or Clinical Order entity created.",
                "detail": "Check request data. Note that only the following Clinical Order Types are recognized: lab_order, radiology_order, pharmacy_order, immunization_order, procedure_order."
            }
            return Response(error_body, status=status.HTTP_400_BAD_REQUEST)

        return Response(response_body, status=status.HTTP_201_CREATED)


    def retrieve_clinical_note(self, request, cnid):
        """ Retrieve Clinical Note details by ID. """

        clinical_note = get_object_or_404(ClinicalNote.objects.all(), primary_key=cnid)
        serializer = ClinicalNoteSerializer(clinical_note)
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
        plan_details_for_encounter = {}
        plan_details_for_encounter['episode_id'] = encounters[0]['episode']['primary_key']
        plan_details_for_encounter['encounter_id'] = eid
        plan_details_for_encounter['provider_ids'] =  [ep.provider_id.hex for ep in encounter_providers]
        plan_details_for_encounter['patient_id'] = encounters[0]['patient_id']

        # Populate details of generic Clinical Notes
        plan_details_for_encounter['clinical_notes'] = clinical_notes_serializer.data

        # Initialize attributes for specialized Clinical Note details.
        plan_details_for_encounter['lab_orders'] = []
        plan_details_for_encounter['radiology_orders'] = []
        plan_details_for_encounter['pharmacy_orders'] = []
        plan_details_for_encounter['immunization_orders'] = []
        plan_details_for_encounter['procedure_orders'] = []
        if clinical_notes.exists():
            for clinical_note in clinical_notes:
                clinical_orders = clinical_note.clinical_orders.all() if hasattr(clinical_note, 'clinical_orders') else None
                clinical_orders_pks = [clinical_order.primary_key for clinical_order in clinical_orders]
                lab_orders = LabOrder.objects.filter(clinicalorder_ptr_id__in=clinical_orders_pks)
                plan_details_for_encounter['lab_orders'].extend(LabOrderSerializer(lab_orders, many=True).data)
                radiology_orders = RadiologyOrder.objects.filter(clinicalorder_ptr_id__in=clinical_orders_pks)
                plan_details_for_encounter['radiology_orders'].extend(RadiologyOrderSerializer(radiology_orders, many=True).data)
                pharmacy_orders = PharmacyOrder.objects.filter(clinicalorder_ptr_id__in=clinical_orders_pks)
                plan_details_for_encounter['pharmacy_orders'].extend(PharmacyOrderSerializer(pharmacy_orders, many=True).data)
                immunization_orders = ImmunizationOrder.objects.filter(clinicalorder_ptr_id__in=clinical_orders_pks)
                plan_details_for_encounter['immunization_orders'].extend(ImmunizationOrderSerializer(immunization_orders, many=True).data)
                procedure_orders = ProcedureOrder.objects.filter(clinicalorder_ptr_id__in=clinical_orders_pks)
                plan_details_for_encounter['procedure_orders'].extend(ProcedureOrderSerializer(procedure_orders, many=True).data)

        print("Plan details for Encounter:", plan_details_for_encounter) #Debug
        return Response(plan_details_for_encounter)


class OrderSetViewSet(viewsets.ViewSet):
    """ API that facilitates CRUD operations on Order Set entities. """

    permission_classes = [TokenHasReadWriteScope]

    def list(self, request):
        """ Retrieve all available Order Sets. Meant for Superuser troubleshooting. Avoid usage in Production environment. """

        all_order_sets = OrderSet.objects.all()
        serializer = OrderSetSerializer(all_order_sets, many=True)
        return Response(serializer.data)


    def create(self, request):
        """ Creates an Order Set potentially comprised of multiple types of Orders. """

        request_body = request.data
        print("Request Body:", request_body) #Debug

        # Process request to either create a new Order Set or add new Orders in an existing Order Set
        entity_created = False
        response_body = {}
        new_order_set = None
        if 'order_set' in request_body:    

            try:
                # If the specified Order Set already exists, retrieve it.
                order_set = OrderSet.objects.get(primary_key=request_body['order_set']['primary_key'])
                response_body['order_set'] = {}
            except OrderSet.DoesNotExist:
                    # If an Order Set has been specified but does not exist, return an error.
                    error_body = {
                        "type": request.build_absolute_uri("/errors/bad-request-data"),
                        "title": "Specified Order Set does not exist.",
                        "detail": "When not creating a new Order Set, the specified Order Set must exist."
                    }
                    return Response(error_body, status=status.HTTP_400_BAD_REQUEST)
            except KeyError:
                # If no existing Order Set has been specified, attempt to create a new Order Set.
                                
                # Parse and validate core Order Set data.
                os_serializer = OrderSetSerializer(data=request_body['order_set'])
                os_serializer.is_valid(raise_exception=True)
                new_order_set = os_serializer.save()
                entity_created = True
                response_body['order_set'] = os_serializer.data

            # If the request involves creation of Orders for the Order Set...
            order_set_request = request_body['order_set']
            if 'lab_order' in order_set_request:
                if new_order_set:
                    order_set_request['lab_order']['order_set'] = new_order_set.primary_key
                else:
                    order_set_request['lab_order']['order_set'] = request_body['order_set']['primary_key']
                lo_serializer = OrderSetLabSerializer(data=order_set_request['lab_order'])
                lo_serializer.is_valid(raise_exception=True)
                lo_serializer.save()
                entity_created = True
                response_body['order_set']['lab_order'] = lo_serializer.data
            
            if 'radiology_order' in order_set_request:
                if new_order_set:
                    order_set_request['radiology_order']['order_set'] = new_order_set.primary_key
                else:
                    order_set_request['radiology_order']['order_set'] = request_body['order_set']['primary_key']
                ro_serializer = OrderSetRadiologySerializer(data=order_set_request['radiology_order'])
                ro_serializer.is_valid(raise_exception=True)
                ro_serializer.save()
                entity_created = True
                response_body['order_set']['radiology_order'] = ro_serializer.data

            if 'pharmacy_order' in order_set_request:
                if new_order_set:
                    order_set_request['pharmacy_order']['order_set'] = new_order_set.primary_key
                else:
                    order_set_request['pharmacy_order']['order_set'] = request_body['order_set']['primary_key']
                pho_serializer = OrderSetPharmacySerializer(data=order_set_request['pharmacy_order'])
                pho_serializer.is_valid(raise_exception=True)
                pho_serializer.save()
                entity_created = True
                response_body['order_set']['pharmacy_order'] = pho_serializer.data
            
            if 'immunization_order' in order_set_request:
                if new_order_set:
                    order_set_request['immunization_order']['order_set'] = new_order_set.primary_key
                else:
                    order_set_request['immunization_order']['order_set'] = request_body['order_set']['primary_key']
                io_serializer = OrderSetImmunizationSerializer(data=order_set_request['immunization_order'])
                io_serializer.is_valid(raise_exception=True)
                io_serializer.save()
                entity_created = True
                response_body['order_set']['immunization_order'] = io_serializer.data
            
            if 'procedure_order' in order_set_request:
                if new_order_set:
                    order_set_request['procedure_order']['order_set'] = new_order_set.primary_key
                else:
                    order_set_request['procedure_order']['order_set'] = request_body['order_set']['primary_key']
                pro_serializer = OrderSetProcedureSerializer(data=order_set_request['procedure_order'])
                pro_serializer.is_valid(raise_exception=True)
                pro_serializer.save()
                entity_created = True
                response_body['order_set']['procedure_order'] = pro_serializer.data
                
        if not entity_created:
            error_body = {
                "type": request.build_absolute_uri("/errors/bad-request-data"),
                "title": "No Order Set or additional Order(s) within an Order Set was created.",
                "detail": "Check request data. Note that only the following Order Types are valid within an Order Set: lab_order, radiology_order, pharmacy_order, immunization_order, procedure_order."
            }
            return Response(error_body, status=status.HTTP_400_BAD_REQUEST)

        return Response(response_body, status=status.HTTP_201_CREATED)


    def retrieve(self, request, osid):
        """ Retrieve Order Set details by ID. """

        order_set = get_object_or_404(OrderSet.objects.all(), primary_key=osid)
        serializer = OrderSetSerializer(order_set)
        return Response(serializer.data)
    

    def destroy(self, request, osid=None):
        """Permanently delete an existing Order Set for a Provider. Allow for concerned Provider and Facility Admin only."""

        order_set = get_object_or_404(OrderSet.objects.all(), primary_key=osid)
        # TODO: Look up Provider details and check permissions
        order_set.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

    def retrieve_for_provider(self, request, pid):
        """
        Retrieve all Order Set details for a specified Provider (associated with a single Facility).
        Only the Provider concerned should have access.
        """
        
        # Retrieve details for the associated Provider from the Employee Management service.
        # Step 1 - Retrieve Access Token for Client Credentials grant type
        try:
            access_token = get_client_credentials_access_token()
        except Exception as e:
            error_body = { "details": f"Failed to get Client Credentials token due to the following error: {e}" } #TODO: Review message
            print(f"{error_body}") #TODO: Log error details
            return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Step 2 - Build URL to retrieve Provider details
        get_provider_by_id_url = settings.GET_PROVIDER_BY_ID_URL.format(pid)
        print("Get Provider By ID URL:", get_provider_by_id_url) #Debug

        # Step 3 - Invoke URL to get Provider details by ID
        provider_details_response = requests.get(
            get_provider_by_id_url, headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
        )
        if provider_details_response.status_code == status.HTTP_200_OK:
            provider = provider_details_response.json()
            if not provider:
                error_body = { "details": f"Failed to retrieve Provider details from Employee Management service response. Response Content: {provider_details_response.content}" } #TODO: Review message
                return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif provider_details_response.status_code == status.HTTP_404_NOT_FOUND:
            error_body = { "details": "Error retrieving Provider details from Employee Management service. Invalid Provider ID input." }
            return Response(error_body, status.HTTP_400_BAD_REQUEST)
        else:
            error_body = { "details": f"Error retrieving Provider details from Employee Management service. Status Code: '{provider_details_response.status_code}', Response Content: {provider_details_response.content}" } #TODO: Log error details
            return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        print("Provider:", provider) #Debug

        # Deny permission if no Auth Token supplied or if the logged-in user is not the Provider who owns the Order Set.
        # Note: OAuth2 Client Credential will pass this check.
        if (not request.auth) or (request.user and request.user.username != provider.member_username):
            error_body = {
                "type": request.build_absolute_uri("/errors/forbidden"),
                "title": "Access denied.",
                "detail": "Only the concerned Provider is allowed to access an Order Set."
            }
            return Response(error_body, status=status.HTTP_403_FORBIDDEN)

        order_sets = OrderSet.objects.filter(provider_id=pid)
        order_sets_serializer = OrderSetSerializer(order_sets, many=True)

        # Populate Response data.
        response_body = {}
        response_body['provider_id'] =  provider['primary_key']
        response_body['order_sets'] = order_sets_serializer.data
        response_body['lab_orders'] = []
        response_body['radiology_orders'] = []
        response_body['pharmacy_orders'] = []
        response_body['immunization_orders'] = []
        response_body['procedure_orders'] = []
        if order_sets.exists():
            order_sets_pks = [order_set.primary_key for order_set in order_sets]
            lab_orders = OrderSetLab.objects.filter(order_set_id__in=order_sets_pks)
            response_body['lab_orders'].extend(OrderSetLabSerializer(lab_orders, many=True).data)
            radiology_orders = OrderSetRadiology.objects.filter(order_set_id__in=order_sets_pks)
            response_body['radiology_orders'].extend(OrderSetRadiologySerializer(radiology_orders, many=True).data)
            pharmacy_orders = OrderSetPharmacy.objects.filter(order_set_id__in=order_sets_pks)
            response_body['pharmacy_orders'].extend(OrderSetPharmacySerializer(pharmacy_orders, many=True).data)
            immunization_orders = OrderSetImmunization.objects.filter(order_set_id__in=order_sets_pks)
            response_body['immunization_orders'].extend(OrderSetImmunizationSerializer(immunization_orders, many=True).data)
            procedure_orders = OrderSetProcedure.objects.filter(order_set_id__in=order_sets_pks)
            response_body['procedure_orders'].extend(OrderSetProcedureSerializer(procedure_orders, many=True).data)

        print("Order Set details for Provider:", response_body) #Debug
        return Response(response_body)


    def destroy_order_set_order(self, request):
        """ Remove existing Order(s) from an Order Set for a Provider. Allow for concerned Provider and Facility Admin only."""
        
        # TODO: Look up Provider from Order Set and check permissions
        entity_deleted = False
        response_body = {}
        request_body = request.data
        if 'lab_order' in request_body:
            try:
                lab_order = get_object_or_404(OrderSetLab.objects.all(), primary_key=request_body['lab_order']['primary_key'])
                lab_order.delete()
                entity_deleted = True
                response_body['lab_order'] = "Removed successfully."
            except KeyError:
                response_body['lab_order'] = "Removal failed. A Lab Order must be specified using 'primary_key'."
            except OrderSetLab.DoesNotExist:
                response_body['lab_order'] = "Removal failed. The specified Lab Order was not found."                
        
        if 'radiology_order' in request_body:
            try:
                radiology_order = get_object_or_404(OrderSetRadiology.objects.all(), primary_key=request_body['radiology_order']['primary_key'])
                radiology_order.delete()
                entity_deleted = True
                response_body['radiology_order'] = "Removed successfully."
            except KeyError:
                response_body['radiology_order'] = "Removal failed. A Radiology Order must be specified using 'primary_key'."
            except OrderSetRadiology.DoesNotExist:
                response_body['radiology_order'] = "Removal failed. The specified Radiology Order was not found."                

        if 'pharmacy_order' in request_body:
            try:
                pharmacy_order = get_object_or_404(OrderSetPharmacy.objects.all(), primary_key=request_body['pharmacy_order']['primary_key'])
                pharmacy_order.delete()
                entity_deleted = True
                response_body['pharmacy_order'] = "Removed successfully."
            except KeyError:
                response_body['pharmacy_order'] = "Removal failed. A Pharmacy Order must be specified using 'primary_key'."
            except OrderSetPharmacy.DoesNotExist:
                response_body['pharmacy_order'] = "Removal failed. The specified Pharmacy Order was not found."                
        
        if 'immunization_order' in request_body:
            try:
                immunization_order = get_object_or_404(OrderSetImmunization.objects.all(), primary_key=request_body['immunization_order']['primary_key'])
                immunization_order.delete()
                entity_deleted = True
                response_body['immunization_order'] = "Removed successfully."
            except KeyError:
                response_body['immunization_order'] = "Removal failed. A Immunization Order must be specified using 'primary_key'."
            except OrderSetImmunization.DoesNotExist:
                response_body['immunization_order'] = "Removal failed. The specified Immunization Order was not found."                
        
        if 'procedure_order' in request_body:
            try:
                procedure_order = get_object_or_404(OrderSetProcedure.objects.all(), primary_key=request_body['procedure_order']['primary_key'])
                procedure_order.delete()
                entity_deleted = True
                response_body['procedure_order'] = "Removed successfully."
            except KeyError:
                response_body['procedure_order'] = "Removal failed. A Procedure Order must be specified using 'primary_key'."
            except OrderSetProcedure.DoesNotExist:
                response_body['procedure_order'] = "Removal failed. The specified Procedure Order was not found."                
                
        if not entity_deleted:
            error_body = {
                "type": request.build_absolute_uri("/errors/bad-request-data"),
                "title": "No Order(s) were removed from an Order Set.",
                "detail": "Check request data. Note that only the following Order Types are valid within an Order Set: lab_order, radiology_order, pharmacy_order, immunization_order, procedure_order."
            }
            return Response(error_body, status=status.HTTP_400_BAD_REQUEST)

        return Response(response_body)
