from functools import wraps
from rest_framework import exceptions
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
def jwt_token_required(view_func):
    @wraps(view_func)
    def decorator(*args, **kwargs):
        try:
            print("wearehere")
            print(args[0].request.headers)
            #print(args[0].request.META)
            token = args[0].request.headers.get('Authorization', None)
            print(token)
            #token=args[0].request.META['Authorization']
            if not token:
                raise exceptions.AuthenticationFailed('Unauthorized')
            else:
                token = args[0].request.headers.get('Authorization', None).split(' ')[1]
        except (KeyError, IndexError):
            raise exceptions.AuthenticationFailed('Invalid authorization header')
        
        try:
            validated_token=JWTAuthentication().get_validated_token(token)
            username = validated_token['username']
            user = User.objects.get(username=username)
        except InvalidToken as e:
            raise exceptions.AuthenticationFailed('Invalid token')
        
        return view_func( user=user,*args, **kwargs)
    
    return decorator
