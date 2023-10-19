from django.urls import path
from .views import ConsultationAssessmentViewSet

urlpatterns = [
    path('consultationAssessment', ConsultationAssessmentViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('consultationAssessment/<str:pId>', ConsultationAssessmentViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('consultationAssessment/<str:eId>/<str:prId>', ConsultationAssessmentViewSet.as_view({
        'get': 'retrieve_encounter',
        'put': 'update_encounter',
        'delete': 'destroy_encounter'
    }))
]
