from functools import wraps
from rest_framework import exceptions
import requests
import json
from django.conf import settings 
def jwt_token_required(view_func):
    @wraps(view_func)
    def decorator(*args, **kwargs):
        try:
            print(args[0])
            token = args[0].request.headers.get('Authorization', None)
            print(token)
            if not token:
                raise exceptions.AuthenticationFailed('Unauthorized')
            #token=args[0].request.META['Authorization']
            url = settings.HDIS_AUTH_SERVER+"/access/check_access/"
            r = requests.post(url, data='{}',
                                headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization':token})

            if r.status_code==200:
                data = json.loads(r.content.decode('utf-8'))
            else:
                raise exceptions.AuthenticationFailed('Unauthorized')


            
            
        except (KeyError, IndexError):
            raise exceptions.AuthenticationFailed('Invalid authorization header')
        
        
        return view_func( data=data,token=token,status=r.status_code,*args, **kwargs)
    
    return decorator
