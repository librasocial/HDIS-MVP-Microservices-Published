from rest_framework import authentication
from rest_framework import exceptions
from rest_framework.authentication import get_authorization_header
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.authentication import JWTAuthentication

class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_header = get_authorization_header(request)
        if not auth_header:
            return self.get_response(request)

        auth = auth_header.decode('utf-8').split()
        if auth[0].lower() != 'bearer':
            raise exceptions.AuthenticationFailed('Invalid token prefix')
        
        if len(auth) == 1:
            raise exceptions.AuthenticationFailed('Invalid token')

        token = auth[1]

        try:
            JWTAuthentication().get_validated_token(token)
        except InvalidToken as e:
            raise exceptions.AuthenticationFailed('Invalid token')

        response = self.get_response(request)
        return response
