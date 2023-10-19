from functools import wraps
from rest_framework import exceptions
import requests
import json
from django.conf import settings 
import requests
def jwt_token_required(view_func):
    @wraps(view_func)
    def decorator(*args, **kwargs):
        try:
            
            access_token = args[0].session.get('access_token')
            refresh_token = args[0].session.get('refresh_token')
            if not access_token:
                print("no access token")
                return view_func(data={},status=401,*args, **kwargs)
            #token=args[0].request.META['Authorization']
            url = settings.HDIS_AUTH_SERVER+"/access/check_access/"
            r = requests.post(url, data='{}',
                                headers={'Content-type': 'application/json', 'Accept': 'application/json','Authorization':f'Bearer {access_token}'})

            print(r.status_code)
            if r.status_code==200:
                data = json.loads(r.content.decode('utf-8'))
                print(data)
                args[0].session['userId']=data['username']
                args[0].session['uniqueFacilityIdentificationNumber']=data['extra']['facilityId'][0]['uniqueFacilityIdentificationNumber']
                args[0].session['userGroup']=data['groups'][0]['name']
                args[0].session['facilityTypeCode']=data['extra']['facilityId'][0]['facilityTypeCode']
                return view_func( data=data,status=r.status_code,*args, **kwargs)
            else:
                print(r.content.decode('utf-8'))
                return view_func(data={},status=r.status_code,*args, **kwargs)


            
            
        except (KeyError, IndexError):
            print(KeyError)
            print(IndexError)
            return view_func(data={},status=401,*args, **kwargs)
        
        
    
    return decorator
