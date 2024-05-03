from .models import *
from .serializers import *
#from .producer import publish
from uuid import UUID
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

######## To Do #########
#Provider Updated event to be published
#doctor creation date
# on older than 7 days, if no registration certificate given, disable doctor
# Provider model needs a field for active, inactive
# Disabling will be manual or out of bound(cron job) trigegring
#negative flows handle
#all doctor fields to be added to be filled by admin/doctor
#add new doctor, move to edit after this
#use primarykey for facility identifier

class EmployeeViewSet(viewsets.ModelViewSet):
    """API that facilitates operations on Employee entities, typically managed by a Facility Admin."""

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [TokenHasReadWriteScope]#, IsFacilityAdminPermission]
    
    def retrieve(self, request, pk):
        """Retrieve details for a specified Employee ID. Setting Query Param 'withDocuments' to 'y' will also retrieve related Documents. """
        
        # employee_details = get_object_or_404(Employee.objects.all(), employee_id=eid)
        # print("Employee:", employee_details) #Debug
        # serializer = EmployeeSerializer(employee_details)
        # response_body = {'employee': serializer.data}

        response = super().retrieve(self, request, pk)
        if request.query_params.get("withDocuments", "n").lower() == "y":
            documents = EmployeeDocuments.objects.filter(employee_id=pk)
            #print("Document URL:", documents.document_file.url) #Debug
            document_serializer = EmployeeDocumentsSerializer(documents, many=True)
            response.data.update({'documents':document_serializer.data})
        
        print("Response Body:", response.data.__dict__) #Debug
        return response


    # TODO: Check implications of deactivating various Employee types.
    def destroy(self, request, pk):
        """Deactivate an Employee."""

        employee_details = get_object_or_404(Employee.objects.all(), employee_id=pk)
        employee_details.status = Employee.Status.Inactive  
        employee_details.save()
        return Response({"detail": "The specified Employee has been successfully deactivated."}, status.HTTP_200_OK)


    @action(detail=False, methods=['GET'], name='Search')
    def search(self, request, *args, **kwargs):
        """Employee Search based on various attributes."""

        #TODO: Limit results by Facility depending on Role of requestor?
        # Get optional query parameters from the request
        fid = request.query_params.get('facility_id')
        username = request.query_params.get('member_username')
        specialty = request.query_params.get('medical_specialty_type_code')
        contact = request.query_params.get('contact_number')
        city = request.query_params.get('current_city')
        status = request.query_params.get('status')

        if not any([fid, username, specialty, contact, city, status]):
            return Response({"detail": "At least one search parameter must be specified."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter the queryset based on the optional parameters
        queryset = Employee.objects.all()
        if fid:
            queryset = queryset.filter(facility_id=fid)
        if username:
            queryset = queryset.filter(member_username=username)
        if specialty:
            queryset = queryset.filter(medical_specialty_type_code=specialty)  
        if contact:
            queryset = queryset.filter(contact=contact)
        if city:
            queryset = queryset.filter(current_city=city)
        if status:
            queryset = queryset.filter(status=status)
        
        # Serialize the filtered queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class EmployeeDocumentsViewSet(viewsets.ModelViewSet):
    """API that facilitates CRUD operations on Employee Documents entities."""

    queryset = EmployeeDocuments.objects.all()
    serializer_class = EmployeeDocumentsSerializer
    #permission_classes = [TokenHasReadWriteScope]#, IsFacilityMemberPermission]

    @action(detail=False, methods=['GET'], url_path='employee/(?P<eid>[^/.]+)', name='List By EID')
    def list_by_employee_id(self, request, eid):
        """Lists all Documents for a specified Employee ID. Accessible only to Admins of the Facility and the concerned Employee."""
        
        # TODO: Implement specific permissions
        documents = EmployeeDocuments.objects.filter(employee_id=eid)
        serializer = EmployeeDocumentsSerializer(documents, many=True)
        return Response(serializer.data)



class EmployeeQualificationsViewSet(viewsets.ModelViewSet):
    """API that facilitates CRUD operations on Employee Qualifications entities."""
    
    queryset = EmployeeQualifications.objects.all()
    serializer_class = EmployeeQualificationsSerializer
    permission_classes = [TokenHasReadWriteScope]#, IsFacilityMemberPermission]

    @action(detail=False, methods=['GET'], url_path='employees/(?P<eid>[^/.]+)', name='List By EID')
    def list_by_employee_id(self, request, eid):
        """Lists all Qualifications for a specified Employee ID. Accessible only to Admins of the Facility and the concerned Employee."""
        
        # TODO: Implement specific permissions
        qualifications = EmployeeQualifications.objects.filter(employee_id=eid)
        serializer = EmployeeQualificationsSerializer(qualifications, many=True)
        return Response(serializer.data)


class ProviderViewSet(viewsets.ModelViewSet):
    """API that facilitates operations on Provider entities, typically managed by a Facility Admin."""

    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer
    permission_classes = [TokenHasReadWriteScope]#, IsFacilityMemberPermission]
    
    
    @action(detail=False, methods=['GET'], name='Search')
    def search(self, request, *args, **kwargs):
        """Provider Search based on various attributes."""

        #TODO: Limit results by Facility depending on Role of requestor?
        # Get optional query parameters from the request
        fid = request.query_params.get('facility_id')
        ahid = request.query_params.get('abha_health_id')
        role_code = request.query_params.get('health_care_provider_role_code')
        type = request.query_params.get('health_care_provider_type')

        if not any([fid, ahid, role_code, status]):
            return Response({"detail": "At least one search parameter must be specified."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter the queryset based on the optional parameters
        queryset = Provider.objects.all()
        if fid:
            queryset = queryset.filter(facility_id=fid)
        if ahid:
            queryset = queryset.filter(abha_health_id=ahid)
        if role_code:
            queryset = queryset.filter(health_care_provider_role_code=role_code)
        if type:
            queryset = queryset.filter(health_care_provider_type=type)

        # Serialize the filtered queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    # TODO: Check whether to retain this operation
    def update_multiple(self, request, eid):
        
        try:
            employee_details = Employee.objects.get(doctorUserId=eid)
            employee_details.medical_specialty_type_code = request.POST['doctorSpeciality']
            employee_details.bank_details = request.POST['doctorBankDetails']
            employee_details.doctorRegistrationNumber=request.POST['doctorRegistrationNumber']
            employee_details.languagesKnown=request.POST['languagesKnown']
            employee_details.currentCity=request.POST['currentCity']
            employee_details.save()
            employee_details.doctorRegistrationNumber=request.POST['doctorRegistrationNumber']
            employee_details.languagesKnown=request.POST['languagesKnown']
            employee_details.currentCity=request.POST['currentCity']
            print(request.POST['doctorRegistrationNumber']) #Debug

            registration_certificate = request.FILES['registration_certificate']
            if registration_certificate:
                try:
                    employee_documents = EmployeeDocuments.objects.get(doctor_id=employee_details, document_type='RegistrationCertificate')
                    employee_documents.document_file.save(registration_certificate.name, registration_certificate)
                    employee_documents.save()

                except EmployeeDocuments.DoesNotExist:
                    employee_documents = EmployeeDocuments(doctor_id=employee_details, document_type='doctorRegistrationCertificate')    
                    employee_documents.document_file.save(registration_certificate.name, registration_certificate)
                    employee_documents.save()

            doctorSignatures=request.FILES['doctorSignatures']  #TODO: Employee level
            if doctorSignatures:
                try:
                    employee_documents = EmployeeDocuments.objects.get(doctor_id=employee_details, document_type='DoctorSignatures')
                    employee_documents.document_file.save(doctorSignatures.name, doctorSignatures)
                    employee_documents.save()
                except EmployeeDocuments.DoesNotExist:
                    employee_documents = EmployeeDocuments(doctor_id=employee_details,documentType='DoctorSignatures')    
                    employee_documents.document_file.save(doctorSignatures.name, doctorSignatures)
                    employee_documents.save()
            return Response(status=201)
        except Employee.DoesNotExist:
            return Response(status=404)


    @action(detail=False, methods=['GET'], url_path='uhpn/(?P<uhpn>[^/.]+)', name='List By UHPN')
    def list_by_uhpn(self, request, uhpn):
        """Lists all Providers for a specified Unique Healthcare Provider Number. Accessible only to Admins of the Facility and higher Roles."""
        
        providers = get_object_or_404(Provider.objects.all(), unique_individual_health_care_provider_number=uhpn)
        serializer = ProviderSerializer(providers)
        return Response(serializer.data)



# TODO: Determine whether to drop or retain this functionality
class DoctorFieldDetailsViewSet(viewsets.ModelViewSet):
    """API that facilitates operations on Employee entities, typically managed by a Facility Admin."""

    def retrieve_fields(self, request, fid):
        doctor_field_details = DoctorFieldDetails.objects.get(facility_id=fid)
        print(doctor_field_details.facility_id)
        serializer = DoctorFieldDetailsSerializer(doctor_field_details)
        return Response(serializer.data)


    def update_fields(self, request, fId):
        doctor_field_details = DoctorFieldDetails.objects.get(facility_id=fId)
        content = list(request.POST.items())
        values = dict(content)
        doctor_field_details.doctorLanguage = values['language']
        doctor_field_details.doctorCity = values['city']
        doctor_field_details.doctorSpeciality = values['speciality']
        doctor_field_details.doctorQualification = values['qualification']
        doctor_field_details.doctorDescription = values['description']
        doctor_field_details.doctorImage = values['image']
        doctor_field_details.doctorSignatures = values['sign']
        doctor_field_details.doctorSchedule = values['schedule']
        doctor_field_details.doctorBankDetails = values['bankDetails']
        doctor_field_details.doctorLeaves = values['leaves']
        doctor_field_details.save()
        return Response('success')


