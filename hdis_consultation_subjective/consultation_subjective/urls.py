from django.urls import path
from .views import ConsultationSubjectivetViewSet

urlpatterns = [
    path('consultationSubjective', ConsultationSubjectivetViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('consultationSubjective/<str:fId>/<str:prId>/<str:date>', ConsultationSubjectivetViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy'
    })),
    path('consultationSubjective/<str:eId>/<str:prId>', ConsultationSubjectivetViewSet.as_view({
        'get': 'retrieve_encounter',
        'put': 'update_encounter',
        'delete': 'destroy_encounter'
    }))
]
