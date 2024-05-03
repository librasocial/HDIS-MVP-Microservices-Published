from .models import *
from .serializers import *
from .oauth2helper import get_client_credentials_access_token
#from .producer import publish, publish_soap
import datetime
import json
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

###### TODOs #####
## decorator as per standard
## book nearest appointment slot for walkins
## checkin autmatically after booking nearest appointment
## handle negative cases

class ResourceScheduleViewSet(viewsets.ViewSet):

    permission_classes = [TokenHasReadWriteScope]#, IsFacilityAdminPermission]    #TODO: Limit to Facility Admins

    def create(self, request):
        """Create a new Resource Schedule for a particular Resource (Provider, Equipment, etc.) with all its related nested entities."""

        request_body = request.data
        resource_details = ResourceSchedule.create_new_schedule(request_body)
        serializer = ResourceScheduleNestedSerializer(resource_details)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    def retrieve(self, request, pk):
        """Retrieve Full Resource Schedule by ID."""

        resource_schedule = get_object_or_404(ResourceSchedule.objects.all(), primary_key=pk)
        serializer = ResourceScheduleNestedSerializer(resource_schedule)
        return Response(serializer.data)


    def update(self, request, pk):
        """Allows update to limited attributes of ResourceSchedule and its related entities;"""

        new_effective_to = request.data.get('effective_to')
        if new_effective_to:
            resource_schedule = get_object_or_404(ResourceSchedule.objects.all(), primary_key=pk)
            resource_schedule.effective_to = new_effective_to
            serializer = ResourceScheduleSerializer(resource_schedule)
            return Response(serializer.data)
        else:
            return Response({"detail": "No updateable parameters provided. Note that updates are allowed only to 'effective_to'."})


    @action(detail=False, methods=['GET'], url_path='resources/(?P<rid>[^/.]+)/date/(?P<dt>\d{4}-\d{2}-\d{2})', name='List by Resource ID as of Date')
    def list_full_schedule(self, request, rid, dt):
        """Lists applicable Resource Schedule Days (including day-level configurations) for a specified Resource ID as of a Date for the 
           entire work week or, optionally, a specific working day of the week passed in through the "day" Query Parameter (e.g. ?day=Mon).
        """
        requested_date = datetime.datetime.strptime(dt, "%Y-%m-%d").date()
        resource_schedule = get_object_or_404(ResourceSchedule.objects.all(), resource_id=rid, 
                                              effective_from__lte=requested_date, effective_to__gte=requested_date)
        day = request.query_params.get('day')
        if day is None:    #Request to retrieve Schedule for all workdays
            print("Retrieving Resource Schedule for all working days of the week...") #Info
            workdays = ResourceScheduleDay.objects.filter(resource_schedule=resource_schedule, day_of_the_week_working_status=True)
        else:    #Request to retrieve Schedule for a single workday
            print("Retrieving Resource Schedule for the specified day...") #Info
            workdays = ResourceScheduleDay.objects.filter(resource_schedule=resource_schedule, day_of_the_week=day, day_of_the_week_working_status=True)
            
        serializer = ResourceScheduleDayNestedSerializer(workdays, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['GET'], url_path='uhpn/(?P<uhpn>[^/.]+)', name='List By UHPN and Date')
    def list_provider_schedule_by_uhpn(self, request, uhpn):
        """Get full Resource Schedule for a Provider based on their UHPN."""

        # Build URL to get Provider details by UHPN
        url = settings.GET_PROVIDER_BY_UHPN_URL.format(uhpn)
        print("Get Provider By UHPN URL:", url) #Debug

        # Retrieve Access Token for Client Credentials grant type
        try:
            access_token = get_client_credentials_access_token()
        except Exception as e:
            error_body = { "details": f"Failed to get Client Credentials token due to the following error: {e}" } #TODO: Review message
            print(f"{error_body}") #TODO: Log error details
            return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Invoke URL to get Provider Details by UHPN
        provider_details_response = requests.get(
            url, headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
        )
        if provider_details_response.status_code == 200:
            response_body = provider_details_response.json()
            employee_id = response_body.get("employee_id")
            if employee_id:
                print("Employee ID:", employee_id) #Debug
                as_of_date_input = request.query_params.get('as_of_date')
                if as_of_date_input:
                    as_of_date = datetime.datetime.strptime(as_of_date_input, '%Y-%m-%d').date()
                else:
                    as_of_date = datetime.date.today()
                print("Request Date:", as_of_date) #Debug
                
                try:
                    provider_schedule = ResourceSchedule.objects.get(resource_id=employee_id, effective_from__lte=as_of_date, effective_to__gte=as_of_date)
                    serializer = ResourceScheduleNestedSerializer(provider_schedule)
                    return Response(serializer.data)
                except ResourceSchedule.DoesNotExist:
                    error_body = { "details": f"No active Schedule found for specified Provider as of date '{as_of_date}'." } #TODO: Log error details
                    return Response(error_body, status.HTTP_404_NOT_FOUND)                    
                except ValueError:
                    error_body = { "details": f"Multiple active Schedules found for specified Provider as of date '{as_of_date}'. Invalid Schedule data must be corrected." } #TODO: Log error details
                    return Response(error_body, status.HTTP_422_UNPROCESSABLE_ENTITY)                    
            else:
                error_body = { "details": f"Successfully invoked Employee Management service but could not retrieve Employee ID for Provider. Response Body: {response_body}" } #TODO: Review message
                return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif provider_details_response.status_code == 404:
            error_body = { "details": f"Provider not found for specified UHPN." }
            return Response(error_body, status.HTTP_404_NOT_FOUND)
        else:
            error_body = { "details": f"Error retrieving Provider details from Employee Management service. Status Code: '{provider_details_response.status_code}', Details: '{response_body}'" } #TODO: Log error details
            return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)


class AppointmentViewSet(viewsets.ViewSet):

    @csrf_exempt    #TODO: Check need and remove across all methods.
    def create(self, request):
        """Create a new Appointment for a Patient with a Provider at a Facility."""
        
        request_body = request.data
        print("Request Body:", request_body) #Debug
        facility_id = request_body['uniqueFacilityIdentificationNumber']

        #TODO: Check Resource Unavailability and block Appointment creation if necessary.
        
        # Retrieve Access Token for Client Credentials grant type
        try:
            access_token = get_client_credentials_access_token()
        except Exception as e:
            error_body = { "details": f"Failed to get Client Credentials token due to the following error: {e}" } #TODO: Review message
            print(f"{error_body}") #TODO: Log error details
            return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Build URL to get Facility details by Local Facility ID
        fac_mgt_url = settings.GET_FACILITY_BY_FACILITY_ID_URL.format(facility_id)
        print("Get Facility Details URL:", fac_mgt_url) #Debug

        # Invoke URL to get Facility Details
        facility_details_response = requests.get(
            fac_mgt_url, headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
        )
        if facility_details_response.status_code == status.HTTP_200_OK:
            facility = facility_details_response.json()
            if not facility:
                error_body = { "details": f"Failed to extract Facility details from Facility Management service response. Response Content: {facility_details_response.content}" } #TODO: Review message
                return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            error_body = { "details": f"Error retrieving Facility Details from Facility Management service. Status Code: '{facility_details_response.status_code}', Response Content: {facility_details_response.content}" } #TODO: Log error details
            return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        print("Facility:", facility) #Debug
        
        
        # Build URL to get Provider details by UHPN
        uhpn = request_body['uniqueIndividualHealthCareProviderNumber']
        emp_mgt_url = settings.GET_PROVIDER_BY_UHPN_URL.format(uhpn)
        print("Get Provider By UHPN URL:", emp_mgt_url) #Debug

        # Invoke URL to get Provider Details by UHPN
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
        lfpid = request_body.get('localFacilityPatientId')
        ptn_mgt_url = settings.GET_PATIENT_BY_LFPID_URL.format(lfpid)
        print("Get Patient Details URL:", ptn_mgt_url) #Debug

        # Invoke URL to get Patient Details by LFPID
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
        
        # Parse date and time inputs for requested appointment
        for_date = request_body['date']
        start_time = request_body['start_time']
        requested_date = datetime.datetime.strptime(for_date, '%Y-%m-%d').date()
        requested_start_time = datetime.datetime.strptime(start_time, '%H:%M').time()
        requested_start_datetime = datetime.datetime.combine(requested_date, requested_start_time)
        requested_day_name = requested_start_datetime.strftime('%a')
        print("Requested Start Datetime:", requested_start_datetime) #Debug
        print("Requested Day of Week:", requested_day_name) #Debug
        
        # Retrieve active Provider Schedule for the identified Provider as of the current date.
        provider_schedule = ResourceSchedule.objects.filter(resource_id=provider.get('employee_id'), 
                                                            effective_from__lte=requested_start_datetime, effective_to__gte=requested_start_datetime)
        if not provider_schedule:
            error_body = { "details": "No active Resource Schedule found for the Provider on the requested date. Please request an alternative date." }
            return Response(error_body, status.HTTP_422_UNPROCESSABLE_ENTITY)
        elif provider_schedule.count() > 1:
            error_body = { "details": "Multiple active Resource Schedules found for the Provider on the requested date. This must be corrected to proceed." }
            return Response(error_body, status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        # Retrieve Schedule Details for the identified Provider on the Day of Week matching that of the requested Appointment.
        provider_schedule_day = ResourceScheduleDay.objects.filter(resource_schedule=provider_schedule.first(), 
                                                                   day_of_the_week=requested_day_name, day_of_the_week_working_status=True).first()
        # Dev Note: It is assumed that there will not be more than one entry in a single Resource Schedule for a particular Day of the Week.
        if not provider_schedule_day:
            error_body = { "details": "No active Schedule found for the Provider on the requested day of week. Please request an alternative day of week." }
            return Response(error_body, status.HTTP_422_UNPROCESSABLE_ENTITY)

        # Check that the requested Time falls within an active Appointment Session on that Day of Week, accounting for duration of an Appointment.
        resource_schedule_session = ResourceScheduleSession.objects.filter(resource_schedule_day=provider_schedule_day, 
                                                                           start_time__lte=requested_start_time, end_time__gt=requested_start_time).first()
        # Dev Note: It is assumed that any requested Start Time will fall within a single active Session.
        error_body = { "details": f"Unable to accommodate the appointment within an active Session for the Provider on that date. Please choose an alternative slot." }
        if not resource_schedule_session:
            return Response(error_body, status.HTTP_422_UNPROCESSABLE_ENTITY)
        
        print("Scheduled Duration:", resource_schedule_session.duration) #Debug
        requested_end_datetime = requested_start_datetime + resource_schedule_session.duration
        print("Requested End Datetime:", requested_end_datetime) #Debug

        if requested_end_datetime.time() > resource_schedule_session.end_time:
            return Response(error_body, status.HTTP_422_UNPROCESSABLE_ENTITY)        
        print("Duration:", requested_end_datetime - requested_start_datetime) #Debug
        
        # TODO: Additional checks for valid appointment request, including Start Time on slot boundary as well as against overbooking settings.

        appointment_dict = dict(patient_id=patient['local_facility_patient_id'], resource_id=provider['employee_id'], facility_id=facility_id, resource_type=ResourceSchedule.ResourceType.Provider,
                                  resource_schedule_session=resource_schedule_session.primary_key, start_datetime=requested_start_datetime, end_datetime=requested_end_datetime)
        appointment_serializer = AppointmentSerializer(data=appointment_dict)
        appointment_serializer.is_valid(raise_exception=True)
        appointment = appointment_serializer.save()
        print('Appointment Created.') #Debug

        print("Appointment Data:", appointment.__dict__) #Debug
        #publish_soap('appointment created', json.dumps(appointment_serializer.data, cls=UUIDEncoder)) #Temporarily disabled
        
        return Response(appointment_serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['GET'], url_path='patient/(?P<pid>[^/.]+)', name='List By Patient ID')
    @csrf_exempt
    def get_appointments_for_patient(self, request, pid):    #TODO: Add access control checks
        """Get all Appointments for a specified Patient, optionally for a specific Resource and Date."""

        # Retrieve Access Token for Client Credentials grant type
        try:
            access_token = get_client_credentials_access_token()
        except Exception as e:
            error_body = { "details": f"Failed to get Client Credentials token due to the following error: {e}" } #TODO: Review message
            print(f"{error_body}") #TODO: Log error details
            return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Build URL to get Patient details by Patient ID
        ptn_mgt_url = settings.GET_PATIENT_BY_LFPID_URL.format(pid)
        print("Get Patient Details URL:", ptn_mgt_url) #Debug

        # Invoke URL to get Patient Details
        patient_details_response = requests.get(
            ptn_mgt_url, headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
        )
        if patient_details_response.status_code == status.HTTP_200_OK:
            patient = patient_details_response.json()
            if not patient:
                error_body = { "details": f"Failed to get Patient details from Patient Management service Response." }
                return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif patient_details_response.status_code == 404:
            error_body = { "details": f"Patient not found for specified Patient ID." }
            return Response(error_body, status.HTTP_404_NOT_FOUND)
        else:
            error_body = { "details": f"Error retrieving Patient Details from Patient Management service. Status Code: '{patient_details_response.status_code}', Details: '{patient_details_response.__dict__}'" } #TODO: Log error details
            return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        print("Patient:", patient) #Debug
        
        appointments = Appointment.objects.filter(patient_id=patient['local_facility_patient_id'], facility_id=patient['facility_id'], 
                                                  resource_type=ResourceSchedule.ResourceType.Provider)
        
        # Parse optional parameters and apply additional filters
        resource_id = request.query_params.get('resource_id')
        if resource_id:
            appointments.filter(resource_id=resource_id)
        
        for_date_input = request.query_params.get('for_date')
        if for_date_input:
            for_date = datetime.datetime.strptime(for_date_input, '%Y-%m-%d').date()
            print("For Date:", for_date) #Debug
            appointments.filter(start_datetime__date=for_date)
        
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)


    @action(detail=False, methods=['GET'], url_path='resource/(?P<rid>[^/.]+)/date/(?P<dt>\d{4}-\d{2}-\d{2})', name='List By Resource ID and Date')
    @csrf_exempt
    def get_appointments_for_resource(self, request, rid, dt):
        """Get all Appointments for a specified Resource (Provider, Equipment, etc.) for a specified date."""
        
        # Parse inputs
        requested_date = datetime.datetime.strptime(dt, '%Y-%m-%d').date()
        print("Request Date:", requested_date) #Debug

        # Apply Resource and Date filters
        appointments = Appointment.objects.filter(resource_id=rid, start_datetime__date=requested_date)
                
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(serializer.data)


    def update(self, request, pk=None):    #TODO: Apply permissions
        """Update an existing Appointment for a Patient with a Provider at a Facility. To be accessed by Facility Members only."""
        
        #TODO: Check if any updates other than cancellation are to be supported
        appointment = get_object_or_404(Appointment.objects.all(), primary_key=pk, status_code=Appointment.Status.Active)
        appointment.status_code = Appointment.Status.Cancelled
        appointment.save()
        return Response({"details": "Appointment has been cancelled."}, status=status.HTTP_200_OK)


    def destroy(self, request, pk=None):    #TODO: Apply permissions
        """Permanently delete an existing Appointment for a Patient with a Provider at a Facility. To be accessed by Superusers only."""

        appointment = get_object_or_404(Appointment.objects.all(), primary_key=pk)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    @action(detail=False, methods=['PUT'], url_path='cancellation/', name='Cancel Appointment')
    def cancel(self, request, patient_id, provider_id, facility_id):    #TODO: Apply permissions, check if separate cancellation operation is required
        """Cancel an existing Appointment for a Patient with a Provider at a Facility. Accessible only to Facility Members."""
        
        appointment = get_object_or_404(Appointment.objects.all(), patient_id=patient_id, resource_id=provider_id, facility_id=facility_id, 
                                        status_code=Appointment.Status.Active)
        appointment.status_code = Appointment.Status.Cancelled
        return Response({"details": "Appointment has been cancelled."}, status=status.HTTP_200_OK)



class ResourceUnavailabilityViewSet(viewsets.ModelViewSet):
    """API that allows the setting of temporary periods of unavailability for a Resource, such as a Provider going on Leave or Equipment breakdown."""

    queryset = ResourceUnavailability.objects.all()
    serializer_class = ResourceUnavailabilitySerializer
    permission_classes = [TokenHasReadWriteScope]#, IsFacilityAdminPermission]
    
    @action(detail=False, methods=['GET'], url_path='search/(?P<rid>[^/.]+)', name='Search')
    def search(self, request, rid, *args, **kwargs):
        """Resource Unavailability Search based on Resource ID, Start Date and End Date."""
        
        # Get and validate mandatory query parameters from the request query parameters
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if not all([start_date, end_date]):
            return Response({"detail": "Start Date and End Date parameters must be specified."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter and serialize results
        results = ResourceUnavailability.objects.filter(resource_id=rid, unavailability_date__gte=start_date, unavailability_date__lte=end_date)
        serializer = self.get_serializer(results, many=True)
        return Response(serializer.data)
