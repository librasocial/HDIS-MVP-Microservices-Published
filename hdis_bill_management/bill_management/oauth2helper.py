# Utility methods for OAuth2 workflow support

import requests
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from oauthlib.oauth2 import WebApplicationClient
from oauth2_provider.models import AccessToken

def get_client_credentials_access_token():
    """
    Obtain an Access Token for a Client Credentials grant based on the configured Client ID & Client Secret.
    This grant type is used for inter-service invocation scenarios that are not on behalf of a User. 
    """
    
    # Submit POST request with URL-encoded parameters
    params = {
        'grant_type': 'client_credentials',
        'client_id': settings.OAUTH2_CLIENT_ID,
        'client_secret': settings.OAUTH2_CLIENT_SECRET,
    }
    response = requests.post(settings.OAUTH2_TOKEN_URL, data=params) #Dev Note: params dict URL-encoded by default
    response.raise_for_status()
    response_body = response.json()
    return response_body['access_token']


def get_authorization_url():
    """Get the authorization URL for the OAuth2 Authorization Code flow"""
    
    authorization_url = settings.OAUTH2_AUTHORIZATION_URL
    oauth2_client = WebApplicationClient(settings.OAUTH2_CLIENT_ID)
    authorization_url, state = oauth2_client.prepare_authorization_request(
        authorization_url, redirect_uri=settings.OAUTH2_REDIRECT_URI
    )

    # Store the state in session for later verification
    return authorization_url, state


def handle_authorization_response(request):
    """Handle the Authorization Code response and exchange it for an Access Token"""

    client_id = settings.OAUTH2_CLIENT_ID
    client_secret = settings.OAUTH2_CLIENT_SECRET
    token_url = settings.OAUTH2_TOKEN_URL

    # Get Authorization Code grant
    client = WebApplicationClient(client_id)
    token_url, headers, body = client.prepare_token_request(
        token_url,
        authorization_response=request.build_absolute_uri(),
        redirect_url=settings.OAUTH2_REDIRECT_URI,
        code=request.GET.get('code'),
    )

    # Exchange the Authorization Code for an Access Token
    response = requests.post(token_url, headers=headers, data=body, auth=(client_id, client_secret))
    response.raise_for_status()
    token = response.json()
    access_token = token['access_token']
    
    # Note: The caller should be prepared for the possibility of requests.exceptions.RequestException being raised
    return access_token


@login_required
def authorize(request):
    """Redirect the user to the Authorization URL"""

    authorization_url, state = get_authorization_url()
    # Store the state in the session for later verification
    request.session['oauth2_state'] = state
    return redirect(authorization_url)


def logout(request):
    """Revoke the Access Token when the user logs out"""

    access_token = AccessToken.objects.filter(user=request.user).first()
    if access_token:
        access_token.revoke()
        return True
    else:
        return False
