from functools import wraps
from rest_framework import exceptions
import requests
import json
from django.conf import settings 
def jwt_token_required(view_func):
    @wraps(view_func)
    def decorator(*args, **kwargs):
        try:
            
            token = args[0].request.headers.get('Authorization', None)
            values=json.loads(args[0].request.body.decode('utf-8'))
            print("printing token values")
            print(values)
            if not token:
                raise exceptions.AuthenticationFailed('Unauthorized')
            #token=args[0].request.META['Authorization']
            url = settings.HDIS_AUTH_SERVER+"/access/check_access/"
            r = requests.post(url, data='{}',
                                headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization':token})

            if r.status_code==200:
                
                #check if the userid and facility matches what is received in request
                data = json.loads(r.content.decode('utf-8'))
                if data['extra']['facilityId'][0]['uniqueFacilityIdentificationNumber']!=values['uniqueFacilityIdentificationNumber']:
                    raise exceptions.AuthenticationFailed('Unauthorized')
                if data['username']!=values['userId']:
                    raise exceptions.AuthenticationFailed('Unauthorized')

            else:
                raise exceptions.AuthenticationFailed('Unauthorized')


            
            
        except (KeyError, IndexError):
            raise exceptions.AuthenticationFailed('Invalid authorization header')
        
        
        return view_func(*args, **kwargs)
    
    return decorator
