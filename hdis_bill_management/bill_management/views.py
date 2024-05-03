from .models import *
from .serializers import *
from .oauth2helper import get_client_credentials_access_token
from decimal import Decimal
import requests
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

class SourceOfPaymentViewSet(viewsets.ModelViewSet):
    """Supports CRUD operations for Source Of Payment entities."""
    
    queryset = SourceOfPaymentDetails.objects.all()
    serializer_class = SourceOfPaymentSerializer
    permission_classes = [TokenHasReadWriteScope]    #TODO: Review permissions



class BillViewSet(viewsets.ModelViewSet):
    """Supports CRUD operations on Bills and individual Items within."""
    
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [TokenHasReadWriteScope]    #TODO: Review permissions

    def create_bill_items(self, request, bid):
        """Create new Bill Items for a particular Bill."""

        bill = get_object_or_404(Bill.objects.all(), bill_id=bid)    #Retrieve specified Bill

        # Parse Request Body, add the Foreign Key reference to the retrieved Bill for each Item, validate & save
        request_body = request.data
        input_serializer = BillItemSerializer(data=request_body, many=True)    #TODO: Potentially improve with Serializer and bulk_create?
        for input_item in input_serializer.initial_data:
            input_item['bill'] = str(bill.bill_id)
        input_serializer.is_valid(raise_exception=True)

        # Look up and populate relevant Service details based on Service ID
        # Step 1 - Retrieve Access Token for Client Credentials grant type
        try:
            access_token = get_client_credentials_access_token()
        except Exception as e:
            error_body = { "details": f"Failed to get Client Credentials token due to the following error: {e}" } #TODO: Review message
            print(f"{error_body}") #TODO: Log error details
            return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Step 2 - For each Bill Item, get Service Details, Tax and Discount information
        # TODO: Look into improving efficiency with bulk lookup.
        for item in input_serializer.validated_data:
            item_tax_rate = None
            try:
                # Step 3 - Build URL to get Service details by ID from Service Master
                srv_dtl_url = settings.GET_SERVICE_BY_ID_URL.format(item['service_id'])
                print("Get Service By ID URL:", srv_dtl_url) #Debug

                # Step 4 - Invoke Service Master to retrieve Service details, including Base Price
                service_details_response = requests.get(
                    srv_dtl_url, headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
                )
                if service_details_response.status_code == status.HTTP_200_OK:
                    service = service_details_response.json()
                    if not service:
                        error_body = { "details": f"Failed to extract Service details from Service Master service response. Response Content: {service_details_response.content}" } #TODO: Review message
                        return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
                    print("Service:", service) #Debug
                    item['service_item_name'] = service['name']
                    
                    try:
                        # Step 5 - Build URL to get Service Price details by Service ID from Service Master
                        prc_dtl_url = settings.GET_PRICE_BY_SERVICE_ID_URL.format(item['service_id'])
                        print("Get Price By Service ID URL:", prc_dtl_url) #Debug
                        # TODO: Check what additional inputs are necessary to apply Price Rules

                        service_price = "0"    #Default Price to use in case of lookup failure or exceptions
                        # Step 6 - Invoke Service Master to retrieve details of Price
                        price_details_response = requests.get(
                            prc_dtl_url, headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
                        )
                        if price_details_response.status_code == status.HTTP_200_OK:
                            pricing_options = price_details_response.json()
                            if pricing_options:
                                applicable_pricing = pricing_options.first()    #TODO: Incorporate logic to determine applicable pricing based on multiple rules
                                service_price = applicable_pricing['service_price']
                                print("Price:", service_price) #Debug
                                #item['quantity_of_service_unit'] = applicable_pricing['unit']    #TODO: Enable after changing Service Master to use master data
                            else:
                                print(f"Failed to extract Price details from Service Master service response. Response Content: {price_details_response.content}") #TODO: Review message
                        else:    #If the look up call is unsuccessful, log the error & set default Price of 0 in the Bill Item
                            print(f"Error retrieving Price Details from Service Master service. Status Code: '{price_details_response.status_code}', Response Content: {price_details_response.content}") #TODO: Log error details
                    
                    except Exception as e:    #In case of an exception during Price lookup, log the error & set default Price of 0 in the Bill Item
                        print(f"Error while looking up Price details for Service ID {item['service_id']} from Service Master. Exception details:\n{repr(e)}") #TODO: Review error message

                    item['service_item_price'] = service_price
                    
                    # TODO: Shift Discount Lookup to separate operation; Accept and save Discount ID as per Service Master or force entry of a comment in its absence; Reject invalid Discount IDs
                    if bool(service.get('is_discount_allowed', 'false')):
                        service_discount_type = 1    #Default Discount Type to use in case of lookup failure or exceptions
                        service_discount_value = "0.0"    #Default Discount Value to use in case of lookup failure or exceptions
                        try:
                            # Step 7 - Build URL to get Service Discount details by Service ID from Service Master
                            dsc_dtl_url = settings.GET_DISCOUNT_BY_SERVICE_ID_URL.format(item['service_id'])
                            print("Get Discount By Service ID URL:", dsc_dtl_url) #Debug

                            # Step 8 - Invoke Service Master to retrieve details of Discount
                            discount_details_response = requests.get(
                                dsc_dtl_url, headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
                            )
                            if discount_details_response.status_code == status.HTTP_200_OK:
                                discount = discount_details_response.json()
                                if discount:    #Populate Discount fields if lookup succeeds
                                    print("Discount:", discount) #Debug
                                    service_discount_type = discount['code']    #TODO: Change field name after modifications to Service Master
                                    service_discount_value = discount['value']
                                else:
                                    print(f"Failed to extract Discount details from Service Master service response. Response Content: {discount_details_response.content}") #TODO: Review message
                            else:    #If the look up call is unsuccessful, log the error & set defaults for Discount fields
                                print(f"Error retrieving Discount Details from Service Master service. Status Code: '{discount_details_response.status_code}', Response Content: {discount_details_response.content}") #TODO: Log error details
                            
                        except Exception as e:    #In case of an error during Discount lookup, log the error & set defaults for Discount fields
                            print(f"Error while looking up Discount details for Service ID {item['service_id']} from Service Master. Exception details:\n{repr(e)}") #TODO: Review error message

                        item['discount_type'] = service_discount_type    #Indicates whether the Discount is an Amount or Percentage
                        item['discount'] = service_discount_value
                    
                    if bool(service.get('is_taxable', 'false')):
                        item_tax_rate = "0"    #Default Tax Rate to use in case of lookup failure or exceptions
                        try:
                            # Step 5 - Build URL to get Service Tax details by Service ID from Service Master
                            tax_dtl_url = settings.GET_TAX_BY_SERVICE_ID_URL.format(item['service_id'])
                            print("Get Tax By Service ID URL:", tax_dtl_url) #Debug

                            # Step 6 - Invoke Service Master to retrieve details of Tax
                            tax_details_response = requests.get(
                                tax_dtl_url, headers={'Authorization': f'Bearer {access_token}', 'Accept': 'application/json'}
                            )
                            if tax_details_response.status_code == status.HTTP_200_OK:
                                tax = tax_details_response.json()
                                if tax:
                                    print("Tax:", tax) #Debug
                                    item_tax_rate = tax['tax_rate']
                                else:
                                    print(f"Failed to extract Tax details from Service Master service response. Response Content: {tax_details_response.content}") #TODO: Review message
                            else:    #If the look up call is unsuccessful, log the error and set defaults for Tax fields
                                print(f"Error retrieving Tax Details from Service Master service. Status Code: '{tax_details_response.status_code}', Response Content: {tax_details_response.content}") #TODO: Log error details
                            
                        except Exception as e:    #In case of an error during Tax lookup, log the error and set defaults for Tax fields
                            print(f"Error while looking up Tax details for Service ID {item['service_id']} from Service Master. Exception details:\n{repr(e)}") #TODO: Review error message
                else:
                    error_body = { "details": f"Error retrieving Service Details from Service Master service. Status Code: '{service_details_response.status_code}', Response Content: {service_details_response.content}" } #TODO: Log error details
                    return Response(error_body, status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            except Exception as e:    #If an exception is thrown during lookup of Service details by ID...
                print(f"Error while looking up details for Service ID {item['service_id']} from Service Master. Exception details:\n{repr(e)}") #TODO: Log error and review error message
                
                # Populate defaults for values to be looked up
                item['service_item_name'] = None
                item['service_item_price'] = 0
                item['tax'] = 0
                item['discount_type'] = 1
                item['discount'] = 0
            
            # Compute and set Subtotal based on Price, Quantity, Tax and Discount
            price = Decimal(item['service_item_price'])
            quantity = Decimal(item.get('quantity_of_service'))
            discount_type = Decimal(item['discount_type'])
            discount_value = Decimal(item['discount'])
            tax_rate = Decimal(item_tax_rate)
            price_before_discount = price * quantity
            discount_amount = discount_value if not discount_type or discount_type==1 else (discount_value * price_before_discount / 100)
            discounted_price = price_before_discount - discount_amount
            tax = discounted_price * tax_rate / 100
            item['tax'] = tax
            subtotal = discounted_price + tax
            item['subtotal'] = subtotal
                
        bill_items = input_serializer.save()

        bill.bill_items.set(bill_items)    #Dev Note: Set does not remove existing items here as the FK is non-nullable
        # TODO: Incorporate Bill-level Discount and update Bill-level total based on Item Subtotals
        response_serializer = BillDetailsSerializer(bill)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


    def retrieve_bill_with_items(self, request, bid):
        """Retrieve a specified Bill with all its Items."""

        bill = get_object_or_404(Bill.objects.all(), bill_id=bid)
        serializer = BillDetailsSerializer(bill)
        return Response(serializer.data)


    def retrieve_bill_item(self, request, ipk):
        """Retrieve a specified Bill Item."""

        bill_item = get_object_or_404(BillItem.objects.all(), primary_key=ipk)
        serializer = BillItemSerializer(bill_item)
        return Response(serializer.data)


    def common_update_logic(self, request, ipk, is_partial):
        """Common logic used in both Full and Partial Update operations."""

        item = get_object_or_404(BillItem.objects.all(), primary_key=ipk)

        # Parse Request Body, add Bill reference, deserialize, validate & save
        request_body = request.data
        request_body['bill'] = item.bill.bill_id
        input_serializer = BillItemSerializer(data=request_body, partial=is_partial)
        input_serializer.is_valid(raise_exception=True)
        input_serializer.save()
        # TODO: Incorporate updates to Bill-level fields based on Item-level update
        return Response(input_serializer.data)


    def update_bill_item(self, request, ipk):
        """Update a specified Bill Item."""

        return self.common_update_logic(request, ipk, False)


    def partial_update_bill_item(self, request, ipk):
        """Partially update a specified Bill Item."""

        return self.common_update_logic(request, ipk, True)


    def destroy_bill_item(self, request, ipk):
        """Delete a specified Bill Item."""

        bill_item = get_object_or_404(BillItem.objects.all(), primary_key=ipk)
        bill_item.delete()
        # TODO: Incorporate updates to Bill-level fields based on Item-level update
        return Response(None, status=status.HTTP_204_NO_CONTENT)
