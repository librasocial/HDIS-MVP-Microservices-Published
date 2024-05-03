from .views import *
from django.urls import path

urlpatterns = [
    path('', ConsultationObjectiveViewSet.as_view({
        #'get': 'list',    #For troubleshooting only
        'post': 'create',
    })),
    path('<str:cnid>', ConsultationObjectiveViewSet.as_view({
        'get': 'retrieve',
    })),
    path('encounter/<str:eid>', ConsultationObjectiveViewSet.as_view({
        'get': 'retrieve_for_encounter',
    })),
]
