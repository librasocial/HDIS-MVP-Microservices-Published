from .models import *
from .serializers import *
from .oauth2helper import get_client_credentials_access_token
import requests
from uuid import UUID
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

class ServiceTypeViewSet(viewsets.ModelViewSet):
    
    queryset = ServiceType.objects.all()
    serializer_class = ServiceTypeSerializer
    permission_classes = [TokenHasReadWriteScope]    #TODO: Review permissions

    

class ServiceViewSet(viewsets.ModelViewSet):
    
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    permission_classes = [TokenHasReadWriteScope]    #TODO: Review permissions
    
    
    def list_by_facility(self, request, fid):
        """Lists all Services offered at a specified Facility."""

        service = get_object_or_404(Service.objects.all(), facility_id=fid)
        serializer = ServiceSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def list_by_provider_uhpn(self, request, uhpn):
        """Lists all Services offered by a specified Provider bsaed on UHPN."""
        
        # Retrieve Access Token for Client Credentials grant type
        try:
            access_token = get_client_credentials_access_token()
        except Exception as e:
            error_body = { "details": f"Failed to get Client Credentials token due to the following error: {e}" } #TODO: Review message
            print(f"{error_body}") #TODO: Log error details
            return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Build URL to get Provider details by UHPN
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
        
        services = Service.objects.filter()
        return 


    @action(detail=False, methods=['GET'], name='Search')
    def search(self, request, *args, **kwargs):
        """Service Search based on various attributes."""

        #TODO: Limit results by Facility depending on Role of requestor?
        # Get query parameters from the request
        facility_id = request.query_params.get('facility_id')
        name = request.query_params.get('name')
        is_active = request.query_params.get('is_active')
        service_type = request.query_params.get('service_type')
        is_component_type = request.query_params.get('is_component_type')
        is_discount_allowed = request.query_params.get('is_discount_allowed')
        
        # Ensure minimum mandatory parameters have been provided to avoid returning excessive data and hampering performance
        if not any([facility_id, name]):
            return Response({"detail": "At least one search parameter among 'facility_id' and 'name' must be specified."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter the queryset based on the parameters
        queryset = Service.objects.all()
        if facility_id:
            queryset = queryset.filter(facility_id=facility_id)
        if name:
            queryset = queryset.filter(name=name)
        if is_active:
            queryset = queryset.filter(is_active=is_active)
        if service_type:
            queryset = queryset.filter(service_type=service_type)
        if is_component_type:
            queryset = queryset.filter(is_component_type=is_component_type)
        if is_discount_allowed:
            queryset = queryset.filter(is_discount_allowed=is_discount_allowed)
        
        # Serialize the filtered queryset
        serializer = ServiceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ComponentServiceViewSet(viewsets.ModelViewSet):
    """Defines Component Services comprised of multiple regular Services."""
    
    queryset = ComponentService.objects.all()
    serializer_class = ComponentServiceSerializer
    permission_classes = [TokenHasReadWriteScope]    #TODO: Review permissions
    
    @action(detail=False, methods=['GET'], url_path='component-service-id/(?P<csid>[^/.]+)', name='List All Components By Component Service ID')
    def list_all_components(self, request, csid):
        """Lists all Components associated with the specified Component Service ID."""

        services = ComponentService.objects.filter(component_service_id=csid)
        if services.exists():
            serializer = ComponentServiceSerializer(services, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Not found"}, status=status.HTTP_404_NOT_FOUND)


class ServicePriceViewSet(viewsets.ModelViewSet):
    """Defines the Pricing Model for a specified Service."""
    
    queryset = ServicePrice.objects.all()
    serializer_class = ServicePriceSerializer
    permission_classes = [TokenHasReadWriteScope]    #TODO: Review permissions



class ServiceDiscountViewSet(viewsets.ModelViewSet):
    """Defines the Discount Model for a specified Service."""
    
    queryset = ServiceDiscount.objects.all()
    serializer_class = ServiceDiscountSerializer
    permission_classes = [TokenHasReadWriteScope]    #TODO: Review permissions



class ServiceTaxViewSet(viewsets.ModelViewSet):
    """Defines the Taxation Model for a specified Service."""
    
    queryset = ServiceTax.objects.all()
    serializer_class = ServiceTaxSerializer
    permission_classes = [TokenHasReadWriteScope]    #TODO: Review permissions
