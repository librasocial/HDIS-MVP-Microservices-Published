from .views import ConsultationAssessmentViewSet
from django.urls import path

urlpatterns = [
    path('', ConsultationAssessmentViewSet.as_view({
        #'get': 'list',    #For troubleshooting only
        'post': 'create',
    })),
    path('<str:cnid>', ConsultationAssessmentViewSet.as_view({
        'get': 'retrieve',
    })),
    path('encounter/<str:eid>', ConsultationAssessmentViewSet.as_view({
        'get': 'retrieve_for_encounter',
    })),
]
