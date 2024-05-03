from .views import ConsultationSubjectiveViewSet
from django.urls import path

urlpatterns = [
    path('', ConsultationSubjectiveViewSet.as_view({
        #'get': 'list',    #For troubleshooting only
        'post': 'create',
    })),
    path('<str:cnid>', ConsultationSubjectiveViewSet.as_view({
        'get': 'retrieve',
    })),
    path('encounter/<str:eid>', ConsultationSubjectiveViewSet.as_view({
        'get': 'retrieve_for_encounter',
    })),
]
