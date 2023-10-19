from functools import wraps
from rest_framework import exceptions
import requests
import json
from django.conf import settings 
def jwt_token_required(view_func):

    @wraps(view_func)
    def decorator(*args, **kwargs):
        print('i am here for check')
        try:

            token = args[0].request.headers.get('Authorization', None)
            content_type=args[0].request.headers.get('Content-type', None)
            
            if content_type!='application/json':
                userid=args[0].request.POST['userId']
                uniqueFacilityIdentificationNumber=args[0].request.POST['uniqueFacilityIdentificationNumber']
            else:    
                values=json.loads(args[0].request.body.decode('utf-8'))
                userid=values['userId']
                uniqueFacilityIdentificationNumber=values['uniqueFacilityIdentificationNumber']

            if not token:
                raise exceptions.AuthenticationFailed('Unauthorized')
            #token=args[0].request.META['Authorization']
            url = settings.HDIS_AUTH_SERVER+"/access/check_access/"
            r = requests.post(url, data='{}',
                                headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization':token})

            if r.status_code==200:
                
                #check if the userid and facility matches what is received in request
                data = json.loads(r.content.decode('utf-8'))
                print(data)
                if data['extra']['facilityId'][0]['uniqueFacilityIdentificationNumber']!=uniqueFacilityIdentificationNumber:
                    raise exceptions.AuthenticationFailed('Unauthorized')
                if data['username']!=userid:
                    raise exceptions.AuthenticationFailed('Unauthorized')

            else:
                raise exceptions.AuthenticationFailed('Unauthorized')


            
            
        except (KeyError, IndexError):
            raise exceptions.AuthenticationFailed('Invalid authorization header')
        
        
        return view_func(*args, **kwargs)
    
    return decorator
