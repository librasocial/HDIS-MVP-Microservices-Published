from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

from .views import ServiceViewSet,ProviderServiceViewSet


urlpatterns = [

path('service_details', ServiceViewSet.as_view({
        'get': 'list',
        'post': 'create',

        'put':'update'
    })),
path('provider_service/', ProviderServiceViewSet.as_view({
    })),






] 