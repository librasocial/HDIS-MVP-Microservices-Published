from functools import wraps
from rest_framework import exceptions
import requests
import json
from django.conf import settings

def jwt_token_required(view_func):
    """Decorator to enforce that access to methods is authenticated based on a JWT token."""

    @wraps(view_func)
    def decorator(*args, **kwargs):
        try:
            # Retrieve the token from request headers and abort operation if no token is found
            token = args[0].request.headers.get('Authorization', None)
            if not token:
                raise exceptions.AuthenticationFailed('Unauthorized')
            
            url = settings.HDIS_AUTH_SERVER+"/access/check_access/"
            response = requests.post(url, data='{}', 
                                     headers={'Content-type': 'application/json', 'Accept': 'application/json', 'Authorization': token})

            request_body = json.loads(args[0].request.body.decode('utf-8'))
            print(request_body) #Debug
            
            if response.status_code == 200:
                #check if the userid and facility matches what is received in request
                response_body = json.loads(response.content.decode('utf-8'))
                # TODO: Check scenario where  the User is allocated to multiple Facilities.
                if response_body['extra']['facilityId'][0]['uniqueFacilityIdentificationNumber'] != request_body['uniqueFacilityIdentificationNumber']:
                    raise exceptions.AuthenticationFailed('Unauthorized - User is not allocated to the Facility in question.')
                if response_body['username'] != request_body['userId']:
                    raise exceptions.AuthenticationFailed('Unauthorized')
            else:
                raise exceptions.AuthenticationFailed('Unauthorized')
            
        except (KeyError, IndexError):
            raise exceptions.AuthenticationFailed('Invalid authorization header')
        
        return view_func(*args, **kwargs)
    
    return decorator
