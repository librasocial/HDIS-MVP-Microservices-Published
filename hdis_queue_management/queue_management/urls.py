from django.urls import path
from . import views
from .views import QueueViewSet
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [

    path('getToken/', QueueViewSet.as_view({
            'post': 'getToken',
    })),
   
] 